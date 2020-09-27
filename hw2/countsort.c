#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void countSort(int* A, int n, int k0, int kf);
void printArray(int* A, int n);

//A  = Array que queremos ordenar
//n  = tamaño de A
//k0 = valor mínimo de los elementos de A
//kf = valor máximo de los elementos de A
void countSort(int* A, int n, int k0, int kf) {

    int i;
    int K[kf-k0+1];
    int* B;
    B = (int*)calloc(n, sizeof(*B));

    for(i=0; i<(kf-k0+1); i++) {
        K[i] = 0;
    }

    for(i=0; i<n; i++) {
        K[A[i]]++;
    }

    for(i=1; i<(kf-k0+1); i++) {
        K[i]+=K[i-1];
    }

    for(i=n-1; i>=0; i--) {
        K[A[i]]--;
        B[K[A[i]]] = A[i];
    }

    memmove(A,B,n*sizeof(*B));
}

void printArray(int* A, int n) {
    int i;
    printf("[");
    for(i=0; i<n; i++) {
        printf(" %d ", A[i]);
    }
    printf("]");
}

int main() {

    int* A;
    int n = 12;

    A = (int*)calloc(n, sizeof(*A));

    A[0]  = 6;
    A[1]  = 4;
    A[2]  = 0;
    A[3]  = 1;
    A[4]  = 7;
    A[5]  = 2;
    A[6]  = 8;
    A[7]  = 5;
    A[8]  = 0;
    A[9]  = 4;
    A[10] = 3;
    A[11] = 1;

    printf("\nArray A before sort:\n");
    printArray(A,n);

    countSort(A,n,0,9);

    printf("\n\nArray A after sort:\n");
    printArray(A,n);
    printf("\n");
}

//EOF
