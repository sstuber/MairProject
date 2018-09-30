import re
from classify_data import ClassificationData, ClassificationDictionary, NumberedClassification

CLASSIFICATION_PATH = './classification_data.txt'
UTTERANCE_LIST_LENGTH = 10
OUTPUT_FILENAME = './numbered_data.txt'


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

        # print(classification_object.utterance)
        # print(numbered_utterance_list)

        numbered_classification.utterance = normalize_utterance_length(numbered_utterance_list)

        numbered_classification_list.append(numbered_classification)

    return numbered_classification_list


def write_numbered_data(numbered_classification_list):
    # Write the numbered data to a .txt file
    print('Writing', OUTPUT_FILENAME)

    with open(OUTPUT_FILENAME, 'w') as f:
        for item in numbered_classification_list:
            f.write(str(item.speech_act) + ', ')
            f.write(str(item.utterance))
            f.write('\n')

def main():

    classification_list = get_classification_data()
    classification_dict_object = ClassificationDictionary()
    numbered_classification_list = number_train_data(classification_dict_object, classification_list)

    write_numbered_data(numbered_classification_list)


if __name__ == "__main__":
    main()

