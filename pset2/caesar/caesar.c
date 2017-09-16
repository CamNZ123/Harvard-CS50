#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) 
{
    if (argc == 2) 
    {
        printf("plaintext: ");
        string s = get_string();
        int i = atoi(argv[1]);                                                                  // Turn the string "26" to int 26 
        i = i % 26;                                                                             // If will modulo it so that 27 becomes 1 and 25 becomes 25
        for (int x = 0; x < strlen(s); x++)                                                     // Go through each char
        {                                                                                      
            if ((s[x] > 64 && s[x] < 91) || (s[x] > 96 && s[x] < 123)) 
            {                                                                                   // If it is a letter
                if (((islower(s[x]) && s[x] + i > 122) || (isupper(s[x]) && s[x] + i > 90)))    // If an overflow will happen 
                {                                                                              
                    s[x] -= 26;                                                                 // Prevent it
                }
                s[x] = s[x] + i;                                                                // Change the letter
            }
        }
        printf("ciphertext: %s\n", s);                                                          // Print it
        
    }
    else                                                                                        // If there is error, return 1
    {                                                                                     
        printf("Usage: ./casear k\n");
        return 1;
    }
    return 0;
} 