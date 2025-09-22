import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Main{
    public static void main(String[] args){

        Scanner scanner = new Scanner(System.in);
        // GameEntry[] entradas = popularScores(2); // ex 1.
        // ArrayList<GameEntry> arrayListDeEntradas = new ArrayList<>(Arrays.asList(popularScores(2))) ; // ex 2.
        List<GameEntry> listaGenericaDeEntradas = Arrays.asList(popularScores(2)); // ex 3.

        System.out.println("Insira os scores de cada participante:");
        for (GameEntry entry : listaGenericaDeEntradas) {

            System.out.print(String.format("Insira o score do %s ", entry.getName()));
            lerPontuacao(scanner, entry);
            // Aqui, é computacionalmente mais caro eu criar a variável "entradaValida" novamente
            // ou alterar o valor dela é mais caro? Acho que recriar a variável várias vezes pode causar overhead no garbage collector, por mais que seja um processo que já é automatizado...
            
            System.out.println(entry);
        }


        Collections.sort(listaGenericaDeEntradas, new GameEntryComparator()); // ex. 3

        System.out.println("Scores inseridos:");
        for(GameEntry entrada : listaGenericaDeEntradas) {
            System.out.println(entrada);
        }

        scanner.close();
    }

    private static void lerPontuacao(Scanner scanner, GameEntry entry) {
        boolean entradaValida = false;

        while(!entradaValida) 
        {
            try 
            {
                int pontuacao = Integer.parseInt(scanner.nextLine());
                entradaValida = true;
                entry.setScore(pontuacao);
            } 
            catch (NumberFormatException e) 
            {
                System.out.println("Entrada inválida. Por favor, insira um número inteiro.");
            }
        }
    }

    public static GameEntry[] popularScores(int quantidade)
    {
        GameEntry[] entries = new GameEntry[]{
            new GameEntry("Lucas"),
            new GameEntry("Ana"),
            new GameEntry("João"),
            new GameEntry("Abacate"),
            new GameEntry("Banana"),
            new GameEntry("Mamão"),
            new GameEntry("Abacaxu"),
            new GameEntry("Kiwi"),
            new GameEntry("Morango"),
            new GameEntry("Laranja"),
        }; 

        return Arrays.copyOf(entries, quantidade); 
    }
}