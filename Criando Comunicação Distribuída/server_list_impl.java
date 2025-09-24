import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;
import java.util.*;
import java.util.concurrent.*;

/**
 * Implementação do gerenciador de lista de servidores
 * Responsável por manter a lista de servidores ativos e coordenar eleições
 * Este componente é o COORDENADOR CENTRAL que decide quem é o master
 */
public class ServerListManagerImpl extends UnicastRemoteObject implements ServerListManager {
    
    private Deque<String> serverList;
    private List<String> globalMessages;
    private final Object lock = new Object();
    private Set<String> electionRequests;
    private ScheduledExecutorService healthChecker;
    private volatile boolean electionInProgress = false;
    
    public ServerListManagerImpl() throws RemoteException {
        super();
        this.serverList = new ConcurrentLinkedDeque<>();
        this.globalMessages = new CopyOnWriteArrayList<>();
        this.electionRequests = Collections.synchronizedSet(new HashSet<>());
        this.healthChecker = Executors.newSingleThreadScheduledExecutor();
        
        // Inicia verificação periódica de saúde do master
        startHealthCheck();
    }
    
    private void startHealthCheck() {
        healthChecker.scheduleWithFixedDelay(() -> {
            try {
                if (!checkMasterHealth() && !electionInProgress) {
                    System.out.println("Health check detectou falha do master. Iniciando eleição automática...");
                    electNewMaster();
                }
            } catch (Exception e) {
                System.err.println("Erro no health check: " + e.getMessage());
            }
        }, 10, 5, TimeUnit.SECONDS); // Verifica a cada 5 segundos após 10 segundos iniciais
    }
    
    @Override
    public void registerServer(String serverName) throws RemoteException {
        synchronized (lock) {
            if (!serverList.contains(serverName)) {
                serverList.addLast(serverName);
                System.out.println("Servidor registrado: " + serverName);
                System.out.println("Lista atual de servidores: " + serverList);
                
                // O primeiro servidor automaticamente se torna master
                if (serverList.size() == 1) {
                    System.out.println("DECISÃO DO GERENCIADOR: " + serverName + " é o primeiro servidor e será o MASTER");
                }
            }
        }
    }
    
    @Override
    public void removeServer(String serverName) throws RemoteException {
        synchronized (lock) {
            boolean removed = serverList.remove(serverName);
            if (removed) {
                System.out.println("Servidor removido: " + serverName);
                System.out.println("Lista atual de servidores: " + serverList);
            }
        }
    }
    
    @Override
    public List<String> getServerList() throws RemoteException {
        synchronized (lock) {
            return new ArrayList<>(serverList);
        }
    }
    
    @Override
    public String getMasterServer() throws RemoteException {
        synchronized (lock) {
            return serverList.isEmpty() ? null : serverList.getFirst();
        }
    }
    
    @Override
    public String requestElection(String requestingServer) throws RemoteException {
        System.out.println("Servidor " + requestingServer + " solicitou eleição");
        electionRequests.add(requestingServer);
        
        // Se múltiplos servidores solicitam eleição, aguarda um pouco para consolidar
        if (electionRequests.size() >= 2 || !checkMasterHealth()) {
            return electNewMaster();
        }
        
        return getMasterServer(); // Retorna o master atual se ainda estiver ativo
    }
    
    @Override
    public boolean checkMasterHealth() throws RemoteException {
        synchronized (lock) {
            if (serverList.isEmpty()) {
                return false;
            }
            
            String currentMaster = serverList.peekFirst();
            try {
                EchoService masterService = (EchoService) Naming.lookup("rmi://localhost/" + currentMaster);
                masterService.isAlive();
                return true;
            } catch (Exception e) {
                System.out.println("Master " + currentMaster + " não está respondendo");
                return false;
            }
        }
    }
    
    @Override
    public String electNewMaster() throws RemoteException {
        synchronized (lock) {
            electionInProgress = true;
            try {
                if (serverList.isEmpty()) {
                    System.out.println("DECISÃO DO GERENCIADOR: Nenhum servidor disponível para eleição");
                    return null;
                }
                
                String currentMaster = serverList.peekFirst();
                String failedMaster = null;
                
                // Verifica se o master atual está realmente inativo
                try {
                    EchoService masterService = (EchoService) Naming.lookup("rmi://localhost/" + currentMaster);
                    masterService.isAlive();
                    System.out.println("DECISÃO DO GERENCIADOR: Master " + currentMaster + " ainda está ativo. Eleição cancelada.");
                    electionRequests.clear();
                    return currentMaster;
                } catch (Exception e) {
                    // Master realmente falhou, proceder com eleição
                    failedMaster = serverList.pollFirst();
                    System.out.println("DECISÃO DO GERENCIADOR: Confirmando falha do master " + failedMaster);
                    System.out.println("DECISÃO DO GERENCIADOR: Removendo " + failedMaster + " da lista de servidores ativos");
                }
                
                // DECISÃO CENTRALIZADA: O próximo na lista se torna o novo master
                String newMaster = serverList.peekFirst();
                
                if (newMaster != null) {
                    System.out.println("╔══════════════════════════════════════════╗");
                    System.out.println("║   ELEIÇÃO COORDENADA PELO GERENCIADOR   ║");
                    System.out.println("╠══════════════════════════════════════════╣");
                    System.out.println("║ Master anterior: " + failedMaster);
                    System.out.println("║ NOVO MASTER ELEITO: " + newMaster);
                    System.out.println("║ Algoritmo: First-In-First-Out (FIFO)    ║");
                    System.out.println("╚══════════════════════════════════════════╝");
                    
                    // Notifica o novo master
                    try {
                        EchoService newMasterService = (EchoService) Naming.lookup("rmi://localhost/" + newMaster);
                        newMasterService.setMaster(true);
                        System.out.println("DECISÃO DO GERENCIADOR: " + newMaster + " foi promovido a MASTER");
                        
                        // Notifica todos os outros clones sobre o novo master
                        for (String serverId : serverList) {
                            if (!serverId.equals(newMaster)) {
                                try {
                                    EchoService cloneService = (EchoService) Naming.lookup("rmi://localhost/" + serverId);
                                    cloneService.setMaster(false);
                                    System.out.println("DECISÃO DO GERENCIADOR: " + serverId + " foi informado que é CLONE");
                                } catch (Exception ex) {
                                    System.err.println("Erro ao notificar clone " + serverId + ": " + ex.getMessage());
                                }
                            }
                        }
                    } catch (Exception e) {
                        System.err.println("Erro ao promover novo master " + newMaster + ": " + e.getMessage());
                        // Se o novo master também falhou, tenta o próximo recursivamente
                        return electNewMaster();
                    }
                } else {
                    System.out.println("DECISÃO DO GERENCIADOR: Nenhum servidor disponível para assumir como master");
                }
                
                electionRequests.clear();
                return newMaster;
            } finally {
                electionInProgress = false;
            }
        }
    }
    
    @Override
    public List<String> getAllMessages() throws RemoteException {
        return new ArrayList<>(globalMessages);
    }
    
    @Override
    public void updateGlobalMessages(List<String> messages) throws RemoteException {
        synchronized (lock) {
            this.globalMessages.clear();
            this.globalMessages.addAll(messages);
            System.out.println("Lista global de mensagens atualizada. Total: " + messages.size());
        }
    }
    
    public static void main(String[] args) {
        try {
            // Cria o RMI Registry se ainda não existir
            try {
                LocateRegistry.createRegistry(1099);
                System.out.println("RMI Registry criado na porta 1099");
            } catch (Exception e) {
                System.out.println("RMI Registry já existe");
            }
            
            // Cria e registra o gerenciador
            ServerListManagerImpl manager = new ServerListManagerImpl();
            Naming.rebind("rmi://localhost/ServerListManager", manager);
            
            System.out.println("ServerListManager iniciado e registrado no RMI Registry");
            System.out.println("Aguardando registros de servidores...");
            
            // Mantém o gerenciador em execução
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                try {
                    Naming.unbind("rmi://localhost/ServerListManager");
                    System.out.println("ServerListManager encerrado");
                } catch (Exception e) {
                    System.err.println("Erro ao encerrar ServerListManager: " + e.getMessage());
                }
            }));
            
        } catch (Exception e) {
            System.err.println("Erro ao iniciar ServerListManager: " + e.getMessage());
            e.printStackTrace();
        }
    }
}