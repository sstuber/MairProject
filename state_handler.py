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
        self.selected_restaurand = None
        self.previous_response = None
        self.current_state: ConverstationSates = None
        self.user_model: UserModel = None
        self.reset_state()

    def reset_state(self):
        self.selected_restaurand = None
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
    def generate_response(self, speech_act, extra_data_dict = None):
        # TODO change to function that depends on the user_state
        state_response[self.current_state][speech_act](state_handler=self, extra_data=extra_data_dict)
        print(f'response generated for: {speech_act}')

    # change current state variable based on speech_act
    def change_state(self, speech_act, extra_data_dict = None):
        return state_change[self.current_state][speech_act](state_handler=self, extra_data=extra_data_dict)

    # general Loop
    def handle_action(self, speech_act, sentence):

        action_data = self.do_action(speech_act, sentence)
        change_data = self.change_state(speech_act, action_data)

        self.generate_response(speech_act, change_data)



def empty(*arg, **dict_args):
    print(arg)
    print(dict_args)
    print('empty action performed')
    return None

def inform_user_model(state_handler, user_input):
    user_preferences = get_preference_from_sentence(user_input)

    # handle preference from parsed sentence
    if user_preferences is not None:

        word_requestable_tuple_list= []

        for requestable_name, variable_path in user_preferences.items():

            word_requestable_tuple = variable_path.get_word_requestable()
            word_requestable_tuple_list.append(word_requestable_tuple)
            # modify user preference
            state_handler.user_model.add_preference(word_requestable_tuple)

        return { 'set_preference':  word_requestable_tuple_list}

    # handle preference
    requestable_list = get_requestable_from_sentence(user_input, state_handler.inform_to_requestable_dict)

    first_word_requestable_tuple = requestable_list[0]

    state_handler.user_model.add_preference(first_word_requestable_tuple)

    return { 'set_preference':  [first_word_requestable_tuple]}


def affirm_suggested_restaurant(state_handler, user_input, **kwargs):

    state_handler.selected_restaurant = state_handler.restaurant_info.selected_restaurant

    return {'restaurant_confirmed': True}


# all functions must return a dict or None
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
        'ack': affirm_suggested_restaurant,
        'affirm': affirm_suggested_restaurant,
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


def change_state_inform_state(state_handler, extra_data = None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if state_handler.current_state == ConverstationSates.Information:
        if state_handler.user_model.all_preferences_filled():

            state_handler.current_state = ConverstationSates.SuggestRestaurant
            extra_data['state_changed'] = True


    return extra_data

def change_state_affirm_suggested_restaurant(state_handler, extra_data = None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if state_handler.current_state == ConverstationSates.SuggestRestaurant:
        if extra_data['restaurant_confirmed']:
            state_handler.current_state = ConverstationSates.RestaurantInformation

    return extra_data


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


def inform_notify_user_of_preference(state_handler,extra_data = None, **kwargs):
    if extra_data is None:
        extra_data = {}

    if 'set_preference' in extra_data:
        changed_preferences_string = 'Your preferences are '
        changed_preferences = extra_data['set_preference']

        for i in range(len(changed_preferences)):
            preference = changed_preferences[i]
            changed_preferences_string = f'{changed_preferences_string}{preference[1].value}: {preference[0]}'

            if i < len(changed_preferences) - 2:
                changed_preferences_string = f'{changed_preferences_string}, '
            elif i < len(changed_preferences) - 1:
                changed_preferences_string = f'{changed_preferences_string} and '

        print(changed_preferences_string)

        next_preference = state_handler.user_model.get_missing_preference()
        next_preference_str = f'What would you like for {next_preference.value}'

        state_handler.previous_response = next_preference_str
        print(next_preference_str)


def inform_setting_user_preference(state_handler, extra_data=None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if 'state_changed' in extra_data:
        suggested_restaurant = state_handler.restaurant_info.get_suggestions()
        restaurant_name = suggested_restaurant['restaurantname']

        add_order = state_handler.user_model.add_order

        print(f'Your preferences are {add_order[0][1].value} {add_order[0][0]}, {add_order[1][1].value} {add_order[1][0]} and {add_order[2][1].value} {add_order[2][0]}')

        suggested_restaurant_str = f'According to your preferences i suggest this restaurant {restaurant_name}'
        print(suggested_restaurant_str)
        state_handler.previous_response = suggested_restaurant_str

def affirm_notify_restaurant_selected(state_handler, extra_data=None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if 'restaurant_confirmed' in extra_data:

        selected_restaurant = state_handler.selected_restaurant
        selected_restaurant_name = selected_restaurant['restaurantname']


        print(f'The selected restaurant is {selected_restaurant_name}')
        print('What for information would you like about this restaurant?')




state_response = {
    ConverstationSates.Information: {
        'ack': empty,
        'affirm': empty,
        'bye': empty,
        'confirm': empty,
        'deny': empty,
        'hello': empty,
        'inform': inform_notify_user_of_preference,
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
        'inform': inform_setting_user_preference,
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
        'ack': affirm_notify_restaurant_selected,
        'affirm': affirm_notify_restaurant_selected,
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
