
from get_preference_from_sentence import get_preference_from_sentence
from classify_sentence import get_lstm_model, cross_validation
from user_model import UserModel



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


def main():

    cv_output = cross_validation()

    for value in cv_output:
        print(value)


    #lstm_model = get_lstm_model()

    #print(lstm_model.get_accuracy())
    #user_model = UserModel()

    # start up conversation

    #print('Hello what can i do for you?\n')

    #do_conversation_step(user_model, lstm_model)

    # CV




if __name__ == "__main__":
    main()


