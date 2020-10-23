all: binaryqueueradix.o binaryqueueradix.so

binaryqueueradix.o: binaryqueueradix.c
	gcc -c -Wall -Werror -fpic binaryqueueradix.c

binaryqueueradix.so: binaryqueueradix.o
	gcc -shared -o binaryqueueradix.so binaryqueueradix.o
