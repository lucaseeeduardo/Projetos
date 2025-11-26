#!/bin/bash
# filepath: /home/personal/Projetos/Criando Comunicação Distribuída/run_scripts.sh

# === Configuração ===
MQTT_JAR="org.eclipse.paho.client.mqttv3-1.2.5.jar"
TARGET_CLASSES="target/classes"
CLASSPATH="$TARGET_CLASSES:$MQTT_JAR"
NUM_SERVERS=20 # Quantidade de servidores Echo a serem iniciados

# === Cores para o output ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem Cor

# --- Funções de Verificação e Setup ---

# Função para verificar pré-requisitos
check_prerequisites() {
    echo -e "${YELLOW}Verificando pré-requisitos...${NC}"
    local all_ok=true
    command -v java &>/dev/null || { echo -e "${RED}✗ Java não encontrado.${NC}"; all_ok=false; }
    command -v mvn &>/dev/null || { echo -e "${RED}✗ Maven não encontrado.${NC}"; all_ok=false; }
    command -v tmux &>/dev/null || { echo -e "${RED}✗ tmux não encontrado.${NC}"; all_ok=false; }
    (systemctl is-active --quiet mosquitto || pgrep -x "mosquitto" > /dev/null) || { echo -e "${RED}✗ Broker Mosquitto não está rodando.${NC}"; all_ok=false; }

    if [ "$all_ok" = true ]; then
        echo -e "${GREEN}✓ Todos os pré-requisitos estão OK.${NC}"
        return 0
    else
        echo -e "${RED}✗ Instale as dependências faltantes e inicie o Mosquitto.${NC}"
        return 1
    fi
}

# Função para baixar dependência MQTT
download_mqtt_dep() {
    if [ ! -f "$MQTT_JAR" ]; then
        echo -e "${YELLOW}Baixando dependência MQTT ($MQTT_JAR)...${NC}"
        wget -q https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/$MQTT_JAR
        echo -e "${GREEN}✓ Download concluído.${NC}"
    fi
}

# Função para compilar o projeto
compile_project() {
    echo -e "${YELLOW}Compilando o projeto com 'mvn clean compile'...${NC}"
    mvn clean compile
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Projeto compilado com sucesso.${NC}"
        return 0
    else
        echo -e "${RED}✗ Falha na compilação.${NC}"
        return 1
    fi
}

# --- Funções de Controle do Sistema ---

# Função para parar todos os processos
stop_all() {
    echo -e "${YELLOW}Parando todos os processos...${NC}"
    # A linha do rmiregistry foi removida pois ele agora é gerenciado pelo ServerListManager
    tmux kill-session -t serverlistmanager 2>/dev/null
    tmux kill-session -t echoclient 2>/dev/null
    for i in $(seq 1 $NUM_SERVERS); do
        tmux kill-session -t "Server$i" 2>/dev/null
    done
    pkill -f "java -cp $CLASSPATH" 2>/dev/null
    echo -e "${GREEN}✓ Processos finalizados.${NC}"
}

# Função para iniciar o sistema completo
start_all() {
    stop_all # Garante um ambiente limpo
    echo -e "${YELLOW}Iniciando o sistema completo...${NC}"

    # 1. Iniciar ServerListManager (que agora também inicia o RMI Registry)
    echo "Iniciando ServerListManager..."
    tmux new-session -d -s serverlistmanager "java -cp $CLASSPATH ServerListManagerImpl"
    
    # 2. Pausa CRÍTICA para garantir que o Manager e o Registry estejam prontos
    echo -e "${YELLOW}Aguardando 5 segundos para o ServerListManager se registrar...${NC}"
    sleep 5

    # 3. Iniciar EchoServers
    echo "Iniciando $NUM_SERVERS EchoServer(s)..."
    for i in $(seq 1 $NUM_SERVERS); do
        tmux new-session -d -s "Server$i" "java -cp $CLASSPATH EchoServer Server$i"
        sleep 0.3
    done

    echo -e "${GREEN}✓ Sistema iniciado! Use a opção 'Anexar a uma sessão' para interagir.${NC}"
}

# Função para iniciar apenas o cliente
start_client() {
    echo -e "${YELLOW}Iniciando o cliente em uma nova sessão tmux...${NC}"
    tmux kill-session -t echoclient 2>/dev/null
    # Inicia o cliente e anexa diretamente
    tmux new-session -s echoclient "java -cp $CLASSPATH EchoClient"
}

# Função para anexar a uma sessão
attach_session() {
    echo -e "${YELLOW}Sessões tmux ativas:${NC}"
    tmux list-sessions -F '#S'
    echo ""
    read -p "Digite o nome da sessão para anexar: " session_name
    if tmux has-session -t "$session_name" 2>/dev/null; then
        tmux attach-session -t "$session_name"
    else
        echo -e "${RED}Sessão '$session_name' não encontrada.${NC}"
    fi
}

# --- Menu Principal ---
while true; do
    echo ""
    echo "=== Menu Principal ==="
    echo "1. Setup Completo (Verificar, Compilar e Iniciar Tudo)"
    echo "2. Iniciar Sistema (RMI, Manager, Servidores)"
    echo "3. Parar Tudo"
    echo "4. Iniciar Cliente Interativo"
    echo "5. Anexar a uma sessão tmux (Ver Logs)"
    echo "6. Apenas Compilar Projeto"
    echo "7. Sair"
    echo ""
    read -p "Escolha uma opção: " choice

    case $choice in
        1)
            check_prerequisites && download_mqtt_dep && compile_project && start_all
            ;;
        2)
            start_all
            ;;
        3)
            stop_all
            ;;
        4)
            start_client
            ;;
        5)
            attach_session
            ;;
        6)
            download_mqtt_dep && compile_project
            ;;
        7)
            echo "Saindo..."
            exit 0
            ;;
        *)
            echo -e "${RED}Opção inválida. Tente novamente.${NC}"
            ;;
    esac
done