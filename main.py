import re
from classify_data import ClassificationData, ClassificationDictionary, NumberedClassification

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

        # numbered_utterance_list = []
        # for utterance in classification_object.utterance:
        #     numbered_utterance = classification_dict_object.get_training_utterance_id(utterance)
        #     numbered_utterance_list.append(numbered_utterance)

        print(classification_object.utterance)
        print(numbered_utterance_list)

        numbered_classification.utterance = numbered_utterance_list

        numbered_classification_list.append(numbered_classification)

    return numbered_classification_list


def main():

    classification_list = get_classification_data()
    classification_dict_object = ClassificationDictionary()
    numbered_classification_list = number_train_data(classification_dict_object, classification_list)

    for i in range(50):
        item = numbered_classification_list[i]
        print(item.utterance)


if __name__ == "__main__":
    main()

