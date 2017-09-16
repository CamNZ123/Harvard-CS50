#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    long long cardnumber = 0;
    do {                            // do while for getting a positive number
        printf("Number: ");
        cardnumber = get_long_long();
    }
    while (cardnumber <= 0);
    
   
    int count = 0;
    long long digits = cardnumber;
    while (digits > 0) {                 // Finding how many digits
        digits = digits / 10;
        count++;
    }

    
    int array0[count];                  // For multiplying every 2nd digit by 2 
    int array1[count];                  // For separating the digits e.g 14 to 1 and 4
    int array2[count];                  // For adding everything together
    
    for (int i = 0; i < count; i++)     // making an array of the digits
    {
        array0[i] = cardnumber % 10;
        array1[i] = array0[i];
        cardnumber = cardnumber / 10;
    }
    
    for (int i = 1; i < count; i += 2) {    // multipling every 2nd one starting from 2nd to last
        array0[i] = array0[i] * 2;
    }
    
    
    for (int i = 0; i < count; i++) {
        array2[i] = 0;
    }
    
    int n = 0;
    for (int i = 1; i < count; i += 2) {    // if more then 1 digits then split the digits to new array
        while (array0[i] > 0) {              // while the number is bigger then 0
            array2[n] = array0[i] % 10;      // set array2 [n] to the array[i] % 10 e.g 14 % 10 = 4
            array0[i] = array0[i] / 10;       // Divide the array[i] by 10 e.g 14 / 10 = 1.4 = 1 (it is an int not a float)
            n++;                            // Add one to n
        }
    }
    
    int answer = array2[0];                 // add every digt that got multipled
    for (int i = 1; i < count; i++) {
        answer = answer + array2[i];
    } 
    
    for (int i = 0; i < count; i += 2){     // add every digt that didn't
        answer = answer + array1[i];
    }
    
    
    
    if (answer % 10 == 0) {                                                 // Find out which type of card it is
        if (array1[14] == 3 && (array1[13] == 4 || array1[13] == 7)) {
            printf("AMEX\n");
        }
        if (array1[15] == 5 && (array1[14] == 1 || array1[14] == 2 || array1[14] == 3 || array1[14] == 4 || array1[14] == 5)) {
            printf("MASTERCARD\n");
        }
        if (count == 13) {
            if (array1[12] == 4) {
                printf("VISA\n");
            }
        }
        if (count == 16) {
            if (array1[15] == 4) {
                printf("VISA\n");
            }
        }
    }
    else {
        printf("INVALID\n");
    }   
    return 0;                       //otherwise return 0
} 