import re


CLASSIFICATION_PATH = './classification_data.txt'

def main():



    classification_file = open(CLASSIFICATION_PATH)

    classification_str = classification_file.read()

    splitfile = re.split(r'\n', classification_str)

    print(splitfile)


if __name__ == "__main__":
    main()

