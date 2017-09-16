#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    printf("Name: ");
    string n = get_string();
    char s = ' ';               
    if (n != NULL) 
    {                                                                       // If it is a valid string
        for (int i = 0; i < strlen(n); i++) 
        {                                                                   // Go through each char
            if ((n[i - 1] == s && n[i] != s) || (i == 0 && n[0] != s))      // If there is a space before the char and the char isn't a space. It is a initial.
            {                                                               
                printf("%c", toupper(n[i]));                                // Then print it
            }
        }
    }
    printf("\n");                                                           // New line
    while (true)
    {
        printf("%s\n", n);
    }
} 