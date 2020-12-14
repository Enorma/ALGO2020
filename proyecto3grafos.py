import re
import sys
import json
import graphviz
from datetime import datetime
from collections import deque

np       = None
nt       = None
m0       = None #tuple
pre      = None
post     = None
marcados = None
sources  = None
jsonstr  = None
count    = 0

def printMatrix(m):

    for i in range(0, len(m)):

        print("[", end="")

        for j in range(0, len(m[i])):
            print(" "+str(m[i][j])+" ", end="")
        #for

        print("]")
    #for
#printMatrix

def captureMatrix(kind):

    global nt
    global np
    global pre
    global post
    global m

    #print("\nCapturando matriz {0}\n".format(kind))

    ask = ""
    if kind=="pre":

        #(1,0,1,0,0)
        sinfuentespre = [
            [1,0,0,0,0],
            [0,1,0,0,0],
            [0,0,1,1,0],
            [0,0,0,1,0],
            [0,0,0,0,1]
        ]

        #(1,0,1,0,0)
        confuentespre = [
            [0,0,0,0,1],
            [0,1,0,1,0],
            [0,1,0,0,0],
            [0,1,0,0,0],
            [0,0,0,0,1]
        ]

        #(0,0,1,1,0)
        ranapre = [
            [1,0,0,0,0],
            [0,1,1,0,0],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0]
        ]

        #(0,1,1,0,0)
        carlos1pre = [
            [1,1,0,0,0],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,0,0,0,1],
            [0,0,0,0,1]
        ]

        #(0,2,2,0,0)
        carlos2pre = [
            [1,1,0,0,0],
            [0,0,0,1,0],
            [0,0,2,0,0],
            [0,0,0,0,1],
            [0,0,0,0,1]
        ]

        #(1, 0, 0, 0)
        alex1pre = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        #(1, 0, 1, 0)
        alex2pre = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]

        #(0, 1, 1, 0, 0)
        alex3pre = [
            [1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1]
        ]

        #(1,0,0,0,0)
        abelranapre = [
            [1,1,0,0,0],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,0,0,0,1],
            [0,0,0,0,1]
        ]

        pre = abelranapre

        ask = "Tokens entrantes a t{0} desde p{1}: "
    else:

        sinfuentespost = [
            [0,0,0,0,1],
            [1,0,0,0,0],
            [0,1,0,0,0],
            [0,0,1,0,0],
            [0,1,0,1,0]
        ]

        confuentespost = [
            [0,0,0,1,0],
            [0,0,0,0,1],
            [1,0,0,0,1],
            [0,0,1,0,0],
            [0,1,1,0,0]
        ]

        ranapost = [
            [0,0,1,0,1],
            [1,0,0,0,0],
            [0,1,0,0,0],
            [0,0,1,0,0],
            [0,1,0,1,0]
        ]

        carlos1post = [
            [0,0,0,0,1],
            [1,0,0,0,0],
            [0,1,0,0,0],
            [1,0,1,0,0],
            [0,1,0,1,0]
        ]

        carlos2post = [
            [0,0,0,0,1],
            [2,0,0,0,0],
            [0,1,0,0,0],
            [1,0,1,0,0],
            [0,1,0,1,0]
        ]

        alex1post = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 1, 0]
        ]

        alex2post = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

        alex3post = [
            [0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0 ,0],
            [1, 0, 1, 0 ,0],
            [0, 1, 0, 1, 0]
        ]

        abelranapost = [
            [0,0,0,0,1],
            [2,0,0,0,0],
            [0,1,0,0,0],
            [1,0,1,0,0],
            [0,1,0,1,0]
        ]

        post = abelranapost

        ask = "Tokens salientes de t{0} hacia p{1}: "
    #if-else

    return #para debuggear

    m = []
    for p in range(0, np):

        m.append([])
        for t in range(0, nt):

            n = int(input(ask.format(t,p)))
            m[p].append(n)
        #for
    #for

    if kind=="pre":
        pre = m
    else:
        post = m
    #if-else
#captureMatrix

def captureInit():

    global np
    global nt
    global m0
    global pre
    global post

    np = int(input("¿Cuántos lugares tiene la red? "))
    nt = int(input("¿Cuántas transiciones tiene la red? "))
    m0 = input("Escribe el marcado inicial separado por comas: ")

    print("El marcado inicial es: [", m0, "]")

    m0 = m0.replace(" ","")
    m0 = m0.split(",")
    m0 = list(map(lambda x: int(x), m0))

    captureMatrix("pre")
    captureMatrix("post")

    print("\nPre:")
    printMatrix(pre)
    print("\nPost:")
    printMatrix(post)
    print()
#captureInit

def makeDict():

    global marcados
    global m0
    global nt

    m0 = tuple(m0)

    marcados = {
        m0 : {
            "type"           : "frontera",
            "originalParent" : {},
            "parents"        : {},
            "children"       : {},
            "pre_t"          : [None]*nt,
            "post_t"         : [None]*nt
        }
    }
#makeDict

def findSources():

    global sources
    sources = []

    for t in range(0, nt):
        if isSource(t):
            sources.append(t)
        #if
    #for
#findSources

def isSource(t):

    for p in range(0, np):
        if pre[p][t]>0:
            return False
        #if
    #for

    return True
#isSource

def calcOmega(parentmark, childmark):

    global marcados

    dad = list(parentmark)
    son = list(childmark)

    isOmega = None

    while(True):

        isOmega = True
        for i in range(np):

            if son[i]!="w" and dad[i]!="w" and son[i]<dad[i]:
                isOmega = False
                break
            #if-elif
        #for

        if isOmega:

            for i in range(np):
                if son[i]=="w" or dad[i]=="w" or son[i]>dad[i]:
                    son[i] = "w"
                #if
            #for

            return tuple(son)
        elif len(marcados[tuple(dad)]["originalParent"].keys())==0:
            return tuple(son)
        else:
            dad = list(marcados[tuple(dad)]["originalParent"]["mark"])
        #if
    #while
#calcOmega

def getKey(val):

    global marcados

    for key, value in marcados.items():
        if val==value:
            return key
        #if
    #for

    return None
#getKey

def getChildren(mark):

    global marcados
    global sources

    if marcados[mark]["type"]!="frontera":
        return
    #if-elif

    isTerminal = True
    enabled    = None
    newmark    = None

    for t in range(nt):

        enabled = True

        newmark = list(mark)

        if t in sources:

            #si t es una fuente, t siempre está habilitada

            for p in range(np):
                if newmark[p]=="w":
                    isTerminal = False
                elif post[p][t]>0:
                    newmark[p] += post[p][t]
                    isTerminal = False
                #if-elif
            #for
        else:

            for p in range(np):
                if (mark[p]!="w") and (pre[p][t] > mark[p]):
                    enabled = False
                    break
                #if
            #for

            #si t no está habilitada, checar la siguiente t
            if not(enabled):
                continue
            #if

            #si llegué aquí, t está habilitada desde el marcado actual
            isTerminal = False

            for p in range(np):
                if newmark[p]!="w":
                    newmark[p] -= pre[p][t]
                    newmark[p] += post[p][t]
                #if
            #for
        #if-else

        if not(isTerminal):

            #calcOmega devuelve newmark ya convertido en tupla
            newmark = calcOmega(mark, newmark)

            if newmark in marcados.keys():

                mtype = "duplicado"

                if mark in marcados[newmark]["parents"].keys():
                    if t not in marcados[newmark]["parents"][mark]:
                        marcados[newmark]["parents"][mark].append(t)
                    #if
                else:
                    marcados[newmark]["parents"][mark] = [t]
                #if
            else:

                mtype = "original"

                marcados[newmark] = {
                    "type"           : "frontera",
                    "originalParent" : {"mark":mark, "pre_t":t},
                    "parents"        : {mark : [t]},
                    "children"       : {},
                    "pre_t"          : [None]*nt,
                    "post_t"         : [None]*nt
                }
            #if-else

            marcados[newmark]["pre_t"][t] = mark

            if newmark in marcados[mark]["children"].keys():
                if t not in marcados[mark]["children"][newmark]["post_t"]:
                    marcados[mark]["children"][newmark]["post_t"].append(t)
                #if
            else:
                marcados[mark]["children"][newmark] = {
                    "post_t" : [t],
                    "type"   : mtype
                }
            #if-else

            marcados[mark]["post_t"][t] = newmark
        #if
    #for

    if isTerminal:
        marcados[mark]["type"] = "terminal"
    else:
        marcados[mark]["type"] = "expandido"
    #if-else

    return
#getChildren

#explora todos los marcados posibles de la red (búsqueda por anchura)
def bfs():

    global pre
    global post
    global marcados
    global m0

    #para guardar los marcados explorados
    closed = deque([])
    #para guardar los marcados por explorar
    openset = deque([marcados[m0]])
 
    #seguir buscando hasta que no hayan más marcados por explorar
    while openset:

        #exploraremos el marcado más viejo de openset
        mark = openset.popleft()

        #si no hemos explorado este marcado
        if mark["type"]=="frontera":

            #meter el marcado en la cola de explorados
            closed.append(mark)

            #identificar a los marcados hijos de openset
            #aquí mark debe ser una simple tupla
            marktuple = tuple(getKey(mark))
            getChildren(marktuple)
            #sys.exit(0) #para debuggear
 
            #meter a los marcados hijos a openset
            children = marcados[marktuple]["children"]

            for m in children.keys():
                if children[m]["type"]=="original":
                    openset.append(marcados[m])
                #if
            #for
        #if
    #while

    #print("marcados final:", marcados) #para debuggear

    return closed
#bfs

def createGraph(Gname):

    return graphviz.Digraph(
        name=Gname,
        filename=Gname+"_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        engine="dot"
    )
#createGraph

def generatePetriNet(G):

    global marcados
    global pre
    global post
    global m0
    global np
    global nt

    #Places
    for x in range(np):

        if(m0[x]!=0):
            labelstr = "P"+str(x)+"\n"+str(m0[x])
        else:
            labelstr = "P"+str(x)+"\n\n"
        #if-else

        G.node(
            "P"+str(x),
            color="black",
            fontsize="12.0",
            label=labelstr,
            fixedsize="true",
            width="0.5"
        )
    #for

    #Transitions
    for x in range(nt):
        G.node(
            "T"+str(x),
            color="black",
            shape="rect",
            fontsize="11.0",
            fixedsize="true",
            width="0.5",
            height="0.15",
            label="T"+str(x),
            fontcolor="white",
            style="filled",
            fillcolor="black"
        )
    #for

    #Edges
    for i in range(np):
        for j in range(nt):
            if(pre[i][j]!=0):
                G.edge("P"+str(i), "T"+str(j), label=str(pre[i][j]), fontsize="10.0", color="red")
            #if
            if(post[i][j]!=0):
                G.edge("T"+str(j), "P"+str(i), label=str(post[i][j]), fontsize="10.0", color="blue")
            #if
        #for
    #for

    return G
#generatePetriNet

def expandTreeNode(G, mark):

    global marcados
    global count

    #Anotaciones

    status = ""
    if marcados[mark]["type"]=="terminal":
        status = "\nTerminal"
    #if-else

    isroot = ""
    if len(marcados[mark]["originalParent"].keys())==0:
        isroot = "RAÍZ\n"
    #if

    #Vértice de marcado

    G.node(
        "expTree"+str(mark),
        shape="plaintext",
        fontsize="14.0",
        label=isroot+str(mark)+status
    )

    #Arista desde su padre

    if len(marcados[mark]["originalParent"].keys())>0:
        G.edge(
            "expTree"+str(marcados[mark]["originalParent"]["mark"]),
            "expTree"+str(mark),
            fontsize="12.0",
            label="t"+str(marcados[mark]["originalParent"]["pre_t"])
        )
    #if

    #Hijos

    for child in marcados[mark]["children"].keys():
        if marcados[mark]["children"][child]["type"]=="duplicado":

            #Crear vértice del hijo
            G.node(
                "expTree"+str(child)+str(count),
                shape="plaintext",
                fontsize="14.0",
                label=str(child)+"\nDuplicado"
            )

            #Arista hacia el hijo
            G.edge(
                "expTree"+str(mark),
                "expTree"+str(child)+str(count),
                fontsize="12.0",
                label="t"+str(marcados[mark]["children"][child]["post_t"])
            )

            count += 1
        else:
            expandTreeNode(G, child)
        #if-else
    #for

    return
#expandTreeNode

def generateExpansionTree(G):

    global marcados
    global count
    count = 0
    expandTreeNode( G, list(marcados.keys())[0] )
    return
#generateExpansionTree

def expandGraphNode(G, mark):

    global marcados

    #Anotaciones

    status = ""
    if marcados[mark]["type"]=="terminal":
        status = "\nTerminal"
    #if-else

    isroot = ""
    if len(marcados[mark]["originalParent"].keys())==0:
        isroot = "RAÍZ\n"
    #if

    G.node(
        "covGraph"+str(mark),
        shape="plaintext",
        fontsize="14.0",
        label=isroot+str(mark)+status
    )

    #Arista desde su padre

    if len(marcados[mark]["originalParent"].keys())>0:
        G.edge(
            "covGraph"+str(marcados[mark]["originalParent"]["mark"]),
            "covGraph"+str(mark),
            fontsize="12.0",
            label="t"+str(marcados[mark]["originalParent"]["pre_t"])
        )
    #if

    #Hijos

    for child in marcados[mark]["children"].keys():
        if marcados[mark]["children"][child]["type"]=="duplicado":

            #Arista hacia el original
            G.edge(
                "covGraph"+str(mark),
                "covGraph"+str(child),
                fontsize="12.0",
                label="t"+str(marcados[mark]["children"][child]["post_t"])
            )
        else:
            expandGraphNode(G, child)
        #if-else
    #for

    return
#expandGraphNode

def generateCoverGraph(G):

    global marcados
    expandGraphNode( G, list(marcados.keys())[0] )
    return
#generateCoverGraph

def exportToJSON():

    global marcados
    global jsonstr

    export = {}

    for mark in marcados.keys():

        export[str(mark)] = {}

        export[str(mark)]["type"] = marcados[mark]["type"]

        if len(marcados[mark]["originalParent"].keys())==0:
            export[str(mark)]["originalParent"] = {}
        else:
            export[str(mark)]["originalParent"] = {
                "mark"  : str(marcados[mark]["originalParent"]["mark"]),
                "pre_t" : marcados[mark]["originalParent"]["pre_t"]
            }
        #if-else

        if len(marcados[mark]["parents"].keys())==0:
            export[str(mark)]["parents"] = {}
        else:
            parents = {}
            for pm,pt in marcados[mark]["parents"].items():
                parents[str(pm)] = pt
            #for
            export[str(mark)]["parents"] = parents
        #if-else

        children = {}
        for c in marcados[mark]["children"].keys():
            children[str(c)] = {
                "post_t" : marcados[mark]["children"][c]["post_t"],
                "type"   : marcados[mark]["children"][c]["type"]
            }
        #for
        export[str(mark)]["children"] = children

        export[str(mark)]["pre_t"]  = [None]*nt
        export[str(mark)]["post_t"] = [None]*nt

        for t in range(nt):

            if isinstance(marcados[mark]["pre_t"][t], tuple):
                export[str(mark)]["pre_t"][t] = str(marcados[mark]["pre_t"][t])
            #if

            if isinstance(marcados[mark]["post_t"][t], tuple):
                export[str(mark)]["post_t"][t] = str(marcados[mark]["post_t"][t])
            #if
        #for
    #for

    jsonstr = json.dumps(export, indent=4, separators=(',', ': '))

    with open("marcados.json", "w") as jsonfile:
        json.dump(export, jsonfile, indent=4, separators=(',', ': '))
    #with

    print("marcados:", jsonstr)
#exportToJSON

def display():

    global pre
    global post
    global m0
    global np
    global nt

    G1 = createGraph("Red_de_Petri")
    generatePetriNet(G1)

    G2 = createGraph("Árbol_de_Expansión")
    generateExpansionTree(G2)

    G3 = createGraph("Grafo_de_Cobertura")
    generateCoverGraph(G3)

    G1.view()
    G2.view()
    G3.view()
#display

def main():
    captureInit()
    findSources()
    makeDict()
    bfs()
    exportToJSON()
    display()
#main

if __name__=="__main__":
    main()
#main

#eof
