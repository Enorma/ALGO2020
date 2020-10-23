#ifndef LONGESTCOMMONSUBSEQUENCE_FILE
#define LONGESTCOMMONSUBSEQUENCE_FILE

    /*lcs.h*/

    int get_max(int a, int b);
    void print_lcs(int** L, char* X, char* Y, int i, int j, char* subseq, int indice);
    void lcs(char* dnastr1, char* dnastr2, int dnalen);
#endif

//EOF
