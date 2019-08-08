from cs50 import get_int

while (True):
    
    # get height from user
    n = get_int("Height: ")
    
    # check if height is an integer between 1 and 8, inclusive
    if n >= 1 and n <= 8:
        break

# print the pyramids
for i in range(1, n + 1):
    
    m = n - i
    
    # print the preceding spaces for the first pyramid
    for j in range(m):
        print(" ", end="")
    
    # print the hashes for the first pyramid
    for k in range(i):
        print("#", end="")
    
    # print the spaces in between the pyramids
    print("  ", end="")
    
    # print the hashes in the second pyramid
    for l in range(i):
        print("#", end="")
    
    # print a new line
    print()
        