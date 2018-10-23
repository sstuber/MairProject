from enum import Enum


class Preferences(Enum):
    Area = 'area'
    Food = 'food'
    PriceRange = 'pricerange'


class Requestables(Enum):
    Address = 'addr',
    Area = 'area',
    Food = 'food',
    Phone = 'phone',
    PriceRange = 'pricerange',
    PostCode = 'postcode',
    Signature = 'signature',
    Name = 'name'


class ConverstationSates(Enum):
    Information = 'information'
    SuggestRestaurant = 'suggestion'
    RestaurantInformation = 'reqinformation'


class UserModel:

    def __init__(self):

        self.preferences = {
            Preferences.Area: None,
            Preferences.Food: None,
            Preferences.PriceRange: None
        }

        self.current_state: ConverstationSates = ConverstationSates.Information

