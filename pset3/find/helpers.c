/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include "helpers.h"


/**
 * Returns true if value is in array of n values, else false.
 */

bool search(int value, int values[], int n)
{
    sort(values, n);
    
    if (n <= 0) 
    { 
        return false;
    }
    int mid = n / 2;
    int low = 0;
    int high = n - 1;
    while (n > 0) 
    {
        if (low == high && values[low] != value) 
        {
            return false;
        }
        else if(values[mid] == value) 
        {
            return true;
        }
        else if (value < values[mid])
        {
            high = mid - 1;
            mid = (low + high) / 2;
        }
        else if (value > values[mid])
        {
            low = mid + 1;
            mid = (low + high) / 2;
        }
        else
        {
            return false;
        }
    }
    return false;

} 

/**
 * Sorts array of n values.
 */

void sort(int values[], int n)
{
    
    int hn = 0;
    for (int i = 0; i < n; i++)                     // For finding the highest num (lowest is 0)
    {                   
        if (values[i] > hn) 
        {
            hn = values[i];
        }
    }
    
    int count[hn + 1];
    for (int i = 0; i < hn + 1; i++)                     // For setting all values in count to 0
    {                   
        count[i] = 0;
    }
    
   
    
    for (int i = 0; i < n; i++)                     // For counting the amount of numbers. e.g array = {0,0,0,1,2,2} count = {3,1,2}
    {                   
        count[values[i]] = count[values[i]] + 1;    
    }
    
    
    int x = 0;
    for (int i = 0; i < hn + 1; i++)                      // For turning the count array into a sorted array
    {                  
            
        for (int j = 0; j < count[i]; j++) 
        {
                
            values[x] = i;
            x++;
                
        }
          
    }
}

