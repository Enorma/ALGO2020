#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
#include "rbt.h"

typedef enum color {red, black} color;

//Estructura del nodo
typedef struct Node {
    int key;    // Para el dato
    color color; // color

    //links para hijos y padre
    struct Node *left, *right, *p;
}Node;

typedef struct Tree {
    Node *root;
    Node *nil;
}Tree;

Node p  = {'\0', black, NULL, NULL, NULL};
Tree t  = {NULL, &p};
Tree *T = &t;

void printNode(char* msg, Node *x) {
    if((x==NULL) || (x==T->nil)) {
        printf("%s, NULL\n", msg);
        return;
    }
    printf("%s, key: %d, color: %s\n", msg, x->key, x->color==red?"red":"black");
}

void leftRotate(Tree *T, Node *x) {

    Node *y  = x->right;
    x->right = y->left;

    if(y->left != T->nil) {
        y->left->p = x;
    }

    y->p = x->p;

    if(x->p == T->nil) {
        T->root     = y;
    }else if(x == x->p->left) {
        x->p->left  = y;
    }else {
        x->p->right = y;
    }

    y->left = x;
    x->p    = y;
}

void rightRotate(Tree *T, Node *x) {

    Node *y = x->left;
    x->left = y->right;

    if(y->right != T->nil) {
        y->right->p = x;
    }

    y->p = x->p;

    if(x->p == T->nil) {
        T->root     = y;
    }else if(x == x->p->right) {
        x->p->right  = y;
    }else {
        x->p->left = y;
    }

    y->right = x;
    x->p    = y;
}

void insertFixup(Tree *T, Node *z) {

    while(z->p->color == red) {

        if(z->p == z->p->p->left) {

            Node *y = z->p->p->right;

            if(y->color == red) {

                z->p->color    = black;
                y->color       = black;
                z->p->p->color = red;
                z              = z->p->p;
            }else {

                if(z == z->p->right) {
                    z = z->p;
                    leftRotate(T,z);
                }

                z->p->color    = black;
                z->p->p->color = red;

                rightRotate(T, z->p->p);
            }
        }else {

            Node *y = z->p->p->left;

            if(y->color == red) {

                z->p->color    = black;
                y->color       = black;
                z->p->p->color = red;
                z              = z->p->p;
            }else {

                if(z == z->p->left) {
                    z = z->p;
                    rightRotate(T,z);
                }

                z->p->color    = black;
                z->p->p->color = red;

                leftRotate(T, z->p->p);
            }
        }
    }

    T->root->color = black;
}

void insert(Tree *T, Node *z) {

    if(T->root==NULL) {

        T->nil->left = T->nil->right = T->nil;
        z->color = black;
        T->root = z;
        return;
    }

    Node *y = T->nil;
    Node *x = T->root;

    while(x != T->nil) {

        y = x;

        if(z->key < x->key) {
            x = x->left;
        }else {
            x = x->right;
        }
    }

    z->p = y;

    if(y == T->nil) {
        T->root  = z;
    }else if(z->key < y->key) {
        y->left  = z;
    }else {
        y->right = z;
    }

    z->left  = T->nil;
    z->right = T->nil;
    z->color = red;

    insertFixup(T, z);
}

Node* search(Node *N, int k) {

    if((N==NULL) || (N==T->nil)) {
        return T->nil;
    }else if(k == N->key) {
        return N;
    }else if(k < N->key) {
        return search(N->left, k);
    }else if(N->key < k) {
        return search(N->right, k);
    }

    return T->nil;
}

void insertInt(int i) {

    struct Node *new = malloc(sizeof(Node));
    new->key = i;
    new->right = new->left = new->p = T->nil;
    insert(T, new);
}

int searchInt(int k) {
    int s = search(T->root, k)->key;
    return s;
}

/*
int main() {

    printf("holamundo!!\n");

    srand(time(NULL));
    int reps = 100000;
    int i,r;

    for(i=0; i<reps; i++) {
        r = rand()%(reps)+1;
        printf("%d\n",r);
        insertInt(r);
    }

    printf("Buscando...\n");
    Node *a = search(T->root, 526);
    printNode("nodo encontrado", a);

    printf("holamundo\n");

    return 0;
}
*/

//eof
