import os
import sys
import ctypes
import matplotlib
import matplotlib.pyplot as plt
from math import log2
from timeit import timeit
from random import randint, randrange, shuffle

slInit   = None
slInsert = None
slDelete = None
slPrint  = None

#clean and rebuild shared objects
def startup():

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove(os.path.join(thispath, "skiplist.o"))
        os.remove(os.path.join(thispath, "skiplist.so"))
    except:
        pass
    #try-except

    os.system("make all")

    print("Done!\n------------------------------------------")
#startup

#easy wrapper for C functions
def wrap_function(lib, funcname, restype, argtypes):
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func
#wrap_function

def showGraph(results1, results2, results3, thispath):

    fig, ax = plt.subplots()
    ax.plot(results2, 'orange', label='delete')
    ax.plot(results1, 'blue',   label='insert')
    ax.plot(results3, 'black',  label='reference')

    ax.set(xlabel='operation #', ylabel='time(s)', title='Time for skiplist')
    ax.grid()
    ax.legend(loc='best', fancybox=True, shadow=True, ncol=3)

    fig.savefig(os.path.join(thispath, "test.png"))
    plt.show()
#showGraph

def skiplistOperations():

    thispath = os.path.abspath(os.path.dirname(__file__))
    libc = ctypes.CDLL(os.path.join(thispath, "skiplist.so"))

    #wrap C's rbt init function and set up its arg/return types
    global slInit
    global slInsert
    global slDelete
    global slPrint
    slInit   = wrap_function(libc, "init",         None,         None)
    slInsert = wrap_function(libc, "wrapInsertar", None,         [ctypes.c_int])
    slDelete = wrap_function(libc, "wrapBorrar",   ctypes.c_int, [ctypes.c_int])
    slPrint  = wrap_function(libc, "wrapImprimir", None,         None)

    slInit()

    '''
    slInsert(10)
    slInsert(65)
    slInsert(92)
    slInsert(93)
    slInsert(43)
    slPrint()
    print()
    input("dale enter para borrar el 92")
    slDelete(92)
    slPrint()

    sys.exit("hasta aquí wey")
    '''

    print("Iniciando inserciones...")

    reps = 5000 #cantidad de inserts/deletes
    i = [] #para guardar tiempos de insert
    d = [] #para guardar tiempos de delete
    l = [] #para generar una referencia del tiempo esperado

    randominputs = set()
    while len(randominputs)<reps:
        randominputs.add(randint(0, reps))
    #while

    randomlist = list(randominputs)
    #print(randomlist)
    shuffle(randomlist)
    #print(randomlist)
    #sys.exit("hasta aquí wey")

    slInsert(reps+1)

    #inserts
    j = 0
    for x in randomlist:

        t1 = timeit(stmt='slInsert('+str(x)+')', setup='from __main__ import slInsert', number=1) #test Insert
        t3 = log2(j+1)/30000 #se divide para ajustar la línea de referencia en la gráfica

        i.append(t1)
        l.append(t3)
        j+=1
    #for

    #randomlist = randomlist[:-1]

    #deletes
    j = 0
    for x in randomlist:

        t2 = timeit(stmt='slDelete('+str(x)+')', setup='from __main__ import slDelete', number=1) #test Delete

        d.append(t2)
        j+=1
    #for

    list.reverse(d)

    showGraph(i, d, l, thispath)
    print("done")
#rbtOperations

def main():
    startup()
    skiplistOperations()
#main

if __name__=="__main__":
    main()
#if

#eof
