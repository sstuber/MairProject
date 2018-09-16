
from enum import Enum


class ConversationTypes(Enum):
    User = 'user'
    System = 'system'


get_conversation_from_turn = {
    ConversationTypes.User: lambda user_turn: user_turn['transcription'],
    ConversationTypes.System: lambda system_turn: system_turn['output']['transcript']
}


class ConversationData:
    def __init__(self, user_data, system_data):
        self.input_data = {
            ConversationTypes.User: user_data,
            ConversationTypes.System: system_data
        }

        self.conversations = {}
        self.set_conversation(ConversationTypes.User)
        self.set_conversation(ConversationTypes.System)

    def set_conversation(self, conversation_type: ConversationTypes):
        turns = self.input_data[conversation_type]['turns']
        get_conversation_from_turn_func = get_conversation_from_turn[conversation_type]

        for turn in turns:
            turn_index = turn['turn-index']

            if turn_index in self.conversations:
                user_dict = self.conversations[turn_index]
                user_dict[conversation_type] = get_conversation_from_turn_func(turn)
            else:
                self.conversations[turn_index] = {
                    conversation_type: get_conversation_from_turn_func(turn)
                }
