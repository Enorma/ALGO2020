import copy
import graphviz
from datetime import datetime

#-------------------------------------------------------------
#AUXILIARES

#lee el archivo de entrada
def readInput():

    try:

        inputfile = open("inputfile.txt", "r")
        lines = [line.rstrip("\n") for line in inputfile]
        inputfile.close()
    except:
        print("no encuentro el archivo...")
        return []
    #try-except

    L = []

    for i in range(len(lines)):
        L.append(lines[i].split())
    #for

    return L
#readInput

#devuelve un conjunto de todas las letras que hay en el archivo de input
def listLetters(L):

    letters = set()

    for i in range(len(L)):
        for j in range(len(L[i])):
            letters.add(L[i][j])
        #for
    #for

    return letters
#listLetters

#representa un conjunto como string
def printSet(s):

    if len(s)==0:
        return " "
    #if

    if len(s)==1:
        return list(s)[0]
    #if

    setstr = ""

    for i in s:
        setstr += i+","
    #for

    return setstr[:-1]
#printSet

#imprime una matriz de incidencia de un grafo
def printGraph(G):

    for i in G.keys():

        print(i+": [ ", end="")

        jkeys = list(G[i].keys())

        for j in range(len(jkeys)):

            if G[i][jkeys[j]]:
                print(jkeys[j]+":1 ", end="")
            else:
                print(jkeys[j]+":0 ", end="")
            #if-else

            if j<(len(jkeys)-1):
                print(", ", end="")
            else:
                print("] :"+i)
            #if
        #for
    #for
#printGraph

#imprime una matriz de incidencia de un autómata
def printAutomata(A):

    states = len(A.keys())
    length = 5+(4*states)+4

    header = "    | "

    for i in A.keys():
        header += str(i).zfill(2)+"| "
    #for

    print(header)
    print("-"*length)

    for i in A.keys():

        print(str(i).zfill(2)+": [", end="")

        for j in A[i].keys():

            if j==list(A[i].keys())[0]:
                print(" ", end="")
            #if

            print(printSet(A[i][j]), end="")

            if j<list(A[i].keys())[-1]:
                print(" | ", end="")
            else:
                print(" ] :"+str(i).zfill(2))
                #print("-"*length)
            #if
        #for
    #for

    print("-"*length)
    print(header)
#printAutomata

#-------------------------------------------------------------
#GRAFOS

#encuentra la relación BEF que representa cuál letra va antes de cuál
#también imprime BEF en pantalla
def findPrecedence(L):

    template = "({0},{1},\u03c3{2})"

    out   = []
    found = []

    for i in range(len(L)):

        slen = len(L[i])

        if i>0:
            out.append("*")
        #if

        if slen==0: #cadena vacía

            printable = template.format("-", "-", str(i+1))
            listable = (None, None, i+1)

            if (printable not in out) and (listable not in found):
                out.append(printable)
                found.append(listable)
            #if

            continue
        elif slen==1: #cadena de una letra

            #del inicio a la letra

            printable = template.format("-",     L[i][0], str(i+1))
            listable = (None,    L[i][0], i+1)

            if (printable not in out) and (listable not in found):
                out.append(printable)
                found.append(listable)
            #if

            #de la letra al final

            printable = template.format(L[i][0], "-",     str(i+1))
            listable = (L[i][0], None,    i+1)

            if (printable not in out) and (listable not in found):
                out.append(printable)
                found.append(listable)
            #if

            continue
        #if-elif

        for j in range(slen):

            if j==0: #primer loop

                printable = template.format("-", L[i][j], str(i+1))
                listable = (None, L[i][j], i+1)

                if (printable not in out) and (listable not in found):
                    out.append(printable)
                    found.append(listable)
                #if
            elif (j+1)==slen: #último loop

                #penúltima letra

                printable = template.format(L[i][j-1], L[i][j], str(i+1))
                listable = (L[i][j-1], L[i][j], i+1)

                if (printable not in out) and (listable not in found):
                    out.append(printable)
                    found.append(listable)
                #if

                #última letra

                printable = template.format(L[i][j],   "-",     str(i+1))
                listable = (L[i][j],   None,    i+1)

                if (printable not in out) and (listable not in found):
                    out.append(printable)
                    found.append(listable)
                #if
            else:

                printable = template.format(L[i][j-1], L[i][j], str(i+1))
                listable = (L[i][j-1], L[i][j], i+1)

                if (printable not in out) and (listable not in found):
                    out.append(printable)
                    found.append(listable)
                #if
            #if
        #for
    #for

    outstr = "BEF(\u03bb) = "+str(out)
    outstr = outstr.replace("'", "")
    outstr = outstr.replace("[", "{\n    ")
    outstr = outstr.replace("]", "\n}")
    outstr = outstr.replace("*, ", "\n    ")
    print(outstr)

    return found
#findPrecedence

#elimina vértices de ida y vuelta entre palabras distintas para obtener PO
def poGraph(prec):

    po_prec = set(copy.deepcopy(prec))

    preclen = len(prec)

    for i in range(preclen):

        if (i+1)==preclen:
            break
        #if

        if (prec[i][0] is None) or (prec[i][1] is None):
            continue
        #if

        for j in range(i+1, preclen):

            if (prec[j][0] is None) or (prec[j][1] is None):
                continue
            #if

            if prec[i][0]==prec[j][1] and prec[i][1]==prec[j][0] and prec[i][2]!=prec[j][2]:
                po_prec.discard(prec[i])
                po_prec.discard(prec[j])
            #if
        #for
    #for

    return list(po_prec)
#poGraph

#genera una matriz de incidencia que representa un grafo
#sirve para representar BEF o PO como grafo
def graphFromPrecedence(prec):

    letters = set()
    preclen = len(prec)

    for i in range(preclen):

        if prec[i][0] is not None:
            letters.add(prec[i][0])
        #if

        if prec[i][1] is not None:
            letters.add(prec[i][1])
        #if
    #for

    letterlist = list(letters)

    G_matrix = {}
    G_row    = {}

    for i in range(len(letterlist)):
        G_row[letterlist[i]] = False
    #for

    for i in range(len(letterlist)):
        G_matrix[letterlist[i]] = copy.deepcopy(G_row)
    #for

    for i in range(preclen):

        if (prec[i][0] is not None) and (prec[i][1] is not None):

            origin = prec[i][0]
            dest   = prec[i][1]

            G_matrix[origin][dest] = True
        #if
    #for

    return G_matrix
#graphFromPrecedence

#-------------------------------------------------------------
#AUTÓMATA NO DETERMINISTA

#ESTA ES LA FUNCIÓN MÁS IMPORTANTE!!!
#combina 2 estados de un autómata, es decir...
#desaparece los 2 estados originales y crea un estado nuevo
#el nuevo tendrá todas las transiciones entrantes y salientes de los viejos
#si alguno de los viejos es inicial/final, el nuevo también
#el nombre del nuevo será un número mayor al de cualquier otro estado
def mergeStates(A, s1, s2, starts, finals, total, tramas):

    if (s1 not in A.keys()) or (s2 not in A.keys()) or (s1 not in A[s1].keys()) or (s1 not in A[s2].keys()) or (s2 not in A[s1].keys()) or (s2 not in A[s2].keys()):
        return (None, None, None, None, None)
    #if

    entrantes = {}
    salientes = {}
    autolazos = set()
    initial   = False
    final     = False

    for i in A.keys():
        for j in A[i].keys():
            if len(A[i][j])>0:

                if (i==s1 or i==s2) and (j==s1 or j==s2): #autolazos

                    autolazos = autolazos.union(A[i][j])
                elif (i==s1 or i==s2): #transiciones salientes

                    if j not in salientes.keys():
                        salientes[j] = A[i][j]
                    else:
                        salientes[j] = salientes[j].union(A[i][j])
                    #if-else
                elif (j==s1 or j==s2): #transiciones entrantes

                    if j not in entrantes.keys():
                        entrantes[i] = A[i][j]
                    else:
                        entrantes[i] = entrantes[j].union(A[i][j])
                    #if-else
                #if-elif
            #if
        #for
    #for

    #print("\nEntrantes:", entrantes)
    #print("\nSalientes:", salientes)
    #print("\nAutolazos:", autolazos)

    #colocar el estado nuevo como estado inicial o final
    #si alguno de los 2 originales lo es
    #luego borrar los originales de ambos conjuntos

    if (s1 in starts) or (s2 in starts):
        starts.add(total)
    #if

    if (s1 in finals) or (s2 in finals):
        finals.add(total)
    #if

    starts.discard(s1)
    starts.discard(s2)
    finals.discard(s1)
    finals.discard(s2)

    #generar una nueva fila para el nuevo estado
    A[total] = {}

    #llenar la fila del nuevo estado
    for i in A.keys():

        if i==s1 or i==s2:
            A[total][i] = set()
            continue
        #if

        if i in salientes.keys():
            A[total][i] = salientes[i]
        else:
            A[total][i] = set()
        #if-else
    #for

    #generar y llenar una nueva columna para el nuevo estado
    for i in A.keys():

        if i==s1 or i==s2:
            continue
        #if

        if i==total:
            A[i][total] = autolazos
            continue
        #if

        if i in entrantes.keys():
            A[i][total] = entrantes[i]
        else:
            A[i][total] = set()
        #if-else
    #for

    #borrar los estados viejos
    del A[s1]
    del A[s2]

    for i in A.keys():
        del A[i][s1]
        del A[i][s2]
    #for

    if tramas is not None:

        #reemplazar los estados viejos en la trama, si estaban en ella
        for i in range(len(tramas)):
            if (s1 in tramas[i]) and (s2 in tramas[i]):

                set_trama_i = set(tramas[i])
                set_trama_i.discard(s1)
                set_trama_i.discard(s2)
                set_trama_i.add(total)
                tramas[i] = list(set_trama_i)
            #if
        #for
    #if

    return A, starts, finals, total+1, tramas
#mergeStates

#obtiene un autómata sencillo (un camino) por cada palabra
def disjointAutomata(L):

    total_words = len(L)

    if total_words==0:

        A_matrix     = {0:{0:set()}}
        start_states = {0}
        final_states = {0}
        total_states = 1
        tramas = []

        return A_matrix, start_states, final_states, total_states, tramas
    #if

    total_letters = sum(len(row) for row in L)
    total_states  = total_words + total_letters

    A_matrix = {}
    A_row    = {}

    for i in range(total_states):
        A_row[i] = set()
    #for

    for i in range(total_states):
        A_matrix[i] = copy.deepcopy(A_row)
    #for

    curr_state = 0

    start_states = set()
    final_states = set()
    tramas = []

    for i in range(total_words):

        tramas.append([])

        wordlen = len(L[i])

        if wordlen==0:
            start_states.add(curr_state)
            final_states.add(curr_state)
            curr_state += 1
            continue
        #if

        for j in range(wordlen):

            A_matrix[curr_state][curr_state+1] = set(L[i][j])

            if j>0 and (j)<wordlen:
                tramas[i].append(curr_state)
            #if

            if j==0:
                start_states.add(curr_state)
            #if

            curr_state += 1

            if (j+1)==wordlen:
                final_states.add(curr_state)
                curr_state += 1
            #if
        #for
    #for

    return A_matrix, start_states, final_states, total_states, tramas
#disjointAutomata

#combina los estados iniciales de un autómata (porque debe existir sólo uno)
def mergeInitials(A, starts, finals, total, tramas):

    while(len(starts)>1):
        initials = list(starts)
        A, starts, finals, total, tramas = mergeStates(A, initials[0], initials[1], starts, finals, total, tramas)
    #while

    return A, starts, finals, total, tramas
#mergeInitials

#encuentra grupos de estados finales con la misma letra entrante
#NO SE USA EN LA VERSIÓN FINAL!!!
def findFinals(A, starts, finals, total, tramas):

    letter_groups = {}

    for i in A.keys():
        for j in A[i].keys():

            if j in finals and len(A[i][j])>0:

                for letter in A[i][j]:

                    if letter not in letter_groups.keys():
                        letter_groups[letter] = set([j])
                    else:
                        letter_groups[letter].add(j)
                    #if-else
                #for
            #if
        #for
    #for

    return letter_groups
#findFinals

#combina los estados finales de un autómata (porque debe existir sólo uno)
def mergeFinals(A, starts, finals, total, tramas):

    #COMBINAR TODOS LOS FINALES

    while(len(finals)>1):
        finalstates = list(finals)
        A, starts, finals, total, tramas = mergeStates(A, finalstates[0], finalstates[1], starts, finals, total, tramas)
    #while

    '''
    #COMBINAR SÓLO FINALES CON MISMA LETRA

    groups = findFinals(A, starts, finals, total, tramas)

    for letter in groups.keys():

        while(len(groups[letter])>1):
            letterfinals = list(groups[letter])
            A, starts, finals, total, tramas = mergeStates(A, letterfinals[0], letterfinals[1], starts, finals, total, tramas)
            groups = findFinals(A, starts, finals, total, tramas)
        #while
    #for
    '''

    return A, starts, finals, total, tramas
#mergeFinals

#obtiene las letras en las transiciones entrantes de un nodo
def getEntrantes(A, node):

    entrantes = set()

    for i in A.keys():
        for j in A[i].keys():
            if j==node and len(A[i][j])>0:
                entrantes = entrantes.union(A[i][j])
            #if
        #for
    #for

    return entrantes
#getEntrantes

#determina si 2 estados son equivalentes y están en la misma trama
#es decir, que deberían combinarse
def areMergeable(A, tramas, s1, s2):

    for t in tramas:

        if (s1 in t) and (s2 in t):

            es1 = getEntrantes(A, s1)
            es2 = getEntrantes(A, s2)

            common = es1.intersection(es2)

            if len(common)>0:
                return True
            #if
        #if
    #for

    return False
#areMergeable

#encuentra todos los pares de estados que deberían combinarse
#SÓLO se usa en el autómata NO determinista trivial
def findMergeables(A, tramas):

    for i in range(len(tramas)):

        if len(tramas[i])<2:
            continue
        #if

        for j in range(len(tramas[i])):

            if (j+1)==len(tramas[i]):
                break
            #if

            for k in range(j+1, len(tramas[i])):

                s1 = tramas[i][j]
                s2 = tramas[i][k]

                if areMergeable(A, tramas, s1, s2):
                    return s1, s2
                #if
            #for
        #for
    #for

    return None, None
#findMergeables

#recorre el autómata trivial encontrando estados combinables
#y combinándolos (obtiene la forma final del autómata NO determinista)
def mergeTraversal(A, starts, finals, total, tramas):

    s1, s2 = findMergeables(A, tramas)

    while(s1!=None and s2!=None):

        #combinar
        A, starts, finals, total, tramas = mergeStates(A, s1, s2, starts, finals, total, tramas)

        #recalcular
        s1, s2 = findMergeables(A, tramas)
    #while

    return A, starts, finals, total, tramas
#mergeTraversal

#-------------------------------------------------------------
#AUTÓMATA DETERMINISTA

#encuentra estados con nodeterminismos
#o sea, transiciones desde el mismo estado, con la misma letra, a estados distintos
def findNonDeterminism(A):

    nds    = None
    chosen = None

    #buscar los nodeterminismos salientes de cada estado
    for i in A.keys():

        nds = {}

        for j in A[i].keys():

            if len(A[i][j])>0:

                for letter in A[i][j]:

                    if letter not in nds.keys():
                        nds[letter] = set([j])
                    else:
                        nds[letter].add(j)
                    #if-else
                #for
            #if
        #for

        #si alguna letra lleva a más de un estado, es un nodeterminismo
        for letter in nds.keys():
            if len(nds[letter])>1:
                chosen = (i, letter)
                break
            #if
        #for

        if chosen is not None:
            break
        #if
    #for

    if chosen is None:
        return []
    #if

    mergeables = []

    #encontrar los estados a los que llegamos con el nodeterminismo
    for j in A[chosen[0]].keys():
        if chosen[1] in A[chosen[0]][j]:
            mergeables.append(j)
        #if
    #for

    return mergeables
#findNonDeterminism

#mezcla los estados con nodeterminismos
#es decir, convierte al autómata en determinista
def NFAtoDFA(A, starts, finals, total):

    nodet = findNonDeterminism(A)

    while(len(nodet)>1):

        A, starts, finals, total, _ = mergeStates(A, nodet[0], nodet[1], starts, finals, total, None)
        nodet = findNonDeterminism(A)
    #while

    return A, starts, finals, total
#NFAtoDFA

#-------------------------------------------------------------
#AUTÓMATA COCIENTE (MÍNIMO)

#analiza los estados y los agrupa en base a hacia donde salen sus transiciones
#a partir de aquí tenemos un diccionario que guarda los grupos de estados
def populateStates(A, finals, letters):

    groups = {
        "A" : set(), #aceptación
        "C" : set(), #pozos
        "B" : set()  #todo lo demás
    }

    Q = {}

    for i in A.keys():

        if i in finals:
            groups["A"].add(i)
        else:
            groups["B"].add(i)
        #if-else

        Q[i] = {
            "group" : "A" if i in finals else "B",
            "final" : i in finals,
            "pozo"  : False if (i in finals) else None
        }

        for l in letters:
            Q[i][l+"_to_state"] = None
            Q[i][l+"_to_group"] = None
        #for

        for j in A[i].keys():

            if len(A[i][j])>0:

                for l in A[i][j]:
                    Q[i][l+"_to_state"] = j
                #for
            #if
        #for
    #for

    return Q, groups
#populateStates

#detecta los estados que sólo vayan hacia sí mismos (pozos)
#y los agrupa en el grupo de los pozos
def detectPozos(Q, groups):

    for i in Q.keys():

        if Q[i]["pozo"]==False:
            continue
        #if

        all_none = True
        all_loop = True

        for j in Q[i].keys():

            if not j.endswith("_to_state"):
                continue
            #if

            if (Q[i][j] is not None) and (Q[i][j]!=i):
                all_none = False
                all_loop = False
                break
            elif Q[i][j] is not None:
                all_none = False
            #if-elif
        #for

        if all_loop and not(all_none):

            Q[i]["group"] = "C"
            Q[i]["pozo"] = True

            groups["C"].add(i)
        #if
    #for

    return Q, groups
#detectPozos

#combina todos los pozos en uno solo
def mergePozos(Q, groups, A, starts, finals, total):

    if len(groups["C"])==0:
        return Q, groups, A, starts, finals, total
    #if

    while(len(groups["C"])>1):
        pozos = list(groups["C"])
        A, starts, finals, total, tramas = mergeStates(A, pozos[0], pozos[1], starts, finals, total, tramas)
        Q, groups = populateStates(A, finals, letters)
        Q, groups = detectPozos(Q, groups)
    #while

    return Q, groups, A, starts, finals, total
#mergePozos

#determina a cuál grupo de estados va cada estado
def populateGroups(Q):

    for i in Q.keys():

        if Q[i]["pozo"]:
            continue
        #if

        for j in Q[i].keys():

            if not j.endswith("_to_state"):
                continue
            #if

            if Q[i][j] is None:
                continue
            #if

            target_state = Q[i][j]
            target_group = Q[target_state]["group"]
            group_key    = j[:-9]+"_to_group"

            Q[i][group_key] = target_group
        #for
    #for

    return Q
#populateGroups

#determina si dos estados son equivalentes, es decir
#si con la misma letra van al mismo grupo de estados
#y ambos son de aceptación o no
def findEquivalence(Q, letters):

    txns    = {}
    equiv   = {}
    visited = set()

    for i in Q.keys():

        if Q[i]["pozo"] or Q[i]["final"]:
            continue
        #if

        abc     = list(letters)
        txns[i] = (None,)*len(letters)

        for j in range(len(letters)):
            temp = list(txns[i])
            temp[j] = Q[i][abc[j]+"_to_group"]
            txns[i] = tuple(temp)
        #for
    #for

    loops = len(txns.keys())
    singlestate = True

    for i in range(loops):

        i_key = list(txns.keys())[i]
        i_txns = txns[i_key]

        if i_key in visited:
            continue
        #if

        singlestate = True

        for j in range(i+1, loops):

            j_key = list(txns.keys())[j]
            j_txns = txns[j_key]

            if i_txns==j_txns:

                singlestate = False
                visited.add(j_key)

                if i_txns not in equiv.keys():
                    equiv[i_txns] = set()
                #if

                equiv[i_txns].add(i_key)
                equiv[i_txns].add(j_key)
            #if
        #for

        if singlestate:
            equiv[i_txns] = set()
            equiv[i_txns].add(i_key)
        #if
    #for

    return equiv
#findEquivalence

#recalcular los grupos de estados después de haber combinado algunos
def refineGroups(Q, equiv, count):

    #Grupos
    #A: estado final
    #C: pozo
    #B1, B2, B3... : grupos de otros estados

    keys = list(equiv.keys())

    for i in keys:
        equiv["B"+str(count)] = equiv.pop(i)
        count += 1
    #for

    for i in Q.keys():
        for j in equiv.keys():
            if i in equiv[j]:
                Q[i]["group"] = j
            #if
        #for
    #for

    Q = populateGroups(Q)

    return Q, equiv, count
#refineGroups

#llama repetidamente a las funciones anteriores para
#realizar el algoritmo del autómata cociente,
#obtiene una relación de grupos de estados equivalentes
def quotient(Q, groups, letters):

    count = 0

    while(True):

        #buscar grupos equivalentes de estados (ignora finales y pozos)
        equiv = findEquivalence(Q, letters)

        #reexpresar los grupos considerando las equivalencias
        Q, equiv, count = refineGroups(Q, equiv, count)

        #agregar estados finales y pozos
        equiv["A"] = groups["A"]
        equiv["C"] = groups["C"]

        if len(equiv)==len(groups):
            return equiv
        else:
            groups = copy.deepcopy(equiv)
        #if
    #while
#quotient

#combina los estados en cada grupo pues son equivalentes
def mergeQuotient(A, starts, finals, total, equiv):

    for i in equiv.keys():

        while(len(equiv[i])>1):

            i_list = list(equiv[i])

            equiv[i].discard(i_list[0])
            equiv[i].discard(i_list[1])
            equiv[i].add(total)

            A, starts, finals, total, _ = mergeStates(A, i_list[0], i_list[1], starts, finals, total, None)
        #while
    #for

    return A, starts, finals, total
#mergeQuotient

#inicializa en proceso del autómata cociente y
#finalmente devuelve el autómata mínimo
def quotientAnalysis(A, starts, finals, total, letters):

    #grupos de inicio:
    #A = estados de aceptación
    #C = pozos
    #B = todo lo demás

    #poblar transición por cada letra
    Q, groups = populateStates(A, finals, letters)

    #detectar pozos
    Q, groups = detectPozos(Q, groups)

    #combinar pozos
    Q, groups, A, starts, finals, total = mergePozos(Q, groups, A, starts, finals, total)

    #poblar transición por cada grupo
    Q = populateGroups(Q)

    #obtener estados del autómata cociente
    equiv = quotient(Q, groups, letters)

    #combinar estados del autómata cociente
    A, starts, finals, total = mergeQuotient(A, starts, finals, total, equiv)

    return A, starts, finals, total
#quotientAnalysis

#-------------------------------------------------------------
#GRAPHVIZ

#crea un objeto de graphviz que representa un grafo
def createGraph(Gname): #GRAPHVIZ

    return graphviz.Digraph(
        name=Gname,
        filename=Gname+"_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        engine="dot"
    )
#createGraph

#crea los vértices y arcos de un digrafo
def generateGraph(GVG, GD): #GRAPHVIZ

    #GVG = GraphViz Graph
    #GD  = Graph Dictionary

    #Vertices
    for i in GD.keys():

        GVG.node(
            i,
            fontsize="12.0",
            color="black",
            label=i,
            fixedsize="true",
            width="0.5"
        )
    #for

    #Edges
    for i in GD.keys():
        for j in GD[i].keys():
            if GD[i][j]:
                GVG.edge(
                    i,
                    j,
                    fontsize="10.0",
                    color="black"
                )
            #if
        #for
    #for

    return GVG
#generateGraph

#crea los estados y transiciones de un autómata
def generateAutomata(GVG, AD, starts, finals): #GRAPHVIZ

    #falta recibir como args las listas de estados iniciales y de aceptación

    #GVG = GraphViz Graph
    #AD  = Automata Dictionary

    GVG.node(
        "dummy",
        width="0.0",
        height="0.0",
        label=""
    )

    #States
    for i in AD.keys():

        #señalar con doble círculo si es estado de aceptación
        perif = "1"
        if i in finals:
            perif = "2"
        #if

        GVG.node(
            "q"+str(i),
            fontsize="12.0",
            color="black",
            label="q"+str(i),
            fixedsize="true",
            width="0.5",
            peripheries=perif
        )
    #for

    #Edges
    for i in AD.keys():

        #falta colocar una flecha que indique el estado inicial
        if i in starts:
            GVG.edge(
                "dummy",
                "q"+str(i),
                fontsize="10.0",
                color="black"
            )
        #if

        for j in AD[i].keys():
            if len(AD[i][j])>0:
                GVG.edge(
                    "q"+str(i),
                    "q"+str(j),
                    fontsize="10.0",
                    color="black",
                    label=printSet(AD[i][j])
                )
            #if
        #for
    #for

    return GVG
#generateAutomata

#imprime los grafos y autómatas en PDF
def display(OG, GPO, AFN, AFNstarts, AFNfinals, AFD, AFDstarts, AFDfinals): #GRAPHVIZ

    G1 = createGraph("Graphviz_Grafo_BEF")
    generateGraph(G1, OG)

    G2 = createGraph("Graphviz_Grafo_PO")
    generateGraph(G2, GPO)

    G3 = createGraph("Graphviz_Autómata_NFA")
    generateAutomata(G3, AFN, AFNstarts, AFNfinals)

    G4 = createGraph("Graphviz_Autómata_DFA_Mínimo")
    generateAutomata(G4, AFD, AFDstarts, AFDfinals)

    G1.view()
    G2.view()
    G3.view()
    G4.view()

    return
#display

#-------------------------------------------------------------
#PRINCIPAL

#llama a todo lo anterior y permite imprimir cada paso para debuggear
def main():

    total = 0 #cuantos estados del autómata hemos creado

    print("\n"+"|"*200+"\n")

    #leer el archivo de entrada
    L = readInput()
    print("\nInput:")
    print(L)

    #obtener conjunto de letras
    letters = listLetters(L)
    print("\nLetras:")
    print(letters)

    #obtener relación de precedencia (imprime el BEF)
    prec = findPrecedence(L)
    print("\nPrecedencia:")
    print(prec)

    #crear precedencia sin ida y vuelta en diferentes tramas
    po_prec = poGraph(prec)
    print("\nPrecedencia PO:")
    print(po_prec)

    #crear digrafo basado en la precedencia original (G)
    G = graphFromPrecedence(prec)
    print("\nGrafo:")
    printGraph(G)

    #crear digrafo basado en la precedencia sin ida y vuelta (PO)
    PG = graphFromPrecedence(po_prec)
    print("\nGrafo PO:")
    printGraph(PG)

    #crear autómata con caminos separados
    DA, starts, finals, total, tramas = disjointAutomata(L)
    if DA is None:

        print("\nNo es posible combinar estados.")
    else:
        print("\nAutómata Disjunto ("+str(len(DA.keys())), "estados):\n")
        printAutomata(DA)
        print("\nEstados iniciales:", starts)
        print("Estados finales:", finals)
        print("Siguiente estado:", total)
        print("Tramas:", tramas)
    #if-else

    #combinar estados iniciales
    DAI, starts, finals, total, tramas = mergeInitials(DA, starts, finals, total, tramas)
    if DAI is None:

        print("\nNo es posible combinar estados.")
    else:
        print("\nAutómata con 1 estado inicial ("+str(len(DAI.keys())), "estados):\n")
        printAutomata(DAI)
        print("\nEstados iniciales:", starts)
        print("Estados finales:", finals)
        print("Siguiente estado:", total)
        print("Tramas:", tramas)
    #if-else

    #combinar estados finales que se alcancen con la misma letra
    DAF, starts, finals, total, tramas = mergeFinals(DAI, starts, finals, total, tramas)
    if DAF is None:

        print("\nNo es posible combinar estados.")
    else:
        print("\nAutómata con estados finales combinados ("+str(len(DAF.keys())), "estados):\n")
        printAutomata(DAF)
        print("\nEstados iniciales:", starts)
        print("Estados finales:", finals)
        print("Siguiente estado:", total)
        print("Tramas:", tramas)
    #if-else

    #combinar estados equivalentes que estén en la misma trama (palabra)
    AM, starts, finals, total, tramas = mergeTraversal(DAF, starts, finals, total, tramas)
    if AM is None:

        print("\nNo es posible combinar estados.")
    else:
        print("\nAutómata no determinista final ("+str(len(AM.keys())), "estados):\n")
        printAutomata(AM)
        print("\nEstados iniciales:", starts)
        print("Estados finales:", finals)
        print("Siguiente estado:", total)
    #if-else

    #copiar el autómata hasta este punto para no perderlo
    AM_keep  = copy.deepcopy(AM)
    AMstarts = copy.deepcopy(starts)
    AMfinals = copy.deepcopy(finals)

    #convertir al autómata en determinista (combinar sus nodeterminismos)
    DFA, starts, finals, total = NFAtoDFA(AM, starts, finals, total)
    if DFA is None:

        print("\nNo es posible combinar estados.")
    else:
        print("\nAutómata determinista: ("+str(len(DFA.keys())), "estados):\n")
        printAutomata(DFA)
        print("\nEstados iniciales:", starts)
        print("Estados finales:", finals)
        print("Siguiente estado:", total)
    #if-else

    #convertir al autómata en mínimo (algoritmo del autómata cociente)
    QA, starts, finals, total = quotientAnalysis(DFA, starts, finals, total, letters)
    if QA is None:

        print("\nNo es posible combinar estados.")
    else:
        print("\nAutómata cociente: ("+str(len(QA.keys())), "estados):\n")
        printAutomata(QA)
        print("\nEstados iniciales:", starts)
        print("Estados finales:", finals)
        print("Siguiente estado:", total)
    #if-else

    #imprimir en graphviz
    display(G, PG, AM_keep, AMstarts, AMfinals, QA, starts, finals)

    return
#main

if __name__=="__main__":
    main()
#if

#eof
