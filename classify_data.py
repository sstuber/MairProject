import re


class ClassificationData:
    def __init__(self, classification_str):

        # Get the speech acts separated by a whitespace.
        classification_split = re.split(r'\s', classification_str, 1)

        self.speech_act = classification_split[0]
        full_utterance_str = classification_split[1]

        self.utterance = re.split(r'\s', full_utterance_str)


class NumberedClassification:
    def __init__(self):
        self.speech_act = 0
        self.utterance = []


class ClassificationDictionary:
    def __init__(self):
        self.speech_act_dict = {}
        self.utterance_dict = {}

        # [0, 1] are reserved for padding and out of dictionary words
        self.utterance_count = 1

        # should this start at 0 or -1?
        self.speech_act_count = 0

    def get_speech_act_id(self, speech_act_str):

        if speech_act_str in self.speech_act_dict:
            return self.speech_act_dict[speech_act_str]
        else:
            # up the current max index
            self.speech_act_count += 1

            # Use new max index to set in dictionary
            self.speech_act_dict[self.speech_act_count] = speech_act_str
            self.speech_act_dict[speech_act_str] = self.speech_act_count

            # Return new max in dex
            return self.speech_act_count

    # While training we assign new id's to new words
    def get_training_utterance_id(self, utterance_str):

        if utterance_str in self.utterance_dict:
            return self.utterance_dict[utterance_str]
        else:
            self.utterance_count += 1

            self.utterance_dict[self.utterance_count] = utterance_str
            self.utterance_dict[utterance_str] = self.utterance_count

            return self.utterance_count

    # while testing we assign 0 to new words
    def get_testing_utterance_id(self, utterance_str):
        if utterance_str in self.utterance_dict:
            return self.utterance_dict[utterance_str]
        else:
            return 0
