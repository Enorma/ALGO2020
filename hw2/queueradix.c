#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define RADIX 10 //base de los numeros a ordenar
#define MAX_DIGITS 9 //longitud de los numeros a ordenar

//JAHALLA
//Nodo de una cola circular.
//A partir de aqui usamos NODE para trabajar con nodos individuales,
//y usamos QUEUE para trabajar con la cola.
typedef struct node_s {

    struct node_s *next; //pointer al siguiente nodo o a NULL
    int val; //contenido del nodo
}NODE, *QUEUE;

//JAHALLA
//Crear un nodo nuevo con un valor
NODE* new_node(int val) {

    //reservar e inicializar memoria para un nodo
    NODE* node = calloc(1, sizeof(*node));

    //Si el calloc salio mal y node es NULL
    if(!node) {
        exit(EXIT_FAILURE);
    }

    //asignar su valor al nodo
    node->val = val;

    //retornar el nodo nuevo
    return node;
}

//JAHALLA
//Encolar un nodo nuevo
void append_node(QUEUE* queue, NODE* node) {

    //head y queue son pointers al nodo cero de la cola
    NODE* head = *queue;

    //checar que la cola no este vacia
    if(head) {
        //insertar el nodo nuevo entre el ultimo y el primer elementos
        node->next = head->next;
        head->next = node;
    }else {
        //insertar el nodo nuevo apuntando a si mismo
        node->next = node;
    }

    //El nodo que encolamos sera el nuevo nodo cero de la cola
    *queue = node;
}

//JAHALLA
//Concatenar una segunda cola a la primera
void cat(QUEUE* a, QUEUE b_head) {

    //Declarar 2 nodos nuevos
    NODE *a_head, *a_tail;

    //Si la cola original esta vacia, no hacer nada mas
    if(b_head==NULL) {
        return;
    }

    //Un nodo nuevo guarda la cola nueva
    a_head = *a;

    //Si la cola nueva no esta vacia
    if(a_head) {
        a_tail       = a_head->next;
        a_head->next = b_head->next;
        b_head->next = a_tail;
    }

    //la cola concatenada se guarda en a
    *a = b_head;
}

//Ordenar una cola con Radix Sort
void sort(QUEUE *queue) {

    int i, j, div;

    //crear un arreglo de RADIX colas y otra cola que usaremos de acumulador
    QUEUE queues[RADIX], accum;

    //Si la cola de entrada esta vacia
    if(*queue==NULL) {
        return;
    }

    //Inicializa el acumulador con la cola de entrada desordenada
    accum = *queue;

    //Iterar a traves de la cola desordenada
    //una iteracion por cada nivel (unidades, decenas, centenas...)
    for(i=0; i<MAX_DIGITS; i++) {

        //div es para referirnos a algun nivel (unidades, decenas, centenas...)
        div = pow(RADIX,i);

        //vaciar todas las colas
        for(j=0; j<RADIX; j++) {
            queues[j] = NULL;
        }

        //Guardar la cola del acumulador para el digito actual
        NODE *p      = accum;
        NODE *p_next = p->next;

        do {

            //Guardar la cola del acumulador y su nodo siguiente
            p      = p_next;
            p_next = p->next;

            //encolar un numero en la cola que tenga su digito
            append_node(&queues[p->val / div % RADIX], p);
        }while(p!=accum);

        //Concatenar todas las colas
        for(accum=NULL, j=0; j<RADIX; j++) {
            cat(&accum, queues[j]);
        }
    }

    //El acumulador ahora esta ordenado
    *queue = accum;
}

int main(void) {

    int i;
    int data[] = {98, 111, 42, 1111, 21, 997, 0, 99999, 20903};

    //Crear una cola
    QUEUE a = NULL;

    //Llenar la cola con data
    for(i=0; i<(sizeof(data)/sizeof(data[0])); i++) {
        append_node(&a, new_node(data[i]));
    }

    //Imprimir la cola desordenada
    NODE *q = a;

    printf("\nCola desordenada:\n[");
    do {
        q = q->next;
        printf(" %d ", q->val);
    }while(q!=a);
    printf("]\n");

    //Ordenar la cola
    sort(&a);

    //Imprimir la cola ordenada
    NODE *p = a;

    printf("\nCola ordenada:\n[");
    do {
        p = p->next;
        printf(" %d ", p->val);
    }while(p!=a);
    printf("]\n");

    return 0;
}

//eof
