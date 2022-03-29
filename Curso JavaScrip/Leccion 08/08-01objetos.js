function Persona (nombre, apellido, email){
    this.nombre = nombre;
    this.apellido = apellido;
    this.email = email;
    this.nombrecomple = function(){
        return this.nombre + " " + this.apellido;
    }
}

let padre = new Persona('Juan', 'Perez', 'raaay@gmail.com');
let hijo = new Persona('Pedro', 'Perez', 'ray3@gmail.com');

console.log (padre);
console.log (hijo);

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

