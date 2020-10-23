
#!/usr/bin/env python
import ctypes
import pathlib
import random
import names
import time

def main():
    # Load the shared library into c types.
    libname = pathlib.Path().absolute() / "liblcs.so"
    c_lib = ctypes.CDLL(libname)
    s = b'pdDRA4'
    s_len = len(s)
    # Init the byte array of the sequence
    s_arr = ctypes.create_string_buffer(s_len)
    s_arr.value = s

    #Call the C function using CTypes
    c_lib.lcs(s, s_len)

    
if __name__ == "__main__":
    main()

    
