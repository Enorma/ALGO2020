#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Utility function to get max of 2 integers */
int get_max(int a, int b) 
{ 
    return (a > b)? a : b; 
} 

void print_lcs(int **L, char* X, char * Y, int i, int j, char* lcs, int indice);


int lcs(char* sequence, int sequence_count) 
{ 	
    int i, j;
    srand(time(NULL));
    int m = rand() % 40; 
    int n = m;
    char* X = (char*)malloc(m);
    char* Y = (char*)malloc(m);
    int random_index = 0;
    for(j = 0; j < m; j++) {
        random_index = rand() % sequence_count; 
        X[j] = sequence[random_index];
        Y[j] = X[j];
    }
    //mutation
    double percentage = 0.7;
    for(j = 0; j < (int)(m * percentage); j++) {
        random_index = rand() % sequence_count;
        Y[j] = sequence[random_index];
    }
    //+1 is for the zeros row and column
    //int L[m+1][n+1];
    int** L = (int**)malloc(sizeof(int*)*(m + 1));
    //fill matrix
    for (i = 0; i <= m; i++) 
    {
        L[i] = (int*)malloc(sizeof(int)*(n + 1));
        for (j = 0; j <= n; j++) 
        {
            if (i == 0 || j == 0) 
                L[i][j] = 0;

            else if (X[i - 1] == Y[j - 1]) 
                L[i][j] = L[i - 1][j - 1] + 1; 

            else
                L[i][j] = get_max(L[i - 1][j], L[i][j - 1]); 
        } 
    } 
    /* L[m][n] contains length of LCS for X[0..n-1] and Y[0..m-1] */
    int indice = L[m][n] - 1;
    char* lcs = (char*)malloc(indice);

    i = m;
    j = n;

    printf("\nSequence 1: \n%s \n", X);
    printf("\nSequence 2: \n%s \n", Y);
    print_lcs(L, X, Y, i, j, lcs, indice);
    printf("-------------\nLCS: %s\n", lcs);
    
    return 0;
} 

void print_lcs(int **L, char* X, char * Y, int i, int j, char* lcs, int indice){
    if ( i == 0 || j == 0){
        return;
    } else if (X[i-1] == Y[j-1]){
        lcs[indice] = X[i-1];
        i-=1;
        j-=1;
        indice-=1;
    }
    else if(L[i-1][j] > L[i][j-1]){
        i-=1;
    } else{
        j-=1;
    }
    print_lcs(L, X, Y, i, j, lcs, indice);
}

