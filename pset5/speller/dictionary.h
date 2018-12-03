// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdlib.h>
#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Trie definition (Dictionary struct)
typedef struct _Trie
{
    bool eot;
    struct _Trie * next[27];
}
Trie;

// Prototypes
bool check(const char *word);
bool load(const char *dictionary);
unsigned int size(void);
bool unload(void);

int getInd(char c);
Trie *newNode();
bool destroy(Trie *head);

#endif // DICTIONARY_H