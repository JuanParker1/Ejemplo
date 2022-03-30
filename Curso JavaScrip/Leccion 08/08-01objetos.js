/*function Persona (nombre, apellido, email){
    this.nombre = nombre;
    this.apellido = apellido;
    this.email = email;
    this.nombrecomple = function(){
        return this.nombre + " " + this.apellido;
    }
}*/

let persona = {
    nombre: "Pedro",
    apellido: "Perez",
    nombrecomple: function (titulo, telefono){
        return this.nombre + " " + this.apellido + " " + titulo + " " + telefono;
    }
}
let persona2 = {
    nombre: "Juan",
    apellido: "loco",
}
//Persona.prototype.telefono = '112232';

//Uso de call para usar
//el metodo persona.nombrecomple()

console.log(persona.nombrecomple('conta', '112233'));

console.log(persona.nombrecomple.call(persona2, 'ING', '121231231212'));
// console.log(persona.nombrecomple.apply(persona2, ['ING', '121231231212']));
//let padre = new Persona('Juan', 'Perez', 'raaay@gmail.com');
//let hijo = new Persona('Pedro', 'Perez', 'ray3@gmail.com');

//padre.telefono = '12312312312312';

//console.log (padre.telefono);
//console.log (hijo.telefono);


let miObjeto = new Object();
let miObjeto2 = {};

let micadena = new String('hola');
let micadena2 = 'hola';

let minumero = new Number(10);
let minumero2 = 10;

let miboolean = new Boolean(true);
let miboolean2 = true;

let miarreglo = new Array();
let miarreglo2 = [];

let mifuncion   = new Function('console.log("hola")');
/*
let persona = {
    nombre: "Juan",
    apellido: "Perez",
    email: "juanperez@gmail.com",
    edad: 30,
    idioma: "es",
    get lang() {
        return this.idioma.toUpperCase();
    },
    set lang (lang) {
        this.idioma = lang.toUpperCase();
    },
    //nombreapellido: function () {
    get nombreapellido() {
        return this.nombre + " " + this.apellido;
    }
}


console.log(persona.lang);

persona.lang = 'en';
console.log(persona.lang);
console.log (persona.idioma);
*/


/*
persona.tel = "123456789";

console.log (persona); 

delete persona ["tel"];

console.log (persona);

// concatenar cada valor de cada propiedad del objeto

console.log(persona.nombre + "," + persona.apellido);

//for in

for (nombrepropiedad in persona) {
    console.log(persona[nombrepropiedad]);
}

let personaArray = Object.values(persona);
console.log (personaArray);

*/
/*
console.log(persona.nombre);
console.log(persona.edad);
console.log(persona);
console.log(persona.nombreapellido());
console.log(persona["nombre"]);

// for in

for (nombrepropiedad in persona) {
    console.log(nombrepropiedad); //visualizamos las propiedades del objeto
    console.log (persona[nombrepropiedad]); //valores de las propiedades
}
*/


/*
let persona2 = new Object();
persona2.nombre = "jose";
persona2.apellido = "perez";
persona2.email = "joseperez@gmail.com";
persona2.edad = 25;
*/

