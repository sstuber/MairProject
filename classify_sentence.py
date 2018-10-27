import re
from lstm_model import LstmModel, UTTERANCE_LIST_LENGTH, normalize_utterance_length
from random import shuffle
from classify_data import ClassificationData, ClassificationDictionary, NumberedClassification
import gc

CLASSIFICATION_PATH = './classification_data.txt'


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

        numbered_classification.utterance = normalize_utterance_length(numbered_utterance_list)

        numbered_classification_list.append(numbered_classification)

    return numbered_classification_list


def number_test_data(classification_dict_object: ClassificationDictionary, classification_list):
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
            classification_dict_object.get_testing_utterance_id, classification_object.utterance
        ))

        numbered_classification.utterance = normalize_utterance_length(numbered_utterance_list)

        numbered_classification_list.append(numbered_classification)

    return numbered_classification_list


def main():

    classification_list = get_classification_data()

    shuffle(classification_list)

    train_data = classification_list[0:round(len(classification_list)*0.85)]
    test_data = classification_list[round(len(classification_list)*0.85):len(classification_list)]

    classification_dict_object = ClassificationDictionary()
    numbered_classification_train_data = number_train_data(classification_dict_object, train_data)
    numbered_classification_test_data = number_test_data(classification_dict_object, test_data)

    lstm_model = LstmModel(numbered_classification_train_data,
                           numbered_classification_test_data, classification_dict_object)

    lstm_model.print_accuracy()
    ask_sentence(lstm_model)


def get_lstm_model():
    classification_list = get_classification_data()

    shuffle(classification_list)

    train_data = classification_list[0:round(len(classification_list)*0.85)]
    test_data = classification_list[round(len(classification_list)*0.85):len(classification_list)]

    classification_dict_object = ClassificationDictionary()
    numbered_classification_train_data = number_train_data(classification_dict_object, train_data)
    numbered_classification_test_data = number_test_data(classification_dict_object, test_data)

    lstm_model = LstmModel(numbered_classification_train_data,
                           numbered_classification_test_data, classification_dict_object, 4, 128, 128)

    return lstm_model


def cross_validation():
    classification_list = get_classification_data()

    shuffle(classification_list)

    train_data = classification_list[0:round(len(classification_list) * 0.85)]

    classification_dict_object = ClassificationDictionary()

    output_list = []
    # Try different values
    for utterance_length in [4, 6]: #[6, 8, 10, 12, 14]:
        for embedding_dimensions in [64, 128, 256]:#[16, 32, 64]:
            for lstm_dimensions in [64, 128, 256]: #[16, 32, 64]:

                # Create 10 folds
                total_accuracy = 0
                bucket_length = round(len(train_data) * 0.1)
                for i in range(0, 9):
                    print(str(utterance_length) + " " + str(embedding_dimensions) + " " + str(
                        lstm_dimensions) + " " + str(i) + "--------------------------------------------------------")

                    if i < 9:
                        train_buckets = train_data[:i*bucket_length] + train_data[(i+1)*bucket_length:]
                        test_bucket = train_data[i*bucket_length:(i+1)*bucket_length]
                    else:
                        train_buckets = train_data[:i * bucket_length]
                        test_bucket = train_data[i * bucket_length:len(train_data)]

                    numbered_classification_train_data = number_train_data(classification_dict_object, train_buckets)
                    numbered_classification_test_data = number_test_data(classification_dict_object, test_bucket)

                    # Train on 9/10 buckets
                    lstm_model = LstmModel(numbered_classification_train_data,
                                           numbered_classification_test_data, classification_dict_object, utterance_length, embedding_dimensions, lstm_dimensions)

                    # Test on 1/10 buckets
                    total_accuracy += lstm_model.get_accuracy()
                    gc.collect()

                output_list.append({str(utterance_length) + " " + str(embedding_dimensions) + " " + str(lstm_dimensions): total_accuracy/10})

    return output_list


def ask_sentence(lstm):
    sentence = input("Enter sentence \n")
    print(f'speech act label: {lstm.predict_sentence(sentence)}\n')
    ask_sentence(lstm)


if __name__ == "__main__":
    main()

