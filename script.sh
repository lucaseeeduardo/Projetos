#!/bin/bash
# --- Configuração ---
MQTT_JAR="org.eclipse.paho.client.mqttv3-1.2.5.jar"
TARGET_CLASSES="target/classes"
CLASSPATH="$TARGET_CLASSES:$MQTT_JAR"
SERVER_ID="Server1"

# --- 1. Download da dependência MQTT (se não existir) ---
if [ ! -f $MQTT_JAR ]; then
    echo "Baixando a biblioteca Paho MQTT..."
    wget -q https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/$MQTT_JAR
fi

# --- 2. Compilação com Maven ---
echo "Compilando projeto com Maven..."
mvn clean compile

if [ $? -ne 0 ]; then
    echo "Erro de compilação Maven. Verifique o código."
    exit 1
fi

echo "Compilação concluída com sucesso."

# --- 3. Execução ---
# Função para garantir que o ServerListManager seja encerrado
cleanup() {
    echo -e "\nEncerrando ServerListManager (PID: $MANAGER_PID)..."
    kill $MANAGER_PID 2>/dev/null
    echo "Limpeza concluída."
}

# Registra a função de limpeza para ser executada ao sair do script
trap cleanup EXIT

# 3a. Inicia o ServerListManagerImpl em background
echo "Iniciando ServerListManagerImpl..."
java -cp $CLASSPATH ServerListManagerImpl &
MANAGER_PID=$!
echo "ServerListManagerImpl iniciado em background (PID: $MANAGER_PID)."

# 3b. Aguarda para garantir que o registro RMI foi concluído
echo "Aguardando 5 segundos para o registro RMI..."
sleep 5

# 3c. Inicia o EchoServer em foreground
echo "Iniciando EchoServer com ID: $SERVER_ID"
java -cp $CLASSPATH EchoServer $SERVER_ID

# O script só continuará a partir daqui após o EchoServer ser encerrado