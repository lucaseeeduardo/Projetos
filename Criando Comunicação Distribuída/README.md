# Sistema de Echo com Replicação Passiva

Este projeto implementa um serviço de Echo distribuído usando RMI (Remote Method Invocation) e MQTT, com replicação passiva para tolerância a falhas.

## Arquitetura

- **ServerListManager**: Gerencia a lista de servidores ativos e elege o servidor mestre
- **EchoServer**: Implementa o serviço de Echo e participa do sistema de replicação
- **EchoClient**: Cliente que consome o serviço de Echo
- **MQTT**: Usado para comunicação entre os servidores para eleição de líder
- **RMI**: Usado para comunicação cliente-servidor

## Pré-requisitos

- **Java 11+**
- **Maven 3.6+**
- **Mosquitto MQTT Broker**
- **tmux** (para gerenciamento de sessões)

### Instalação dos Pré-requisitos (Ubuntu/Debian)

```bash
# Java (se não estiver instalado)
sudo apt update
sudo apt install openjdk-11-jdk

# Maven
sudo apt install maven

# Mosquitto MQTT Broker
sudo apt install mosquitto mosquitto-clients

# tmux
sudo apt install tmux

# Iniciar Mosquitto
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

## Como Executar

### Opção 1: Script Automatizado (Recomendado)

```bash
# Dar permissão de execução
chmod +x run_scripts.sh

# Executar o script
./run_scripts.sh
```

O script oferece as seguintes opções:
1. **Verificar pré-requisitos** - Verifica se Java, Maven e Mosquitto estão instalados
2. **Compilar projeto** - Compila e gera os JARs executáveis
3. **Iniciar sistema completo** - Inicia RMI Registry, Manager, 3 Servidores e Cliente
4. **Iniciar apenas RMI Registry** - Inicia apenas o RMI Registry
5. **Iniciar apenas ServerListManager** - Inicia apenas o gerenciador de servidores
6. **Adicionar novo servidor** - Adiciona um novo servidor ao sistema
7. **Iniciar cliente** - Inicia apenas o cliente
8. **Mostrar status das sessões** - Mostra sessões tmux ativas
9. **Parar todos os processos** - Para todos os processos Java e tmux
10. **Sair** - Sai do script

### Opção 2: Execução Manual

```bash
# 1. Compilar o projeto
mvn clean package

# 2. Iniciar RMI Registry (em um terminal)
rmiregistry &

# 3. Iniciar ServerListManager (em outro terminal)
java -jar target/server-manager-jar-with-dependencies.jar

# 4. Iniciar servidores Echo (em terminais separados)
java -jar target/echo-server-jar-with-dependencies.jar Server1
java -jar target/echo-server-jar-with-dependencies.jar Server2
java -jar target/echo-server-jar-with-dependencies.jar Server3

# 5. Iniciar cliente (em outro terminal)
java -jar target/echo-client-jar-with-dependencies.jar
```

## Gerenciamento de Sessões com tmux

O script usa tmux para gerenciar as sessões. Comandos úteis:

```bash
# Listar sessões ativas
tmux list-sessions

# Conectar a uma sessão específica
tmux attach -t serverlistmanager
tmux attach -t Server1
tmux attach -t echoclient

# Desconectar de uma sessão (dentro da sessão)
Ctrl+B, depois D

# Parar todas as sessões
tmux kill-server
```

## Estrutura de Arquivos

```
├── src/main/java/
│   ├── EchoClient.java              # Cliente do sistema
│   ├── EchoServer.java              # Implementação do servidor Echo
│   ├── EchoService.java             # Interface do serviço Echo
│   ├── ServerListManager.java       # Interface do gerenciador de servidores
│   └── ServerListManagerImpl.java   # Implementação do gerenciador
├── target/
│   ├── echo-client-jar-with-dependencies.jar
│   ├── echo-server-jar-with-dependencies.jar
│   └── server-manager-jar-with-dependencies.jar
├── pom.xml                          # Configuração Maven
├── run_scripts.sh                   # Script de execução
└── README.md                        # Este arquivo
```

## Funcionalidades

- **Replicação Passiva**: O sistema elege um servidor mestre que processa as requisições
- **Tolerância a Falhas**: Se o servidor mestre falhar, um novo é eleito automaticamente
- **Comunicação RMI**: Cliente se comunica com servidores via RMI
- **MQTT para Eleição**: Servidores usam MQTT para coordenação e eleição de líder
- **Monitoramento**: Scripts permitem monitorar o status do sistema

## Solução de Problemas

### Java não encontrado
```bash
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Maven não encontrado
```bash
sudo apt install maven
```

### Mosquitto não está rodando
```bash
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```

### Erro de compilação "No sources to compile"
Os arquivos Java devem estar em `src/main/java/`. O script já corrige isso automaticamente.

### JARs não encontrados
Execute a compilação primeiro: `mvn clean package`

## Logs e Debugging

- Use `tmux attach -t <sessão>` para ver logs em tempo real
- Logs do Mosquitto: `sudo journalctl -u mosquitto -f`
- Verificar processos Java: `jps -l`