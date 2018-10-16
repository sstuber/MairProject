from functools import reduce
from Levenshtein.StringMatcher import StringMatcher
from graph_data import GraphNode, LEFT_HAND_ID, RIGHT_HAND_ID, find_tree_paths
import re
import json

ONTOLOGY_PATH = './ontology.json'
TYPES_PATH = './types.csv'
DEFAULT_DISTANCE = 999999999999999999999999
MATCH_REGEX = r'(\w+|\(.+\))(\/|\\)(\(.+\)|\w+)|(\w+)'

VALUE_DICT = {
    'restaurant': ['pricerange'],
    'food': ['food'],
    'town': ['area']
}


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

    if word_name in types_dict:
        types_dict[word_name].append(word_value)
    else:
        types_dict[word_name] = [word_value]
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


def amount_of_dubbles(acc: int, word_tuple):
    _, type_array = word_tuple

    length_type_array = len(type_array)

    if length_type_array > 1:
        return length_type_array + acc

    return acc

def tuple_to_graph_node(tuple):
    name, type_array = tuple

    return_array = []
    for type_str in type_array:
        return_array.append(GraphNode((name, type_str)))

    return return_array


# graph array is an array of node arrays
def fold_graph_array(graph_array):

    #  end condition
    if len(graph_array) == 1:
        print(f'Succes fully ended with {graph_array[0][0]}')
        return graph_array[0][0]

    for i in range(len(graph_array)):
        left_nodes = [None]
        current_nodes = graph_array[i]
        right_nodes = [None]

        if i != 0:
            left_nodes = graph_array[i-1]

        if i < len(graph_array) - 1:
            right_nodes = graph_array[i+1]

        for n in range(len(left_nodes)):
            for m in range(len(current_nodes)):
                for o in range(len(right_nodes)):
                    left_node = left_nodes[n]
                    current_node = current_nodes[m]
                    right_node = right_nodes[o]

                    # Check if we can do a elimination with the current node
                    found_node_tuple = current_node.elem_func(left_node,current_node, right_node)

                    if found_node_tuple is None:
                        continue

                    found_node, used_node_sentence, elem_type = found_node_tuple

                    # remove used nodes from the list
                    filtered_array = list(filter(
                        lambda node:
                        node[0].sentence != used_node_sentence and node[0].sentence != current_node.sentence, graph_array
                    ))

                    print(found_node.sentence)
                    print(found_node.type)

                    insert_index = i

                    if elem_type == 'left' and insert_index > 0:
                        insert_index -= 1

                    filtered_array.insert(insert_index, [found_node])

                    result = fold_graph_array(filtered_array)

                    if result is not None:
                        return result
                    # go deeper with new array with 2 nodes less

    return None


def get_variable_dict():
    file = open(ONTOLOGY_PATH)
    json_file = json.load(file)

    file.close()

    informables = json_file['informable']
    variable_dict = {}

    for key, value in informables.items():
        for variable_word in value:
            variable_dict[variable_word] = key

    return variable_dict


def main():
    types_dict = get_types_file_dict()

    sentence = input('Enter senntence\n')

    sequence = transform_sentence(types_dict, sentence)

    graph_array = list(map(tuple_to_graph_node, sequence))

    final_graph = fold_graph_array(graph_array)

    if final_graph is None:
        return

    final_graph.print_whole_graph(0)

    value = find_tree_paths(final_graph)

    print(value)


if __name__ == "__main__":
    main()
