all: fw.o fw.so

fw.o: fw.c
	gcc -c -Wall -Werror -fpic fw.c

fw.so: fw.o
	gcc -shared -o fw.so fw.o