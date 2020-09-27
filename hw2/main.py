import os
import ctypes

#clean and rebuild shared objects

def startup():

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove(os.path.join(thispath, "binaryqueueradix.o"))
        os.remove(os.path.join(thispath, "binaryqueueradix.so"))
    except:
        pass
    #try-except

    os.system("make all")

    print("Done!\n------------------------------------------")
#startup

def sortingOperations():

    #easy wrapper for C functions
    def wrap_function(lib, funcname, restype, argtypes):
        func = lib.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func
    #wrap_function

    libc = ctypes.CDLL("./binaryqueueradix.so")

    #wrap C's listReader function and set up its arg/return types
    radixSort = wrap_function(libc, "connector", ctypes.POINTER(ctypes.c_int), [ctypes.POINTER(ctypes.c_int), ctypes.c_int])

    #C RadixSort is limited to K binary digits so...
    #...only positive integers from 0 to (2^K)-1 (inclusive) are allowed.
    #K value can be changed in C code (look for MAX_DIGITS constant)
    #K value is 9 now so 0-511.
    the_list = [506, 469, 498, 326, 381, 274, 298, 94, 5, 2]
    the_size = len(the_list)

    #generate a sequence of c_int's,
    #its size will be the length of the_list
    cint_sequence = ctypes.c_int * the_size

    #call c_int (it's a constructor)
    #pass the_list as arg
    #the whole list (the_list) is passed via varargs (*)
    cint_array = cint_sequence(*the_list)

    print("\nWELCOME TO THE RADIX SORTER!\n")

    print("This is the unsorted list in Python!\n", the_list)
    sorted_result = radixSort(cint_array, the_size)
    sorted_list = [sorted_result[i] for i in range(0,the_size)]
    print("This is the sorted list in Python!\n", sorted_list)
#listOperations


def main():
    startup()
    sortingOperations()
#main


if __name__ == "__main__":
    main()
#if

#eof
