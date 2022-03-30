class Persona{
    constructor(nombre, apellido, email){
        this._nombre = nombre;
        this._apellido = apellido;
        this._email = email;
    }
    get nombre(){
        return this._nombre;
    }
    set nombre(nombre){
        this._nombre = nombre;
    }
    get apellido(){
        return this._apellido;
    }
    set apellido(apellido){
        this._apellido = apellido;
    }
    get email(){
        return this._email;
    }
    set email(email){
        this._email = email;
    }
    nombreCompleto() {
        return this._nombre + " " + this._apellido;
    }
}


class Empleado extends Persona{
        constructor (nombre, apellido, email, departamento, salario){
            super(nombre, apellido, email); // llamar al constructor de la clase padre
            this._departamento = departamento;
            this._salario = salario;
        }
        get departamento(){
            return this._departamento;
        }
        set departamento(departamento){
            this._departamento = departamento;
        }
        get salario(){
            return this._salario;
        }
        set salario(salario){
            this._salario = salario;
        }
        //Sobreescribir el metodo nombreCompleto
        nombreCompleto(){
            return super.nombreCompleto + " (" + this._departamento + ")";
        }
    }


let persona1 = new Persona("pedro", "perez", "pedropere@gmail.com");
console.log (persona1);

let empleado1 = new Empleado("maria", "Gonsalez", "mgonsalez@gmail.com", "contabiliad", "15000"); 
console.log(empleado1);
console.log(empleado1.nombre);
console.log(empleado1.nombreCompleto());


/*
let persona2 = new Persona("juan", "perez", "sdsdsdd@gmail.com");
console.log (persona2);
*/