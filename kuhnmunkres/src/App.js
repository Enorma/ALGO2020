import React, {useState} from 'react';
import './App.css';

const SIZELIMIT = 10;
const EDGELIMIT = 99;

//------------------------
//DEFINE STAGES

const INITIALIZE = 0;
const STEP1 = 1;

//------------------------
//FUNCIONES

//returns a random integer from 0 to limit (both inclusive)
const getRand = max => Math.floor(Math.random()*(max+1));

const makeMatrix = (size, limit) => {

    const matrix = [];
    let vector = [];

    for(let i=0; i<size; i++) {
        vector = vector.slice(99);
        for(let j=0; j<size; j++) {
            vector.push(getRand(limit));
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

//------------------------------
//OPERACIONES CON CONJUNTOS

Set.prototype.isSubSet = otherSet => {

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

Set.prototype.union = otherSet => {

    let unionSet = new Set();

    for(let elem of this) {
        unionSet.add(elem);
    }

    for(let elem of otherSet) {
        unionSet.add(elem);
    }

    return unionSet;
}

Set.prototype.intersection = otherSet => {

    let intersectionSet = new Set();

    for(let elem of otherSet) {
        if(this.has(elem)) {
            intersectionSet.add(elem);
        }
    }

    return intersectionSet;
}

Set.prototype.diff = otherSet => {

    let diffSet = new Set();

    for(let elem of this) {
        if(!otherSet.has(elem)) {
            diffSet.add(elem);
        }
    }

    return diffSet;
}

Set.prototype.symDiff = otherSet => {

    let united = this.union(otherSet);
    let intersected = this.intersection(otherSet);
    let symDiffSet = united.diff(intersected);

    return symDiffSet;
};

//------------------------------
//COMPONENTES

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
    value=getRand(limit),
    onChange,
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
            className="numinput"
            onChange={onChange}
        />
    );
};

const InputMatrix = ({
    content=[],
    limit=EDGELIMIT,
    onChange,
    }) => {

    const data = [...content];

    const table = [];
    for(let i=0; i<data.length; i++) {
        table.push([]);
        for(let j=0; j<data.length; j++) {
            table[i] = [...table[i], <NumInput key={`${i},${j}`} cell={`${i},${j}`} limit={limit} value={data[i][j]} onChange={onChange} />];
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

const App = () => {

    //declare initial state variables
    const [stage,      setStage]      = useState(INITIALIZE);
    const [matrixSize, setMatrixSize] = useState(2);
    const [matrix,     setMatrix]     = useState(makeMatrix(matrixSize, EDGELIMIT));
    const [asigtype,   setAsigtype]   = useState("max");

    const [labelX,     setLabelX]     = useState((new Array(matrixSize)).fill(null));
    const [labelY,     setLabelY]     = useState((new Array(matrixSize)).fill(null));

    const [GL,         setGL]         = useState(new Set()); //conjunto de aristas del subgrafo de igualdad
    const [ML,         setML]         = useState(new Set()); //conjunto de aristas del matching dobre GL
    const [VX,         setVX]         = useState(new Set()); //conjunto de vértices de un lado de la bipartición
    const [VY,         setVY]         = useState(new Set()); //conjunto de vértices del otro lado de la bipartición
    const [S,          setS]          = useState(new Set()); //subconjunto de vértices del grafo
    const [T,          setT]          = useState(new Set()); //subconjunto de vértices del grafo
    const [NS,         setNS]         = useState(new Set()); //conjunto de vértices vecinos de S

    const handleSizeChange = size => {
        setMatrixSize(size);
        setMatrix(makeMatrix(size, EDGELIMIT));
        setStage(INITIALIZE);
    };

    const handleNumChange = event => {
        const [x, y] = event.target.id.split(",");
        const newval = event.target.value;
        const newmatrix = matrixDeepCopy(matrix);
        newmatrix[Number(x)][Number(y)] = Number(newval);
        setMatrix(newmatrix);
        setStage(INITIALIZE);
    };

    const handleReRandomize = () => {
        setMatrix(makeMatrix(matrixSize, EDGELIMIT));
        setStage(INITIALIZE);
    };

    const handleRadioClick = event => {
        if(event.target.id!==asigtype) {
            setAsigtype(event.target.id);
            setStage(INITIALIZE);
        }
    };

    const handleCalcClick = () => {
        setStage(STEP1);
        //aquí van los cálculos del mugres
    };

    return (
        <div className="App">
            <p className="title">Algoritmo Kuhn-Munkres</p>
            <header className="App-header">

                <SizeInput id={"sizepicker"} limit={SIZELIMIT} onChange={handleSizeChange} />

                {stage>=INITIALIZE && (<React.Fragment>

                    <InputMatrix content={matrix} limit={EDGELIMIT} onChange={handleNumChange} />
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
                </React.Fragment>)}

                {stage>=STEP1 && (<React.Fragment>

                    <p>TO BE CONTINUED...</p>
                </React.Fragment>)}
            </header>
        </div>
    );
};

export default App;

//eof
