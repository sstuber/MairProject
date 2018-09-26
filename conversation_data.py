from enum import Enum
from typing import Dict
import re


class ConversationTypes(Enum):
    System = 'system'
    User = 'user'


Conversation_Collection = Dict[int, Dict[ConversationTypes, str]]


def user_turn_to_conversation(user_turn: Dict) -> str:
    return user_turn['transcription']


def system_turn_to_conversation(system_turn: Dict) -> str:
    return system_turn['output']['transcript']


# Dictionary ConversationType -> (function Dict -> string)
TURN_TO_CONVERSATION_FUNC_DICT = {
    ConversationTypes.User: user_turn_to_conversation,
    ConversationTypes.System: system_turn_to_conversation
}


class ConversationData:
    def __init__(self, user_data, system_data):
        self.user_data = user_data
        self.classification = []

        self.input_data: Dict[ConversationTypes, Dict] = {
            ConversationTypes.User: user_data,
            ConversationTypes.System: system_data
        }
        self.set_classification_data()

        self.conversations: Conversation_Collection = {}
        self.set_conversation(ConversationTypes.User)
        self.set_conversation(ConversationTypes.System)

    def set_conversation(self, conversation_type: ConversationTypes):
        turns = self.input_data[conversation_type]['turns']
        turn_to_conversation_func = TURN_TO_CONVERSATION_FUNC_DICT[conversation_type]

        for turn in turns:
            turn_index = turn['turn-index']

            if turn_index in self.conversations:
                user_dict = self.conversations[turn_index]
                user_dict[conversation_type] = turn_to_conversation_func(turn)
            else:
                self.conversations[turn_index] = {
                    conversation_type: turn_to_conversation_func(turn)
                }

    def set_classification_data(self):
        turns = self.user_data['turns']

        classification_data = []

        for turn in turns:
            transcription = turn['transcription']
            classification = turn['semantics']['cam']

            classification = re.sub(r'\(.*\)', '', classification)

            classification_data.append(f'{classification} {transcription}\n')

        self.classification = classification_data

    def get_full_classification_str(self):
        classify_str = ''

        for classify_string in self.classification:
            classify_str += classify_string

        return classify_str

    def get_title(self):
        title_json = self.input_data[ConversationTypes.User]

        session_id = title_json['session-id']
        task_information = title_json['task-information']['goal']['text']

        title_str = f'session id: {session_id}\n{task_information}'

        return title_str

    # print the whole conversation
    def print_conversation(self):
        print(self.conversation_to_string())

    def conversation_to_string(self):
        conversation = self.get_title()

        for i in range(len(self.conversations)):
            conversation_dict = self.conversations[i]

            for conversation_type in ConversationTypes:
                pronoun = conversation_type.value
                sentence = conversation_dict[conversation_type]

                conversation = conversation + f'{pronoun}: {sentence}\n'

        conversation = conversation + '\n'

        return conversation
