#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "lcs.h"

/* Utility function to get max of 2 integers */
int get_max(int a, int b) {
    return (a > b) ? a : b;
}

void print_lcs(int** L, char* X, char* Y, int i, int j, char* subseq, int indice) {

    if(i==0 || j==0) {
        return;
    }else if(X[i-1] == Y[j-1]) {
        subseq[indice] = X[i-1];
        i -= 1;
        j -= 1;
        indice -= 1;
    }else if(L[i-1][j] > L[i][j-1]) {
        i -= 1;
    }else {
        j -= 1;
    }

    print_lcs(L, X, Y, i, j, subseq, indice);
}

void lcs(char* dnastr1, char* dnastr2, int dnalen) {

    int i, j, indice;

    //crear matriz de LCS
    //usamos ambas dimensiones +1 para la fila/columna de ceros

    int** L = (int**)malloc(sizeof(int*)*(dnalen+1));

    //fill matrix
    for(i=0; i<=dnalen; i++) {

        L[i] = (int*)malloc(sizeof(int)*(dnalen+1));

        for(j=0; j<=dnalen; j++) {

            if(i==0 || j==0) {
                L[i][j] = 0;
            }else if(dnastr1[i-1] == dnastr2[j-1]) {
                L[i][j] = L[i-1][j-1]+1;
            }else {
                L[i][j] = get_max(L[i-1][j], L[i][j-1]);
            }
        }
    }

    //L[dnalen][dnalen] tiene la longitud de la LCS
    indice = L[dnalen][dnalen] - 1;
    char* subseq = (char*)malloc(indice);

    i = j = dnalen;

    print_lcs(L, dnastr1, dnastr2, i, j, subseq, indice);
    printf("LCS es %s de longitud %d\n", subseq, indice+1);

    //liberar memoria de subseq
    free(subseq);

    //liberar memoria de L
    int f;
    for(f=0; f<(dnalen+1); f++) {
        free(L[f]);
    }
    free(L);
}

//eof
