import json
import os



def formatFile(dictionary, filename, b):
    with open(filename) as json_data:
        d = json.load(json_data)

        turns = d['turns']

        for turn in turns:
            turnIndex = turn['turn-index']
            if b:
                dictionary[turnIndex] = turn['output']['transcript']
            else:
                dictionary[turnIndex] = turn['transcription']

def printDialog(userDictionary, systemDictionary):
    for i in range(max(len(userDictionary), len(systemDictionary))):
        print("system:", systemDictionary[i])
        print("user:", userDictionary[i])

    print("--------------------")

if __name__== "__main__":
    folders = []

    path = '/Users/mba/Downloads/dstc2_traindev/data/Mar13_S1A1/'
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            folders.append(entry.name)

    for i in range(50):
        folder = folders[i]
        logfile = '/Users/mba/Downloads/dstc2_traindev/data/Mar13_S1A1/' + folder + '/log.json'
        labelfile = '/Users/mba/Downloads/dstc2_traindev/data/Mar13_S1A1/' + folder + '/label.json'

        userDictionary = {}
        systemDictionary = {}

        formatFile(userDictionary, labelfile, False)
        formatFile(systemDictionary, logfile, True)

        printDialog(userDictionary, systemDictionary)