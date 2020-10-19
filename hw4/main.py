import os
import ctypes
import matplotlib
import matplotlib.pyplot as plt
from math import log2
from timeit import timeit
from random import randint

#clean and rebuild shared objects
def startup():

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove(os.path.join(thispath, "rbt.o"))
        os.remove(os.path.join(thispath, "rbt.so"))
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
    ax.plot(results1, 'blue',   label='insert')
    ax.plot(results2, 'orange', label='search')
    ax.plot(results3, 'green',  label='reference')

    ax.set(xlabel='input #', ylabel='time(s)', title='Time for red black tree')
    ax.grid()
    ax.legend(loc='upper center', bbox_to_anchor=(0.82, 1), fancybox=True, shadow=True, ncol=3)

    fig.savefig(os.path.join(thispath, "test.png"))
    plt.show()
#showGraph

def rbtOperations():

    thispath = os.path.abspath(os.path.dirname(__file__))
    libc = ctypes.CDLL(os.path.join(thispath, "rbt.so"))

    #wrap C's rbt init function and set up its arg/return types
    global rbtInsert
    global rbtSearch
    rbtInsert = wrap_function(libc, "insertInt", None, [ctypes.c_int])
    rbtSearch = wrap_function(libc, "searchInt", ctypes.c_int, [ctypes.c_int])

    print("Iniciando inserciones...")

    reps = 10000 #cantidad de inserts/searches
    i = [] #para guardar tiempos de insert
    s = [] #para guardar tiempos de search
    l = [] #para generar una referencia del tiempo esperado

    for x in range(reps):

        r = randint(0, reps)

        t1 = timeit(stmt='rbtInsert('+str(r)+')', setup='from __main__ import rbtInsert', number=1) #testInsert
        t2 = timeit(stmt='rbtSearch('+str(r)+')', setup='from __main__ import rbtSearch', number=1) #testSearch
        t3 = log2(x+1)/1000000 #se divide para ajustar la línea de referencia en la gráfica

        i.append(t1)
        s.append(t2)
        l.append(t3)
    #for

    showGraph(i, s, l, thispath)
    print("done")
#rbtOperations

def main():
    startup()
    rbtOperations()
#main

if __name__=="__main__":
    main()
#if

#eof
