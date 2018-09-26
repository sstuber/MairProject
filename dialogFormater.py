import json
import os
from conversation_data import ConversationData, ConversationTypes

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


def main():

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

    # write all conversations to a file
    all_conversations = ''
    for conversation in conversation_data_list:
        all_conversations = all_conversations + conversation.conversation_to_string()

    file = open('./conversations.txt', 'w')
    file.write(all_conversations)

    # Print a conversation and print the next by pressing enter
    for i in range(len(conversation_data_list)):
        conversation = conversation_data_list[i]
        conversation.print_conversation()
        input('Press enter to continue')


if __name__ == "__main__":
    main()
