/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "dictionary.h"

int wordcount = 0; // global word count in dictionary

int hash (const char* word) // will return the first char (e.g a = 1, z = 26) times the length of the string (e.g a = 1, aaa = 3)
{
    if (word[0] == '\'')
    {
        return 27 * strlen(word);
    }
    else
    {
        return (tolower(word[0]) - 96) * strlen(word);
    }
}


typedef struct node             // node declaration
{
	char word[LENGTH+1];
	struct node* next;

}
node;


node* hashtable[65536] = {NULL};    // hashtable declaration

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    char lowerword[LENGTH + 1];     // temp var for storing the CONST word in lowercase
    
    for (int i = 0; i < strlen(word); i++)
    {
        lowerword[i] = tolower(word[i]);
    }
    
    lowerword[strlen(word)] = '\0';
    int bucket = hash(word);        // The index of the hastable
    
    node* cursor = hashtable[bucket];   // cursor to the hashtable[index]
    
    while (cursor != NULL)              // Go through the linked list in hashtable[index] and look for the word
    {
        if (strcmp(lowerword, cursor->word) == 0)
        {
            return true;                // word is found return true
        }
        cursor = cursor->next;
    }
    
    return false;   // haven't found the word return false
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 * 
 */
 
char word[LENGTH+1];

bool load(const char *dictionary)
{
    FILE *fp = fopen(dictionary, "r");      // Set the file and check if it has opened correctly
    
    if (fp == NULL)
    {
        printf("Could not open %s\n", dictionary);
        return false;
    }
    
    while (fscanf(fp, "%s\n", word)!= EOF)      // Go through each line
    {
        node* cword = malloc(sizeof(node));     // Make a node
        strcpy(cword -> word, word);            // Put the word into the node
        int bucket = hash(word);                // Hash it
        
        if (hashtable[bucket] == NULL)          // If the bucket hasn't been initialized
        {
            hashtable[bucket] = cword;          // Set the bucket the link to the next node
            cword -> next = NULL;       
        }
        else                                    // If it has been initialized
        {
            cword -> next = hashtable[bucket];  // Make the word point to the bucket
            hashtable[bucket] = cword;          // Make the bucket point to the word
        }
        wordcount++;
    }
    
    fclose(fp);
    return true;
    
   
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return wordcount;       // Return the global wordcount
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int bucket = 0; bucket < 65536; bucket++)      // Go through each bucket
    {
        if (hashtable[bucket] != NULL)                  // If it isn't empty
        {
            while(hashtable[bucket] != NULL)            // Go through each node
            {
                node* cursor = hashtable[bucket];       // Set the cursor the the first node
                hashtable[bucket] = cursor->next;       // Make the bucket point to the next node
                free(cursor);                           // Free the (cursor) node
            }
        }
    }
    return true;                                        // Return true
}
