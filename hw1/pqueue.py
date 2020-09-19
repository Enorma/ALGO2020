import os
import ctypes

#borrar y recompilar las librerías (los archivos .c y .h deben estar en este mismo directorio)
def startup():

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #borrar las librerías (los archivos .c y .h deben estar en este mismo directorio)
    try:
        os.remove(os.path.join(thispath, "maxheap.o"))
        os.remove(os.path.join(thispath, "maxheap.so"))
        os.remove(os.path.join(thispath, "minheap.o"))
        os.remove(os.path.join(thispath, "minheap.so"))
    except:
        pass
    #try-except

    #El Makefile debe tener comandos de gcc para generar los .so
    os.system("make all")

    print("Done!\n------------------------------------------")
#startup

def pQueue():

    #-------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------
    #SETUP: LEER LAS LIBRERÍAS DE C Y WRAPPEAR SUS FUNCIONES EN PYTHON
    #ESTO ABSTRAE UNA COLA DE PRIORIDAD (LAS OPERACIONES ENQUEUE/DEQUEUE)

    #wrapper para funciones de C
    def wrap_function(lib, funcname, restype, argtypes):
        func = lib.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func
    #wrap_function

    #consumir librerías de C
    libmax = ctypes.CDLL("./maxheap.so")
    libmin = ctypes.CDLL("./minheap.so")

    #wrappear funciones de C para heaps y establecer sus tipos de args y return

    #MAX HEAP -------------------- lib --- function ------- return ---------------------- args ---
    maxReader      = wrap_function(libmax, "listReader",    None,                         [ctypes.POINTER(ctypes.c_int), ctypes.c_int])
    maxEnqueue     = wrap_function(libmax, "insert",        None,                         [ctypes.c_int])
    maxDequeue     = wrap_function(libmax, "removeMax",     ctypes.c_int,                 None)
    maxFront       = wrap_function(libmax, "readMax",       ctypes.c_int,                 None)
    getMaxHeapSize = wrap_function(libmax, "throwHeapSize", ctypes.c_int,                 None)
    getMaxHeap     = wrap_function(libmax, "throwHeap",     ctypes.POINTER(ctypes.c_int), None)
    initMaxHeap    = wrap_function(libmax, "initMaxHeap",   None,                         None)
    printMaxHeap   = wrap_function(libmax, "printArray",    None,                         None)

    #MIN HEAP -------------------- lib --- function ------- return ---------------------- args ---
    minReader      = wrap_function(libmin, "listReader",    None,                         [ctypes.POINTER(ctypes.c_int), ctypes.c_int])
    minEnqueue     = wrap_function(libmin, "insert",        None,                         [ctypes.c_int])
    minDequeue     = wrap_function(libmin, "removeMin",     ctypes.c_int,                 None)
    minFront       = wrap_function(libmin, "readMin",       ctypes.c_int,                 None)
    getMinHeapSize = wrap_function(libmin, "throwHeapSize", ctypes.c_int,                 None)
    getMinHeap     = wrap_function(libmin, "throwHeap",     ctypes.POINTER(ctypes.c_int), None)
    initMinHeap    = wrap_function(libmin, "initMinHeap",   None,                         None)
    printMinHeap   = wrap_function(libmin, "printArray",    None,                         None)

    #-------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------
    #SETUP: CREAR LISTAS DE PYTHON QUE CONVERTIREMOS EN HEAPS

    #declarar 3 listas de ints: ascendente, descendente y vacía (para probar el peor caso al construir el heap)
    asc_list = [5,  10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    dsc_list = [75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10,  5]
    nul_list = []

    #generar secuencias de c_int's a partir de las listas
    #su tamaño será el tamaño de la lista
    asc_sequence = ctypes.c_int * len(asc_list)
    dsc_sequence = ctypes.c_int * len(dsc_list)
    nul_sequence = ctypes.c_int * len(nul_list)

    #llamar c_int (es un constructor)
    #pasar la lista como vararg (*) para guardar todos sus elementos como c_int
    asc_array = asc_sequence(*asc_list)
    dsc_array = dsc_sequence(*dsc_list)
    nul_array = nul_sequence(*nul_list)

    #-------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------
    #START: LLAMAR A LAS FUNCIONES DE C Y CONVERTIR UNA LISTA EN HEAP
    #TEST: DESPUÉS, DEMOSTRAR LAS OPERACIONES DE LA COLA (ENQUEUE/DEQUEUE/FRONT)
    #DEMOSTRAR QUE TODO FUNCIONA Y ES ACCESIBLE DESDE PYTHON

    print("\nWELCOME TO THE PRIORITY QUEUE DEMO!\n")

    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #|||||||||||||||||||||| MIN HEAP / MIN PRIORITY QUEUE |||||||||||||||||||||||||||||||||||||||||||
    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    #-----INICIALIZAR LA MIN HEAP / PQUEUE-----
    print("-----------------------------------------\nWe'll build a MIN heap/pqueue.\n")

    #des-comentar para debuggear...
    #print("These are the lists in Python!\n", asc_list, "\n", dsc_list, "\n", nul_list, "\n")

    #enviar una lista de Python a C, leerla en C y construir un heap con ella
    #se debe mandar un arreglo de c_int y su tamaño, ej:
    #(asc_array & asc_list), (dsc_array & dsc_list) o (nul_array & nul_list)
    print("Sending this list to C:\n", dsc_list, sep="")
    minReader(dsc_array, len(dsc_list))

    #ESTA VARIABLE ES NUESTRO HANDLE PARA VER EL HEAP EN PYTHON!!
    #recuperar el array/heap desde C (vive en memoria del .so)
    #se puede obtener el tamaño del heap con getMaxHeapSize() o getMinHeapSize()
    c_heap = getMinHeap() #puntero de arreglo de ints de C

    #re-convertir el array/heap de C de vuelta a lista de Python, sólo para demostrar que se puede...
    p_heap = [c_heap[i] for i in range(getMinHeapSize())]
    print("\nMin-Heapified list, back in Python:\n", p_heap, sep="")

    #-----PRUEBAS CON MIN HEAP / PQUEUE-----
    print("\nTESTING THE MIN-PRIORITY QUEUE")

    #prueba de ENQUEUE (insertar al final de la cola / nodo hoja del heap)
    #[T(n) = log n] en el peor caso (el valor debe viajar hasta el frente)
    #[T(n) = 1] en el mejor caso (el valor está bien al final de la cola)
    print("\nTest: Enqueue some values...")

    eq = 1 #peor caso
    minEnqueue(eq)
    print("enqueued:", eq)
    eq = 80 #mejor caso
    minEnqueue(eq)
    print("enqueued:", eq)
    eq = 42
    minEnqueue(eq)
    print("enqueued:", eq)
    eq = 22
    minEnqueue(eq)
    print("enqueued:", eq)
    eq = 58
    minEnqueue(eq)
    print("enqueued:", eq)

    #imprimir el heap es [T(n) = n]
    printMinHeap()

    #leer el frente de la cola es [T(n) = 1]
    print("\nTest: Read front of the queue:", minFront())

    #prueba de DEQUEUE (borrar el frente de la cola / raíz del heap)
    #[T(n) = log n] en el peor caso (se debe rebalancear hasta algún nodo hoja)
    #[T(n) = 1] en el mejor caso (el nodo que se coloca al frente ya es el mínimo)
    print("\nTest: Dequeue some values...")

    dq = minDequeue()
    print("dequeued:", dq)
    dq = minDequeue()
    print("dequeued:", dq)
    dq = minDequeue()
    print("dequeued:", dq)

    printMinHeap()

    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #|||||||||||||||||||||| MAX HEAP / MAX PRIORITY QUEUE |||||||||||||||||||||||||||||||||||||||||||
    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    #-----INICIALIZAR LA MAX HEAP / PQUEUE-----
    print("-----------------------------------------\nWe'll build a MAX heap/pqueue.\n")

    #des-comentar para debuggear...
    #print("These are the lists in Python!\n", asc_list, "\n", dsc_list, "\n", nul_list, "\n")

    #enviar una lista de Python a C, leerla en C y construir un heap con ella
    #se debe mandar un arreglo de c_int y su tamaño, ej:
    #(asc_array & asc_list), (dsc_array & dsc_list) o (nul_array & nul_list)
    print("Sending this list to C:\n", asc_list, sep="")
    maxReader(asc_array, len(asc_list))

    #ESTA VARIABLE ES NUESTRO HANDLE PARA VER EL HEAP EN PYTHON!!
    #recuperar el array/heap desde C (vive en memoria del .so)
    #se puede obtener el tamaño del heap con getMaxHeapSize() o getMaxHeapSize()
    c_heap = getMaxHeap() #puntero de arreglo de ints de C

    #re-convertir el array/heap de C de vuelta a lista de Python, sólo para demostrar que se puede...
    p_heap = [c_heap[i] for i in range(getMaxHeapSize())]
    print("\nMax-Heapified list, back in Python:\n", p_heap, sep="")

    #-----PRUEBAS CON MAX HEAP / PQUEUE-----
    print("\nTESTING THE MAX-PRIORITY QUEUE")

    #prueba de ENQUEUE (insertar al final de la cola / nodo hoja del heap)
    #[T(n) = log n] en el peor caso (el valor debe viajar hasta el frente)
    #[T(n) = 1] en el mejor caso (el valor está bien al final de la cola)
    print("\nTest: Enqueue some values...")

    eq = 1 #mejor caso
    maxEnqueue(eq)
    print("enqueued:", eq)
    eq = 80 #peor caso
    maxEnqueue(eq)
    print("enqueued:", eq)
    eq = 42
    maxEnqueue(eq)
    print("enqueued:", eq)
    eq = 22
    maxEnqueue(eq)
    print("enqueued:", eq)
    eq = 58
    maxEnqueue(eq)
    print("enqueued:", eq)

    #imprimir el heap es [T(n) = n]
    printMaxHeap()

    #leer el frente de la cola es [T(n) = 1]
    print("\nTest: Read front of the queue:", maxFront())

    #prueba de DEQUEUE (borrar el frente de la cola / raíz del heap)
    #[T(n) = log n] en el peor caso (se debe rebalancear hasta algún nodo hoja)
    #[T(n) = 1] en el mejor caso (el nodo que se coloca al frente ya es el máximo)
    print("\nTest: Dequeue some values...")

    dq = maxDequeue()
    print("dequeued:", dq)
    dq = maxDequeue()
    print("dequeued:", dq)
    dq = maxDequeue()
    print("dequeued:", dq)

    printMaxHeap()
#pQueue

def main():
    startup()
    pQueue()
#main

if __name__=="__main__":
    main()
#if

#eof
