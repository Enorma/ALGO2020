#ifndef SKIPLIST_FILE
#define SKIPLIST_FILE

    /*skiplist.h*/

    typedef struct node node;
    int filp();
    int geth(node *n);
    int volado(node *n);
    node *crearNodo(int value);
    node *crearlista(int value);
    void imprimirskiplist(node *n);
    void wrapImprimir();
    void insertar(node *n, int value);
    void wrapInsertar(int value);
    int borrar(node *n, int value);
    int wrapBorrar(int value);
    void init();
#endif

//EOF
