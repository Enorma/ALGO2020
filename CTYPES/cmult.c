//cmult.c

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "cmult.h"

float cmult(int int_param, float float_param) {
    float return_value = int_param*float_param;
    printf("In cmult: int: %d * float %.1f = %.1f\n", int_param, float_param, return_value);
    return return_value;
}

int counterFunction(void) {
    static int counter = 0;
    counter++;
    return counter;
}

void addOneToString(char* inputstr) {
    int ii;
    for (ii=0; ii<strlen(inputstr); ii++) {
        inputstr[ii]++;
    }
}

char* allocCString(void) {
    char* phrase = strdup("Mamma mia soy un string en C!!");
    printf("C allocated %ld bytes at address %p for string: %s\n", (long int)phrase, phrase, phrase);
    return phrase;
}

void freeCString(char* charptr) {
    printf("About to free %ld bytes at address %p for string: %s\n", (long int)charptr, charptr, charptr);
    free(charptr);
}

/* Point.c */

/* Display a Point value */
void show_point(Point point) {
    printf("Point in C is:      (%d, %d)\n", point.x, point.y);
}

/* Increment a Point which was passed by value */
void move_point(Point point) {
    show_point(point);
    point.x++;
    point.y++;
    show_point(point);
}

/* Increment a Point which was passed by reference */
void move_point_by_ref(Point *point) {
    show_point(*point);
    point->x++;
    point->y++;
    show_point(*point);
}

/* Return point by value */
Point get_point(void) {
    static int counter = 0;
    Point point = {counter++, counter++};
    printf("Returning Point (%d, %d)\n", point.x, point.y);
    return point;
}

/* Line.c */

/* Show a Line value */
void show_line(Line line) {
    printf("Line in C is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y, line.end.x, line.end.y);
}

/* Update x,y values of both ends of the line*/
void move_line_by_ref(Line *line) {
    show_line(*line);
    move_point_by_ref(&line->start);
    move_point_by_ref(&line->end);
    show_line(*line);
}

/* Return Line by value*/
Line get_line(void) {
    Line l = {get_point(), get_point()};
    return l;
}

//eof
