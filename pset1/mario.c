#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompts user to define height of pyramid
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h > 23 || h < 0);

    // returns number of rows
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h + 1; j++)
        {
            if (j < h - 1 - i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}