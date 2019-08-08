from sys import argv
import crypt

# set maximum number of letters for password
LETT = 5

# check for correct number of command-line arguments
if len(argv) != 2:
    exit("Usage: python crack.py hash")

# store the hash in a variable
h = argv[1]

# store the salt
salt = h[0:2]

# define variables for generating ordered list of letters
index = []
init = "a"

# generate an ordered list of uppercase and lowercase letters
for i in range(52):

    if i == 0:
        index.append(init)

    elif i > 0 and i < 26:
        init = chr(ord(init) + 1)
        index.append(init)

    elif i == 26:
        init = "A"
        index.append(init)

    else:
        init = chr(ord(init) + 1)
        index.append(init)


# recursive function for generating all possible letter combinations of a given length
def generate(i):

    # iterate through characters of the list
    for j in range(i):

        # iterate through letters in the index
        for k in range(53):

            # reset the character to 'a' at the end
            if k == 52:
                word[j] = 'a'
            else:

                # assign the appropriate letter to the list
                word[j] = index[k]

                # convert the list to a string
                test = ''.join(word)

                # run the hash function
                hsh = crypt.crypt(test, salt)

                # compare the hash function to the input
                if hsh == h:
                    print(f"{test}")
                    quit()

                # recursively call the function
                else:
                    generate(j)


# iteratively generate passwords of lengths 1 through LETT
for z in range(LETT):

    # initialize an ordered list representing a password
    word = ['a'] * (z + 1)

    # call the recursive function that generates and checks passwords
    generate(z + 1)

