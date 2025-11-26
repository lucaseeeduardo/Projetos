# Sistema de Echo com Replicação Passiva

Este projeto implementa um serviço de Echo distribuído usando RMI e MQTT, com replicação passiva e tolerância a falhas.

## 1. Instalar Dependências (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install openjdk-11-jdk maven mosquitto mosquitto-clients tmux wget
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

## 2. Iniciar o Sistema

```bash
chmod +x run_scripts.sh
./run_scripts.sh
# Escolha a opção 1 (Setup Completo)
```

## 3. Entrar como Cliente e Mandar Mensagem

```bash
tmux attach -t echoclient
# Digite sua mensagem e pressione Enter
# Use 'exit' para sair do cliente
```

## 4. Obter Mensagens dos Servidores

```bash
tmux attach -t Server1
# Veja o log do servidor master
tmux attach -t Server2
# Veja o log do servidor backup
```
Ou, no cliente:
```bash
# No prompt do cliente, digite:
list
# Para ver o histórico de mensagens
```

## 5. Matar um Servidor e Testar Failover

```bash
tmux kill-session -t Server1
# Aguarde alguns segundos para o sistema eleger um novo master

tmux attach -t echoclient
# Envie uma nova mensagem

# Veja o histórico novamente:
list
```

## Dicas

- Para listar sessões tmux: `tmux list-sessions`
- Para conectar/desconectar: `tmux attach -t <sessão>` / `Ctrl+B D`
- Para reiniciar o sistema: pare tudo pelo menu do script e inicie novamente

Pronto para uso.