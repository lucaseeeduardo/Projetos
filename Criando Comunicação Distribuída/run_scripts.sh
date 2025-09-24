#!/bin/bash

# Script para facilitar a execução do sistema de Echo com Replicação

echo "=== Sistema de Echo com Replicação Passiva ==="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se o Mosquitto está rodando
check_mosquitto() {
    if systemctl is-active --quiet mosquitto; then
        echo -e "${GREEN}✓ Mosquitto MQTT Broker está rodando${NC}"
        return 0
    else
        echo -e "${RED}✗ Mosquitto MQTT Broker não está rodando${NC}"
        echo -e "${YELLOW}Iniciando Mosquitto...${NC}"
        sudo systemctl start mosquitto
        sleep 2
        if systemctl is-active --quiet mosquitto; then
            echo -e "${GREEN}✓ Mosquitto iniciado com sucesso${NC}"
            return 0
        else
            echo -e "${RED}Erro ao iniciar Mosquitto. Por favor, instale e inicie manualmente.${NC}"
            return 1
        fi
    fi
}

# Função para compilar o projeto
compile_project() {
    echo -e "${YELLOW}Compilando projeto...${NC}"
    mvn clean package
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Projeto compilado com sucesso${NC}"
        return 0
    else
        echo -e "${RED}✗ Erro ao compilar projeto${NC}"
        return 1
    fi
}

# Função para iniciar o ServerListManager
start_manager() {
    echo -e "${YELLOW}Iniciando ServerListManager...${NC}"
    gnome-terminal --title="ServerListManager" -- java -jar target/server-manager-jar-with-dependencies.jar &
    sleep 3
    echo -e "${GREEN}✓ ServerListManager iniciado${NC}"
}

# Função para iniciar um servidor Echo
start_server() {
    local server_id=$1
    echo -e "${YELLOW}Iniciando EchoServer: $server_id...${NC}"
    gnome-terminal --title="$server_id" -- java -jar target/echo-server-jar-with-dependencies.jar "$server_id" &
    sleep 2
    echo -e "${GREEN}✓ EchoServer $server_id iniciado${NC}"
}

# Função para iniciar o cliente
start_client() {
    echo -e "${YELLOW}Iniciando EchoClient...${NC}"
    gnome-terminal --title="EchoClient" -- java -jar target/echo-client-jar-with-dependencies.jar &
    echo -e "${GREEN}✓ EchoClient iniciado${NC}"
}

# Menu principal
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1) Compilar projeto"
    echo "2) Iniciar sistema completo (Manager + 3 Servidores + Cliente)"
    echo "3) Iniciar apenas ServerListManager"
    echo "4) Adicionar novo servidor"
    echo "5) Iniciar cliente"
    echo "6) Parar todos os processos Java"
    echo "7) Verificar status do Mosquitto"
    echo "8) Sair"
    echo ""
}

# Loop principal
while true; do
    show_menu
    read -p "Opção: " choice
    
    case $choice in
        1)
            compile_project
            ;;
        2)
            # Verifica Mosquitto
            if ! check_mosquitto; then
                echo -e "${RED}Não é possível continuar sem o Mosquitto${NC}"
                continue
            fi
            
            # Compila se necessário
            if [ ! -f "target/server-manager-jar-with-dependencies.jar" ]; then
                compile_project
            fi
            
            # Inicia componentes
            start_manager
            start_server "Server1"
            start_server "Server2"
            start_server "Server3"
            sleep 2
            start_client
            
            echo -e "${GREEN}Sistema completo iniciado!${NC}"
            ;;
        3)
            start_manager
            ;;
        4)
            read -p "Digite o ID do novo servidor: " server_id
            if [ ! -z "$server_id" ]; then
                start_server "$server_id"
            else
                echo -e "${RED}ID do servidor não pode ser vazio${NC}"
            fi
            ;;
        5)
            start_client
            ;;
        6)
            echo -e "${YELLOW}Parando todos os processos Java...${NC}"
            pkill -f "java -jar"
            echo -e "${GREEN}✓ Processos parados${NC}"
            ;;
        7)
            check_mosquitto
            ;;
        8)
            echo "Saindo..."
            exit 0
            ;;
        *)
            echo -e "${RED}Opção inválida${NC}"
            ;;
    esac
done