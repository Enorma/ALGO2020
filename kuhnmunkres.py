from functools import reduce

MAXVERT = 10
MAXEDGE = 99

#GLOBALES FIJAS
vertices_A = "" #cantidad de filas
vertices_B = "" #cantidad de columnas
diff       = "" #filas - columnas
bigdim     = "" #cantidad de filas/columnas (la mayor)
lildim     = "" #cantidad de filas/columnas (la menor)
graph      = [] #la matriz con la que trabajamos
graph2     = [] #una copia de graph

#GLOBALES RECALCULABLES
rowzeros     = "" #cantidad de filas con ceros no marcados
colzeros     = "" #cantidad de columnas con ceros no marcados
g_rows       = [] #cantidad de ceros en cada fila
g_cols       = [] #cantidad de ceros en cada columna
cell_marks   = [] #matriz de ceros marcados
row_marks    = [] #lista de filas marcadas
col_marks    = [] #lista de columnas marcadas
using_cols   = [] #lista de columnas con ceros ya elegidos
zeros_by_row = [] #columna con cero elegido en cada fila

#---------------------------------------------------
#PASOS DE INICIALIZACIÓN

#para pedir un número al usuario y validarlo
def askInteger(msg, lb, ub):

    prompted = ""
    valid = False

    while not(valid):

        try:
            prompted = float(input(msg)) #pedir un número al usuario, convertirlo a float
            try:
                prompted = int(prompted) #convertir el número a int
            except:
                print("Debes ingresar un entero entre {0} y {1}".format(lb, ub)) #si no se puede convertir de float a int
                valid = False
                continue
            #try-except
        except:
            print("Debes ingresar un entero entre {0} y {1}".format(lb, ub)) #si no se puede convertir de string a float
            valid = False
            continue
        #try-except

        if prompted>=lb and prompted<=ub: #checar que el número esté en el rango
            valid = True
        else:
            print("Debes ingresar un entero entre {0} y {1}".format(lb, ub)) #si el número sale del rango
            valid = False
            continue
        #if-else
    #while

    return prompted
#askInteger

#para imprimir la matriz del grafo
def printGraph():

    global graph
    global MAXEDGE
    global vertices_A
    global vertices_B
    global row_marks
    global col_marks
    global zeros_by_row

    rm = ""
    cm = ""

    #imprimir marcas verticales para columnas
    if len(col_marks)>0:
        for x in col_marks:
            cm += "  | " if x==1 else "    " #funciona para números de 2 dígitos
        #for
    #if

    #iterar sobre cada fila
    for i in range(vertices_A):

        #imprimir (si hubiera) marcas entre cada 2 filas
        print(cm)

        #imprimir marcas horizontales para filas
        if len(row_marks)>0 and row_marks[i]==1:
            rm = "-"
        else:
            rm = " "
        #if-else

        #imprimir celda por celda
        for j in range(vertices_B):

            #si fuera un cero ya escogido en el resultado final, imprimirlo entre paréntesis
            if len(zeros_by_row)>0 and zeros_by_row[i]==j:
                print( "("+str(graph[i][j]).zfill(len(str(MAXEDGE)))+")", end="" )
            else:
                print( rm+str(graph[i][j]).zfill(len(str(MAXEDGE)))+rm, end="" )
            #if
        #for
        print()
    #for
    print(cm)

    return
#printGraph

#para pedir datos al usuario
def form():

    global MAXVERT
    global MAXEDGE
    global graph
    global vertices_A
    global vertices_B

    '''
    #pedir dimensiones de la matriz
    vertices_A = askInteger("\nIngrese la cantidad de vértices de partida (filas) (max {0}): ".format(MAXVERT), 1, MAXVERT)
    vertices_B = askInteger("\nIngrese la cantidad de vértices de destino (columnas) (max {0}): ".format(MAXVERT), 1, MAXVERT)

    #llenar la matriz, fila por fila
    for i in range(vertices_A):

        v_edges = []

        print("\nIngrese pesos de aristas desde A{0}:".format(i))

        #llenar la matriz, celda por celda
        for j in range(vertices_B):
            j_edge = askInteger("\tArista de A{0} a B{1} (max {2}): ".format(i,j,MAXEDGE), 0, MAXEDGE)
            v_edges.append(j_edge)
        #for

        graph.append(v_edges)
    #for
    '''

    #valores hardcodeados para debuggear
    vertices_A = 5
    vertices_B = 5

    graph = [
        [ 7,  1,  1,  7,  2],
        [14, 11, 12, 16,  9],
        [19,  5, 12,  5, 12],
        [16,  4,  5,  7, 13],
        [12,  8, 12,  3,  5]
    ]

    #hacer una copia profunda de graph, porque graph va a cambiar
    #graph2 es de donde sacaremos los pesos de los aristas escogidos al final
    for i in range(vertices_A):
        graph2.append([])
        for j in range(vertices_B):
            graph2[i].append(graph[i][j])
        #for
    #for

    print("\nMatriz ingresada:")
    printGraph()
    input("ENTER para continuar...\n")

    return
#form

#rellenar con ceros una matriz rectangular para hacerla cuadrada
def zeroPad():

    global graph
    global vertices_A
    global vertices_B
    global bigdim
    global lildim
    global diff

    #restar los tamaños de las dimensiones nos indica si la matriz es vertical, horizontal o cuadrada
    diff = vertices_A - vertices_B

    if diff==0: #igual filas que columnas (cuadrada)

        bigdim = lildim = vertices_A #asignar ambas dimensiones igualmente y salir

        return
    elif diff>0: #más filas que columnas (vertical)

        for i in range(vertices_A):
            graph[i] += [0]*diff #agregar columnas a la derecha, llenas de ceros
        #for

        bigdim = vertices_A #la dimensión grande es la vertical (filas)
        lildim = vertices_B
    elif diff<0: #más columnas que filas (horizontal)

        for i in range(diff*-1):
            graph.append([0]*vertices_B) #agregar filas a la abajo, llenas de ceros
        #for

        bigdim = vertices_B #la dimensión grande es la horizontal (columnas)
        lildim = vertices_A
    #if-elif

    print("\nConvertida a matriz cuadrada:")
    printGraph()
    input("ENTER para continuar...\n")

    return
#zeroPad

#---------------------------------------------------
#PASO #1: REDUCIR POR FILAS

#restar a cada fila su elemento mínimo
def rowReduction():

    global graph
    global bigdim

    #iterar en cada fila
    for i in range(bigdim):
        min_edge = min(graph[i]) #calcular el mínimo de la fila
        graph[i] = list(map(lambda x: x-min_edge, graph[i])) #restar el mínimo a cada elemento
    #for

    print("\nDespués de reducir por filas:")
    printGraph()
    input("ENTER para continuar...\n")

    return
#rowReduction

#---------------------------------------------------
#PASO #2: REDUCIR POR COLUMNAS

#restar a cada columna su elemento mínimo
def columnReduction():

    global graph
    global bigdim

    #iterar en cada columna
    for j in range(bigdim):

        min_edge = graph[0][j]

        #iterar en cada celda de la columna
        for i in range(bigdim):
            if graph[i][j]<min_edge: #calcular el mínimo de la columna
                min_edge = graph[i][j]
            #if
        #for

        #iterar en cada celda de la columna
        for i in range(bigdim):
            graph[i][j] -= min_edge #restar el mínimo a cada elemento
        #for
    #for

    print("\nDespués de reducir por columnas:")
    printGraph()
    input("ENTER para continuar...\n")

    return
#columnReduction

#---------------------------------------------------
#PASO #3: MARCAR FILAS/COLUMNAS QUE TENGAN CEROS
#PASO #4: GENERAR MÁS CEROS DE SER NECESARIO

#contar ceros en cada fila/columna e inicializar globales para colocar marcas
def calcZeros():

    global graph
    global vertices_A
    global vertices_B
    global g_rows
    global g_cols
    global cell_marks
    global row_marks
    global col_marks

    #para contar ceros en cada fila/columna
    g_rows = [0]*vertices_A #inicializar en ceros
    g_cols = [0]*vertices_B

    #para poner marcas a cada fila/columna
    row_marks = [0]*vertices_A #inicializar en ceros
    col_marks = [0]*vertices_B

    #iterar en cada fila
    for i in range(vertices_A):

        #iterar en cada columna
        for j in range(vertices_B):

            #si se encuentra un cero
            if graph[i][j]==0:

                #incrementar contadores de ceros
                g_rows[i]+=1
                g_cols[j]+=1
            #if
        #for

        #para poner marcas a cada celda
        cell_marks.append([0]*vertices_B) #inicializar en ceros
    #for

    print("Ceros en cada fila: ", g_rows)
    print("Ceros en cada columna: ", g_cols)
    input("ENTER para continuar...\n")

    return
#calcZeros

#contar las filas/columnas que tienen ceros no marcados
def countUnmarkedZeros():

    global graph
    global vertices_A
    global vertices_B
    global rowzeros
    global colzeros
    global cell_marks

    #inicializar contadores
    rowzeros = 0
    colzeros = 0

    #iterar por filas, luego columnas
    for i in range(vertices_A):
        for j in range(vertices_B):

            #si se encuentra un cero no marcado, incrementar el contador
            if graph[i][j]==0 and cell_marks[i][j]==0:
                rowzeros += 1
                break #con haber encontrado un cero basta para esa fila
            #if
        #for
    #for

    #iterar por columnas, luego filas
    for j in range(vertices_B):
        for i in range(vertices_A):

            #si se encuentra un cero no marcado, incrementar el contador
            if graph[i][j]==0 and cell_marks[i][j]==0:
                colzeros += 1
                break #con haber encontrado un cero basta para esa columna
            #if
        #for
    #for

    return
#countUnmarkedZeros

#marcar una fila/columna que tenga ceros no marcados
def tryLookup():

    global graph
    global vertices_A
    global vertices_B
    global cell_marks
    global row_marks
    global col_marks
    global rowzeros
    global colzeros

    #encontrar la fila no marcada con más ceros no marcados

    maxzerorow   = 0 #señala la fila con más ceros
    maxzeros_row = 0 #cuenta cuántos ceros tiene esa fila

    #iterar por filas
    for i in range(vertices_A):

        #si la fila ya está marcada, ignorarla
        if row_marks[i]:
            continue
        #if

        #contar cuantos ceros no marcados hay en la fila 
        cur_zeros = 0
        for j in range(vertices_B):
            if graph[i][j]==0 and cell_marks[i][j]==0:
                cur_zeros += 1 #contar cada cero no marcado
            #if
        #for

        #si la fila actual es la que tiene más ceros
        if cur_zeros>maxzeros_row:
            maxzeros_row = cur_zeros #guardar la cantidad de ceros
            maxzerorow   = i
        #if
    #for

    #encontrar la columna no marcada con más ceros no marcados

    maxzerocol   = 0 #señala la columna con más ceros
    maxzeros_col = 0 #cuenta cuántos ceros tiene esa columna

    #iterar por columnas
    for j in range(vertices_B):

        #si la columna ya está marcada, ignorarla
        if col_marks[j]:
            continue
        #if

        #contar cuantos ceros no marcados hay en la columna 
        cur_zeros = 0
        for i in range(vertices_A):
            if graph[i][j]==0 and cell_marks[i][j]==0:
                cur_zeros += 1 #contar cada cero no marcado
            #if
        #for

        #si la columna actual es la que tiene más ceros
        if cur_zeros>maxzeros_col:
            maxzeros_col = cur_zeros #guardar la cantidad de ceros
            maxzerocol   = j
        #if
    #for

    #si no se encontraron ceros, salir
    if maxzeros_row==0 and maxzeros_col==0:
        return -1
    #if

    #siempre elegir la fila o columna que tenga más ceros
    #si hay empate entre una fila y una columna, aplicar el criterio de desempate:
    #si hay menos filas que columnas con ceros no marcados, elegir la fila, y viceversa
    #si de nuevo hay empate, elegir la fila.

    #contar las filas/columnas que tienen al menos un cero no marcado
    countUnmarkedZeros()

    #si hay más ceros en alguna columna, o si hay empate y hay más filas que columnas con ceros no marcados
    if (maxzeros_row<maxzeros_col) or (maxzeros_row==maxzeros_col and rowzeros>colzeros):

        #escoger y marcar una columna
        col_marks[maxzerocol] = 1

        for i in range(vertices_A):
            if graph[i][maxzerocol]==0:
                cell_marks[i][maxzerocol] = 1 #marcar cada cero en la columna
            #if
        #for
    else:

        #escoger y marcar una fila
        row_marks[maxzerorow] = 1

        for i in range(vertices_B):
            if graph[maxzerorow][i]==0:
                cell_marks[maxzerorow][i] = 1 #marcar cada cero en la fila
            #if
        #for
    #if-elif-else

    printGraph()
    input("ENTER para continuar...\n")

    return 1
#tryLookup

#generar nuevos ceros en caso de no encontrar asignación óptima
def zeroShift():

    global graph
    global vertices_A
    global vertices_B
    global cell_marks
    global row_marks
    global col_marks

    #buscar la celda no marcada que tenga el valor mínimo de toda la matriz
    mincell = MAXEDGE
    for i in range(vertices_A): #iterar por filas

        #si la fila actual está marcada, ignorarla
        if row_marks[i]==1:
            continue
        #if

        #iterar por celdas
        for j in range(vertices_B):

            #si la columna de la celda actual no está marcada
            #y si el elemento actual es menor al mínimo guardado
            if col_marks[j]==0 and graph[i][j]<mincell:
                mincell = graph[i][j] #guardar el mínimo
            #if
        #for
    #for

    #generar ceros dependiendo del status de cada celda
    for i in range(vertices_A):
        for j in range(vertices_B):

            if row_marks[i]==1 and col_marks[j]==1: #celda en un cruce marcado, sumarle el mínimo
                graph[i][j] += mincell
            elif row_marks[i]==1 or col_marks[j]==1: #celda en una línea marcada, ignorarla
                continue
            else:
                graph[i][j] -= mincell #cualquier otra celda, restarle el mínimo
            #if
        #for
    #for

    print("\nDespués de ajustar ceros:")
    printGraph()
    input("ENTER para continuar...\n")

    return
#zeroShift

#loop que marca líneas y ajusta ceros mientras no se encuentre el óptimo
def findZeroLines():

    global rowzeros
    global colzeros
    global g_rows
    global g_cols
    global cell_marks
    global row_marks
    global col_marks
    global lildim

    #el loop se romperá cuando se encuentre el óptimo
    while(True):

        #reinicializar globales en cada vuelta
        rowzeros   = ""
        colzeros   = ""
        g_rows     = []
        g_cols     = []
        cell_marks = []
        row_marks  = []
        col_marks  = []

        #volver a calcular cuantos ceros hay en este momento
        calcZeros()

        #marcar líneas con ceros
        print("\nMarcando líneas...")
        print("------------------------------")
        while tryLookup()>-1: #mientras no devuelva -1, sigue marcando líneas con ceros
            pass
        #while
        print("------------------------------")

        #contar las líneas marcadas
        count = 0
        count += reduce((lambda x,y : x+y), row_marks)
        count += reduce((lambda x,y : x+y), col_marks)

        #deben estar marcadas N líneas en una matriz de NxN
        #si son menos de N, no se ha encontrado el óptimo

        print("\nTodos los ceros se cubrieron con {0} líneas.".format(count))
        if count<lildim:
            print("No son suficientes líneas. Ajustando ceros...")
            zeroShift() #generar nuevos ceros y reintentar el loop
        else:
            print("Existe una asignación óptima.") #romper el ciclo
            break
        #if-else
    #while

    #ya no necesitamos estas variables
    rowzeros   = ""
    colzeros   = ""
    g_rows     = []
    g_cols     = []
    cell_marks = []
    row_marks  = []
    col_marks  = []

    print("\nBuscar asignación óptima en:")
    printGraph()
    input("ENTER para continuar...\n")

    return
#findZeroLines

#---------------------------------------------------
#PASO #5: BUSCAR CEROS ÓPTIMOS

#cada llamada recursiva explora una fila buscando un cero óptimo
def findOptimals(i):

    global graph
    global vertices_A
    global vertices_B
    global using_cols
    global zeros_by_row

    #si ya se han explorado todas las filas,
    #ya tenemos el apareamiento óptimo. salir.
    if i==vertices_A:
        return True
    #if

    #iterar por celdas
    for j in range(vertices_B):

        #si encontramos un cero no marcado
        if graph[i][j]==0 and using_cols[j]==0:

            #guardar la columna actual y marcarla
            zeros_by_row[i] = j
            using_cols[j]   = 1

            #explorar la siguiente fila
            if findOptimals(i+1):
                return True
            #if

            #si llegamos aquí, el cero encontrado no es óptimo,
            #desmarcarlo y seguir buscando en esta fila
            using_cols[j] = 0
        #if
    #for

    #si se ha explorado toda la fila, no se encontró un óptimo en ella
    #volver a la fila anterior y seguir buscando en ella
    return False
#findOptimals

#llama a la búsqueda (recursiva) de ceros óptimos y presenta resultados
def findOptimalsWrapper():

    global graph2
    global using_cols
    global zeros_by_row
    global vertices_A
    global vertices_B

    #inicializar en cero y -1 las listas que usa la búsqueda recursiva
    using_cols   = [0]*vertices_B
    zeros_by_row = [-1]*vertices_A

    #llamar a la búsqueda recursiva empezando por la primera fila
    solved = findOptimals(0)

    #si la búsqueda no devolvió true, o si alguna fila no tiene un cero óptimo
    if not(solved) or (-1 in zeros_by_row):

        print("No pude encontrar la asignación óptima...")
    else:

        #se encontró un resultado óptimo, presentarlo
        sumaoptima = 0
        print("La asignación óptima es:")

        #aquí se usa la copia de la matriz que hicimos al inicio
        #ya que esa conserva sus valores originales

        #iterar por filas
        for i in range(vertices_A):
            sumaoptima += graph2[i][zeros_by_row[i]] #sumar el peso de cada arista óptimo
            print("A{0} hacia B{1} = {2}".format(i, zeros_by_row[i], graph2[i][zeros_by_row[i]]))
        #for

        #presentar finalmente la matriz con sus ceros escogidos
        print("\nLa suma de aristas óptimos es:", sumaoptima)
        printGraph()
        input("ENTER para salir...\n")
    #if-else

    return
#findOptimalsWrapper

#---------------------------------------------------
#DRIVER

def main():
    form()
    zeroPad()
    rowReduction()
    columnReduction()
    findZeroLines()
    findOptimalsWrapper()
#main

if __name__=="__main__":
    main()
#if

#eof
