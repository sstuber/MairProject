from get_preference_from_sentence import get_preference_from_sentence
from user_model import UserModel, Requestables, ConverstationSates
from state_helper_functions import get_inform_requestable_dict, get_requestable_from_sentence



# this class should handle the state and its constants
class StateHandler:

    def __init__(self, lstm_model):
        # State constants
        self.lstm_model = lstm_model
        self.inform_to_requestable_dict = get_inform_requestable_dict()

        # State variables
        self.previous_response = None
        self.current_state: ConverstationSates = None
        self.user_model: UserModel = None
        self.reset_state()

    def reset_state(self):
        self.user_model = UserModel()
        self.current_state = ConverstationSates.Information
        self.previous_response = ''

    def continue_conversation(self):
        if self.current_state == ConverstationSates.Finished:
            return False

        return True

    def do_action(self, speech_act, sentence):
        return

    # paramaters should incluse information form do aciton
    def generate_response(self, speech_act):
        print(f'response generated for: {speech_act}')

    # change current state variable based on speech_act
    def change_state(self, speech_act):
        return

    # general Loop
    def handle_action(self, speech_act, sentence):

        self.do_action(sentence, sentence)
        self.generate_response(speech_act)

        self.change_state(speech_act)


def empty_function ():
    return None

def inform_user_model(state_handler, user_input):
    user_preferences = get_preference_from_sentence(user_input)

    # handle preference from parsed sentence
    if user_preferences is not None:

        for requestable_name, variable_path in user_preferences.items():

            word_requestable_tuple = variable_path.get_word_requestable()

            # modify user preference
            state_handler.user_model.add_preference(word_requestable_tuple)

        return

    # handle preference
    requestable_list = get_requestable_from_sentence(user_preferences,state_handler.inform_to_requestable_dict)

    first_word_requestable_tuple = requestable_list[0]

    state_handler.user_model.add_preference(first_word_requestable_tuple)


# modify user model
state_actions = {
    ConverstationSates.Information: {
        'ack': empty_function,
        'affirm': empty_function,
        'bye': empty_function,
        'confirm': empty_function,
        'deny': empty_function,
        'hello': empty_function,
        'inform': empty_function,
        'negate': empty_function,
        'null': empty_function,
        'repeat': empty_function,
        'reqalts': empty_function,
        'reqmore': empty_function,
        'request': empty_function,
        'restart': empty_function,
        'thankyou': empty_function
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': empty_function,
        'affirm': empty_function,
        'bye': empty_function,
        'confirm': empty_function,
        'deny': empty_function,
        'hello': empty_function,
        'inform': empty_function,
        'negate': empty_function,
        'null': empty_function,
        'repeat': empty_function,
        'reqalts': empty_function,
        'reqmore': empty_function,
        'request': empty_function,
        'restart': empty_function,
        'thankyou': empty_function
    },
    ConverstationSates.RestaurantInformation: {
        'ack': empty_function,
        'affirm': empty_function,
        'bye': empty_function,
        'confirm': empty_function,
        'deny': empty_function,
        'hello': empty_function,
        'inform': empty_function,
        'negate': empty_function,
        'null': empty_function,
        'repeat': empty_function,
        'reqalts': empty_function,
        'reqmore': empty_function,
        'request': empty_function,
        'restart': empty_function,
        'thankyou': empty_function
    },
    ConverstationSates.Finished: {
        'ack': empty_function,
        'affirm': empty_function,
        'bye': empty_function,
        'confirm': empty_function,
        'deny': empty_function,
        'hello': empty_function,
        'inform': empty_function,
        'negate': empty_function,
        'null': empty_function,
        'repeat': empty_function,
        'reqalts': empty_function,
        'reqmore': empty_function,
        'request': empty_function,
        'restart': empty_function,
        'thankyou': empty_function
    }
}

state_change = {
    ConverstationSates.Information: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    },
    ConverstationSates.RestaurantInformation: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    },
    ConverstationSates.Finished: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    }
}

state_response = {
    ConverstationSates.Information: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    },
    ConverstationSates.RestaurantInformation: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    },
    ConverstationSates.Finished: {
        'ack': '',
        'affirm': '',
        'bye': '',
        'confirm': '',
        'deny': '',
        'hello': '',
        'inform': '',
        'negate': '',
        'null': '',
        'repeat': '',
        'reqalts': '',
        'reqmore': '',
        'request': '',
        'restart': '',
        'thankyou': ''
    }
}
