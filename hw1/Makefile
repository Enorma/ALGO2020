all: maxheap.o maxheap.so minheap.o minheap.so

maxheap.o: maxheap.c
	gcc -c -g -Wall -Werror -fpic maxheap.c

maxheap.so: maxheap.o
	gcc -shared -o maxheap.so maxheap.o

minheap.o: minheap.c
	gcc -c -g -Wall -Werror -fpic minheap.c

minheap.so: minheap.o
	gcc -shared -o minheap.so minheap.o
