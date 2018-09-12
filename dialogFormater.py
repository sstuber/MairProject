import json
import os

DATA_PATH = './testdata'

def format_file(dictionary, filename, b):
    with open(filename) as json_data:
        d = json.load(json_data)

        turns = d['turns']

        for turn in turns:
            turn_index = turn['turn-index']
            if b:
                dictionary[turn_index] = turn['output']['transcript']
            else:
                dictionary[turn_index] = turn['transcription']


def print_dialog(user_dict, system_dict):
    for i in range(max(len(user_dict), len(system_dict))):
        print("system:", system_dict[i])
        print("user:", user_dict[i])

    print("--------------------")


if __name__ == "__main__":
    folders = []

    for entry in os.scandir(DATA_PATH+'/Mar13_S1A1/'):
        if not entry.name.startswith('.') and entry.is_dir():
            folders.append(entry.name)

    for i in range(50):
        folder = folders[i]
        log_file = DATA_PATH + '/Mar13_S1A1/' + folder + '/log.json'
        label_file = DATA_PATH + '/Mar13_S1A1/' + folder + '/label.json'

        user_dictionary = {}
        system_dictionary = {}

        format_file(user_dictionary, label_file, False)
        format_file(system_dictionary, log_file, True)

        print_dialog(user_dictionary, system_dictionary)
