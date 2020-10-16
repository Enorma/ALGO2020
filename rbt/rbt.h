#ifndef REDBLACKTREE_FILE
#define REDBLACKTREE_FILE

    /*rbt.h*/

    typedef struct Node Node;
    typedef struct Tree Tree;
    void printNode(char* msg, Node *x);
    void leftRotate(Tree *T, Node *x);
    void rightRotate(Tree *T, Node *x);
    void insertFixup(Tree *T, Node *z);
    void insert(Tree *T, Node *z);
    Node* search(Node *N, int k);
    void insertInt(int i);
    int searchInt(int k);
    int main();
#endif

//EOF
