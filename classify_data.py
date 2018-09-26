import re

class ClassificationData:
    def __init__(self, classification_str):

        classificationsplit = re.split(r'\s', classification_str, 1 )

        self.speech_act = classificationsplit[0]
        self.utterance = classificationsplit[1]



