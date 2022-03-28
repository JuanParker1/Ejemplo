
/*let condicion = true;

if (condicion){
    console.log("Si se cumple la condicion");


}
else {
 console.log("No se cumple la condicion");

}

let numero = 3;
 if ( numero == 1){
    console.log("El numero es 1");
}
else if (numero == 2){
    console.log("El numero es 2");
} 
else    {
    console.log("El numero es 3");
}  
*/
/* // CALCULAR ESTACION DE TIEMPO
let mes = 5;
let estacion;
// if (mes == 1 || mes == 2 || mes == 12){
if (mes >= 1 && mes <= 3){
    estacion = "Verano";
}
else if (mes >= 4 && mes <= 6){
    estacion = "Otoño";
}
else if (mes >= 7 && mes <= 9){
    estacion = "Invierno";
}
else if (mes >= 10 && mes <= 12){
    estacion = "Primavera";
}
else {
    estacion = "Mes invalido";
}
console.log(estacion);
*/
/*
let hora = 13;
let tipo;

if (hora >= 00 && hora < 06){
    tipo = "Buenos noches";
}
else if (hora >= 06 && hora < 12){
    tipo = "Buenos días";
}
else if (hora >= 12 && hora < 18){
    tipo = "Buenas tardes";
}
else if (hora >= 18 && hora < 24){
    tipo = "Buenas noches";
}
else {
    tipo = "Hora invalida";
}
console.log(tipo);
*/
/*
let numero = 2;
let numerotexto = 'valor desconocido';

switch ( numero){   
    case 1:
        numerotexto = 'uno';
        break;
    case 2:
        numerotexto = 'dos';
        break;
    case 3:
        numerotexto = 'tres';
        break;
    default:
        numerotexto = 'valor desconocido';
        break;
    }
console.log(numerotexto);
*/

let mes = 2;
let estacion = 'valor desconocido';

switch (mes){
    case 1: case 2: case 12:
            estacion = 'Verano';
            break;
    case 3: case 4: case 5:
            estacion = 'Otoño';
            break;
    case 6: case 7: case 8:
            estacion = 'Invierno';
            break;
    case 9: case 10: case 11:
            estacion = 'Primavera';
            break;
    default:
        estacion = 'Mes invalido';
        break;
}
console.log(estacion);
