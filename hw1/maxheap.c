//maxheap.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>
#include "maxheap.h"

//GLOBALES
int* A; //arreglo de enteros para guardar el heap/array
int heap_size = 0; //cantidad de elementos en el heap/array

//imprimir un arreglo dinamico
void printArray() {

    printf("\nCurrent heap/array:\n[");

    int i;
    for(i=0; i<heap_size; i++) {
        printf(" %02d ", A[i]);
    }

    printf("]\n");
}//printArray

//intercambio de posicion de 2 elementos en el heap/array
//recibe int pointers sencillos (no arreglos) entonces se los enviamos con &
void swap(int* a, int* b) {
    int _t;
    _t = *a;
    *a = *b;
    *b = _t;
}//swap

//obtener indice del hijo izquierdo de un nodo i del heap
int leftChild(int i) {
    if( i>=0 && i<heap_size && ( (i*2+1)<heap_size ) ) {
        return i*2+1;
    }
    return -1;
}//leftChild

//obtener indice del hijo derecho de un nodo i del heap
int rightChild(int i) {
    if( i>=0 && i<heap_size && ( (i*2+2)<heap_size ) ) {
        return i*2+2;
    }
    return -1;
}//rightChild

//obtener indice del padre de un nodo i del heap
int parent(int i) {
    if( i>0 && i<heap_size && ((i-1)/2)>=0 ) {
        return (i-1)/2;
    }
    return -1;
}//parent

//leer el nodo raiz pero no borrarlo
int readMax() {

    return A[0];
}//readMax

//rebalancear el heap (usar despues de cada insert o remove)
void maxHeapify(int i) {

    if(i<0 || i>=heap_size) {
        return;
    }

    int left  = leftChild(i);
    int right = rightChild(i);

    //encontrar el maximo entre i y sus hijos
    int max = i;

    if( left>=0 && left<heap_size ) {
        if(A[left]>A[max]) {
            max = left;
        }
    }

    if( right>=0 && right<heap_size ) {
        if(A[right]>A[max]) {
            max = right;
        }
    }

    //max es alguno de los hijos
    if(max!=i) {
        swap(&A[i], &A[max]);
        maxHeapify(max);
    }
}//maxHeapify

//modificar el valor de cualquier nodo del heap
void edit(int i, int new_value) {

    if(i<0 || i>=heap_size) {
        return;
    }

    if(new_value>A[i]) { //se usa en edit e insert

        A[i] = new_value;

        while( i>0 && A[i]>A[parent(i)] ) {
            swap(&A[i], &A[parent(i)]);
            i = parent(i);
        }
    }else if(new_value<A[i]) { //se usa solo en edit

        A[i] = new_value;
        maxHeapify(i);
    }
}//edit

//construir un heap a partir de un arreglo y su tamaño (que nos envia Python)
void buildMaxHeap() {

    int i;
    for(i=heap_size/2; i>=0; i--) {
        maxHeapify(i);
    }
}//buildMaxHeap

//agregar (encolar) un valor nuevo al heap
void insert(int new_value) {

    //incrementa el contador de elementos
    heap_size++;

    //reservar una celda adicional de RAM a la derecha
    A = (int*)realloc( A, heap_size*sizeof(*A) );

    //inicializar la celda nueva con un valor minimo
    A[heap_size-1] = INT_MIN;

    //printArray(); //des-comentar para debuggear

    //escribir el valor nuevo en la celda nueva
    edit(heap_size-1, new_value);
}//insert

//leer el nodo raiz, borrarlo y rebalancear
int removeMax() {

    //devolver un valor minimo si el heap esta vacio
    if(!heap_size) {
        return INT_MIN;
    }

    //devolver el primer elemento (es el maximo)
    int max = A[0];

    //disminuir la cantidad de elementos
    heap_size--;

    //intercambiar el primero y el ultimo
    A[0] = A[heap_size];

    //borrar el ultimo elemento (reemplazandolo por un valor minimo)
    A[heap_size] = INT_MIN;

    //liberar memoria que usaba el ultimo elemento
    A = (int*)realloc(A, heap_size*sizeof(*A));

    if(heap_size) {
        //rebalancear el heap desde la raiz
        maxHeapify(0);
    }

    return max;
}//removeMax

//funcion para ser llamada desde Python
//recibe una lista de Python y su tamaño
void listReader(int* P, int k) {

    //inicializar el arreglo A con malloc para luego poder usar realloc
    A = (int*)malloc(0);

    //atrapar la lista que envia Python (y su tamaño)
    int i;
    for (i=0; i<k; i++) {
        A = (int*)realloc(A, (i+1)*sizeof(*A));
        A[i] = P[i];
    }
    heap_size = k;

    //desplegar la lista antes de convertirla en heap
    //printArray(); //des-comentar para debuggear

    //construir un heap a partir de la lista
    buildMaxHeap();

    //desplegar la lista ya convertida en heap
    //printArray(); //des-comentar para debuggear
}//listReader

//inicializar modulo con un heap vacio
void initMaxHeap() {

    //si el array/heap estuviera inicializado, limpiarlo antes
    if(A) {
        free(A);
    }

    //inicializar el arreglo con malloc para luego poder usar realloc
    A = (int*)malloc(0);
    heap_size = 0;

    //desplegar el nuevo heap
    //printArray(); //des-comentar para debuggear
}//initMaxHeap

//funcion que Python puede llamar para obtener el heap
int* throwHeap() {
    return A;
}//throwHeap

int throwHeapSize() {
    return heap_size;
}//throwHeapSize

/*
int main() {

    //int j = 15;
    //int* x;
    //x = (int*)malloc(j*sizeof(int));

    //x[0]  = 35;
    //x[1]  = 5;
    //x[2]  = 2;
    //x[3]  = 8;
    //x[4]  = 10;
    //x[5]  = 6;
    //x[6]  = 9;
    //x[7]  = 5;
    //x[8]  = 17;
    //x[9]  = 13;
    //x[10] = 14;
    //x[11] = 16;
    //x[12] = 19;
    //x[13] = 20;
    //x[14] = 30;

    listReader(x, j);

    printArray();

    insert(65);

    int* B = (int*)malloc(1000);
    printf("%d", B[0]);

    return 1;
}//main
*/

//eof
