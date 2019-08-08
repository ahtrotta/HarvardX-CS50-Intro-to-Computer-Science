// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a trie
node *root;

// initialize word count variable
int word_count = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = calloc(1, sizeof(node));
    if (!root)
    {
        return false;
    }
    root->is_word = false;

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        // create copy of root location
        node *ptr = root;
        
        // iterate over word
        for (int i = 0, n = strlen(word); i < n; i++)
        {
            // convert character to integer
            int x = (word[i] == '\'') ? 26 : word[i] - 97;
            
            // generate new node if empty
            if (!ptr->children[x])
            {
                // allocate space for new node
                node *tmp = calloc(1, sizeof(node));
                
                // check if calloc succeeded
                if (!tmp)
                {
                    unload();
                    return false;
                }
                
                // initialize is_word to false
                tmp->is_word = false;
                
                // point the prior node to newly allocated node
                ptr->children[x] = tmp;
            }
            
            // follow pointer
            ptr = ptr->children[x];
            
            // if last letter of word then set is_word to true
            if (i == (n - 1))
            {
                ptr->is_word = true;
                word_count++;
            }
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // check if root exists
    if (!root)
    {
        return 0;
    }

    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // initialize crsr to root node
    node *crsr = root;
    
    // iterate over word
    for (int k = 0, m = strlen(word); k < m; k++)
    {
        // convert uppercase to lowercase
        char c = (isupper(word[k])) ? tolower(word[k]) : word[k];
        
        // convert character to integer
        int y = (c == '\'') ? 26 : c - 97;
        
        if (!crsr->children[y])
        {
            return false;
        }
        else if (k == (m - 1))
        {
            if (crsr->children[y]->is_word == false)
            {
                return false;
            }
            else 
            {
                return true;
            }
        }
        else
        {
            crsr = crsr->children[y];
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // call recursive function
    mem_free(root);
    return true;
}


// recursive function to free memory    
void mem_free(node *pnt)
{
    // call mem_free for every pointer in current node
    for (int l = 0; l < N; l++)
    {
        if (pnt->children[l] != NULL)
        {
            mem_free(pnt->children[l]);
        }
    }

    // base case
    free(pnt); 
}
