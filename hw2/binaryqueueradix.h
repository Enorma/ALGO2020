#ifndef BINARYQUEUERADIX_FILE
#define BINARYQUEUERADIX_FILE

    /*binaryqueueradix.h*/

    typedef struct node_s NODE, *QUEUE;
    NODE *new_node(int val);
    void append_node(QUEUE *queue, NODE *node);
    void cat(QUEUE *a, QUEUE b_head);
    void sort(QUEUE *queue);
    int* connector(int* numbers, int size);
#endif

//eof
