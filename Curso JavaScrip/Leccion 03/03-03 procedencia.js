/*let a = 3, b = 2, c = 1, d = 4;

let z = a * b + c;
console.log(z);

z = c + a * b;
console.log(z);

z = a * b + c / d;
console.log(z);


z = a * b / d;
console.log(z);
*/
/*
let a = 1

a += 2; // a = a + 2
console.log(a);

a -=2; // a = a - 2
console.log(a);

a *= 2; // a = a * 2
console.log(a);

a /= 2; // a = a / 2
console.log(a);

a /= 2; // a = a / 2
console.log(a);

a %= 2; // a = a % 2
console.log(a);

a **= 2; // a = a ** 2
console.log(a);
*/

//let a = 2, b = 2, c = 1, d = 4;
/*
let z = a == b; // se revisa el valor sin importal el tipo de dato
console.log(z);

z = a === c; // se revisa el valor y el tipo de dato
console.log(z);
*/
/*
let z = a != b; // se revisa el valor sin importal el tipo de dato
console.log(z);

z = a !== c; // se revisa el valor y el tipo de dato
console.log(z);
*/
/*
let z = a < b; // se revisa el valor sin importal el tipo de dato
console.log(z);

z = a <= c; // se revisa el valor y el tipo de dato
console.log(z);
*/
/*
// ejercicio de  par o impar
let a = 10

if (a % 2 == 0 ) {
    console.log('a es par');
}
else {
    console.log('a es impar');
}*/

/*
// ejercicio de edad
let edad = 30, adulto = 18

if (edad >= adulto) {
    console.log('es mayor de edad');
}
else {
    console.log('es menor de edad');
}*/
/*
let a = 5
let ValorMin = 0
let ValorMax = 10


// && operador AND - solo true si ambos son true
if (a >= ValorMin && a <= ValorMax) {
    console.log('a esta dentro del rango');
}
else {
    console.log('a esta fuera del rango');
}


// || operador OR, regresa true si cualquiera es true
let vacaciones = false, diadescanso = false;

if (vacaciones || diadescanso) {
    console.log('puede ir al juego');
}
else {
    console.log('no puede ir al juego');
}

// 

let resultado = (3<4) ? 'es mayor' : 'es menor';
console.log(resultado);


let numero = 9;

resultado = (numero % 2 == 0) ? 'es par' : 'es impar';
console.log(resultado);


////////////////////////////////////////////////
*/
/*

let minumero = "19";

let edad = Number(minumero);
console.log(typeof edad);

resultado = (minumero >= 18) ? 'puede votar' : 'No puede votar';
console.log(resultado);

if (isNaN(edad)) {
    console.log('no es un numero');
}
else {
if ( edad >= 18 ) {
    console.log('es Puede votar');
}
else {
    console.log('es No puede votar');
}
}*/

let x = 5;
let y = 10;
let z = ++x + y--;
console.log(x);
console.log(y);
console.log(z);

let resultado = 4 + 5 * 6/3;//(4+((5+6)/3))
console.log(resultado);

resultado = ( 4 + 5 ) * 6 / 3; //((4+5)*6)/3
console.log(resultado);