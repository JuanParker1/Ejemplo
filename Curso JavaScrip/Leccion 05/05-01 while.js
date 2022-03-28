let contador = 0;
/*
while ( contador < 3){
    console.log(contador);
    contador++;
}
*/
/*
do {
    console.log(contador);
    contador++;
} while (contador < 3);
console.log('Fin');
*/
/*
for (let contador = 0; contador < 3; contador++) {
    console.log(contador);
}
console.log("Fin");
*/
/*
for (let contador =0; contador <=10 ; contador++) {
    if (contador % 2 == 0) {
        console.log(contador);
        break;
    }
   
}
console.log("Fin");
*/
inicio:
for (contador = 0; contador <= 10; contador++){
    if (contador %2 !=+ 0){
        continue inicio; //ir a la siguiente iteracion
    }
    else {
        console.log(contador);
    }
}
console.log("Fin");