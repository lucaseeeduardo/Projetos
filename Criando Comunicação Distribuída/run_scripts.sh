#!/bin/bash

# Script para facilitar a execução do sistema de Echo com Replicação

echo "=== Sistema de Echo com Replicação Passiva ==="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se o Java está instalado
check_java() {
    if command -v java &> /dev/null; then
        java_version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
        echo -e "${GREEN}✓ Java encontrado: $java_version${NC}"
        return 0
    else
        echo -e "${RED}✗ Java não encontrado. Por favor, instale Java 11 ou superior.${NC}"
        return 1
    fi
}

# Função para verificar se o Maven está instalado
check_maven() {
    if command -v mvn &> /dev/null; then
        mvn_version=$(mvn -version | head -n 1 | awk '{print $3}')
        echo -e "${GREEN}✓ Maven encontrado: $mvn_version${NC}"
        return 0
    else
        echo -e "${RED}✗ Maven não encontrado. Por favor, instale Maven.${NC}"
        return 1
    fi
}

# Função para verificar se o Mosquitto está rodando
check_mosquitto() {
    if systemctl is-active --quiet mosquitto 2>/dev/null; then
        echo -e "${GREEN}✓ Mosquitto MQTT Broker está rodando${NC}"
        return 0
    elif command -v mosquitto &> /dev/null; then
        echo -e "${YELLOW}✓ Mosquitto instalado, mas não está rodando como serviço${NC}"
        echo -e "${YELLOW}Você pode iniciar manualmente com: mosquitto -c /etc/mosquitto/mosquitto.conf -d${NC}"
        return 0
    else
        echo -e "${RED}✗ Mosquitto MQTT Broker não encontrado${NC}"
        echo -e "${YELLOW}Instale com: sudo apt-get install mosquitto mosquitto-clients${NC}"
        return 1
    fi
}

# Função para verificar pré-requisitos
check_prerequisites() {
    echo -e "${YELLOW}Verificando pré-requisitos...${NC}"
    local all_ok=true
    
    if ! check_java; then
        all_ok=false
    fi
    
    if ! check_maven; then
        all_ok=false
    fi
    
    if ! check_mosquitto; then
        all_ok=false
    fi
    
    if [ "$all_ok" = true ]; then
        echo -e "${GREEN}✓ Todos os pré-requisitos estão OK${NC}"
        return 0
    else
        echo -e "${RED}✗ Alguns pré-requisitos não foram atendidos${NC}"
        return 1
    fi
}

# Função para compilar o projeto
compile_project() {
    echo -e "${YELLOW}Compilando projeto...${NC}"
    
    if ! check_java || ! check_maven; then
        echo -e "${RED}✗ Pré-requisitos não atendidos para compilação${NC}"
        return 1
    fi
    
    mvn clean package
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Projeto compilado com sucesso${NC}"
        echo -e "${GREEN}✓ JARs gerados em target/${NC}"
        return 0
    else
        echo -e "${RED}✗ Erro ao compilar projeto${NC}"
        return 1
    fi
}

# Função para iniciar o RMI Registry em tmux
start_rmi_registry() {
    echo -e "${YELLOW}Iniciando RMI Registry...${NC}"
    
    # Para qualquer rmiregistry em execução
    pkill -f "rmiregistry" 2>/dev/null
    
    # Mata sessão tmux anterior se existir
    tmux kill-session -t rmiregistry 2>/dev/null
    
    # Inicia RMI Registry em sessão tmux
    tmux new-session -d -s rmiregistry -- rmiregistry
    sleep 2
    
    # Verifica se está rodando
    if pgrep -f "rmiregistry" > /dev/null; then
        echo -e "${GREEN}✓ RMI Registry iniciado em sessão tmux 'rmiregistry'${NC}"
        echo -e "${YELLOW}Use 'tmux attach -t rmiregistry' para ver os logs${NC}"
        return 0
    else
        echo -e "${RED}✗ Erro ao iniciar RMI Registry${NC}"
        return 1
    fi
}

# Função para iniciar o ServerListManager
start_manager() {
    echo -e "${YELLOW}Iniciando ServerListManager...${NC}"
    
    if [ ! -f "target/server-manager-jar-with-dependencies.jar" ]; then
        echo -e "${RED}✗ JAR do ServerListManager não encontrado. Execute a compilação primeiro.${NC}"
        return 1
    fi
    
    # Mata sessão anterior se existir
    tmux kill-session -t serverlistmanager 2>/dev/null
    
    tmux new-session -d -s serverlistmanager -- java -jar target/server-manager-jar-with-dependencies.jar
    sleep 3
    echo -e "${GREEN}✓ ServerListManager iniciado em sessão tmux 'serverlistmanager'${NC}"
    echo -e "${YELLOW}Use 'tmux attach -t serverlistmanager' para ver os logs${NC}"
}

# Função para iniciar um servidor Echo
start_server() {
    local server_id=$1
    echo -e "${YELLOW}Iniciando EchoServer: $server_id...${NC}"
    
    if [ ! -f "target/echo-server-jar-with-dependencies.jar" ]; then
        echo -e "${RED}✗ JAR do EchoServer não encontrado. Execute a compilação primeiro.${NC}"
        return 1
    fi
    
    # Mata sessão anterior se existir
    tmux kill-session -t "$server_id" 2>/dev/null
    
    tmux new-session -d -s "$server_id" -- java -jar target/echo-server-jar-with-dependencies.jar "$server_id"
    sleep 2
    echo -e "${GREEN}✓ EchoServer $server_id iniciado em sessão tmux '$server_id'${NC}"
    echo -e "${YELLOW}Use 'tmux attach -t $server_id' para ver os logs${NC}"
}

# Função para iniciar o cliente
start_client() {
    echo -e "${YELLOW}Iniciando EchoClient...${NC}"
    
    if [ ! -f "target/echo-client-jar-with-dependencies.jar" ]; then
        echo -e "${RED}✗ JAR do EchoClient não encontrado. Execute a compilação primeiro.${NC}"
        return 1
    fi
    
    # Mata sessão anterior se existir
    tmux kill-session -t echoclient 2>/dev/null
    
    tmux new-session -d -s echoclient -- java -jar target/echo-client-jar-with-dependencies.jar
    echo -e "${GREEN}✓ EchoClient iniciado em sessão tmux 'echoclient'${NC}"
    echo -e "${YELLOW}Use 'tmux attach -t echoclient' para interagir com o cliente${NC}"
}

# Função para listar sessões tmux ativas
show_status() {
    echo -e "${YELLOW}Status das sessões tmux:${NC}"
    if command -v tmux &> /dev/null; then
        sessions=$(tmux list-sessions 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "$sessions"
            echo ""
            echo -e "${YELLOW}Processos Java em execução:${NC}"
            jps | grep -v "Jps"
            echo ""
            echo -e "${YELLOW}RMI Registry:${NC}"
            if pgrep -f "rmiregistry" > /dev/null; then
                echo -e "${GREEN}✓ RMI Registry está rodando${NC}"
            else
                echo -e "${RED}✗ RMI Registry não está rodando${NC}"
            fi
        else
            echo -e "${YELLOW}Nenhuma sessão tmux ativa${NC}"
        fi
    else
        echo -e "${RED}tmux não está instalado${NC}"
    fi
    echo ""
}

# Função para conectar a uma sessão tmux
connect_to_session() {
    echo -e "${YELLOW}Sessões tmux disponíveis:${NC}"
    if tmux list-sessions 2>/dev/null; then
        echo ""
        echo -e "${YELLOW}Sessões principais:${NC}"
        echo "  rmiregistry     - RMI Registry"
        echo "  serverlistmanager - Gerenciador de servidores"
        echo "  echoclient      - Cliente interativo"
        echo "  Server1         - Servidor Echo 1"
        echo "  Server2         - Servidor Echo 2"
        echo "  Server3         - Servidor Echo 3"
        echo ""
        read -p "Digite o nome da sessão para conectar (ou Enter para cancelar): " session_name
        
        if [ ! -z "$session_name" ]; then
            if tmux has-session -t "$session_name" 2>/dev/null; then
                echo -e "${GREEN}Conectando à sessão '$session_name'...${NC}"
                echo -e "${YELLOW}Use Ctrl+B depois D para desconectar sem fechar a sessão${NC}"
                sleep 2
                tmux attach -t "$session_name"
            else
                echo -e "${RED}Sessão '$session_name' não encontrada${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}Nenhuma sessão tmux ativa${NC}"
    fi
}

# Menu principal
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1) Verificar pré-requisitos"
    echo "2) Compilar projeto"
    echo "3) Iniciar sistema completo (RMI + Manager + 3 Servidores + Cliente)"
    echo "4) Iniciar apenas RMI Registry"
    echo "5) Iniciar apenas ServerListManager"
    echo "6) Adicionar novo servidor"
    echo "7) Iniciar cliente"
    echo "8) Mostrar status das sessões"
    echo "9) Conectar a uma sessão"
    echo "10) Parar todos os processos"
    echo "11) Sair"
    echo ""
}

# Loop principal
while true; do
    show_menu
    read -p "Opção: " choice
    
    case $choice in
        1)
            check_prerequisites
            ;;
        2)
            compile_project
            ;;
        3)
            # Verifica pré-requisitos
            if ! check_prerequisites; then
                echo -e "${RED}Não é possível continuar sem os pré-requisitos${NC}"
                continue
            fi
            
            # Compila se necessário
            if [ ! -f "target/server-manager-jar-with-dependencies.jar" ]; then
                echo -e "${YELLOW}JARs não encontrados. Compilando...${NC}"
                if ! compile_project; then
                    continue
                fi
            fi
            
            # Inicia componentes
            start_rmi_registry
            start_manager
            start_server "Server1"
            start_server "Server2" 
            start_server "Server3"
            sleep 2
            start_client
            
            echo -e "${GREEN}Sistema completo iniciado!${NC}"
            echo -e "${YELLOW}Use 'tmux list-sessions' para ver todas as sessões${NC}"
            ;;
        4)
            start_rmi_registry
            ;;
        5)
            start_manager
            ;;
        6)
            read -p "Digite o ID do novo servidor: " server_id
            if [ ! -z "$server_id" ]; then
                start_server "$server_id"
            else
                echo -e "${RED}ID do servidor não pode ser vazio${NC}"
            fi
            ;;
        7)
            start_client
            ;;
        8)
            show_status
            ;;
        9)
            connect_to_session
            ;;
        10)
            echo -e "${YELLOW}Parando todos os processos...${NC}"
            
            # Para sessões tmux específicas primeiro
            echo -e "${YELLOW}Finalizando sessões tmux...${NC}"
            tmux kill-session -t rmiregistry 2>/dev/null
            tmux kill-session -t serverlistmanager 2>/dev/null
            tmux kill-session -t echoclient 2>/dev/null
            tmux kill-session -t Server1 2>/dev/null
            tmux kill-session -t Server2 2>/dev/null
            tmux kill-session -t Server3 2>/dev/null
            
            # Para qualquer sessão tmux restante com números
            for i in {1..20}; do
                tmux kill-session -t "$i" 2>/dev/null
            done
            
            # Para processos Java que possam ter sobrado
            echo -e "${YELLOW}Finalizando processos Java...${NC}"
            pkill -f "java -jar" 2>/dev/null
            pkill -f "rmiregistry" 2>/dev/null
            
            # Verifica se ainda há processos rodando
            sleep 1
            remaining=$(jps | grep -v "Jps" | wc -l)
            
            if [ $remaining -eq 0 ]; then
                echo -e "${GREEN}✓ Todos os processos foram finalizados com sucesso!${NC}"
            else
                echo -e "${YELLOW}Ainda há $remaining processo(s) Java em execução:${NC}"
                jps | grep -v "Jps"
                echo -e "${YELLOW}Use 'pkill -9 java' se necessário para forçar o encerramento${NC}"
            fi
            ;;
        11)
            echo "Saindo..."
            exit 0
            ;;
        *)
            echo -e "${RED}Opção inválida${NC}"
            ;;
    esac
done