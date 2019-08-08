#include <cs50.h>
#include <math.h>
#include <stdio.h>

int counter(long int x);

int main(void)
{
    // Get credit card from user
    long int num = get_long("Number: ");

    // Determine how many digits are in the number
    long int num_clone = num;
    int digits = counter(num_clone);
    
    // Initialize counters
    int count = 0;
    int count2 = 0;
    int two_first = 0;
    
    for (int i = 1; i <= digits; i++)
    {
        // Sequentially extract the last digit of the number and remove it
        int j = num % 10;
        num -= j;
        num /= 10;
        
        // Get first two digits of number
        if (i == digits - 1)
        {
            two_first += j;
        }
        else if (i == digits)
        {
            two_first += j * 10;
        }
        
        // Decision tree based on every other digit
        int k = i % 2;
        if (k == 0)
        {
            j *= 2;
            int j_count = counter(j);
            
            // Add all digits 
            for (int l = 0; l < j_count; l++)
            {
                int m = j % 10;
                j -= m;
                j /= 10;
                count2 += m;
            }
        }
        else if (k != 0)
        {
            count += j;
        }
    }
    
    // Define variables for checking the number
    int sum = count + count2;
    int check = sum % 10;
    int four_check = two_first / 10;
    
    // Check if card is valid according to Luhn's algorithm
    if (check != 0)
    {
        printf("INVALID\n");
    }
    else if (digits == 15)
    {
        // Check if the number starts with 34 or 37
        if (two_first == 34 || two_first == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (digits == 13)
    {
        // Check if the number starts with 4
        if (four_check == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (digits == 16)
    {
        // Check if the number starts with 51, 52, 53, 54, 55 for Mastercard or 4 for Visa
        if (four_check == 4)
        {
            printf("VISA\n");
        }
        else if (two_first == 51 || two_first == 52 || two_first == 53 || two_first == 54 || two_first == 55)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

int counter(long int x)
{
    int digits = 0;
    while (x > 0)
    {
        x /= 10;
        digits++;
    }
    return digits;
}

