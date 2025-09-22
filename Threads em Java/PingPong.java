import java.lang.Thread;

public class PingPong extends Thread{
    private String palavra;
    private boolean executando;
    public PingPong(String palavra) {
        this.palavra = palavra;
    }

    public Thread estaExecutando() {
        executando = true;
        for (int i = 0; i < 100; i++) {
            System.out.println(palavra);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        executando = false;
        return this;
    }

    public static void main(String[] args) {
        System.out.println("Iniciando o jogo...");
        
        PingPong ping = new PingPong("Ping");
        PingPong pong = new PingPong("Pong");

        ping.start();
        pong.start();

        var thread1 =  ping.start().estaExecutando();
        while (estaExecutando) {
            System.out.println("Jogo em andamento...");
            // Aguardando a conclusão das threads
        }
        System.out.println("Jogo Finalizado!");
    }
}