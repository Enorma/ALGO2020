#coeficientes de g, h
factorG = 1 #incrementa el valor de gx
factorH = 1 #incrementa el valor de hx

#para elegir cómo calcular h(x)
#si manhattan es False, usa el método de diferencias
manhattan = True

#colas de nodos
colaQ = None #closed set
colaP = None #open set

#tablero inicial
init = [
    '1', '5', '6',
    '8', '4', '_',
    '7', '3', '2'
]

#tablero meta
term = [
    '1', '2', '3',
    '8', '_', '4',
    '7', '6', '5'
]

#posición del espacio vacío ("_") en el tablero meta (se calcula en el main)
termEmpty = None

# Movimientos posibles del Puzzle para la posición actual del espacio vacío
movimientos = {

    # Esquinas
    0: {3:"v",  1:">"},
    2: {5:"v",  1:"<"},
    6: {3:"^",  7:">"},
    8: {5:"^",  7:"<"},

    # Laterales
    1: {0:"<",  4:"v",  2:">"},
    3: {6:"v",  4:">",  0:"^"},
    5: {2:"^",  4:"<",  8:"v"},
    7: {8:">",  4:"^",  6:"<"},

    # Centro
    4: {1:"^",  5:">",  7:"v",  3:"<"}
}

#Calcular todas las posibles distancias de manhattan para el tablero meta elegido
def getManhattanMatrix(finalboard):

    manhattanBase = [
        [0,1,2,1,2,3,2,3,4], #0
        [1,0,1,2,1,2,3,2,3], #1
        [2,1,0,3,2,1,4,3,2], #2
        [1,2,3,0,1,2,1,2,3], #3
        [2,1,2,1,0,1,2,1,2], #4
        [3,2,1,2,1,0,3,2,1], #5
        [2,3,4,1,2,3,0,1,2], #6
        [3,2,3,2,1,2,1,0,1], #7
        [4,3,2,3,2,1,2,1,0]  #8
    ]

    aux_matrix = []

    for i in range(0,9):
        fvalue = "_" if i==0 else str(i)
        findex = finalboard.index(fvalue)
        aux_matrix.append(manhattanBase[findex])
    #for

    return aux_matrix
#getManhattanMatrix

#precomputar distancias de Manhattan
mmatrix = getManhattanMatrix(term)

#Calcular la distancia de manhattan de una casilla con respecto al tablero meta
def calcManhattanOne(cindex, currboard, aux_matrix):
    cvalue = 0 if currboard[cindex]=="_" else int(currboard[cindex])
    return aux_matrix[cvalue][cindex]
#calcManhattan

#Calcular la suma de las distancias de manhattan con respecto al tablero meta
def calcManhattanSum(currboard, aux_matrix):

    acc = 0

    for i in range(0,9):
        acc += calcManhattanOne(i, currboard, aux_matrix)
    #for

    return acc
#calcManhattan

#Clase para los nodos del árbol
class Nodo:

    def __init__(self, tablero, parent, mov):

        global factorG
        global manhattan

        self._tablero = tablero # snapshot del tablero
        self._parent  = parent  # nodo padre
        self._mov     = mov     # movimiento (^,v,<,>) que produjo este nodo desde el padre

        #determinar índice del espacio vacío ("_")
        self._space = "".join(self.getTablero()).find("_")

        #determinar profundidad del nodo en el árbol (gx = distancia recorrida desde el inicio)
        self._gx = 0 if not parent else parent.getGx() + factorG #incrementa el valor de gx

        #determinar cómo calcular heurística h(x) y calcularla
        _hx = self.calcMDHx() if manhattan else self.calcDFHx()

        #obtener valor del nodo haciendo f(x) = g(x) + h(x)
        self._fx = self.getGx() + _hx
    #init

    #Calcular si un nodo tiene f(x) menor o igual a otro (se desempata con g(x))+
    def __lt__(self, other):

        if ( self.getFx()<other.getFx() ) or ( ( self.getFx()==other.getFx() ) and ( self.getGx()>other.getGx() ) ):
            return True
        #if

        return False
    #lt

    #Calcular si un nodo tiene tablero igual a otro
    def __eq__(self, other):

        return self.getTablero() == other.getTablero()
    #eq

    #Calculo de heurística (MD: manhattan distances)
    def calcMDHx(self):

        global mmatrix
        global factorH

        return factorH * calcManhattanSum(self.getTablero(), mmatrix)
    #calcHx

    #Calculo de heurística (DF: different positions)
    def calcDFHx(self):

        global termEmpty
        global factorH
        global term

        #el error de la posición del espacio vacío se cuenta solo una vez
        #si se encuentra en distintas posiciones(Estado final e inicial).

        suma = factorH * sum([1 for x in range(9) if self.getTablero()[x]!=term[x]])

        return suma-factorH if self.getSpace()!=termEmpty else suma
    #calcHx

    #Getters...

    def getTablero(self):

        return self._tablero
    #getTablero

    def getParent(self):

        return self._parent
    #getParent

    def getMov(self):

        return self._mov
    #getMov

    def getSpace(self):

        return self._space
    #getSpace

    def getGx(self):

        return self._gx
    #getGx

    def getFx(self):

        return self._fx
    #getFx
#Nodo

#closed set para guardar los nodos ya explorados
class ColaQ:

    def __init__(self):

        self._queue = []
    #init

    #encolar un nodo ya explorado
    def enqueue(self, nodo):

        if self.isEmpty() or not(self.contains(nodo)):
            self._queue.append(nodo)
        #if
    #enqueue

    #Búsqueda de un nodo en el closed set
    def contains(self, cur_node):

        for enqueued_node in self._queue:
            if cur_node==enqueued_node:
                return True
            #if
        #for

        return False
    #contains

    #Devuelve si el closed set es vacío
    def isEmpty(self):

        return not self._queue
    #isEmpty

    #Devuelve tamaño del closed set
    def getSize(self):

        return len(self._queue)
    #getSize
#ColaQ

#open set para guardar los nodos aún no explorados
#se reordena cada enqueue() y no acepta repetidos
class BestFirst:

    def __init__(self):

        self._queue = []
    #init

    #Encolar
    def enqueue(self, nodo):

        if self.isEmpty():

            self._queue.append(nodo)
        elif not(self.contains(nodo)):

            self._queue.append(nodo)

            #Reordenar
            for x in range(len(self._queue)-1, 0, -1):

                if self._queue[x] < self._queue[x-1]:
                    self._queue[x], self._queue[x-1] = self._queue[x-1], self._queue[x]
                else:
                    break
                #if-else
            #for
        #if-elif
    #enqueue

    #Desencolar
    def dequeue(self):

        return self._queue.pop(0)
    #dequeue

    #Búsqueda de duplicados y obtención de index
    def contains(self, cur_node):

        if not self.isEmpty():
            for index, enqueued_node in enumerate(self._queue):
                if cur_node==enqueued_node:
                    return True, index
                #if
            #for
        #if

        return False
    #contains

    #Determinar si está cola vacía
    def isEmpty(self):

        return not self._queue
    #isEmpty

    #Obtener un nodo del open set
    def getNode(self, index):

        return self._queue[index]
    #getNode

    # Longitud de cola
    def getSize(self):

        return len(self._queue)
    #getSize
#BestFirst

#imprime un tablero
def printBoard(array):
    print(array[0:3])
    print(array[3:6])
    print(array[6:9])
#printBoard

#escribe un tablero en un archivo de texto
def logBoard(array, _fd):
    _fd.write(str(array[0:3])+"\n")
    _fd.write(str(array[3:6])+"\n")
    _fd.write(str(array[6:9])+"\n")
#logBoard

#Función para determinar hijos y agregarlos a P
def expand(nodo):

    global colaP
    global colaQ
    global movimientos

    # Determinar posición de espacio vacío
    pos = nodo.getSpace()

    # Iterar sobre las posibles nuevas posiciones (diccionario)
    for x in movimientos[pos].keys():

        #clonar el tablero actual
        tableroHijo = nodo.getTablero().copy()

        #swap
        tableroHijo[pos], tableroHijo[x] = tableroHijo[x], tableroHijo[pos]

        # Generar nuevo nodo
        Hijo = Nodo(tableroHijo, nodo, movimientos[pos][x])

        # Determinar si nuevo nodo existe actualemente en P o en Q
        if not colaP.contains(Hijo) and not colaQ.contains(Hijo):
            colaP.enqueue(Hijo)
        #if
    #for
#expand

# Función principal
def aStar(raiz, terminal):

    global colaQ
    global colaP
    global init

    #abrir un archivo para loggear el juego
    _fd = open("puzzlelog.txt", "w")
    _fd.write("Explorando nodos...")

    # Primer elemento en cola
    colaP.enqueue(raiz)

    # Iterar hasta que P contenga el estado meta o quede vacía
    while not(colaP.isEmpty()) and not(colaP.contains(terminal)):

        # Remover elemento de cola P y mover a Q
        u = colaP.dequeue()
        colaQ.enqueue(u)

        # Generar hijos de nodo actual
        expand(u)

        logtxt = "\nNodos por explorar:  "+str(colaP.getSize())
        print(logtxt)
        _fd.write("\n"+logtxt)
        logtxt =   "Nodos ya explorados: "+str(colaQ.getSize())
        print(logtxt)
        _fd.write("\n"+logtxt)
    #while

    if colaP.isEmpty():
        logtxt = "\n\nNo hay solución, open set vacío...\n\n"
        print(logtxt)
        _fd.write("\n"+logtxt)
    else:

        #si se ha llegado hasta aquí, ¡la solución ya está en el open set!

        #guardar el camino del inicio a la meta
        _, goalindex = colaP.contains(terminal) #contains() devuelve True y el índice al encontrar un nodo
        nodePath     = colaP.getNode(goalindex)
        path         = []

        #recorrer camino desde la meta hacia el inicio
        while nodePath.getMov() is not None:

            #guardar estado del tablero en cada nodo
            path.append(nodePath.getTablero())

            #guardar valores de g(x), f(x) de cada nodo y el movimiento que lo produjo
            path.append( "\ng(x)="+str(nodePath.getGx())+" , f(x)="+str(nodePath.getFx())+" , mov: "+str(nodePath.getMov()) )

            #subir un nivel y repetir
            nodePath = nodePath.getParent()
        #while

        path.reverse()

        logtxt = "\n\nSTART!"
        print(logtxt)
        _fd.write(logtxt)

        logtxt = "\n\ng(x)="+str(raiz.getGx())+" , f(x)="+str(raiz.getFx())+" , mov: "+str(raiz.getMov())
        print(logtxt)
        _fd.write(logtxt+"\n")

        printBoard(raiz.getTablero())
        logBoard(raiz.getTablero(), _fd)

        for elem in path:
            if isinstance(elem, list):
                printBoard(elem)
                logBoard(elem, _fd)
            else:
                print(elem)
                _fd.write(elem+"\n")
            #if-else
        #for

        logtxt = "\nFINISH!\n"
        print(logtxt)
        _fd.write(logtxt)
    #if-else

    _fd.close()
#aStar

def main():

    global init
    global term
    global termEmpty
    global colaQ
    global colaP

    #Borrar el log del juego
    try:
        os.remove("./puzzlelog.txt")
    except:
        pass
    #try-except

    # determinar índice del espacio vacío ("_")
    termEmpty = "".join(term).find("_")

    # Instanciar Colas
    colaQ = ColaQ()
    colaP = BestFirst()

    goal = Nodo(term, None, None)
    root = Nodo(init, None, None)

    aStar(root, goal)
#main

if __name__=="__main__":
    main()
#if

#eof
