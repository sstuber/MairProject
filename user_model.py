from enum import Enum


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

    def get_preference(self, requestable: Requestables):

        if requestable not in self.preferences:
            print('invalid preference requested')
            return None

        return self.preferences[requestable]

    def delete_preference(self, requestable):

        if requestable not in self.preferences:
            print('invalid preference')
            return

        if self.preferences[requestable] is None:
            print('preference already empty')
            return

        word = self.preferences[requestable]

        self.add_order = list(filter(lambda x: x != (word, requestable), self.add_order))
        self.preferences[requestable] = None

    def add_preference(self, word_requestable_tuple):

        word, requestable = word_requestable_tuple

        if requestable not in self.preferences:
            print('invalid preference')
            return False

        self.preferences[requestable] = word

        print (f'preference {requestable} has changed to {self.preferences[requestable]}')

        self.add_order.append(word_requestable_tuple)

        return True





