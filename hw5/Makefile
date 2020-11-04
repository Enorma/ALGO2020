all: skiplist.o skiplist.so

skiplist.o: skiplist.c
	gcc -c -Wall -Werror -fpic skiplist.c

skiplist.so: skiplist.o
	gcc -shared -o skiplist.so skiplist.o