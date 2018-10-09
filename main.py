from functools import reduce
from Levenshtein.StringMatcher import StringMatcher
import re


TYPES_PATH = './types.csv'
DEFAULT_DISTANCE = 999999999999999999999999
MATCH_REGEX =r'(\w+|\(.+\))(\/|\\)(\(.+\)|\w+)|(\w+)'


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


def add_word_to_dict(types_dict, word_list):

    word_name = word_list[0]
    word_value = word_list[2]
    types_dict[word_name] = word_value
    return types_dict


def transform_sentence(types_dict, sentence):

    sentence = re.sub(r'[^\w\s]', '', sentence)
    lowercase_sentence = sentence.lower()
    split_sentence = re.split(r'\s+', lowercase_sentence)

    return_list = []
    for word_str in split_sentence:
        if word_str in types_dict:
            item_type = types_dict[word_str]
            return_list.append((word_str, item_type))

        else:
            closest_item_match = find_closest_match(types_dict, word_str)
            return_list.append(closest_item_match)

    return return_list


# returns item, item_type tuple
def find_closest_match(types_dict, search_str):

    closest_match = ''
    closest_distance = DEFAULT_DISTANCE

    for key in types_dict:

        key_distance = StringMatcher(seq1=search_str, seq2=key).distance()

        if key_distance < closest_distance:
            closest_match = key
            closest_distance = key_distance

    closest_type = types_dict[closest_match]

    return closest_match, closest_type


def main():

    test = '(NP/S)/NP'

    regex = re.match(MATCH_REGEX, test)

    print(regex.groupdict())
    print(regex.groups())

    types_dict = get_types_file_dict()

    sentence = input("Enter sentence \n")

    sequence = transform_sentence(types_dict,sentence)

    print(sequence)




if __name__ == "__main__":
    main()
