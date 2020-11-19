import React, {useState, useEffect} from 'react';
import './App.css';

//------------------------------
//CONSTANTES GLOBALES

const SIZELIMIT = 10;
const EDGELIMIT = 99;
const MAXSTEPS  = 2000;
const MAXPATHS  = 50;

//------------------------------
//CONSTANTES PARA FASES

const INITIALIZE = -1;
const STEP0      =  0;
const STEP1      =  1;
const STEP2      =  2;
const STEP3      =  3;
const STEPF      =  4;

//------------------------------
//VARIABLES GLOBALES

//variables de control de fase
let next       = INITIALIZE; //variable que indica en qué fase estamos
let count      = 0;          //contador de componentes para sus keys
let paths      = 0;          //contador de caminos m-aumentantes calculados

//historiales
let errtrack   = 0;          //contador de intentos desde el paso 0
let history1   = {};         //para guardar los valores de la vuelta anterior
let history2   = {};         //para guardar los valores de la vuelta actual

//valores numéricos
let alfa       = null;       //número que representa el factor alfaL

//vértices sueltos
let freevertex = null;       //número que representa un vértice no saturado
let yvert      = null;       //número que representa el vértice Y vecino de S
let zvert      = null;       //número que representa el vértice Z saturado con Y

//arreglos de aristas
let optimals   = [];         //arreglo de aristas del matching óptimo

//arreglos de pesos de aristas
let labelx     = [];         //arreglo de pesos óptimos de aristas de cada fila
let labely     = [];         //arreglo de pesos óptimos de aristas de cada columna

//conjuntos de aristas
let gl         = new Set();  //conjunto de aristas del subgrafo de igualdad
let matching   = new Set();  //conjunto de aristas del matching sobre GL
let newedges   = new Set();  //conjunto de aristas nuevos en el camino m-aumentante

//conjuntos de vértices
let vertxset   = new Set();  //conjunto de vértices de un lado de la bipartición
let vertyset   = new Set();  //conjunto de vértices del otro lado de la bipartición
let neighbors  = new Set();  //conjunto de vértices vecinos de S
let sset       = new Set();  //subconjunto de vértices del grafo (disjunto de T)
let tset       = new Set();  //subconjunto de vértices del grafo (disjunto de S)

//------------------------------
//COSAS HARDCODEADAS PARA TESTEAR

const gl0 = new Set([[4,4],[1,2],[4,0],[3,4],[0,0],[1,4],[3,0],[2,2]]); //16 max, 20 pasos, 3 paths
const ejemplo0 = [ //max 16
    [ 5,  0,  0,  1,  2],
    [ 0,  0,  3,  1,  3],
    [ 1,  1,  5,  0,  3],
    [ 4,  1,  0,  1,  4],
    [ 4,  1,  3,  1,  4]
];

const gl1 = new Set([[0,1],[4,4],[2,1],[4,3],[3,1],[1,1],[1,4],[0,2],[2,2],[1,0],[3,2],[1,3]]); //14 max, 8 pasos, 1 path
const ejemplo1 = [ //max 14
    [ 3,  5,  5,  4,  1],
    [ 2,  2,  0,  2,  2],
    [ 2,  4,  4,  1,  0],
    [ 0,  1,  1,  0,  0],
    [ 1,  2,  1,  3,  3]
];

const gl3 = new Set([[4,4],[2,4],[0,4],[2,0],[1,4],[0,2],[3,2]]); //16 max, 30 pasos, 5 paths
const ejemplo3 = [ //max 16
    [ 0,  0,  4,  1,  4],
    [ 4,  1,  2,  0,  5],
    [ 5,  1,  2,  0,  5],
    [ 0,  0,  3,  1,  2],
    [ 0,  0,  0,  1,  5]
];

const gl4 = new Set([[2,4],[4,0],[3,4],[0,0],[2,0],[1,4],[3,2]]); //15 max, 23 pasos, 4 paths
const ejemplo4 = [ //max 15
    [ 4,  1,  3,  0,  3],
    [ 2,  1,  1,  1,  4],
    [ 4,  1,  1,  0,  4],
    [ 3,  1,  4,  1,  4],
    [ 5,  1,  4,  1,  3]
];

const gl5 = new Set([[0,4],[4,3],[2,3],[3,3],[1,0]]); //80 max, 36 pasos, 5 paths
const ejemplo5 = [ //max 80
    [ 4,  1, 14,  0, 18],
    [20, 15,  5, 18, 13],
    [ 1,  7, 15, 20, 14],
    [ 6,  4, 17, 18,  5],
    [ 9,  0,  2, 18,  0]
];

//---

const gl2 = new Set([[4,4],[1,2],[3,4],[0,0],[2,2],[1,0]]); //15 (fail)
const ejemplo2 = [ //max 15
    [ 2,  1,  0,  1,  1],
    [ 5,  0,  5,  0,  3],
    [ 1,  0,  3,  0,  0],
    [ 0,  0,  0,  0,  5],
    [ 1,  0,  2,  1,  3]
];

const gl7 = new Set([[4,4],[1,2],[0,3],[3,3],[2,2]]); //377 max (fail)
const ejemplo7 = [ //max 377
    [63, 25, 48, 95, 23],
    [46, 32, 78, 61, 42],
    [12, 65, 98, 43, 67],
    [25, 36, 42, 85, 76],
    [61, 42, 13, 52, 86]
];

const gl6 = new Set([[4,0],[0,0],[0,3],[2,0],[4,2],[3,0],[1,3]]); //62 max (fail)
const ejemplo6 = [ //max 62
    [ 7,  1,  1,  7,  2],
    [14, 11, 12, 16,  9],
    [19,  5, 12,  5, 12],
    [16,  4,  5,  7, 13],
    [12,  8, 12,  3,  5]
];

//---

const ejemploA = [ //4x4
    [ 0, 1, 3, 0],
    [ 1, 1, 1, 0],
    [ 3, 0, 3, 0],
    [ 0, 0, 0, 0],
];

const ejemplo = ejemplo5;
const glejemplo = gl7;

//------------------------------
//OPERACIONES CON CONJUNTOS

//no son arrows para que this sea el Set que las llama
Set.prototype.isSubSet = function(otherSet) {

    if(this.size > otherSet.size) {
        return false;
    }else {
        for(let elem of this) {
            if(!otherSet.has(elem)) {
                return false;
            }
        }
        return true;
    }
};

Set.prototype.equals = function(otherSet) {

    if(this.isSubSet(otherSet) && otherSet.isSubSet(this)) {
        return true;
    }else {
        return false;
    }
};

Set.prototype.hasEdge = function(x, y) {

    for(let e of this) {
        if(e[0]===x && e[1]===y) {
            return true;
        }
    }

    return false;
};

Set.prototype.symDiff = function(otherSet) {

    let newset = new Set();

    for(let e of this) {
        if(!otherSet.hasEdge(e[0], e[1])) {
            newset.add(e);
        }
    }

    for(let e of otherSet) {
        if(!this.hasEdge(e[0], e[1])) {
            newset.add(e);
        }
    }

    return newset;
};

Array.prototype.shuffle = function() {

    for(let i = this.length-1; i>0; i--) {
        const j = Math.floor(Math.random() * (i+1));
        [ this[i],this[j] ] = [ this[j],this[i] ];
    }

    return this;
};

Set.prototype.shuffle = function() {

    const buff = Array.from(this);
    this.clear();
    buff.shuffle();

    while(buff.length) {
        this.add(buff.pop());
    }
};

Set.prototype.strEdgeSet = function() {

    let str = "{";
    this.forEach(a => {str += `(${a[0]},${a[1]}),`});
    str += "}";
    return str;
};

Set.prototype.strVertSet = function() {

    let str = "{";
    this.forEach(v => {str += `${v},`});
    str += "}";
    return str;
};

//------------------------------
//CLASES

class Vertice {

    constructor(side, num, padre, peso) {
        this.side  = side;
        this.num   = num;
        this.padre = padre;
        this.peso  = peso;

        this.toString = function() {
            return(`vértice: ${this.side}${this.num}, padre: ${this.padre}, peso: ${this.peso}`);
        }

        this.equals = function(otrovert) {
            if(this.side===otrovert.side && this.num===otrovert.num) {
                return true;
            }else {
                return false;
            }
        }

        this.history = function() {
            let p = this.padre;
            let h = `${this.side}${this.num}, `;
            while(p!==null) {
                h += `${p.side}${p.num}, `;
                p = p.padre;
            }
            return h;
        }
    }
}

//------------------------------
//FUNCIONES AUXILIARES

//returns a random integer from 0 to limit (both inclusive)
const getRand = max => Math.floor(Math.random()*(max+1));

const makeMatrix = (size, limit) => {

    const matrix = [];
    let vector   = [];

    size = Number(size);
    for(let i=0; i<size; i++) {
        vector = vector.slice(99);
        for(let j=0; j<size; j++) {
            vector.push(size===5 ? ejemplo[i][j] : getRand(limit));
            //vector.push(getRand(limit));
        }
        matrix.push(vector);
    }

    return [...matrix];
};

const matrixDeepCopy = matrix => {

    const newmatrix = [];

    for(let i=0; i<matrix.length; i++) {
        newmatrix.push([]);
        newmatrix[i] = [...matrix[i]];
    }

    //console.log(newmatrix); //descomentar para debuggear

    return [...newmatrix];
};

const totalWeight = (edgeset, matrix) => {

    let acc = 0;
    edgeset.forEach(a => {
        acc += matrix[a[0]][a[1]];
    });

    return acc;
};

//-----------------------------------------------------------
//CONTROL PARA REINTENTAR

const compareHistory = () => {

    for(let k of Object.keys(history1)) {
        if(history1[k]!==history2[k]) {
            return false;
        }
    }

    for(let k of Object.keys(history2)) {
        if(history2[k]!==history1[k]) {
            return false;
        }
    }

    return true;
};

const getHistory = () => {

    const hist = {

        "alfa"       : alfa===0       ? 0 : alfa       ? alfa.toString()       : "null",
        "freevertex" : freevertex===0 ? 0 : freevertex ? freevertex.toString() : "null",
        "yvert"      : yvert===0      ? 0 : yvert      ? yvert.toString()      : "null",
        "zvert"      : zvert===0      ? 0 : zvert      ? zvert.toString()      : "null",

        "labelx"     : labelx    ? labelx.toString()      : "null",
        "labely"     : labely    ? labely.toString()      : "null",

        "gl"         : gl        ? gl.strEdgeSet()        : "null",
        "matching"   : matching  ? matching.strEdgeSet()  : "null",
        "newedges"   : newedges  ? newedges.strEdgeSet()  : "null",

        "vertxset"   : vertxset  ? vertxset.strVertSet()  : "null",
        "vertyset"   : vertyset  ? vertyset.strVertSet()  : "null",
        "neighbors"  : neighbors ? neighbors.strVertSet() : "null",
        "sset"       : sset      ? sset.strVertSet()      : "null",
        "tset"       : tset      ? tset.strVertSet()      : "null",
    };

    return hist;
};

//------------------------------
//MICRO COMPONENTES AUXILIARES

const RenderWeightArray = ({name, weightarr}) => {
    return(
        <React.Fragment>
            <br />
            <span className="resultline">
                {`${name}: { ${weightarr} }`}
            </span>
        </React.Fragment>
    );
};

const RenderVertSet = ({vertset}) => {

    let arr = Array.from(vertset.values());

    return(
        <React.Fragment>
            <br />
            <span className="resultline">
                {"{ "+arr.toString()+" }"}
            </span>
        </React.Fragment>
    );
};

const RenderEdgeSet = ({edgeset}) => {

    let arr = Array.from(edgeset.values());

    return(
        <React.Fragment>
            <br />
            <span className="resultline">
                {"{"+arr.map(a => ` (${a})`)+" }"}
            </span>
        </React.Fragment>
    );
};

//------------------------------
//COMPONENTES INTERACTIVOS

const SizeInput = ({
    limit=SIZELIMIT,
    onChange,
    }) => {

    const [val, setVal] = useState(2);

    const handleInputChange = (event) => {
        setVal(event.target.value);
        onChange(event.target.value);
    };

    return(
        <p>
            <label htmlFor="sizepickerinternal">Elegir tamaño de matriz:&#9;</label>
            <input
                type="number"
                id="sizepickerinternal"
                min="2"
                max={limit.toString()}
                value={val}
                className="numinput"
                onChange={handleInputChange}
            />
        </p>
    );
};

const NumInput = ({
    cell,
    limit=EDGELIMIT,
    //value=getRand(limit),
    value=0,
    onChange,
    css="numinput"
    }) => {

    const [val, setVal] = useState(value);
    if(val!==value) {
        setVal(value);
    }

    return(
        <input
            type="number"
            id={cell}
            min="0"
            max={limit.toString()}
            value={val}
            className={css}
            onChange={onChange}
        />
    );
};

const InputMatrix = ({
    content=[],
    limit=EDGELIMIT,
    optimals,
    onChange,
    }) => {

    let css;
    const data = [...content];

    const table = [];
    for(let i=0; i<data.length; i++) {
        table.push([]);
        for(let j=0; j<data.length; j++) {
            css = optimals.find(x => x[0]===i && x[1]===j) ? "boldinput" : "numinput";
            table[i] = [...table[i], <NumInput key={`${i},${j}`} cell={`${i},${j}`} limit={limit} value={data[i][j]} css={css} onChange={onChange} />];
        }
    }

    const rowcolbreaks = {
        "gridTemplateRows"    : `repeat(${data.length}, 1.5em)`,
        "gridTemplateColumns" : `repeat(${data.length}, 2.2em)`,
    };

    const grid = <div className="matrixContainer" style={rowcolbreaks}>{table}</div>;

    return grid;
};

//------------------------------
//COMPONENTES INFORMATIVOS

//pasos anteriores al loop principal del algoritmo
const StepZero = ({
    labelx,   //labels de las filas:                   <array of weights: array of NUMBER or empty array>
    labely,   //labels de las columnas:                <array of weights: array of NUMBER or empty array>
    gl,       //Aristas del subgrafo de igualdad:      <set of edges: set of (NUMBER,NUMBER) or empty set>
    matching, //Matching arbitrario:                   <set of edges: set of (NUMBER,NUMBER) or empty set>
    vertxset, //conjunto de vértices x en el matching: <set of vert: set of NUMBER | empty set>
    vertyset, //conjunto de vértices y en el matching: <set of vert: set of NUMBER | empty set>
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                =============== PASO 0 ===============
            </p>
            <p>
                Etiquetado inicial:
                <RenderWeightArray name={"filas"} weightarr={labelx} />
                <RenderWeightArray name={"columnas"} weightarr={labely} />
            </p>
            <p>
                Aristas del subgrafo de igualdad Gl:
                <RenderEdgeSet edgeset={gl} />
            </p>
            <p>
                Matching arbitrario:
                <RenderEdgeSet edgeset={matching} />
            </p>
            <p>
                Vértices X en el matching:
                <RenderVertSet vertset={vertxset} />
            </p>
            <p>
                Vértices Y en el matching:
                <RenderVertSet vertset={vertyset} />
            </p>
        </React.Fragment>
    );
};

//resultados del paso 1 cuando no hemos terminado
const StepOneNonFinal = ({
    freevertex, //Vértice de X insaturado: <vert: NUMBER or NONE>
    sset,       //conjunto de vértices S:  <set of vert: set of NUMBER or empty set>
    tset,       //conjunto de vértices T:  <set of vert: set of NUMBER or empty set>
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                =============== PASO 1 ===============
            </p>
            <p>
                Vértice en X no saturado en el matching:<br />
                <span className="resultline">{freevertex}</span>
            </p>
            <p>
                Conjunto de Vértices S:
                <RenderVertSet vertset={sset} />
            </p>
            <p>
                Conjunto de Vértices T:
                <RenderVertSet vertset={tset} />
            </p>
        </React.Fragment>
    );
};

//resultados al finalizar el algoritmo
const StepOneFinal = ({
    matching, //Matching Óptimo: <set of edges: set of (NUMBER,NUMBER) or empty set>
    matrix,   //la matriz:       <2D array of weights: 2D array of NUMBER>
    steps,
    paths,
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                ============== FINISH!! ==============
            </p>
            <p>
                Matching Óptimo:
                <RenderEdgeSet edgeset={matching} />
            </p>
            <p>
                Peso Óptimo:<br />
                <span className="resultline">{totalWeight(matching, matrix)}</span>
            </p>
            <p>
                <span className="resultline">
                    {`Se calcularon ${steps} pasos y ${paths} caminos m-aumentantes.`}
                </span>
            </p>
        </React.Fragment>
    );
};

//resultados del paso 2, cuando T=NS
const StepTwoA = ({
    neighbors, //Vértices vecinos de S:            <set of vert: set of NUMBER or empty set>
    alfa,      //valor de alfa L:                  <NUMBER>
    labelx,    //labels de las filas:              <array of weights: array of NUMBER or empty array>
    labely,    //labels de las columnas:           <array of weights: array of NUMBER or empty array>
    gl,        //Aristas del subgrafo de igualdad: <set of edges: set of (NUMBER,NUMBER) or empty set>
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                =============== PASO 2A ===============
            </p>
            <p>
                Conjunto T y Vértices vecinos del conjunto S:
                <RenderVertSet vertset={neighbors} />
            </p>
            <p>
                <span className="resultline">
                    {"El conjunto T es igual al conjunto de vecinos de S"}
                </span>
            </p>
            <p>
                Valor de &#x0251;l:<br />
                <span className="resultline">{alfa}</span>
            </p>
            <p>
                Re-etiquetados:
                <RenderWeightArray name={"filas"} weightarr={labelx} />
                <RenderWeightArray name={"columnas"} weightarr={labely} />
            </p>
            <p>
                Aristas del subgrafo de igualdad Gl:
                <RenderEdgeSet edgeset={gl} />
            </p>
        </React.Fragment>
    );
};

//resultados del paso 2, cuando T<NS
const StepTwoB = ({
    neighbors, //Vértices vecinos de S: <set of vert: set of NUMBER or empty set>
    tset,      //conjunto de vértices T: <set of vert: set of NUMBER or empty set>
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                =============== PASO 2B ===============
            </p>
            <p>
                Vértices vecinos del conjunto S en Gl:
                <RenderVertSet vertset={neighbors} />
            </p>
            <p>
                Conjunto de Vértices T:
                <RenderVertSet vertset={tset} />
            </p>
            <p>
                <span className="resultline">
                    {"El conjunto T es subconjunto propio del conjunto de vecinos de S"}
                </span>
            </p>
        </React.Fragment>
    );
};

//resultados del paso 3, cuando busca un camino m-aumentante
const StepThreeA = ({
    yvert,    //Vértice Y en NS y no en T:                <vert: NUMBER | NONE>
    zvert,    //Vértice Z saturado con Y:                 <vert: NUMBER | NONE>
    vertxset, //conjunto de vértices x en el matching:    <set of vert: set of NUMBER | empty set>
    vertyset, //conjunto de vértices y en el matching:    <set of vert: set of NUMBER | empty set>
    gl,       //Aristas del subgrafo de igualdad:         <set of edges: set of (NUMBER,NUMBER) or empty set>
    newedges, //Aristas nuevos en el camino m-aumentante: <set of edges: set of NUMBER,NUMBER | empty set>
    matching, //Matching nuevo:                           <set of edges: set of (NUMBER,NUMBER) or empty set>
    reps,
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                {`=============== PASO 3A (vuelta # ${reps}) ===============`}
            </p>
            <p>
                Vértice Y incluido entre los vecinos del conjunto S y no incluido en T:<br />
                <span className="resultline">{yvert ? yvert : "no se encontró"}</span>
            </p>
            <p>
                Vértice Z m-saturado por el vértice Y en el matching:<br />
                <span className="resultline">{zvert ? zvert : "no se encontró"}</span>
            </p>
            <p>
                <span className="resultline">
                    {"No se encontró un vértice Z. Calculando camino m-aumentante..."}
                </span>
            </p>
            <p>
                Aristas añadidos al camino m-aumentante:
                <RenderEdgeSet edgeset={newedges} />
            </p>
            <p>
                Aristas del subgrafo de igualdad Gl:
                <RenderEdgeSet edgeset={gl} />
            </p>
            <p>
                Matching nuevo:
                <RenderEdgeSet edgeset={matching} />
            </p>
            <p>
                Vértices X en el matching:
                <RenderVertSet vertset={vertxset} />
            </p>
            <p>
                Vértices Y en el matching:
                <RenderVertSet vertset={vertyset} />
            </p>
        </React.Fragment>
    );
};

//resultados del paso 3, cuando recalcula los conjuntos S y T
const StepThreeB = ({
    yvert,    //Vértice Y en NS y no en T: <vert: NUMBER | NONE>
    zvert,    //Vértice Z saturado con Y:  <vert: NUMBER | NONE>
    sset,     //conjunto de vértices S:    <set of vert: set of NUMBER or empty set>
    tset,     //conjunto de vértices T:    <set of vert: set of NUMBER or empty set>
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                =============== PASO 3B ===============
            </p>
            <p>
                Vértice Y incluido entre los vecinos del conjunto S y no incluido en T:<br />
                <span className="resultline">{yvert}</span>
            </p>
            <p>
                Vértice Z m-saturado por el vértice Y en el matching:<br />
                <span className="resultline">{zvert}</span>
            </p>
            <p>
                <span className="resultline">
                    {"Se encontró un vértice Z. Incluyendo Z en S y Y en T..."}
                </span>
            </p>
            <p>
                Conjunto de Vértices S incluyendo Z:
                <RenderVertSet vertset={sset} />
            </p>
            <p>
                Conjunto de Vértices T incluyendo Y:
                <RenderVertSet vertset={tset} />
            </p>
        </React.Fragment>
    );
};

const ErrorBanner = ({
    steps,
    paths,
    }) => {

    return(
        <React.Fragment>
            <p className="steptitle">
                =============== ERROR!! ===============
            </p>
            <p>
                <span className="resultline">
                    {`Se calcularon ${steps} pasos y ${paths} caminos m-aumentantes.`}
                </span>
            </p>
        </React.Fragment>
    );
};

//------------------------------
//PANTALLA PRINCIPAL

const App = () => {

    //-----------------------------------------------------------
    //STATE HOOKS

    //para controlar el flujo de la presentación
    const [info,       setInfo]       = useState([]);    //arreglo que guardará componentes informativos en el orden en que aparecen

    //para controlar los parámetros iniciales
    const [matrixSize, setMatrixSize] = useState(2);     //tamaño de la matriz
    const [matrix,     setMatrix]     = useState(makeMatrix(matrixSize, EDGELIMIT)); //la matriz
    const [asigtype,   setAsigtype]   = useState("max"); //para determinar matching mínimo o máximo

    //-----------------------------------------------------------
    //EVENT HANDLERS

    const resetAll = step => {

        next       = step;
        //count      = 0;
        paths      = 0;
        alfa       = null;
        freevertex = null;
        yvert      = null;
        zvert      = null;
        optimals   = [];
        labelx     = [];
        labely     = [];
        gl         = new Set();
        matching   = new Set();
        newedges   = new Set();
        vertxset   = new Set();
        vertyset   = new Set();
        neighbors  = new Set();
        sset       = new Set();
        tset       = new Set();

        setInfo([]);
    };

    const handleSizeChange = size => {
        setMatrixSize(size);
        setMatrix(makeMatrix(size, EDGELIMIT));
        resetAll(INITIALIZE);
    };

    const handleNumChange = event => {
        const [x, y] = event.target.id.split(",");
        const newval = event.target.value;
        const newmatrix = matrixDeepCopy(matrix);
        newmatrix[Number(x)][Number(y)] = Number(newval);
        setMatrix(newmatrix);
        resetAll(INITIALIZE);
    };

    const handleReRandomize = () => {
        setMatrix(makeMatrix(matrixSize, EDGELIMIT));
        resetAll(INITIALIZE);
    };

    const handleRadioClick = event => {
        if(event.target.id!==asigtype) {
            setAsigtype(event.target.id);
            resetAll(INITIALIZE);
        }
    };

    const handleCalcClick = () => {
        count = 0;
        resetAll(STEP0);
    };

    //-----------------------------------------------------------
    //PASOS DEL ALGORITMO

    //PASO 0

    const primerLabeling = () => {

        labelx = new Array(matrixSize);
        labely = new Array(matrixSize);

        for(let i=0; i<matrixSize; i++) {
            labelx[i] = Math.max(...matrix[i]);
            labely[i] = 0;
        }

        //console.log("labelx:", labelx); //descomentar para debuggear
        //console.log("labely:", labely); //descomentar para debuggear

        return;
    };

    const calcSubgrafoDeIgualdad = () => {

        gl.clear();

        for(let x=0; x<matrixSize; x++) {
            for(let y=0; y<matrixSize; y++) {

                if((labelx[x] + labely[y]) === matrix[x][y]) {
                    gl.add([x,y]);
                }
            }
        }

        gl.shuffle();

        //console.log("gl:", gl); //descomentar para debuggear

        return;
    };

    const primerMatching = () => {

        gl.forEach(a => {

            if(!vertxset.has(a[0]) && !vertyset.has(a[1])) {
                matching.add(a);
                vertxset.add(a[0]);
                vertyset.add(a[1]);
            }
        });

        //console.log("matching:", matching); //descomentar para debuggear
        //console.log("vertxset:", vertxset); //descomentar para debuggear
        //console.log("vertyset:", vertyset); //descomentar para debuggear

        return;
    };

    const paso0 = () => {

        if(asigtype==="min") {
            console.log("no has implementado esta merga aún...");
        }

        primerLabeling();
        calcSubgrafoDeIgualdad();

        //gl = glejemplo; //hardcodeado para testear

        primerMatching();

        next = STEP1;

        const infostep = <StepZero key={++count} labelx={labelx} labely={labely} gl={gl} matching={matching} vertxset={vertxset} vertyset={vertyset} />;
        setInfo([...info, infostep]);

        return;
    };

    //PASO 1

    const encontrarVerticeSolo = () => {

        for(let i=0; i<matrixSize; i++) {
            if(!vertxset.has(i)) {
                freevertex = i;
                return;
            }
        }

        freevertex = -1;
        return;
    };

    const paso1 = () => {

        let infostep = null;
        encontrarVerticeSolo();

        if(freevertex===-1) {

            optimals = Array.from(matching.values());

            next = STEPF;

            infostep = <StepOneFinal key={++count} matching={matching} matrix={matrixDeepCopy(matrix)} steps={count} paths={paths} />;
        }else {

            sset.clear();
            tset.clear();

            sset.add(freevertex);

            next = STEP2;

            infostep = <StepOneNonFinal key={++count} freevertex={freevertex} sset={sset} tset={tset} />;
        }

        setInfo([...info, infostep]);
        return;
    };

    //PASO 2

    const vecinosDeS = () => {

        neighbors.clear();

        gl.forEach(a => {
            if(sset.has(a[0]) && !neighbors.has(a[1])) {
                neighbors.add(a[1]);
            }
        });

        //console.log("neighbors:", neighbors); //descomentar para debuggear

        return;
    };

    const calcAlfa = () => {

        alfa    = Infinity;
        let val = Infinity;

        for(let i=0; i<matrixSize; i++) {
            for(let j=0; j<matrixSize; j++) {

                if(sset.has(i) && !tset.has(j)) {

                    val = labelx[i] + labely[j] - matrix[i][j];

                    if(val<alfa) {
                        alfa = val;
                    }
                }
            }
        }

        //console.log("alfa:", alfa); //descomentar para debuggear

        return;
    };

    const reconstruirLabels = () => {

        for(let i=0; i<matrixSize; i++) {
            if(sset.has(i)) {
                labelx[i] -= alfa;
            }
        }

        for(let i=0; i<matrixSize; i++) {
            if(tset.has(i)) {
                labely[i] += alfa;
            }
        }

        //console.log("labelx:", labelx); //descomentar para debuggear
        //console.log("labely:", labely); //descomentar para debuggear

        return;
    };

    const paso2 = () => {

        let infostep = null;
        vecinosDeS();

        if(tset.equals(neighbors)) { //step 2A

            calcAlfa();
            reconstruirLabels();
            calcSubgrafoDeIgualdad();

            infostep = <StepTwoA key={++count} neighbors={neighbors} alfa={alfa} labelx={labelx} labely={labely} gl={gl} />;
        }else { //step 2B

            infostep = <StepTwoB key={++count} neighbors={neighbors} tset={tset} />;
        }

        next = STEP3;
        setInfo([...info, infostep]);

        return;
    };

    //PASO 3

    const calcCaminoMAumentante = () => {

        paths++;
        newedges.clear();

        let openarr     = [];
        let closedarr   = [];
        let rset        = new Set();
        let actual      = null;
        let newweight   = null;
        let found       = null;
        let hijo        = null;
        let start       = null;

        for(let a of gl) {

            if(a[0]===-0 || a[0]===+0) {a[0] = 0;}
            if(a[1]===-0 || a[1]===+0) {a[1] = 0;}

            start = null;

            if(!vertxset.has(a[0])) {

                start = new Vertice("x", a[0], null, null);

                openarr = [];
                closedarr = [];

                openarr.push(start);

                while(openarr.length > 0) {

                    actual = openarr.pop();

                    //condición para parar y devolver resultado exitoso
                    if(actual.side==="y" && !vertyset.has(actual.num)) {

                        while(actual.padre!==null) {

                            if(actual.side==="x") {
                                rset.add([ actual.num , actual.padre.num ]);
                            }else {
                                rset.add([ actual.padre.num , actual.num ]);
                            }

                            actual = actual.padre;
                        }

                        newedges = rset;
                        return;
                    }

                    newweight = actual.peso + 1;

                    for(let e of gl) {

                        if(e[0]===-0 || e[0]===+0) {e[0] = 0;}
                        if(e[1]===-0 || e[1]===+0) {e[1] = 0;}

                        if( (actual.side==="x" && actual.num===e[0]) || (actual.side==="y" && actual.num===e[1] && matching.hasEdge(e[0],e[1])) ) {

                            found = false;

                            if(actual.side==="x") {
                                hijo = {"side":"y", "num":e[1]};
                            }else {
                                hijo = {"side":"x", "num":e[0]};
                            }

                            for(let o of openarr) {

                                if(o.num===hijo.num) {

                                    found = true;

                                    if(o.peso > newweight) {
                                        o.peso  = newweight;
                                        o.padre = actual;
                                    }

                                    break;
                                }
                            }

                            if(!found) {

                                for(let c of closedarr) {

                                    if(c.num===hijo.num) {

                                        found = true;

                                        if(c.peso > newweight) {

                                            c.peso  = newweight;
                                            c.padre = actual;

                                            openarr.unshift(c);
                                            closedarr.filter(x => !x.equals(c));
                                        }

                                        break;
                                    }
                                }
                            }

                            if(!found) {

                                const newv = new Vertice(hijo.side, hijo.num, actual, newweight);

                                if(hijo.side==="y" && !vertyset.has(hijo.num)) {
                                    openarr.push(newv); //insertar al final de open
                                }else {
                                    openarr.unshift(newv); //insertar al inicio de open
                                }
                            }
                        }
                    }

                    closedarr.push(actual);
                }
            }
        }

        newedges = rset;
        return;
    };

    const reCalcMatching = () => {

        //set op symDiff
        matching = matching.symDiff(newedges);

        vertxset.clear();
        vertyset.clear();

        matching.forEach(a => {
            vertxset.add(a[0]);
            vertyset.add(a[1]);
        });

        //console.log("matching:", matching); //descomentar para debuggear
        //console.log("vertxset:", vertxset); //descomentar para debuggear
        //console.log("vertyset:", vertyset); //descomentar para debuggear

        return;
    };

    const paso3 = () => {

        let infostep = null;

        yvert = null;
        for(let v of neighbors) {
            if(!tset.has(v)) {
                yvert = v;
                break;
            }
        }

        zvert = null;
        for(let a of matching) {
            if(a[1]===yvert) {
                zvert = a[0];
            }
        }

        if(zvert!==null) { //step 3B

            sset.add(zvert);
            tset.add(yvert);

            next = STEP2;

            infostep = <StepThreeB key={++count} yvert={yvert} zvert={zvert} sset={sset} tset={tset} />;
        }else { //step 3A

            calcCaminoMAumentante();
            reCalcMatching();

            if(paths>=MAXPATHS) {
                next = STEPF;
                infostep = <ErrorBanner key={++count} steps={count} paths={paths} />;
                setInfo([...info, infostep]);
                return;
            }

            if(newedges.size===0) {

                if(errtrack===0) { //una vez que no hay camino m-aumentante

                    errtrack = 1;
                    history1 = {};
                    history2 = {};
                }else if(errtrack===1) { //dos veces seguidas que no hay camino m-aumentante

                    errtrack = 2;
                    history1 = getHistory();
                    history2 = {};
                }else if(errtrack===2) { //tres veces seguidas que no hay camino m-aumentante

                    history2 = getHistory();

                    if(compareHistory()) { //las últimas 2 vueltas fueron idénticas, resetear o se va a ciclar

                        resetAll(STEP0);
                        return;
                    }else { //las últimas 2 vueltas fueron diferentes, seguir al pendiente

                        errtrack = 2;
                        history1 = history2;
                        history2 = {};
                    }
                }
            }else {

                errtrack = 0;
                history1 = {};
                history2 = {};
            }

            next = STEP1;

            infostep = <StepThreeA key={++count} reps={paths} yvert={yvert} zvert={zvert} vertxset={vertxset} vertyset={vertyset} gl={gl} newedges={newedges} matching={matching} />;
        }

        setInfo([...info, infostep]);
        return;
    };

    //MANEJO DE ERROR

    const errorOut = () => {

        next = STEPF;
        let infostep = <ErrorBanner key={++count} steps={count} paths={paths} />;
        setInfo([...info, infostep]);
        return;
    };

    //-----------------------------------------------------------
    //EFFECT HOOKS

    useEffect(() => {

        if(count<=MAXSTEPS) {

            switch(next) {
                case STEP0:
                    paso0();
                    break;
                case STEP1:
                    paso1();
                    break;
                case STEP2:
                    paso2();
                    break;
                case STEP3:
                    paso3();
                    break;
                default:
                    break;
                //default
            }
        }else {
            errorOut();
        }
    }, [info]);

    //-----------------------------------------------------------
    //JSX

    return (
        <div className="App">
            <p className="title">Algoritmo Kuhn-Munkres</p>
            <header className="App-header">

                {/*PASOS DE INICIALIZACIÓN*/}
                <React.Fragment>

                    <SizeInput id={"sizepicker"} limit={SIZELIMIT} onChange={handleSizeChange} />

                    <div className={"inputmatrix"}>
                        <InputMatrix content={matrix} limit={EDGELIMIT} optimals={optimals} onChange={handleNumChange} />
                    </div>

                    <p><button className="mainbutton" onClick={handleReRandomize}>RE-RANDOM</button></p>

                    <div className="asigPicker">

                        <p>{"Asignación óptima a calcular:"}</p>

                        <label htmlFor="max" className="radioContainer">Máxima&#9;
                            <input type="radio" name="asigtype" id="max" value="max" onClick={handleRadioClick} checked={asigtype==="max"} />
                            <span className="radioSpan"></span>
                        </label>

                        <br />

                        <label htmlFor="min" className="radioContainer">Mínima&#9;
                            <input type="radio" name="asigtype" id="min" value="min" onClick={handleRadioClick} checked={asigtype==="min"} />
                            <span className="radioSpan"></span>
                        </label>
                    </div>

                    <p><button className="mainbutton" onClick={handleCalcClick}>CALCULAR</button></p>
                </React.Fragment>

                {/*INFO DEL ALGORITMO*/}
                {info}
            </header>
        </div>
    );
};

export default App;

//eof
