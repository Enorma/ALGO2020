#ifndef HASHTABLE_FILE
#define HASHTABLE_FILE

    /*hashtable.h*/

    typedef struct person person;
    void makeHashMatrix();
    unsigned char checkBit(int n, unsigned char d);
    unsigned char* charToBin(char c);
    unsigned char* strToBin(char* str);
    unsigned int getHash(char* name);
    void initHashTable();
    void printTable();
    bool hashTableInsert(char* name, unsigned int age);
    bool hashTableDelete(char* name);
    int hashTableRead(char* name);
    void connector();
    void finish();
#endif

//EOF
