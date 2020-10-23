all: lcs.o lcs.so

lcs.o: lcs.c
	gcc -c -Wall -Werror -fpic lcs.c

lcs.so: lcs.o
	gcc -shared -o lcs.so lcs.o