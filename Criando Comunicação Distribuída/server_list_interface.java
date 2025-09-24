import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

/**
 * Interface para gerenciar a lista de servidores ativos
 * Utilizado para coordenação e eleição de master
 */
public interface ServerListManager extends Remote {
    
    /**
     * Registra um novo servidor na lista
     * @param serverName Nome do servidor no registro RMI
     * @throws RemoteException
     */
    void registerServer(String serverName) throws RemoteException;
    
    /**
     * Remove um servidor da lista (quando detectada falha)
     * @param serverName Nome do servidor a remover
     * @throws RemoteException
     */
    void removeServer(String serverName) throws RemoteException;
    
    /**
     * Obtém a lista ordenada de servidores ativos
     * @return Lista de nomes dos servidores
     * @throws RemoteException
     */
    List<String> getServerList() throws RemoteException;
    
    /**
     * Obtém o nome do servidor master atual
     * @return Nome do servidor master
     * @throws RemoteException
     */
    String getMasterServer() throws RemoteException;
    
    /**
     * Elege um novo master (remove o antigo e promove o próximo)
     * @return Nome do novo servidor master
     * @throws RemoteException
     */
    String electNewMaster() throws RemoteException;
    
    /**
     * Solicita eleição de novo master (chamado pelos clones ao detectar falha)
     * @param requestingServer Servidor que está solicitando a eleição
     * @return Nome do novo servidor master eleito
     * @throws RemoteException
     */
    String requestElection(String requestingServer) throws RemoteException;
    
    /**
     * Verifica periodicamente a saúde do master atual
     * @return true se o master está ativo, false caso contrário
     * @throws RemoteException
     */
    boolean checkMasterHealth() throws RemoteException;
    
    /**
     * Obtém todas as mensagens do sistema (para sincronização)
     * @return Lista de mensagens
     * @throws RemoteException
     */
    List<String> getAllMessages() throws RemoteException;
    
    /**
     * Atualiza a lista de mensagens globais
     * @param messages Lista de mensagens atualizada
     * @throws RemoteException
     */
    void updateGlobalMessages(List<String> messages) throws RemoteException;
}