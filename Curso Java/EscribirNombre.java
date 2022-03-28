import java.util.Scanner;

public class EscribirNombre {
    public static void main(String args[]) {
        System.out.println("Escribe tu nombre: ");
        Scanner consola = new Scanner(System.in); //lee info de la consola (in)
        var usuario = consola.nextLine(); //lee una linea de texto (nextLine)
        System.out.println("Usuario = " + usuario);
        System.out.println("Escribe el titulo prof " + usuario + "!");
        var titulo = consola.nextLine();
        System.out.println("Resultado = " + titulo + " " + usuario);
}
}