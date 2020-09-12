import os
import ctypes

#clean and rebuild shared objects
def startup():

    print("------------------------------------------\nBuilding C objects...")

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove("listreader.o")
        os.remove("listreader.so")
    except:
        pass
    #try-except

    os.system("make all")

    print("Done!\n------------------------------------------")
#startup

def listOperations():

    #easy wrapper for C functions
    def wrap_function(lib, funcname, restype, argtypes):
        func = lib.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func
    #wrap_function

    libc = ctypes.CDLL("./listreader.so")

    #wrap C's listReader function and set up its arg/return types
    listReader = wrap_function(libc, "listReader", None, [ctypes.POINTER(ctypes.c_int), ctypes.c_int])

    the_list = [0, 1, 1, 2, 3, 5, 8, 13, 21] #python vanilla list

    #generate a sequence of c_int's,
    #its size will be the length of the_list
    cint_sequence = ctypes.c_int * len(the_list)

    #call c_int (it's a constructor)
    #pass the_list as arg
    #the whole list (the_list) is passed via varargs (*)
    cint_array = cint_sequence(*the_list)

    print("\nWELCOME TO THE LIST READER!\n")

    print("This is the list in Python!\n", the_list, "\n")
    listReader(cint_array, len(the_list))
#listOperations

def main():
    startup()
    listOperations()
#main

if __name__=="__main__":
    main()
#if

#eof
