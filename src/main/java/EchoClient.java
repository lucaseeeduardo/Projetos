import java.rmi.Naming;
import java.util.List;
import java.util.Scanner;

/**
 * Cliente para o serviço de Echo com tolerância a falhas
 */
public class EchoClient {
    
    private ServerListManager serverListManager;
    private EchoService currentServer;
    private String currentServerId;
    
    public EchoClient() {
        try {
            // Obtém referência ao gerenciador de lista
            serverListManager = (ServerListManager) Naming.lookup("rmi://localhost/ServerListManager");
            connectToMaster();
        } catch (Exception e) {
            System.err.println("Erro ao conectar ao sistema: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private boolean connectToMaster() {
        try {
            String masterId = serverListManager.getMasterServer();
            if (masterId != null) {
                currentServer = (EchoService) Naming.lookup("rmi://localhost/" + masterId);
                currentServerId = masterId;
                System.out.println("Conectado ao servidor master: " + masterId);
                return true;
            } else {
                System.err.println("Nenhum servidor master disponível");
                return false;
            }
        } catch (Exception e) {
            System.err.println("Erro ao conectar ao master: " + e.getMessage());
            return false;
        }
    }
    
    private void handleServerFailure() {
        System.out.println("Detectada falha no servidor. Reconectando...");
        
        int attempts = 0;
        while (attempts < 5) {
            try {
                Thread.sleep(2000); // Aguarda 2 segundos
                
                // Tenta reconectar ao novo master
                if (connectToMaster()) {
                    System.out.println("Reconectado com sucesso ao novo master!");
                    return;
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            attempts++;
        }
        
        System.err.println("Não foi possível reconectar após " + attempts + " tentativas");
    }
    
    public void echo(String message) {
        try {
            if (currentServer == null && !connectToMaster()) {
                System.err.println("Não há servidor disponível");
                return;
            }
            
            String response = currentServer.echo(message);
            System.out.println("Resposta do servidor: " + response);
            
        } catch (Exception e) {
            System.err.println("Erro ao enviar mensagem: " + e.getMessage());
            handleServerFailure();
            
            // Tenta novamente após reconexão
            try {
                if (currentServer != null) {
                    String response = currentServer.echo(message);
                    System.out.println("Resposta do servidor (após reconexão): " + response);
                }
            } catch (Exception ex) {
                System.err.println("Falha definitiva ao enviar mensagem: " + ex.getMessage());
            }
        }
    }
    
    public void getListOfMessages() {
        try {
            if (currentServer == null && !connectToMaster()) {
                System.err.println("Não há servidor disponível");
                return;
            }
            
            List<String> messages = currentServer.getListOfMsg();
            
            if (messages.isEmpty()) {
                System.out.println("Nenhuma mensagem no histórico");
            } else {
                System.out.println("\n=== Histórico de Mensagens ===");
                for (int i = 0; i < messages.size(); i++) {
                    System.out.println((i + 1) + ". " + messages.get(i));
                }
                System.out.println("Total: " + messages.size() + " mensagens");
            }
            
        } catch (Exception e) {
            System.err.println("Erro ao obter lista de mensagens: " + e.getMessage());
            handleServerFailure();
            
            // Tenta novamente após reconexão
            try {
                if (currentServer != null) {
                    List<String> messages = currentServer.getListOfMsg();
                    System.out.println("\n=== Histórico de Mensagens (após reconexão) ===");
                    for (int i = 0; i < messages.size(); i++) {
                        System.out.println((i + 1) + ". " + messages.get(i));
                    }
                }
            } catch (Exception ex) {
                System.err.println("Falha definitiva ao obter mensagens: " + ex.getMessage());
            }
        }
    }
    
    public void showServerStatus() {
        try {
            List<String> servers = serverListManager.getServerList();
            String master = serverListManager.getMasterServer();
            
            System.out.println("\n=== Status do Sistema ===");
            System.out.println("Servidor Master: " + master);
            System.out.println("Servidores ativos:");
            for (String server : servers) {
                String role = server.equals(master) ? " [MASTER]" : " [CLONE]";
                System.out.println("  - " + server + role);
            }
            System.out.println("Total de servidores: " + servers.size());
            
        } catch (Exception e) {
            System.err.println("Erro ao obter status do sistema: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        EchoClient client = new EchoClient();
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("\n=== Cliente do Serviço de Echo ===");
        System.out.println("Comandos disponíveis:");
        System.out.println("  1 - Enviar mensagem (echo)");
        System.out.println("  2 - Listar todas as mensagens");
        System.out.println("  3 - Mostrar status do sistema");
        System.out.println("  4 - Sair");
        
        boolean running = true;
        while (running) {
            System.out.print("\nEscolha uma opção: ");
            
            try {
                int option = Integer.parseInt(scanner.nextLine().trim());
                
                switch (option) {
                    case 1:
                        System.out.print("Digite a mensagem: ");
                        String message = scanner.nextLine();
                        if (!message.trim().isEmpty()) {
                            client.echo(message);
                        } else {
                            System.out.println("Mensagem vazia não permitida");
                        }
                        break;
                        
                    case 2:
                        client.getListOfMessages();
                        break;
                        
                    case 3:
                        client.showServerStatus();
                        break;
                        
                    case 4:
                        running = false;
                        System.out.println("Encerrando cliente...");
                        break;
                        
                    default:
                        System.out.println("Opção inválida. Tente novamente.");
                }
                
            } catch (NumberFormatException e) {
                System.out.println("Por favor, digite um número válido");
            }
        }
        
        scanner.close();
        System.out.println("Cliente encerrado");
    }
}