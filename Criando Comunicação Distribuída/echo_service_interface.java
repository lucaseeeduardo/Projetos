import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

/**
 * Interface RMI para o serviço de Echo com replicação
 */
public interface EchoService extends Remote {
    
    /**
     * Método echo que retorna a mensagem enviada e replica para os servidores clone
     * @param message Mensagem a ser ecoada
     * @return Mensagem ecoada
     * @throws RemoteException
     */
    String echo(String message) throws RemoteException;
    
    /**
     * Obtém a lista de todas as mensagens já ecoadas
     * @return Lista de mensagens
     * @throws RemoteException
     */
    List<String> getListOfMsg() throws RemoteException;
    
    /**
     * Verifica se o servidor está ativo (heartbeat)
     * @return true se o servidor está ativo
     * @throws RemoteException
     */
    boolean isAlive() throws RemoteException;
    
    /**
     * Obtém o ID do servidor
     * @return ID do servidor
     * @throws RemoteException
     */
    String getServerId() throws RemoteException;
    
    /**
     * Define se o servidor é master ou clone
     * @param isMaster true se for master
     * @throws RemoteException
     */
    void setMaster(boolean isMaster) throws RemoteException;
    
    /**
     * Verifica se o servidor é master
     * @return true se for master
     * @throws RemoteException
     */
    boolean isMaster() throws RemoteException;
    
    /**
     * Sincroniza mensagens com um novo servidor
     * @param messages Lista de mensagens para sincronização
     * @throws RemoteException
     */
    void syncMessages(List<String> messages) throws RemoteException;
}