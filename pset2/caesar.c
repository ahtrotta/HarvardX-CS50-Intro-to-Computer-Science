#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    //check if one positive integer was input as a command line argument
    if (argc != 2 || atoi(argv[1]) < 0)
    {
        printf("Error! Input one positive integer as a command line argument.\n");
        return 1;
    }

    //request a string from user
    string plaintext = get_string("plaintext: ");

    //store the key
    int k = atoi(argv[1]);

    //declare output string
    char ciphertext[strlen(plaintext)];

    //convert plaintext input to ciphertext output
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            ciphertext[i] = ((((int) plaintext[i] - 65) + k) % 26) + 65;
        }
        else if (islower(plaintext[i]))
        {
            ciphertext[i] = ((((int) plaintext[i] - 97) + k) % 26) + 97;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    //print output
    printf("ciphertext: %s\n", ciphertext);

    return 0;
}