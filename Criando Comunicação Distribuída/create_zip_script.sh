#!/bin/bash

# Script para criar a estrutura completa do projeto e gerar um ZIP

PROJECT_NAME="echo-service-replication"
PROJECT_DIR="./$PROJECT_NAME"

echo "==================================="
echo "Criando estrutura do projeto..."
echo "==================================="

# Remove diretório anterior se existir
if [ -d "$PROJECT_DIR" ]; then
    echo "Removendo diretório anterior..."
    rm -rf "$PROJECT_DIR"
fi

# Cria estrutura de diretórios
mkdir -p "$PROJECT_DIR/src/main/java"
mkdir -p "$PROJECT_DIR/docs"

echo "Criando arquivos Java..."

# ===== INTERFACES =====

# EchoService.java
cat > "$PROJECT_DIR/src/main/java/EchoService.java" << 'EOF'
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
EOF

# ServerListManager.java
cat > "$PROJECT_DIR/src/main/java/ServerListManager.java" << 'EOF'
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
EOF

echo "Criando implementações..."

# EchoServer.java
cat > "$PROJECT_DIR/src/main/java/EchoServer.java" << 'EOF'
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Implementação do servidor de Echo com replicação e tolerância a falhas
 */
public class EchoServer extends UnicastRemoteObject implements EchoService, MqttCallback {
    
    private static final String MQTT_BROKER = "tcp://localhost:1883";
    private static final String REPLICATION_TOPIC = "echo/replication";
    private static final int HEARTBEAT_INTERVAL = 3; // segundos
    private static final int HEARTBEAT_TIMEOUT = 10; // segundos
    
    private String serverId;
    private boolean isMaster;
    private List<String> messages;
    private MqttClient mqttClient;
    private ServerListManager serverListManager;
    private ScheduledExecutorService scheduler;
    private String masterServerId;
    
    public EchoServer(String serverId) throws RemoteException {
        super();
        this.serverId = serverId;
        this.isMaster = false;
        this.messages = new CopyOnWriteArrayList<>();
        this.scheduler = Executors.newScheduledThreadPool(2);
        
        try {
            // Conecta ao MQTT Broker
            connectToMqtt();
            
            // Obtém referência ao gerenciador de lista
            serverListManager = (ServerListManager) Naming.lookup("rmi://localhost/ServerListManager");
            
            // Registra este servidor
            serverListManager.registerServer(serverId);
            
            // Verifica se é o primeiro servidor (será o master)
            List<String> serverList = serverListManager.getServerList();
            if (serverList.size() == 1 && serverList.get(0).equals(serverId)) {
                setMaster(true);
                System.out.println("Servidor " + serverId + " é o MASTER inicial");
            } else {
                // Se não é o primeiro, sincroniza mensagens e se inscreve no tópico
                syncMessages(serverListManager.getAllMessages());
                subscribeToReplicationTopic();
                System.out.println("Servidor " + serverId + " é um CLONE");
                
                // Inicia monitoramento do master
                startMasterMonitoring();
            }
            
            // Registra no RMI Registry
            Naming.rebind("rmi://localhost/" + serverId, this);
            
            System.out.println("Servidor " + serverId + " iniciado com sucesso!");
            
        } catch (Exception e) {
            e.printStackTrace();
            throw new RemoteException("Erro ao inicializar servidor: " + e.getMessage());
        }
    }
    
    private void connectToMqtt() throws MqttException {
        String clientId = "EchoServer_" + serverId + "_" + UUID.randomUUID().toString();
        MemoryPersistence persistence = new MemoryPersistence();
        
        mqttClient = new MqttClient(MQTT_BROKER, clientId, persistence);
        MqttConnectOptions connOpts = new MqttConnectOptions();
        connOpts.setCleanSession(true);
        connOpts.setAutomaticReconnect(true);
        
        mqttClient.setCallback(this);
        mqttClient.connect(connOpts);
        
        System.out.println("Conectado ao MQTT Broker: " + MQTT_BROKER);
    }
    
    private void subscribeToReplicationTopic() throws MqttException {
        if (!isMaster && mqttClient.isConnected()) {
            mqttClient.subscribe(REPLICATION_TOPIC);
            System.out.println("Inscrito no tópico: " + REPLICATION_TOPIC);
        }
    }
    
    private void unsubscribeFrom