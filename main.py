from functools import reduce
import re

TYPES_PATH = './types.csv'


def get_types_file_dict():
    types_file = open(TYPES_PATH)

    types_str = types_file.read()

    types_file.close()

    # remove the first line
    types_str = re.split(r'\n', types_str, 1)[1]

    # split the the other lines
    types_split_str = re.split(r'\n', types_str)

    # separate each line by the comma
    split_sentences = map(lambda x: re.split(r',', x), types_split_str)
    # remove the empty lines
    filtered_sentenced = filter(lambda x: len(x[2]) != 0, split_sentences)
    # reduce list in dictionary
    final_dict = reduce(add_word_to_dict, filtered_sentenced, {})

    return final_dict


def add_word_to_dict(dict,word_list):

    word_name = word_list[0]
    word_value = word_list[2]
    dict[word_name] = word_value
    return dict


def main():

    types_dict = get_types_file_dict()


if __name__ == "__main__":
    main()
