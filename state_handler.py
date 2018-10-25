from get_preference_from_sentence import get_preference_from_sentence
from user_model import UserModel, Requestables, ConverstationSates
from state_helper_functions import get_inform_requestable_dict, get_requestable_from_sentence, RestaurantInfo



# this class should handle the state and its constants
class StateHandler:

    def __init__(self, lstm_model):
        # State constants
        self.restaurant_info = RestaurantInfo()
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
        self.restaurant_info.reset()

    def continue_conversation(self):
        if self.current_state == ConverstationSates.Finished:
            return False

        return True

    def do_action(self, speech_act, sentence):
        stateactions = state_actions
        return state_actions[self.current_state][speech_act](state_handler=self, user_input=sentence)

    # paramaters should incluse information form do aciton
    def generate_response(self, speech_act):
        # TODO change to function that depends on the user_state
        print(state_response[self.current_state][speech_act])
        print(f'response generated for: {speech_act}')

    # change current state variable based on speech_act
    def change_state(self, speech_act):
        return state_change[self.current_state][speech_act](state_handler=self)

    # general Loop
    def handle_action(self, speech_act, sentence):

        self.do_action(speech_act, sentence)
        self.generate_response(speech_act)

        self.change_state(speech_act)


def empty(*arg, **dict_args):
    print(arg)
    print(dict_args)
    print('empty action performed')
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
    requestable_list = get_requestable_from_sentence(user_input, state_handler.inform_to_requestable_dict)

    first_word_requestable_tuple = requestable_list[0]

    state_handler.user_model.add_preference(first_word_requestable_tuple)


# modify user model
state_actions = {
    ConverstationSates.Information: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': inform_user_model,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': empty,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    },
    ConverstationSates.RestaurantInformation: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': empty,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    },
    ConverstationSates.Finished: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': empty,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    }
}


def change_state_inform_state(state_handler):
    if state_handler.current_state == ConverstationSates.Information:
        if state_handler.user_model.all_preferences_filled():

            state_handler.current_state = ConverstationSates.SuggestRestaurant


state_change = {
    ConverstationSates.Information: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': change_state_inform_state,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': empty,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    },
    ConverstationSates.RestaurantInformation: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': empty,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
    },
    ConverstationSates.Finished: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': empty,
        'negate': empty,
        'null': empty,
        'repeat': empty,
        'reqalts': empty,
        'reqmore': empty,
        'request': empty,
        'restart': empty,
        'thankyou': empty
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
