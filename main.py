import re
import tensorflow as tf
from random import shuffle
from classify_data import ClassificationData, ClassificationDictionary, NumberedClassification
from keras.layers import Input, Embedding, LSTM, Dense, Dropout, TimeDistributed, Activation
from keras.models import Model, Sequential
from numpy import array

CLASSIFICATION_PATH = './classification_data.txt'
UTTERANCE_LIST_LENGTH = 10


def get_classification_data():
    classification_file = open(CLASSIFICATION_PATH)

    classification_str = classification_file.read()

    split_file = re.split(r'\n', classification_str)

    classification_data_list = []

    for item in split_file:
        if len(item) == 0:
            continue

        classification_data_list.append(ClassificationData(item))
    return classification_data_list


def normalize_utterance_length(utterance_list):
    normalized_utterance = []
    utterance_length = len(utterance_list)

    for i in range(UTTERANCE_LIST_LENGTH):
        if i < utterance_length:
            normalized_utterance.append(utterance_list[i])
        else:
            normalized_utterance.append(1)

    return normalized_utterance


def number_train_data(classification_dict_object: ClassificationDictionary, classification_list):
    numbered_classification_list = []

    # Transform each classification object to a numbered one
    for classification_object in classification_list:
        numbered_classification = NumberedClassification()

        # First get the numbered speech act
        numbered_classification.speech_act = classification_dict_object.get_speech_act_id(
            classification_object.speech_act
        )

        # Then transform the utterance string list to a numbered string list
        numbered_utterance_list = list(map(
            classification_dict_object.get_training_utterance_id, classification_object.utterance
        ))

        # numbered_utterance_list = []
        # for utterance in classification_object.utterance:
        #     numbered_utterance = classification_dict_object.get_training_utterance_id(utterance)
        #     numbered_utterance_list.append(numbered_utterance)

        numbered_classification.utterance = normalize_utterance_length(numbered_utterance_list)

        numbered_classification_list.append(numbered_classification)

    return numbered_classification_list


def main():

    classification_list = get_classification_data()
    classification_dict_object = ClassificationDictionary()
    numbered_classification_list = number_train_data(classification_dict_object, classification_list)

    # Randomize order of sentences
    shuffle(numbered_classification_list)

    # Split randomly in train and test data
    train_data = numbered_classification_list[0:round(len(numbered_classification_list)*0.85)]
    test_data = numbered_classification_list[round(len(numbered_classification_list)*0.85):len(numbered_classification_list)]

    # Split into input and output for the neural network
    train_values = []
    train_labels = []
    for i in train_data:
        train_values.append(i.utterance)
        output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        output[i.speech_act] = 1
        train_labels.append(output)

    # Change to numpy array
    train_values = array(train_values)
    train_labels = array(train_labels)

    vocabulary_size = classification_dict_object.utterance_count+1

    # Input has shape of a single sentence (10,)
    input_tensor = Input(shape=train_values[0].shape)

    # Create layers
    embedding_layer = Embedding(vocabulary_size, output_dim=64)(input_tensor)
    hidden_layer = LSTM(units=64, activation='relu')(embedding_layer)
    output_layer = Dense(units=15, activation='softmax')(hidden_layer)

    # Create model
    model = Model(inputs=input_tensor, outputs=output_layer)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train model
    model.fit(train_values, train_labels, epochs=5)

    # Split into input and output for the neural network
    test_values = []
    test_labels = []
    for i in test_data:
        test_values.append(i.utterance)
        test_labels.append(i.speech_act)

    test_values = array(test_values)
    test_labels = array(test_labels)

    # Predict labels
    predicted_labels = model.predict(test_values, len(test_values))
    predicted_labels = array([xi.argmax() for xi in predicted_labels])

    # Print percentage correctly predicted
    correct = 0
    for i in range(len(test_labels)):
        if predicted_labels[i] == test_labels[i]:
            correct += 1
    print(correct/len(test_labels))


if __name__ == "__main__":
    main()

