#!/bin/bash
# Script para executar o cliente Echo

# --- Configuração ---
MQTT_JAR="org.eclipse.paho.client.mqttv3-1.2.5.jar"
TARGET_CLASSES="target/classes"
CLASSPATH="$TARGET_CLASSES:$MQTT_JAR"

# Verifica se as classes foram compiladas
if [ ! -d "$TARGET_CLASSES" ]; then
    echo "Erro: Diretório target/classes não encontrado!"
    echo "Execute primeiro o script do servidor: ./run_mqtt_server.sh"
    exit 1
fi

# Verifica se o JAR MQTT existe
if [ ! -f "$MQTT_JAR" ]; then
    echo "Erro: Biblioteca MQTT não encontrada!"
    echo "Execute primeiro o script do servidor para baixar a dependência."
    exit 1
fi

# Inicia o cliente
echo "==================================="
echo "   Iniciando EchoClient"
echo "==================================="
echo ""
echo "Digite suas mensagens e pressione Enter para enviar."
echo "Digite 'exit' para sair."
echo ""

java -cp $CLASSPATH EchoClient