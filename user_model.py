from enum import Enum


class Preferences(Enum):
    Area = 'area'
    Food = 'food'
    PriceRange = 'pricerange'


class UserModel:

    def __init__(self):

        self.preferences = {
            Preferences.Area: None,
            Preferences.Food: None,
            Preferences.PriceRange: None
        }


