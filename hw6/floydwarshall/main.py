from ctypes import string_at
import os
import sys
import ctypes
import matplotlib
import matplotlib.pyplot as plt
from math import log2
from timeit import timeit
from random import randint, randrange, shuffle

slInit = None
mdim   = 16

#clean and rebuild shared objects
def startup():

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove(os.path.join(thispath, "fw.o"))
        os.remove(os.path.join(thispath, "fw.so"))
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

def printMatrix(s):

    m = s.split(" ")

    for i in range(mdim**2):

        if (i % mdim)==0:
            print()
        #if

        print(m[i], end=" ")
    #for
#printMatrix

def fwOperations():

    global slInit

    thispath = os.path.abspath(os.path.dirname(__file__))
    libc = ctypes.CDLL(os.path.join(thispath, "fw.so"))

    #wrap C's functions and set up its arg/return types
    floydWarshall = wrap_function(libc, "runFW", ctypes.POINTER(ctypes.c_char), [ctypes.POINTER(ctypes.c_char), ctypes.c_int, ctypes.c_int])

    print("Algoritmo Floyd Warshall")

    inputstr = "0 42 18 35 1 20 25 29 9 13 15 6 46 32 28 12 42 0 46 43 28 37 42 5 3 4 43 33 22 17 19 46 48 27 0 22 39 20 13 18 10000000 36 45 4 12 23 34 24 15 42 12 0 4 19 48 45 13 8 38 10 24 42 30 29 17 36 41 43 0 39 7 41 43 15 49 47 6 41 30 21 1 7 2 44 49 0 30 24 35 5 7 41 17 27 32 9 45 40 27 24 38 39 0 19 33 30 42 34 16 40 9 5 31 28 7 24 37 22 46 0 25 23 21 30 28 24 48 13 37 41 12 37 6 18 6 25 0 32 3 1 1 42 25 17 31 8 42 8 38 8 38 4 34 0 46 10 10 9 22 39 23 47 7 31 14 19 1 42 13 6 0 11 10 25 38 49 34 46 42 3 1 42 37 25 21 47 22 0 49 10000000 19 35 32 35 4 10000000 19 39 1 39 28 18 29 44 0 49 34 8 22 11 18 14 15 10 17 36 2 1 10000000 20 7 0 49 4 25 9 45 10 40 3 46 36 44 44 24 38 15 4 0 49 1 9 19 31 47 49 32 40 49 10 8 23 23 39 43 0"

    print("\nMatriz de entrada:")
    printMatrix(inputstr)

    inputptr = ctypes.create_string_buffer(str.encode(inputstr))

    print("\n\nCalculando distancias mínimas...")
    outputptr = floydWarshall(inputptr, len(inputstr), mdim)
    outputstr = string_at(outputptr).decode()

    print("\nMatrix de salida:")
    printMatrix(outputstr)

    print()

    '''
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
    '''
#rbtOperations

def main():
    startup()
    fwOperations()
#main

if __name__=="__main__":
    main()
#if

#eof
