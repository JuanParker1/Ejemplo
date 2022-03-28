
//let autos = new Array("Fiat", "Ford", "Chevrolet", "Renault");

const autos = ["Fiat", "Ford", "Chevrolet", "Renault"];
console.log(autos);

autos[0] = "Mazda";
console.log(autos[0]);
console.log(autos);

// se accedio de forma individual
for (let i = 0; i < autos.length; i++){
    console.log ( i + " : " +  autos [i]);
}


// se agrega honda con push

autos.push ("Honda");
console.log(autos);

console.log(autos.length);
//se agrega un elemento al final
autos [autos.length] = "Toyota";
console.log(autos);
// se saltea una posicion
autos[7] = "alfa romeo";
console.log(autos);

console.log ( typeof autos);
// consulta el tipo de dato
console.log(Array.isArray(autos));
console.log (autos instanceof Array);