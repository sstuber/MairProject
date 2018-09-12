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

def get_foldernames_in_path(path):
    directory_names = []

    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            directory_names.append(entry.name)

    return directory_names


def get_all_data_paths():
    data_directory_paths = []

    for top_dir_name in get_foldernames_in_path(DATA_PATH):
        for sub_dir_name in get_foldernames_in_path(f'{DATA_PATH}/{top_dir_name}'):
            final_path = f'{DATA_PATH}/{top_dir_name}/{sub_dir_name}'
            data_directory_paths.append(final_path)

    print(data_directory_paths)
    print(len(data_directory_paths))


def main():
    folders = []

    for entry in os.scandir(DATA_PATH + '/Mar13_S1A1/'):
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


if __name__ == "__main__":
    main()
