from get_preference_from_sentence import get_preference_from_sentence, ONTOLOGY_PATH
from classify_sentence import get_lstm_model
from user_model import UserModel, Requestables
from state_handler import StateHandler
import json


def handle_conversation_step(state_handler):

    user_input = input('')

    speech_act = state_handler.lstm_model.predict_sentence(user_input)

    state_handler.handle_action(speech_act, user_input)

    handle_conversation_step(state_handler)


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


def get_requestable_from_sentence(sentence, requestable_dict):

    results = []
    for key, value in requestable_dict.items():

        if key in sentence:
            results.append((key, value))

    return results


def main():
    lstm_model = get_lstm_model()

    state_handler = StateHandler(lstm_model)

    # start up conversation

    print('Hello, what can I do for you?')
    state_handler.previous_response = 'What can I do for you?'

    handle_conversation_step(state_handler)


if __name__ == "__main__":
    main()






