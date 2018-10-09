
import re

MATCH_REGEX = r'(\w+|\(.+\))(\/|\\)(\(.+\)|\w+)|(\w+)'

LEFT_HAND_ID = 0
FUNCTION_ID = 1
RIGHT_HAND_ID = 2
SINGLETON_ID = 3


class GraphNode:

    def __str__(self):
        return f'GraphNode: {self.sentence} {self.type} {self.match_tuple}\n'

    def __init__(self, information_tuple):
        self.sentence, self.type = information_tuple
        self.right_child = None
        self.left_child = None

        match_object = re.match(MATCH_REGEX, self.type)

        self.match_tuple = match_object.groups()

        function_dict = {
            '/': elem_right,
            '\ ': elem_left,
            None: singleton_func
        }

        self.elem_func = function_dict[self.match_tuple[FUNCTION_ID]]


def normalize_type(type_str: str):

    if type_str[0] == '(':
        type_str = type_str[1:-1]

    return type_str


def elem_right(left_node, right_node, current_node):

    # if right node does not exist we do nothing
    if right_node is None:
        return None

    right_hand_side = current_node.match_tuple[RIGHT_HAND_ID]

    # if type does not fit this elem we do nothing
    if right_node.type != right_hand_side:
        return None

    # get left side of equation from current node
    new_type = current_node.match_tuple[LEFT_HAND_ID]
    new_type = normalize_type(new_type)
    # format the new sentence
    new_sentence = f'{current_node.sentence} {right_node.sentence}'

    node = GraphNode((new_sentence, new_type))

    node.left_child = current_node
    node.right_child = right_node

    return node


def elem_left(left_node, right_node, current_node):

    if left_node is None:
        return None

    left_hand_side = current_node.match_tuple[LEFT_HAND_ID]

    if left_node.type != left_hand_side:
        return None

    new_type = current_node.match_tuple[RIGHT_HAND_ID]
    new_type = normalize_type(new_type)

    new_sentence = f'{left_node.sentence} {current_node.sentence}'

    node = GraphNode((new_sentence, new_type))

    node.left_child = left_node
    node.right_child = current_node

    return node


def singleton_func(left_node, right_node, current_node):
    return None

