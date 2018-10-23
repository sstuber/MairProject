
from get_preference_from_sentence import get_preference_from_sentence, ONTOLOGY_PATH
from classify_sentence import get_lstm_model
from user_model import UserModel, Requestables
import json



def do_conversation_step(user_model: UserModel, lstm_model):

    user_input = input('')

    speech_act = lstm_model.predict_sentence(user_input)

    print(speech_act)


    # TODO generate a correct response to the users input for each speech_act
    if speech_act == 'inform':
        user_preferences = get_preference_from_sentence(user_input)

        if user_preferences is None:
            # TODO use whole sentence as preference
            print('sentence was not parsed')
            do_conversation_step(user_model, lstm_model)
            return

        # TODO actually put found preferences in user model
        for key, value in user_preferences.items():
            print(f'found preference type: {value.variable_type_name}')

    # end conversation
    if speech_act == 'bye' or speech_act == 'thankyou':
        print('Thank you, good bye')
        return


    # go in recursion on this function
    do_conversation_step(user_model, lstm_model)


def get_requestable_dict():
    file = open(ONTOLOGY_PATH)
    json_file = json.load(file)

    file.close()

    informables = json_file['informable']
    variable_dict = {}

    for key, value in informables.items():
        for variable_word in value:
            variable_dict[variable_word] = Requestables(key)

    return variable_dict





def main():
    lstm_model = get_lstm_model()

    user_model = UserModel()

    # start up conversation

    print('Hello what can i do for you?')

    do_conversation_step(user_model, lstm_model)


if __name__ == "__main__":
    main()


def get_requestable_from_sentence(sentence, requestable_dict):

    results = []
    for key, value in requestable_dict.items():

        if key in sentence:
            results.append(value)

    return results



