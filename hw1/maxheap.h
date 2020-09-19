#ifndef MAXHEAP_FILE
#define MAXHEAP_FILE

    //maxheap.h

    void printArray();
    void swap(int* a, int* b);
    int leftChild(int i);
    int rightChild(int i);
    int parent(int i);
    int readMax();
    void maxHeapify(int i);
    void edit(int i, int new_value);
    void buildMaxHeap();
    void insert(int new_value);
    int removeMax();
    void listReader(int* P, int k);
    void initMaxHeap();
    int* throwHeap();
    int throwHeapSize();
    //int main();
#endif

//eof
