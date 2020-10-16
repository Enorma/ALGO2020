import os
import ctypes
import matplotlib
import matplotlib.pyplot as plt
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

def rbtOperations():
    libc = ctypes.CDLL("./rbt.so")

    #wrap C's rbt init function and set up its arg/return types
    rbtInsert = wrap_function(libc, "insertInt", None, [ctypes.c_int])
    rbtSearch = wrap_function(libc, "searchInt", ctypes.c_int, [ctypes.c_int])

    print("Iniciando inserciones...")

    def testInsert():
        rbtInsert(randint(0, 2))
    #testInsert

    s = ""
    for i in range(2):
        #r = randint(0, 400000)
        t = timeit(testInsert, number=1)
        s += str(t)+","
    #for

    print("Escribiendo resultados...")

    s = s[:-1]
    csv = open("timer.csv","w")
    csv.write(s)
    print("Ya'stuvo")
#rbtOperations

def main():
    startup()
    rbtOperations()
#main

if __name__=="__main__":
    main()
#if

#eof
