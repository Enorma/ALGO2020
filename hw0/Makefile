all: listreader.o listreader.so

listreader.o: listreader.c
	gcc -c -Wall -Werror -fpic listreader.c

listreader.so: listreader.o
	gcc -shared -o listreader.so listreader.o
