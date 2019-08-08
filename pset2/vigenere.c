#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{

    //check if there is one and only one command line argument
    if (argc != 2)
    {
        printf("Error! Input one command line argument.\n");
        return 1;
    }

    //check if the command line argument is a string
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if ((int) argv[1][i] < 65 || (int) argv[1][i] > 122)
        {
            printf("Error! Input a string as a command line argument.\n");
            return 1;
        }
        else if ((int) argv[1][i] > 90 && (int) argv[1][i] < 97)
        {
            printf("Error! Input a string as a command line argument.\n");
            return 1;
        }
    }

    //store length of keyword
    int len = strlen(argv[1]);

    //store the keyword and convert to all lowercase letters
    char a[len];
    for (int i = 0; i < len; i++)
    {
        if (isupper(argv[1][i]))
        {
            a[i] = tolower(argv[1][i]);
        }
        else
        {
            a[i] = argv[1][i];
        }
    }

    //declare keyword array as integers
    int k[len];

    //convert keyword to int starting at 0
    for (int i = 0; i < len; i++)
    {
        k[i] = ((int) a[i]) - 97;
    }

    //request the plaintext
    string plaintext = get_string("plaintext: ");

    //declare output string
    char ciphertext[strlen(plaintext) + 1];

    //declare counter variable for keyword cycling
    int j = 0;

    //convert plaintext input to ciphertext output
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            ciphertext[i] = (((((int) plaintext[i]) - 65) + k[j]) % 26) + 65;
            j = (j + 1) % len;
        }
        else if (islower(plaintext[i]))
        {
            ciphertext[i] = (((((int) plaintext[i]) - 97) + k[j]) % 26) + 97;
            j = (j + 1) % len;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    //print output
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", ciphertext[i]);
    }
    printf("\n");

    return 0;
}
