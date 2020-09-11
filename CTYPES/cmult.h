#ifndef INSERTIONSORT_FILE
#define INSERTIONSORT_FILE

    /*cmult.h*/

    float cmult(int int_param, float float_param);
    int counterFunction(void);
    void addOneToString(char* inputstr);
    char* allocCString(void);
    void freeCString(char* charptr);

    /* Point.h */
    /* Simple structure for ctypes example */
    typedef struct {
        int x;
        int y;
    } Point;

    void show_point(Point point);
    void move_point(Point point);
    void move_point_by_ref(Point *point);
    Point get_point(void);

    /* Line.h */
    /* Compound C structure for our ctypes example */
    typedef struct {
        Point start;
        Point end;
    } Line;

    void show_line(Line line);
    void move_line_by_ref(Line *line);
    Line get_line(void);

#endif

//eof
