import keras

'''
x_train is a list of lists, with each sub-list containing the integers of utterances
y_train is a list of integers, with each integer representing the speech act of the corresponding set of utterances.
'''

class LSTM_model():
    def __init__(self):
        self.FILENAME_SPEECHACT = './numbered_data_speechact.txt'
        self.FILENAME_UTTERANCES = './numbered_data_utterances.txt'

        (x_train, y_train) = self.get_traindata()
        (x_test, y_test) = self.get_testdata()


    def get_traindata(self):
        # Import 85% of numbered data as training set
        utterances = open(self.FILENAME_UTTERANCES, 'r')
        # convert text to list
        utterances.close()

        speechacts = open(self.FILENAME_SPEECHACT, 'r')
        # convert text to list
        speechacts.close()


    def get_testdata(self):
        # Import 15% of numbered data as test set
        utterances = open(self.FILENAME_UTTERANCES, 'r')
        # convert text to list
        utterances.close()

        speechacts = open(self.FILENAME_SPEECHACT, 'r')
        # convert text to list
        speechacts.close()
