import os
import ctypes

#rebuild C shared objects (everything should be in this same directory!!)
try:
    os.remove("cmult.o")
    os.remove("libcmult.so")
except:
    pass
#try-except

os.system("make all")

libc = ctypes.CDLL("./libcmult.so")

print("\nWELCOME TO CTYPES TEST!\n")

#--------------------------------------------------------------------------------

print("Simple multiplication function:")

cmult = libc.cmult #multiplication function

#define arg and return types
cmult.argtypes = [ctypes.c_int, ctypes.c_float]
cmult.restype = ctypes.c_float

res = cmult(2,6.5) #call with params

print("c function says", res)

#--------------------------------------------------------------------------------

print("\nSimple counter function:")

counter = libc.counterFunction #counter function

#define arg and return types (all void!)

count = counter()

print("c function says", count)

#--------------------------------------------------------------------------------

print("\nC function to modify a Python string")
original_string = "starting string"

#need to encode the original string to get bytes for string_buffer
#ctypes' string buffer (char* byte obj) is actually mutable in both C and Python
mutable_string = ctypes.create_string_buffer(str.encode(original_string))

print("Before:", mutable_string.value)

addone = libc.addOneToString #string modification function

#define arg and return types
addone.argtypes = [ctypes.c_char_p]
addone.restype  = ctypes.c_void_p

#call with params
addone(mutable_string)

print("After: ", mutable_string.value)

#--------------------------------------------------------------------------------

print("\nC function to allocate memory for a Python string")

#return a value as char pointer to store its memory address
#we need this address in order to re-send it to C later
alloc_func = libc.allocCString
alloc_func.restype = ctypes.POINTER(ctypes.c_char) #return as pointer
c_string_address = alloc_func()

#copy and convert the pointer to something we can use on the Python side
phrase = ctypes.c_char_p.from_buffer(c_string_address) #from char pointer to string buffer
print("Bytes in Python: {0}".format(phrase.value)) #from string buffer to python string

#send the char pointer back to C
print("\nC function to de-allocate memory of a Python string")
free_func = libc.freeCString
free_func.argtypes = [ctypes.POINTER(ctypes.c_char)]
free_func(c_string_address)

#--------------------------------------------------------------------------------

#Python class wrapper for C struct
class Point(ctypes.Structure):

    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)
    #repr
#Point

#--------------------------------------------------------------------------------

#easy wrapper for C functions
def wrap_function(lib, funcname, restype, argtypes):
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func
#wrap_function

#get functions from C lib and config their args and return types
show_point        = wrap_function(libc, 'show_point',        None, [Point])
move_point        = wrap_function(libc, 'move_point',        None, [Point])
move_point_by_ref = wrap_function(libc, 'move_point_by_ref', None, [ctypes.POINTER(Point)])

#--------------------------------------------------------------------------------

print("\nCreating new Point struct from C")

#instantiate new (python object) Point
p = Point(1, 2)

#call C function
show_point(p)

#--------------------------------------------------------------------------------

print("\nCreating a new point and moving it (by value)")
a = Point(5, 6)
print("Point in Python is:", a)
move_point(a)
print("Point in Python is:", a, "(it didn't change...)")

print("\nCreating a new point and moving it (by reference)")
a = Point(5, 6)
print("Point in Python is:", a)
move_point_by_ref(a)
print("Point in Python is:", a, "(it did change!)")

#--------------------------------------------------------------------------------

#Python class wrapper for C struct with proper python-like features
class EnhancedPoint(ctypes.Structure):

    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __init__(self, lib, x=None, y=None):
        if x:
            self.x = x
            self.y = y
        else:
            get_point = wrap_function(lib, 'get_point', EnhancedPoint, None)
            self = get_point()
        #if-else

        self.show_point_func     = wrap_function(lib, 'show_point',        None, [EnhancedPoint])
        self.move_point_func     = wrap_function(lib, 'move_point',        None, [EnhancedPoint])
        self.move_point_ref_func = wrap_function(lib, 'move_point_by_ref', None, [ctypes.POINTER(EnhancedPoint)])
    #init

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)
    #repr

    def show_point(self):
        self.show_point_func(self)
    #show_point

    def move_point(self):
        self.move_point_func(self)
    #move_point

    def move_point_by_ref(self):
        self.move_point_ref_func(self)
    #move_point_by_ref
#EnhancedPoint

#--------------------------------------------------------------------------------

ep = EnhancedPoint(libc)
print("\nThis is an enhanced point:", ep)

#--------------------------------------------------------------------------

print("\nPass a struct into C")
ep = EnhancedPoint(libc, 1, 2)
print("Point in python is:", ep)
ep.show_point()

#--------------------------------------------------------------------------

print("\nMove, Pass by value")
ep = EnhancedPoint(libc, 5, 6)
print("Point in python is:", ep)
ep.move_point()
print("Point in python is:", ep, "(it didn't change...)")

#--------------------------------------------------------------------------

print("\nMove, Pass by reference")
ep = EnhancedPoint(libc, 5, 6)
print("Point in python is:", ep)
ep.move_point_by_ref()
print("Point in python is:", ep, "(it did change!)")

#--------------------------------------------------------------------------

#Check how this changes in C, but not in Python, because it's pass-by-value
print("\nGet Struct from C")
ep = EnhancedPoint(libc)
print("New Point in python (from C) is", ep)
ep = EnhancedPoint(libc)
print("New Point in python (from C) is", ep)
ep = EnhancedPoint(libc)
print("New Point in python (from C) is", ep)
ep = EnhancedPoint(libc)
print("New Point in python (from C) is", ep)

#--------------------------------------------------------------------------

class Line(ctypes.Structure):

    _fields_ = [('start', EnhancedPoint), ('end', EnhancedPoint)]

    def __init__(self, lib):

        get_line = wrap_function(lib, 'get_line', Line, None)
        line = get_line()

        self.start = line.start
        self.end   = line.end
        self.show_line_func = wrap_function(lib, 'show_line',        None, [Line])
        self.move_line_func = wrap_function(lib, 'move_line_by_ref', None, [ctypes.POINTER(Line)])
    #init

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)
    #repr

    def show_line(self):
        self.show_line_func(self)
    #show_line

    def move_line(self):
        self.move_line_func(self)
    #move_line
#Line

#--------------------------------------------------------------------------

#declare a new line
print("\nGenerating new line:")
l = Line(libc)

print("\nThis is the new line:")
l.show_line()

print("\nMoving the line:")
l.move_line()

print("\nThis is the moved line:")
l.show_line()

#eof
