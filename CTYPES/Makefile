all: cmult.o libcmult.so

cmult.o: cmult.c
	gcc -c -Wall -Werror -fpic cmult.c

libcmult.so: cmult.o
	gcc -shared -o libcmult.so cmult.o
