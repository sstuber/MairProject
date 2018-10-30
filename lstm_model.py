
from keras.layers import Input, Embedding, LSTM, Dense, Dropout, TimeDistributed, Activation
from keras.models import Model, Sequential
from numpy import array
import re

UTTERANCE_LIST_LENGTH = 6
EPOCHS = 5


class LstmModel:
    def __init__(self, numbered_classification_train_data, numbered_classification_test_data,
                 classification_dict_object):
        self.classification_dict_object = classification_dict_object

        self.train_data = numbered_classification_train_data
        self.test_data = numbered_classification_test_data
        # Split into input and output for the neural network
        train_values = []
        train_labels = []
        for i in self.train_data:
            train_values.append(i.utterance)
            output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            output[i.speech_act] = 1
            train_labels.append(output)

        # Change to numpy array
        train_values = array(train_values)
        train_labels = array(train_labels)

        vocabulary_size = classification_dict_object.utterance_count + 1

        # Input has shape of a single sentence (10,)
        input_tensor = Input(shape=train_values[0].shape)

        # Create layers
        embedding_layer = Embedding(vocabulary_size, output_dim=256, mask_zero=True)(input_tensor)
        hidden_layer = LSTM(units=64, activation='relu')(embedding_layer)
        output_layer = Dense(units=15, activation='softmax')(hidden_layer)

        # Create model
        self.model = Model(inputs=input_tensor, outputs=output_layer)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train model
        self.model.fit(train_values, train_labels, epochs=EPOCHS)

    def print_accuracy(self):
        # Split into input and output for the neural network
        test_values = []
        test_labels = []
        for i in self.test_data:
            test_values.append(i.utterance)
            test_labels.append(i.speech_act)

        test_values = array(test_values)
        test_labels = array(test_labels)

        # Predict labels
        predicted_labels = self.model.predict(test_values, len(test_values))
        predicted_labels = array([xi.argmax() for xi in predicted_labels])

        # Print percentage correctly predicted
        correct = 0
        for i in range(len(test_labels)):
            if predicted_labels[i] == test_labels[i]:
                correct += 1
        print(correct / len(test_labels))

    # given a numbered sentence it will return the name of the speech_act
    def predict_sentence(self, sentence):
        sentence = re.sub(r'[^\w\s]', '', sentence)

        split_sentence = re.split(r'\s', sentence)
        numbered_sentence = list(map(self.classification_dict_object.get_testing_utterance_id, split_sentence))
        normalized_numbered_sentence = normalize_utterance_length(numbered_sentence)

        predicted_sentences = self.model.predict(array([normalized_numbered_sentence]))
        speech_act_id = predicted_sentences[0].argmax()

        return self.classification_dict_object.get_speech_act_id(speech_act_id)


def normalize_utterance_length(utterance_list):
    normalized_utterance = []
    utterance_length = len(utterance_list)

    for i in range(UTTERANCE_LIST_LENGTH):
        if i < utterance_length:
            normalized_utterance.append(utterance_list[i])
        else:
            normalized_utterance.append(1)

    return normalized_utterance
