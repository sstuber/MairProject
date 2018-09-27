import re
from classify_data import ClassificationData

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


def main():
    get_classification_data()


if __name__ == "__main__":
    main()

