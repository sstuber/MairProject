from get_preference_from_sentence import ONTOLOGY_PATH
from user_model import UserModel, Requestables, ConverstationSates, ANY_PREFERENCE_CONSTANT
import json
import csv

def get_inform_requestable_dict():
    file = open(ONTOLOGY_PATH)
    json_file = json.load(file)

    file.close()

    informables = json_file['informable']
    variable_dict = {}

    for key, value in informables.items():
        for variable_word in value:
            variable_dict[variable_word] = Requestables(key)

    return variable_dict


# return word + requestable
def get_requestable_from_sentence(sentence: str, requestable_dict):

    results = []
    for word, requestable in requestable_dict.items():

        if word in sentence:
            results.append((word, requestable))

    return results


def get_restaurant_list():
    reader = csv.DictReader(open('restaurantinfo.csv'))

    restaurant_dict_list = []
    for restaurant_dict in reader:
        restaurant_dict_list.append(restaurant_dict)

    return restaurant_dict_list


class RestaurantInfo:

    def __init__(self):
        reader = csv.DictReader(open('restaurantinfo.csv'))

        restaurant_dict_list = []
        for restaurant_dict in reader:
            restaurant_dict_list.append(restaurant_dict)

        self.restaurant_list = restaurant_dict_list
        self.preferred_restaurant_list = None
        self.selected_restaurant = None
        self.current_index = 0

    def reset(self):
        self.preferred_restaurant_list = None
        self.selected_restaurant = None
        self.current_index = 0

    def get_next_suggestion(self):
        self.current_index += 1

        if self.current_index >= len(self.preferred_restaurant_list):
            return None

        self.selected_restaurant = self.preferred_restaurant_list[self.current_index]
        return self.selected_restaurant

    def get_suggestions(self, food_preference=None, pricerange_preference=None, area_preference=None):

        if self.preferred_restaurant_list is not None:
            return self.get_next_suggestion()

        preferred_restaurants = []

        # if A restaurant has all our preferences or we don't care
        for restuarant_dict in self.restaurant_list:

            if food_preference is not None:
                if restuarant_dict['food'] != food_preference and food_preference != ANY_PREFERENCE_CONSTANT:
                    continue

            if pricerange_preference is not None:
                if restuarant_dict['pricerange'] != pricerange_preference and pricerange_preference != ANY_PREFERENCE_CONSTANT:
                    continue

            if area_preference is not None:
                if restuarant_dict['area'] != area_preference and area_preference != ANY_PREFERENCE_CONSTANT:
                    continue

            preferred_restaurants.append(restuarant_dict)

        if len(preferred_restaurants) == 0:
            return None

        self.preferred_restaurant_list = preferred_restaurants
        self.selected_restaurant = preferred_restaurants[0]

        return self.selected_restaurant

