all: rbt.o rbt.so

rbt.o: rbt.c
	gcc -c -Wall -Werror -fpic rbt.c

rbt.so: rbt.o
	gcc -shared -o rbt.so rbt.o