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
    
    private void unsubscribeFromReplicationTopic() throws MqttException {
        if (mqttClient.isConnected() && mqttClient.isConnected()) {
            mqttClient.unsubscribe(REPLICATION_TOPIC);
            System.out.println("Desinscrito do tópico: " + REPLICATION_TOPIC);
        }
    }
    
    @Override
    public String echo(String message) throws RemoteException {
        if (!isMaster) {
            throw new RemoteException("Apenas o servidor master pode processar requisições de echo");
        }
        
        // Adiciona timestamp à mensagem
        String timestampedMessage = "[" + new Date() + "] " + message;
        
        // Adiciona à lista local
        messages.add(timestampedMessage);
        
        // Atualiza lista global
        try {
            serverListManager.updateGlobalMessages(messages);
        } catch (Exception e) {
            System.err.println("Erro ao atualizar lista global: " + e.getMessage());
        }
        
        // Publica mensagem para replicação via MQTT
        try {
            publishMessage(timestampedMessage);
        } catch (MqttException e) {
            System.err.println("Erro ao publicar mensagem MQTT: " + e.getMessage());
        }
        
        System.out.println("Echo processado: " + timestampedMessage);
        return timestampedMessage;
    }
    
    private void publishMessage(String message) throws MqttException {
        if (isMaster && mqttClient.isConnected()) {
            MqttMessage mqttMessage = new MqttMessage(message.getBytes());
            mqttMessage.setQos(2); // QoS 2 para garantia de entrega exatamente uma vez
            mqttClient.publish(REPLICATION_TOPIC, mqttMessage);
            System.out.println("Mensagem publicada para replicação: " + message);
        }
    }
    
    @Override
    public List<String> getListOfMsg() throws RemoteException {
        return new ArrayList<>(messages);
    }
    
    @Override
    public boolean isAlive() throws RemoteException {
        return true;
    }
    
    @Override
    public String getServerId() throws RemoteException {
        return serverId;
    }
    
    @Override
    public void setMaster(boolean isMaster) throws RemoteException {
        this.isMaster = isMaster;
        
        try {
            if (isMaster) {
                // Se tornou master, desinscreve do tópico de replicação
                unsubscribeFromReplicationTopic();
                System.out.println("Servidor " + serverId + " agora é MASTER");
            } else {
                // Se tornou clone, inscreve no tópico de replicação
                subscribeToReplicationTopic();
                System.out.println("Servidor " + serverId + " agora é CLONE");
            }
        } catch (MqttException e) {
            System.err.println("Erro ao alterar status de inscrição MQTT: " + e.getMessage());
        }
    }
    
    @Override
    public boolean isMaster() throws RemoteException {
        return isMaster;
    }
    
    @Override
    public void syncMessages(List<String> messages) throws RemoteException {
        this.messages.clear();
        this.messages.addAll(messages);
        System.out.println("Mensagens sincronizadas. Total: " + messages.size());
    }
    
    // Callbacks MQTT
    @Override
    public void connectionLost(Throwable cause) {
        System.err.println("Conexão MQTT perdida: " + cause.getMessage());
        // Tenta reconectar
        try {
            Thread.sleep(5000);
            connectToMqtt();
            if (!isMaster) {
                subscribeToReplicationTopic();
            }
        } catch (Exception e) {
            System.err.println("Erro ao reconectar: " + e.getMessage());
        }
    }
    
    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        if (!isMaster && topic.equals(REPLICATION_TOPIC)) {
            String receivedMessage = new String(message.getPayload());
            messages.add(receivedMessage);
            System.out.println("Mensagem replicada recebida: " + receivedMessage);
        }
    }
    
    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // Callback quando a entrega é completa
    }
    
    private void startMasterMonitoring() {
        scheduler.scheduleWithFixedDelay(() -> {
            try {
                if (!isMaster) {
                    String currentMaster = serverListManager.getMasterServer();
                    if (currentMaster != null && !currentMaster.equals(masterServerId)) {
                        masterServerId = currentMaster;
                    }
                    
                    if (masterServerId != null) {
                        try {
                            EchoService master = (EchoService) Naming.lookup("rmi://localhost/" + masterServerId);
                            master.isAlive();
                        } catch (Exception e) {
                            System.err.println("Master " + masterServerId + " não responde. Solicitando eleição ao gerenciador...");
                            requestElectionFromManager();
                        }
                    }
                }
            } catch (Exception e) {
                System.err.println("Erro no monitoramento: " + e.getMessage());
            }
        }, HEARTBEAT_INTERVAL, HEARTBEAT_INTERVAL, TimeUnit.SECONDS);
    }
    
    private void requestElectionFromManager() {
        try {
            System.out.println("Clone " + serverId + " detectou falha e está solicitando eleição ao ServerListManager");
            String newMaster = serverListManager.requestElection(serverId);
            
            if (newMaster != null && newMaster.equals(serverId)) {
                // Este servidor foi eleito pelo gerenciador como novo master
                System.out.println("NOTIFICAÇÃO: ServerListManager elegeu este servidor (" + serverId + ") como novo MASTER!");
                masterServerId = serverId;
            } else if (newMaster != null) {
                masterServerId = newMaster;
                System.out.println("NOTIFICAÇÃO: ServerListManager elegeu " + newMaster + " como novo MASTER");
            }
        } catch (Exception e) {
            System.err.println("Erro ao solicitar eleição: " + e.getMessage());
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
            
            // Gera ID único para o servidor ou usa o fornecido
            String serverId = (args.length > 0) ? args[0] : "EchoServer_" + System.currentTimeMillis();
            
            EchoServer server = new EchoServer(serverId);
            
            // Mantém o servidor em execução
            System.out.println("Servidor " + serverId + " aguardando requisições...");
            
            // Adiciona shutdown hook para limpeza
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                try {
                    server.scheduler.shutdown();
                    if (server.mqttClient != null && server.mqttClient.isConnected()) {
                        server.mqttClient.disconnect();
                        server.mqttClient.close();
                    }
                    server.serverListManager.removeServer(serverId);
                    Naming.unbind("rmi://localhost/" + serverId);
                    System.out.println("Servidor " + serverId + " encerrado corretamente");
                } catch (Exception e) {
                    System.err.println("Erro ao encerrar servidor: " + e.getMessage());
                }
            }));
            
        } catch (Exception e) {
            System.err.println("Erro ao iniciar servidor: " + e.getMessage());
            e.printStackTrace();
        }
    }
}