import os
import ctypes

#clean and rebuild shared objects

def startup():

    print("------------------------------------------\nBuilding C objects...")

    thispath = os.path.abspath(os.path.dirname(__file__))

    #rebuild C shared objects (everything should be in this same directory!!)
    try:
        os.remove(os.path.join(thispath, "hashtable.o"))
        os.remove(os.path.join(thispath, "hashtable.so"))
    except:
        pass
    #try-except

    os.system("make all")

    print("Done!\n------------------------------------------")
#startup

def hashTableOperations():

    #easy wrapper for C functions
    def wrap_function(lib, funcname, restype, argtypes):
        func = lib.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func
    #wrap_function

    libc = ctypes.CDLL("./hashtable.so")

    #wrap C's listReader function and set up its arg/return types
    init           = wrap_function(libc, "connector",       None,          None)
    printTable     = wrap_function(libc, "printTable",      None,          None)
    finish         = wrap_function(libc, "finish",          None,          None)
    insertKeyValue = wrap_function(libc, "hashTableInsert", ctypes.c_bool, [ctypes.POINTER(ctypes.c_char), ctypes.c_uint])
    deleteKeyValue = wrap_function(libc, "hashTableDelete", ctypes.c_bool, [ctypes.POINTER(ctypes.c_char)])
    getValue       = wrap_function(libc, "hashTableRead",   ctypes.c_uint, [ctypes.POINTER(ctypes.c_char)])

    print("\nWELCOME TO THE HASH TABLE!\n")

    print("Let's initialize the hash table!\n")
    init()

    print("We'll add a new key:value pair: {0}, {1} years old".format("Marco", 99))
    insertKeyValue(ctypes.create_string_buffer(b"Marco"), 99)
    print("We'll add a new key:value pair: {0}, {1} years old".format("Jose", 99))
    insertKeyValue(ctypes.create_string_buffer(b"Jose"), 99)
    print("We'll add a new key:value pair: {0}, {1} years old".format("Javier", 99))
    insertKeyValue(ctypes.create_string_buffer(b"Javier"), 99)
    print("We'll add a new key:value pair: {0}, {1} years old".format("Juan", 99))
    insertKeyValue(ctypes.create_string_buffer(b"Juan"), 99)
    print("We'll add a new key:value pair: {0}, {1} years old".format("Cinthia", 99))
    insertKeyValue(ctypes.create_string_buffer(b"Cinthia"), 99)
    print("We'll add a new key:value pair: {0}, {1} years old".format("Eduardo", 99))
    insertKeyValue(ctypes.create_string_buffer(b"Eduardo"), 99)

    printTable()

    print("We'll delete a key:value pair: {0}".format("Marco"))
    deleteKeyValue(ctypes.create_string_buffer(b"Marco"))
    print("We'll delete a key:value pair: {0}".format("Kike"))
    deleteKeyValue(ctypes.create_string_buffer(b"Kike"))
    print("We'll delete a key:value pair: {0}".format("Alex"))
    deleteKeyValue(ctypes.create_string_buffer(b"Alex"))
    print("We'll delete a key:value pair: {0}".format("Bernardo"))
    deleteKeyValue(ctypes.create_string_buffer(b"Bernardo"))

    printTable()
    finish()
#hashTableOperations

def main():
    startup()
    hashTableOperations()
#main

if __name__ == "__main__":
    main()
#if

#eof
