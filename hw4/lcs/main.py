import os
import time
import ctypes
import matplotlib
import matplotlib.pyplot as plt
from math import log2
from timeit import timeit
from random import randint

thispath = ""

#clean and rebuild shared objects
def startup():

    global thispath

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove(os.path.join(thispath, "lcs.o"))
        os.remove(os.path.join(thispath, "lcs.so"))
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

def getDNALetter():

    r = randint(0, 3)

    if r==0:
        return "A"
    elif r==1:
        return "C"
    elif r==2:
        return "T"
    elif r==3:
        return "G"
    #if-elif
#getDNALetter

def genDNA(ssize):

    if ssize<=0:
        return False
    #if

    dnastr = ""

    for i in range(ssize):
        dnastr += getDNALetter()
    #for

    return dnastr
#genDNA

def mutate(dnastr, percentage):

    if percentage<0 or percentage>1 or len(dnastr)<=0:
        return False
    #if

    m = int(round(len(dnastr)*percentage, 0))

    for i in range(m):
        r = randint(0, len(dnastr)-1)
        dnastr = dnastr[:r] + getDNALetter() + dnastr[(r+1):]
    #for

    return dnastr
#mutate

def showGraph(result_arr):

    global thispath

    fig, ax = plt.subplots()
    ax.plot(result_arr[0], 'blue',   label='length 05')
    ax.plot(result_arr[1], 'orange', label='10')
    ax.plot(result_arr[2], 'green',  label='15')

    ax.set(xlabel="LCS's computed", ylabel='time', title='Time for LCS with DNA strings of different lengths')
    ax.grid()
    ax.legend(loc='upper center', bbox_to_anchor=(0.82, 1), fancybox=True, shadow=True, ncol=3)

    fig.savefig(os.path.join(thispath, "test.png"))
    plt.show()
#showGraph

def lcsOperations():

    thispath = os.path.abspath(os.path.dirname(__file__))
    libc = ctypes.CDLL(os.path.join(thispath, "lcs.so"))

    #wrap C's lcs function and set up its arg/return types
    getLCS = wrap_function(libc, "lcs", None, [
        ctypes.POINTER(ctypes.c_char),
        ctypes.POINTER(ctypes.c_char),
        ctypes.c_int
    ])

    #descomentar lo siguiente para hacer una prueba sencilla
    '''
    dnalen       = 5   #longitud de las cadenas de ADN
    randomfactor = 0.9 #debe estar entre 0 y 1

    dna1 = genDNA(dnalen)
    dna2 = mutate(dna1, randomfactor)

    print("generamos la cadena:", dna1)
    print("la cadena mutada es:", dna2)

    cstr1 = ctypes.create_string_buffer(dna1.encode())
    cstr2 = ctypes.create_string_buffer(dna2.encode())

    getLCS(cstr1, cstr2, dnalen)
    '''

    #-------------------------------------------------------

    results = []
    x = 0

    dnalen       = 5   #longitud de las cadenas de ADN
    randomfactor = 0.9 #debe estar entre 0 y 1

    for j in range(3):

        dnalen += (j*5) #incrementa tipo 5, 10, 15
        acum = 0

        results.append([])

        for i in range(1000):

            dna1 = genDNA(dnalen)
            dna2 = mutate(dna1, randomfactor)

            cstr1 = ctypes.create_string_buffer(dna1.encode())
            cstr2 = ctypes.create_string_buffer(dna2.encode())

            start_time = time.time()
            getLCS(cstr1, cstr2, dnalen)
            elapsed_time = time.time() - start_time
            acum += elapsed_time
            results[x].append(acum)
        #for

        x += 1
    #for

    showGraph(results)
#lcsOperations

def main():
    startup()
    lcsOperations()
#main

if __name__ == "__main__":
    main()
#if

#eof
