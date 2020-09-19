//listreader.c

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "listreader.h"

void listReader(int* intlist, int listlen) {

    //read and print the whole list!

    int i;
    printf("This is the list in C!\n[");
    for(i=0; i<listlen; i++) {
        printf(" %d ", intlist[i]);
    }
    printf("]\n\nHave a nice day! bye!\n");
}

//eof
