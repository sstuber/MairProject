import re
from lstm_model import LstmModel
from random import shuffle
from classify_data import ClassificationData, ClassificationDictionary, NumberedClassification

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

        # numbered_utterance_list = []
        # for utterance in classification_object.utterance:
        #     numbered_utterance = classification_dict_object.get_training_utterance_id(utterance)
        #     numbered_utterance_list.append(numbered_utterance)

        numbered_classification.utterance = normalize_utterance_length(numbered_utterance_list)

        numbered_classification_list.append(numbered_classification)

    return numbered_classification_list


def main():

    classification_list = get_classification_data()

    shuffle(classification_list)

    train_data = classification_list[0:round(len(classification_list)*0.85)]
    test_data = classification_list[
                round(len(classification_list)*0.85):len(classification_list)]

    classification_dict_object = ClassificationDictionary()
    numbered_classification_train_data = number_train_data(classification_dict_object, train_data)
    numbered_classification_test_data = number_test_data(classification_dict_object, test_data)

    lstm_model = LstmModel(numbered_classification_train_data,
                           numbered_classification_test_data, classification_dict_object)

    lstm_model.print_accuracy()


if __name__ == "__main__":
    main()

