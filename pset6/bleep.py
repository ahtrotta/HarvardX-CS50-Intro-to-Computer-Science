from cs50 import get_string
from sys import argv


def main():

    # check for the correct number of command-line arguments
    if len(argv) != 2:
        exit("Usage: python bleep.py dictionary")

    # get input from the user
    s = get_string("What message would you like to censor?\n")

    # define a set to store banned words in memory
    naughty = set()

    # open file of banned words
    file = open(argv[1], "r")

    # iterate over each line of file
    for line in file:

        # add each words to the set words
        naughty.add(line.rstrip("\n"))

    # close file
    file.close()

    # split input into a list
    words = s.split()

    for word in words:
        if word.lower() in naughty:
            word = '*' * len(word)
        print(f"{word}", end=" ")

    print()


if __name__ == "__main__":
    main()
