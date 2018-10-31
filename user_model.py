from enum import Enum

ANY_PREFERENCE_CONSTANT = 'any'

class Preferences(Enum):
    Area = 'area'
    Food = 'food'
    PriceRange = 'pricerange'


class Requestables(Enum):
    Address = 'addr'
    Area = 'area'
    Food = 'food'
    Phone = 'phone'
    PriceRange = 'pricerange'
    PostCode = 'postcode'
    Signature = 'signature'
    Name = 'name'
    Any = ANY_PREFERENCE_CONSTANT


class ConverstationSates(Enum):
    Information = 'information'
    SuggestRestaurant = 'suggestion'
    RestaurantInformation = 'reqinformation'
    Finished = 'finished'


# This class should only hold data
class UserModel:

    def __init__(self):

        self.add_order = []

        self.preferences = {
            Requestables.Area: None,
            Requestables.Food: None,
            Requestables.PriceRange: None
        }

    def get_missing_preference(self):

        if self.preferences[Requestables.Area] is None:
            return Requestables.Area

        if self.preferences[Requestables.Food] is None:
            return Requestables.Food

        if self.preferences[Requestables.PriceRange] is None:
            return Requestables.PriceRange

        return None

    def get_preference(self, requestable: Requestables):

        if requestable not in self.preferences:
            print('invalid preference requested')
            return None

        return self.preferences[requestable]

    def all_preferences_filled(self):

        preferences_are_filled = True

        for requestable, word in self.preferences.items():
            if word is None:
                preferences_are_filled = False

        return preferences_are_filled

    def delete_preference(self, requestable):

        if requestable not in self.preferences:
            print('invalid preference')
            return

        if self.preferences[requestable] is None:
            return

        word = self.preferences[requestable]

        self.add_order = list(filter(lambda x: x != (word, requestable), self.add_order))
        self.preferences[requestable] = None

    def replace_preference(self,word_requestable_tuple):
        if word_requestable_tuple is None:
            return

        self.delete_preference(word_requestable_tuple[1])

        self.add_preference(word_requestable_tuple)

    def add_preference(self, word_requestable_tuple):

        word, requestable = word_requestable_tuple

        if requestable not in self.preferences:
            print('invalid preference')
            return False

        # if self.preferences[requestable] is not None:
        #    print('overwrite preference')

        self.preferences[requestable] = word

        # print (f'preference {requestable} has changed to {self.preferences[requestable]}')

        self.add_order.append(word_requestable_tuple)

        return True





