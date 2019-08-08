from cs50 import get_int

# get input from user
z = get_int("Number: ")

# cast the int to a string
card = str(z)

# determine length of string
n = len(card)

# initialize counter variables
count = 0

# perform Luhn's Algorithm
if n == 13 or n == 15:
    
    # iterate over card number
    for i in range(n):
        
        # check if index is even
        if i % 2 == 1:
            
            # convert character to integer and multiply by 2
            x = (int(card[i]) * 2)
            
            # add the digits of x to count
            if x >= 10:
                y = x % 10
                count += (y + 1)
            else:
                count += x
       
        # add digit to count        
        else:
            count += int(card[i])
    
    # check to see if it passes Luhn's Algorithm
    if count % 10 != 0:
        print("INVALID")
    
    # check if the first two numbers are valid for AMEX
    elif n == 15:
        if card[0:2] == "34" or card[0:2] == "37":
            print("AMEX")
            
        else:
            print("INVALID")
    
    # check if the first two numbres are valid for VISA
    elif n == 13:
        if card[0] == "4":
            print("VISA")
            
        else:
            print("INVALID")

# perform Luhn's Algorithm            
elif n == 16:
    
    # iterate over card number
    for i in range(n):
        
        # check if index is odd
        if i % 2 == 0:
            
            # convert character to integer and multiply by 2
            x = (int(card[i]) * 2)
            
            # add the digits of x to count
            if x >= 10:
                y = x % 10
                count += (y + 1)
            else:
                count += x
        
        # add the digit to count
        else:
            count += int(card[i])
      
    # check if the first digits are valid for MASTERCARD        
    if card[0:2] == "51" or card[0:2] == "52" or card[0:2] == "53" or card[0:2] == "54" or card[0:2] == "55":
        print("MASTERCARD")
    
    # check if the first digit is valid for VISA    
    elif card[0] == "4":
        print("VISA")
        
    else:
        print("INVALID")
    
else:
    print("INVALID")