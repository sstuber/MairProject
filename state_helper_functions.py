from get_preference_from_sentence import ONTOLOGY_PATH
from user_model import UserModel, Requestables, ConverstationSates
import json


def get_inform_requestable_dict():
    file = open(ONTOLOGY_PATH)
    json_file = json.load(file)

    file.close()

    informables = json_file['informable']
    variable_dict = {}

    for key, value in informables.items():
        for variable_word in value:
            variable_dict[variable_word] = Requestables(key)

    return variable_dict


# return word + requestable
def get_requestable_from_sentence(sentence: str, requestable_dict):

    results = []
    for word, requestable in requestable_dict.items():

        if word in sentence:
            results.append((word, requestable))

    return results
