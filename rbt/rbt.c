#include<stdio.h>
#include<stdlib.h>

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

void insertFixup(Tree *T, Node *z){

    while(z->p->color == red) {

        if(z->p == z->p->p->left) {

            Node *y = z->p->p->right;

            if(y->color == red) {
                z->p->color    = black;
                y->color       = black;
                z->p->p->color = red;
                z              = z->p->p;
            }else if(z == z->p->right) {
                z = z->p;

                leftRotate(T,z);
            }

            z->p->color    = black;
            z->p->p->color = red;

            rightRotate(T, z->p->p);
        }else {

            Node *y = z->p->p->left;

            if(y->color == red) {
                z->p->color    = black;
                y->color       = black;
                z->p->p->color = red;
                z              = z->p->p;
            }else if(z == z->p->left) {
                z = z->p;
                leftRotate(T,z);
            }

            z->p->color    = black;
            z->p->p->color = red;

            leftRotate(T, z->p->p);
        }

        T->root->color = black;
    }
}

void insert(Tree *T, Node *z) {

    if(T->root==NULL) {
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

int main() {

    printf("holamundo!!\n");
    printf("Color de T: %d\n", T->nil->key);

    Node s = {10, black, T->nil, T->nil, T->nil};
    Node q = {52, black, T->nil, T->nil, T->nil};
    Node r = {70, black, T->nil, T->nil, T->nil};
    //Node u = {70, black, T->nil, T->nil, T->nil};

    insert(T, &s);
    insert(T, &q);
    insert(T, &r);

    printf("Key de root:  %d\n", T->root->key);
    printf("Key de left:  %d\n", T->root->left->key);
    printf("Key de right: %d\n", T->root->right->key);
    printf("holamundo");

    return 0;
}

//eof
