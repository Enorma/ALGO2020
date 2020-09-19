#ifndef MINHEAP_FILE
#define MINHEAP_FILE

    //minheap.h

    void printArray();
    void swap(int* a, int* b);
    int leftChild(int i);
    int rightChild(int i);
    int parent(int i);
    int readMin();
    void minHeapify(int i);
    void edit(int i, int new_value);
    void buildMinHeap();
    void insert(int new_value);
    int removeMin();
    void listReader(int* P, int k);
    void initMinHeap();
    int* throwHeap();
    int throwHeapSize();
    //int main();
#endif

//eof
