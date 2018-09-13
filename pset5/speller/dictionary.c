// Implements a dictionary's functionality

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include "dictionary.h"

typedef struct tries
{
    bool eot;
    struct tries *next[27];
}
Trie;

bool destroy(Trie *head);
Trie *newNode();

Trie *newNode()
{
    Trie *tmp = malloc(sizeof(Trie));
    tmp->eot = false;
    for (int i = 0; i< 27; i++)
    {
        tmp->next[i] = NULL;
    }
    return tmp;
}

bool destroy(Trie *head)
{
    if (!head)
    {
        for (int i = 0; i < 27; i++)
        {
            if (!head->next[i]) destroy(head->next[i]);
        }
        free(head);
    }
    return 1;
}


Trie *lib;
bool loaded = false;
unsigned int libSize = 0;

int getInd(char c);

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    Trie *trav = lib;
    for (int i = 0; i < strlen(word); i++)
    {
        int ind = getInd(word[i]);
        if (trav->next[ind] == NULL)
        {
            return false;
        }
        trav = trav->next[ind];
    }
    return trav->eot;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    lib = newNode();
    FILE *fileptr = fopen(dictionary, "r");
    if (!lib || !fileptr) return false;
    else
    {
        char c = 0;
        Trie *trav;
        do
        {
            libSize++;
            trav = lib;
            while(true)
            {
                c = fgetc(fileptr);
                if (c == EOF) break;
                if (c == '\n')
                {
                    trav->eot = true;
                    break;
                }
                int ind = getInd(c);
                if (trav->next[ind] == NULL) trav->next[ind] = newNode();
                trav = trav->next[ind];
            }

        }
        while (c != EOF);
        libSize--;
        return true;
    }
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return libSize;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    return destroy(lib);
}

int getInd(char c)
{
    int ind = -1;
    if (c == 39) ind = 26;
    else if (c >= 'a' && c <= 'z') ind = (c - 'a');
    else if (c >= 'A' && c <= 'Z') ind = (c - 'A');
    return ind;
}