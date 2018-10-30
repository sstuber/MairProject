from get_preference_from_sentence import get_preference_from_sentence
from user_model import UserModel, Requestables, ConverstationSates, ANY_PREFERENCE_CONSTANT
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


def set_user_preference_from_simple_sentence(state_handler, user_input):
    preferables = {
        'area': Requestables.Area,
        'price range': Requestables.PriceRange,
        'food': Requestables.Food
    }

    # handle preference
    requestable_list = get_requestable_from_sentence(user_input, state_handler.inform_to_requestable_dict)

    if len(requestable_list) == 0:
        return {'set_preference': []}

    first_word_requestable_tuple = requestable_list[0]

# if any preference is stated then find out on what it is about
    if first_word_requestable_tuple[1] == Requestables.Any:

        preferred_list = get_requestable_from_sentence(user_input, preferables)

        # if type of preference is not mentioned use missing
        if len(preferred_list) == 0:
            set_user_preference = state_handler.user_model.get_missing_preference()

            first_word_requestable_tuple = (ANY_PREFERENCE_CONSTANT, set_user_preference)
        else:
            given_preference_tuple = preferred_list[0]
            requestable_preference_type = given_preference_tuple[1]
            first_word_requestable_tuple = (ANY_PREFERENCE_CONSTANT, requestable_preference_type)

    state_handler.user_model.replace_preference(first_word_requestable_tuple)

    return {'set_preference': [first_word_requestable_tuple]}


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

        return {'set_preference':  word_requestable_tuple_list}

    return set_user_preference_from_simple_sentence(state_handler, user_input)


def affirm_suggested_restaurant(state_handler, user_input, **kwargs):

    state_handler.selected_restaurant = state_handler.restaurant_info.selected_restaurant

    return {'restaurant_confirmed': True}


def no_action(state_handler, user_input):
    return {}


def request_information(state_handler, user_input):
    request_dict = {"phone" : "phone",
                    "number": "phone",
                    "address": "addr",
                    "where": "addr",
                    "postcode": "postcode",
                    'area': 'area',
                    'food': 'food',
                    'price range': 'pricerange',
                    'name': 'restaurantname'}

    requestable_list = get_requestable_from_sentence(user_input, request_dict)

    information_requests = set()
    for (_, request) in requestable_list:
        information_requests.add(request)

    if state_handler.current_state == ConverstationSates.SuggestRestaurant:
        state_handler.selected_restaurant = state_handler.restaurant_info.selected_restaurant

    return {"requests" : information_requests, 'restaurant_confirmed': True}


def restart_conversation(state_handler, user_input):
    state_handler.reset_state()

    return {}


def reqalt_update_information(state_handler, user_input, **kwargs):
    extra_data = set_user_preference_from_simple_sentence(state_handler, user_input)

    if len(extra_data['set_preference']) > 0:
        state_handler.restaurant_info.reset()

    return extra_data

def repeat_information(state_handler, user_input, **kwargs):

    return {}


# all functions must return a dict or None
# modify user model
# null = doesnt understand (in current state), give null response
state_actions = {
    ConverstationSates.Information: {
        'ack': no_action,       # null
        'affirm': no_action,    # null
        'bye': no_action,
        'confirm': no_action,   # null
        'deny': no_action,      # null
        'hello': no_action,
        'inform': inform_user_model,
        'negate': no_action,    # null
        'null': no_action,
        'repeat': request_information,
        'reqalts': reqalt_update_information,
        'reqmore': no_action,   # null
        'request': no_action,   # null
        'restart': restart_conversation,
        'thankyou': no_action
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': affirm_suggested_restaurant,
        'affirm': affirm_suggested_restaurant,
        'bye': no_action,
        'confirm': no_action,   # null
        'deny': no_action,      # null
        'hello': no_action,
        'inform': no_action,    # null
        'negate': no_action,    # null
        'null': no_action,
        'repeat': request_information,
        'reqalts': reqalt_update_information,
        'reqmore': empty,   # moet nog
        'request': request_information,
        'restart': restart_conversation,
        'thankyou': no_action
    },
    ConverstationSates.RestaurantInformation: {
        'ack': no_action,       # null
        'affirm': no_action,    # null
        'bye': no_action,
        'confirm': no_action,   # null
        'deny': no_action,      # null
        'hello': no_action,
        'inform': reqalt_update_information,
        'negate': no_action,    # null
        'null': no_action,
        'repeat': request_information,
        'reqalts': reqalt_update_information,
        'reqmore': empty,       # moet nog
        'request': request_information,
        'restart': restart_conversation,
        'thankyou': no_action
    },
    ConverstationSates.Finished: {
        'ack': no_action,
        'affirm': no_action,
        'bye': no_action,
        'confirm': no_action,
        'deny': no_action,
        'hello': no_action,
        'inform': no_action,
        'negate': no_action,
        'null': no_action,
        'repeat': no_action,
        'reqalts': no_action,
        'reqmore': no_action,
        'request': no_action,
        'restart': restart_conversation,
        'thankyou': no_action
    }
}


def check_preference_and_suggest_restaurant(state_handler, extra_data):
    if state_handler.user_model.all_preferences_filled():
        state_handler.current_state = ConverstationSates.SuggestRestaurant
        extra_data['state_changed'] = True


def change_state_inform_state(state_handler, extra_data = None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if state_handler.current_state == ConverstationSates.Information:
        check_preference_and_suggest_restaurant(state_handler, extra_data)

    return extra_data


def change_state_affirm_suggested_restaurant(state_handler, extra_data = None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if state_handler.current_state == ConverstationSates.SuggestRestaurant:
        if extra_data['restaurant_confirmed']:
            state_handler.current_state = ConverstationSates.RestaurantInformation

    return extra_data


# if inform and not everything filled we stay in inform
# if any other state changing 1 preference will keep everything filled thus we can suggest a restaurant anyway
def change_state_reqalt_general(state_handler, extra_data = None, **kwargs):
    check_preference_and_suggest_restaurant(state_handler, extra_data)
    return extra_data


def no_state_change(state_handler, extra_data):
    if extra_data is None:
        extra_data = {}

    return extra_data


def change_end_conversation(state_handler, extra_data = None):
    previous_state = state_handler.current_state
    state_handler.current_state = ConverstationSates.Finished

    return {"previous_state" : previous_state}


def change_request(state_handler, extra_data = None):
    if extra_data is None:
        extra_data = {}

    if state_handler.current_state == ConverstationSates.SuggestRestaurant:
        state_handler.current_state = ConverstationSates.RestaurantInformation

    return extra_data


# - should be impossible to reach
state_change = {
    ConverstationSates.Information: {
        'ack': no_state_change,     # null
        'affirm': no_state_change,  # null
        'bye': change_end_conversation,
        'confirm': no_state_change, # null
        'deny': no_state_change,    # null
        'hello': no_state_change,
        'inform': change_state_inform_state,
        'negate': no_state_change,  # null
        'null': no_state_change,
        'repeat': no_state_change,
        'reqalts': change_state_reqalt_general,
        'reqmore': empty,           # moet nog
        'request': no_state_change, # null
        'restart': no_state_change,
        'thankyou': change_end_conversation
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': change_state_affirm_suggested_restaurant,
        'affirm': change_state_affirm_suggested_restaurant,
        'bye': change_end_conversation,
        'confirm': no_state_change, # null
        'deny': no_state_change,    # null
        'hello': no_state_change,
        'inform': no_state_change,  # null
        'negate': no_state_change,  # null
        'null': no_state_change,
        'repeat': no_state_change,
        'reqalts': change_state_reqalt_general,
        'reqmore': empty,           # moet nog
        'request': change_request,
        'restart': no_state_change,
        'thankyou': change_end_conversation
    },
    ConverstationSates.RestaurantInformation: {
        'ack': no_state_change,     # null
        'affirm': no_state_change,  # null
        'bye': change_end_conversation,
        'confirm': no_state_change, # null
        'deny': no_state_change,    # null
        'hello': no_state_change,
        'inform': no_state_change,  # null
        'negate': no_state_change,  # null
        'null': no_state_change,
        'repeat': no_state_change,
        'reqalts': change_state_reqalt_general,
        'reqmore': no_state_change, # null
        'request': change_request,
        'restart': no_state_change,
        'thankyou': change_end_conversation
    },
    ConverstationSates.Finished: {
        'ack': no_state_change,
        'affirm': no_state_change,
        'bye': change_end_conversation,
        'confirm': no_state_change,
        'deny': no_state_change,
        'hello': no_state_change,
        'inform': no_state_change,
        'negate': no_state_change,
        'null': no_state_change,
        'repeat': no_state_change,
        'reqalts': no_state_change,
        'reqmore': no_state_change,
        'request': no_state_change,
        'restart': empty,   # -
        'thankyou': change_end_conversation
    }
}


def print_user_preferences(state_handler,extra_data = None):
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


def inform_notify_user_of_preference(state_handler,extra_data = None, **kwargs):
    if extra_data is None:
        extra_data = {}

    if 'set_preference' in extra_data:
        print_user_preferences(state_handler,extra_data)



def print_suggest_restaurant(state_handler):

    food_pref = state_handler.user_model.get_preference(Requestables.Food)
    price_pref = state_handler.user_model.get_preference(Requestables.PriceRange)
    area_pref = state_handler.user_model.get_preference(Requestables.Area)

    suggested_restaurant = state_handler.restaurant_info.get_suggestions(
        food_preference=food_pref, pricerange_preference=price_pref, area_preference=area_pref
    )

    if suggested_restaurant is None:
        no_restaurant_str = 'There is no restaurant with your preferences. Try to change your preferences'
        state_handler.previous_response = no_restaurant_str
        print(no_restaurant_str)
        return

    restaurant_name = suggested_restaurant['restaurantname']

    add_order = state_handler.user_model.add_order

    print(
        f'Your preferences are {add_order[0][1].value} {add_order[0][0]}, {add_order[1][1].value} {add_order[1][0]} and {add_order[2][1].value} {add_order[2][0]}')

    suggested_restaurant_str = f'According to your preferences i suggest this restaurant {restaurant_name}'
    print(suggested_restaurant_str)
    state_handler.previous_response = suggested_restaurant_str


def inform_setting_user_preference(state_handler, extra_data=None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if 'state_changed' in extra_data:
        print_suggest_restaurant(state_handler)

def reqalt_suggest_restaurant(state_handler, extra_data=None, **kwargs):

    print_suggest_restaurant(state_handler)


def affirm_notify_restaurant_selected(state_handler, extra_data=None, **kwargs):

    if extra_data is None:
        extra_data = {}

    if 'restaurant_confirmed' in extra_data:

        selected_restaurant = state_handler.selected_restaurant
        selected_restaurant_name = selected_restaurant['restaurantname']

        response_str = f'The selected restaurant is {selected_restaurant_name}. What for information would you like about this restaurant?'
        state_handler.previous_response = response_str
        print(response_str)


def hello_information(state_handler, extra_data=None, **kwargs):
    next_preference = state_handler.user_model.get_missing_preference()
    next_preference_str = f'Hello! What would you like for {next_preference.value}'

    state_handler.previous_response = next_preference_str
    print(next_preference_str)


def hello_other(state_handler, extra_data=None, **kwargs):
    suggested_restaurant = state_handler.restaurant_info.get_suggestions()
    restaurant_name = suggested_restaurant['restaurantname']

    suggested_restaurant_str = f'Hello! What for information would you like about {restaurant_name}?'

    state_handler.previous_response = suggested_restaurant_str
    print(suggested_restaurant_str)


def hello_general(state_handler, extra_data =None, **kwargs):
    previous_response = state_handler.previous_response

    print(f'Hello! {previous_response}')


def null_general(state_handler, extra_data =None, **kwargs):
    previous_response = state_handler.previous_response

    print(f'I did not understand you... {previous_response}')


def end_conversation(state_handler, extra_data=None, **kwargs):
    if extra_data is None:
        extra_data = {}

    if extra_data['previous_state'] == ConverstationSates.RestaurantInformation:
        response_str = "Goodbye, enjoy your meal."
    elif extra_data['previous_state'] == ConverstationSates.Finished:
        print("The conversation has finished. Start over if you would like to find another restaurant.")
        return
    else:
        response_str = "Goodbye."

    state_handler.previous_response = response_str
    print(response_str)


def give_restaurant_information(state_handler, extra_data=None, **kwargs):
    if extra_data is None:
        print("Sorry, I did not understand your request.")
    else:
        selected_restaurant = state_handler.selected_restaurant
        response_str = selected_restaurant['restaurantname'] + "'s "

        for request in extra_data['requests']:
            if request == 'phone':
                response_str += "phone number"
            elif request == 'addr':
                response_str += "address"
            elif request == 'postcode':
                response_str += "postcode"
            elif request == 'food':
                response_str += 'food'
            elif request == 'pricerange':
                response_str += 'price range'
            elif request == 'area':
                response_str += 'area'
            elif request == 'restaurantname':
                response_str += 'name'

            response_str += " is " + selected_restaurant[request] + " and its "

        response_str = response_str[:-9]
        response_str += "."

        state_handler.previous_response = response_str
        print(response_str)


def response_restart(state_handler, extra_data=None, **kwargs):
    response_str = "Hello, what can I do for you?"
    state_handler.previous_response = response_str
    print(response_str)


def conversation_finished(state_handler, extra_data=None, **kwargs):
    print("The conversation has finished. Start over if you would like to find another restaurant.")


def response_repeat(state_handler, extra_data=None, **kwargs):
    if len(extra_data["requests"]) == 0:
        print(state_handler.previous_response)
    else:
        print("----")
        give_restaurant_information(state_handler, extra_data)


# - should be impossible to reach
state_response = {
    ConverstationSates.Information: {
        'ack': null_general,        # null
        'affirm': null_general,     # null
        'bye': empty,               # -
        'confirm': null_general,    # null
        'deny': null_general,       # null
        'hello': hello_general,
        'inform': inform_notify_user_of_preference,
        'negate': null_general,     # null
        'null': null_general,
        'repeat': response_repeat,
        'reqalts': inform_notify_user_of_preference,
        'reqmore': empty,           # moet nog
        'request': null_general,    # null
        'restart': response_restart,
        'thankyou': empty           # -
    },
    ConverstationSates.SuggestRestaurant: {
        'ack': affirm_notify_restaurant_selected,
        'affirm': affirm_notify_restaurant_selected,
        'bye': empty,               # -
        'confirm': null_general,    # null
        'deny': null_general,       # null
        'hello': hello_general,
        'inform': inform_setting_user_preference,
        'negate': null_general,     # null
        'null': null_general,
        'repeat': response_repeat,
        'reqalts': reqalt_suggest_restaurant,
        'reqmore': empty,           # moet nog
        'request': empty,           # -
        'restart': empty,           # -
        'thankyou': empty           # -
    },
    ConverstationSates.RestaurantInformation: {
        'ack': affirm_notify_restaurant_selected,
        'affirm': affirm_notify_restaurant_selected,
        'bye': empty,               # -
        'confirm': null_general,    # null
        'deny': null_general,       # null
        'hello': hello_general,
        'inform': empty,            # -
        'negate': null_general,     # null
        'null': null_general,
        'repeat': response_repeat,
        'reqalts': empty,           # -
        'reqmore': empty,           # -
        'request': give_restaurant_information,
        'restart': empty,           # -
        'thankyou': empty           # -
    },
    ConverstationSates.Finished: {
        'ack': conversation_finished,
        'affirm': conversation_finished,
        'bye': end_conversation,
        'confirm': conversation_finished,
        'deny': conversation_finished,
        'hello': conversation_finished,
        'inform': conversation_finished,
        'negate': conversation_finished,
        'null': conversation_finished,
        'repeat': conversation_finished,
        'reqalts': conversation_finished,
        'reqmore': conversation_finished,
        'request': conversation_finished,
        'restart': empty,   # -
        'thankyou': end_conversation
    }
}
