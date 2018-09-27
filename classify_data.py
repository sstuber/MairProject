import re


class ClassificationData:
    def __init__(self, classification_str):

        # Get the speech acts separated by a whitespace.
        classification_split = re.split(r'\s', classification_str, 1)

        self.speech_act = classification_split[0]
        full_utterance_str = classification_split[1]

        self.utterance = re.split(r'\s', full_utterance_str)

class ClassificationDictionary:
    def __init__(self):
        self.speech_act_dict = {}
        self.utterance_dict = {}

        # [0, 1] are reserved for padding and out of dictionary words
        self.utterance_count = 1
        self.speech_act_count = 0

    def get_speech_act_id(self, speech_act_str):
        return

    def get_utterance_act_id(self, utterance_str):
        return

