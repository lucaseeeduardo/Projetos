#!/bin/bash

# Script para conectar rapidamente às sessões tmux do sistema Echo

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Conexão Rápida às Sessões tmux ==="
echo ""

# Verifica se há sessões ativas
if ! tmux list-sessions &>/dev/null; then
    echo -e "${RED}Nenhuma sessão tmux ativa${NC}"
    echo "Execute './run_scripts.sh' para iniciar o sistema"
    exit 1
fi

echo -e "${YELLOW}Sessões disponíveis:${NC}"
echo ""
echo "1) rmiregistry       - RMI Registry"
echo "2) serverlistmanager - Gerenciador de servidores" 
echo "3) echoclient        - Cliente interativo"
echo "4) Server1           - Servidor Echo 1"
echo "5) Server2           - Servidor Echo 2"
echo "6) Server3           - Servidor Echo 3"
echo "7) Listar todas as sessões"
echo "8) Sair"
echo ""

read -p "Escolha uma opção: " choice

case $choice in
    1)
        session="rmiregistry"
        ;;
    2)
        session="serverlistmanager"
        ;;
    3)
        session="echoclient"
        ;;
    4)
        session="Server1"
        ;;
    5)
        session="Server2"
        ;;
    6)
        session="Server3"
        ;;
    7)
        echo -e "${YELLOW}Todas as sessões ativas:${NC}"
        tmux list-sessions
        echo ""
        read -p "Digite o nome da sessão: " session
        ;;
    8)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo -e "${RED}Opção inválida${NC}"
        exit 1
        ;;
esac

if [ ! -z "$session" ]; then
    if tmux has-session -t "$session" 2>/dev/null; then
        echo -e "${GREEN}Conectando à sessão '$session'...${NC}"
        echo -e "${YELLOW}Use Ctrl+B depois D para desconectar sem fechar a sessão${NC}"
        sleep 2
        tmux attach -t "$session"
    else
        echo -e "${RED}Sessão '$session' não encontrada${NC}"
        echo "Sessões disponíveis:"
        tmux list-sessions
    fi
fi