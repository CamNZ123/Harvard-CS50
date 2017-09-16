#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) 
{
    bool b = true;                                                                              // Loop for checking that the key has no numbers
    if (argc == 2) 
    {
        for (int i = 0; i < strlen(argv[1]); i++) 
        {
            if ((argv[1][i] > 64 && argv[1][i] < 91) || (argv[1][i] > 96 && argv[1][i] < 123)) 
            {
                // If it is a letter    
            } 
            else 
            {
                b = false;
            }
        }
    }
    
    if (argc == 2 && b) 
    {
        

        printf("plaintext: ");
        string s = get_string();
        string l = argv[1];
        int j = strlen(s);
        int keylength = strlen(l);
        int lettercount = 0;                                                                      // Index var
        int letterIntVal = 0;                                                                              // Value for changing letter
        for (int x = 0; x < j; x++) 
        {
            if ((s[x] > 64 && s[x] < 91) || (s[x] > 96 && s[x] < 123))                          // If it is a letter 
            {                        
                
                if (lettercount == keylength) 
                {
                    lettercount = 0;
                }
                
                if (islower(l[lettercount])) 
                {                                                                               // Turning a to z to 0 to 26
                    letterIntVal = l[lettercount] - 97;
                }

                if (isupper(l[lettercount])) 
                {                                                                               // Turning A to Z to 0 to 26
                    letterIntVal = l[lettercount] - 65;
                }
                if (((islower(s[x]) && s[x] + letterIntVal > 122) || (isupper(s[x]) && s[x] + letterIntVal > 90)))    // If it will loop over, it will loop back 26
                {  
                    s[x] -= 26;                     
                }
                
                s[x] = s[x] + letterIntVal;                                                                // Change the letter
                
                lettercount++;
                
            }
        }
        printf("ciphertext: %s\n", s);
        
    }
    else 
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    return 0.;
}