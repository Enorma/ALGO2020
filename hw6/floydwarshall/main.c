#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXBUF 100

int inputlen, matrixdim;
int *matrix, *auxmatrix;
char *inputstr, *outputstr;

int measureString(char* s) {

    int i;
    int count = 0;

    for(i=0; i<MAXBUF; i++) {
        if(s[i]=='\0') {
            return count;
        }else {
            count++;
        }
    }

    return count;
}

void printMatrix() {

    int i;
    for(i=0; i<(matrixdim*matrixdim); i++) {

        if(i%matrixdim==0) {
            printf("\n");
        }

        printf("%d ", matrix[i]);
    }

    printf("\n");
}

void strToMatrix() {

    //printf("\nstrToMatrix"); //descomentar para debuggear

    char* tokens;
    tokens = strtok(inputstr, " [],");

    int i = 0;
    while(tokens!=NULL) {
        matrix[i] = atoi(tokens);
        tokens = strtok(NULL, " [],");
        i++;
    }

    //printMatrix(); //descomentar para debuggear
}

void floydWarshall() {

    //printf("\nfloydWarshall"); //descomentar para debuggear

    int i=0, j=0, k=0, ij=0, ik=0, kj=0;

    for(k=0; k<matrixdim; k++) {

        auxmatrix = (int*)malloc(matrixdim * matrixdim * sizeof(int));

        for(i=0; i<matrixdim; i++) {
            for(j=0; j<matrixdim; j++) {

                ij = i * matrixdim + j;
                ik = i * matrixdim + k;
                kj = k * matrixdim + j;

                if( matrix[ij] < ( matrix[ik] + matrix[kj] ) ) {
                    auxmatrix[ij] = matrix[ij];
                }else {
                    auxmatrix[ij] = matrix[ik]+matrix[kj];
                }
            }
        }

        free(matrix);
        matrix = auxmatrix;
    }

    //printMatrix(); //descomentar para debuggear
}

void matrixToStr() {

    //printf("\nmatrixToStr"); //descomentar para debuggear

    char* converted;
    converted = (char*)malloc(MAXBUF);

    int i;
    for(i=0; i<(matrixdim*matrixdim); i++) {

        converted = (char*)memset(converted, '\0', MAXBUF);
        sprintf(converted, "%d ", matrix[i]);

        outputstr = strncat(outputstr, converted, measureString(converted));
    }

    //printf("\noutput: [%s]", outputstr); //descomentar para debuggear
}

char* runFW(char* mstr, int slen, int mdim) {

    //printf("\n\nrunFW"); //descomentar para debuggear

    inputlen  = slen;
    matrixdim = mdim;

    inputstr = (char*)malloc(inputlen * sizeof(char));
    strcpy(inputstr, mstr);

    size_t msize = MAXBUF * matrixdim * matrixdim * sizeof(char);
    outputstr = (char*)malloc(msize);
    outputstr = (char*)memset(outputstr, '\0', msize);

    matrix = (int*)malloc(matrixdim * matrixdim * sizeof(int));

    //printf("\ninput: [%s]\n", inputstr); //descomentar para debuggear

    strToMatrix();
    floydWarshall();
    matrixToStr();

    free(inputstr);
    free(auxmatrix);

    return outputstr;
}

int main() {

    //printf("\nmain"); //descomentar para debuggear

    char s[] = "0 42 18 35 1 20 25 29 9 13 15 6 46 32 28 12 42 0 46 43 28 37 42 5 3 4 43 33 22 17 19 46 48 27 0 22 39 20 13 18 10000000 36 45 4 12 23 34 24 15 42 12 0 4 19 48 45 13 8 38 10 24 42 30 29 17 36 41 43 0 39 7 41 43 15 49 47 6 41 30 21 1 7 2 44 49 0 30 24 35 5 7 41 17 27 32 9 45 40 27 24 38 39 0 19 33 30 42 34 16 40 9 5 31 28 7 24 37 22 46 0 25 23 21 30 28 24 48 13 37 41 12 37 6 18 6 25 0 32 3 1 1 42 25 17 31 8 42 8 38 8 38 4 34 0 46 10 10 9 22 39 23 47 7 31 14 19 1 42 13 6 0 11 10 25 38 49 34 46 42 3 1 42 37 25 21 47 22 0 49 10000000 19 35 32 35 4 10000000 19 39 1 39 28 18 29 44 0 49 34 8 22 11 18 14 15 10 17 36 2 1 10000000 20 7 0 49 4 25 9 45 10 40 3 46 36 44 44 24 38 15 4 0 49 1 9 19 31 47 49 32 40 49 10 8 23 23 39 43 0";
    int sl = 727;
    int md = 16;
    char* os;

    printf("\norigin: [%s]\n", s);

    os = runFW(s, sl, md);

    printf("\nending: [%s]\n", os);

    return 1;
}

//EOF
