public class HollaMundo2 {
    public static void main(String args[]) {
        var usuario = "Juan";
        var titulo = "Ingeniero";
        var union = usuario + " " + titulo;
        System.out.println("union =" + union);
        
        var i = 3;
        var j = 4;

        //var suma = i + j;
        System.out.println( i + j);
        //lee de izq a derecha si arranca cadena-muere cadena
        System.out.println( usuario + i+j); //Juan43
}
}