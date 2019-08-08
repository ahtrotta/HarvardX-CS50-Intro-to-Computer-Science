#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    float owed;
    do
    {
        owed = get_float("Change owed: ");
    }
    while (owed < 0);

    owed *= 100;
    owed = roundf(owed);

    int i = 0;
    while (owed >= 25)
    {
        owed -= 25;
        i++;
    }
    while (owed >= 10)
    {
        owed -= 10;
        i++;
    }
    while (owed >= 5)
    {
        owed -= 5;
        i++;
    }
    while (owed >= 1)
    {
        owed -= 1;
        i++;
    }

    printf("%i\n", i);
}
