/*//hosting
miFuncion(2,5);

//declaracion de la funcion
function miFuncion (a,b) {
    console.log("SUma: " + (a+b));
}
// llamda de la funcion
miFuncion (2,3);*/
/*
function miFuncion(a,b) {
    return a+b;
}

let resultado = miFuncion(2,3);
console.log(resultado);

let x = function (a,b) {
    return a+b;
};

resultado = x(1,3);
console.log(resultado);

(function (){
    console.log("Ejeccutando...");
})();

const sumarfunciontipofecha = (a,b) => a+b;
resultado = sumarfunciontipofecha(2,3);
console.log(resultado);

*/
// declaracion funcion de tipo expresion
/*
let sumar = function (a = 3,b = 7){
    console.log(arguments[0]);
    console.log(arguments [1]);
    console.log(arguments [2]);
        return a+b
};

resultado = sumar(2,3);
console.log(resultado);
*/
/*
let resultado = sumartodo(2,3,4,5,6,7,8,9,10);
console.log(resultado);

function sumartodo() {
    let suma = 0
    for (let i = 0; i < arguments.length; i++) {
        suma += arguments[i]; // suma = suma + argumento[i]
    }
    return suma;
}
*/

// Tipos Primitivos
let x = 10;

function cambiarvalor (a){
    a = 20;
}
// Paso por valor
cambiarvalor (x); //10
console.log(x);

// Paso por refertencia
const persona = { 
    nombre: "Juan",
    edad: 20
}

function cambiarvalorobjeto (p1){
    p1.nombre = "Pedro";
    p1.edad = 30;
}
// paso por referencia
cambiarvalorobjeto(persona);
console.log(persona);