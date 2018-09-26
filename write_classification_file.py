import json
import os
from conversation_data import ConversationData, ConversationTypes
from main import CLASSIFICATION_PATH

DATA_PATH = './testdata'

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
    return data_directory_paths


def write_classification_file():
    all_paths = get_all_data_paths()
    conversation_data_list = []

    # Read all files
    for i in range(len(all_paths)):
        print(i)
        path = all_paths[i]

        log_file = f'{path}/log.json'
        label_file = f'{path}/label.json'

        log_json = json.load(open(log_file))
        label_json = json.load(open(label_file))

        # Parse read data
        conversation_data_list.append(ConversationData(label_json, log_json))

    all_classifications = ''

    for conversation in conversation_data_list:
        all_classifications = all_classifications + conversation.get_full_classification_str()

    file = open(CLASSIFICATION_PATH, 'w')
    file.write(all_classifications)


def main():
    write_classification_file()


if __name__ == "__main__":
    main()
