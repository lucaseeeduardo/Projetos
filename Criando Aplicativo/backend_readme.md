# Backend - Sistema de Agendamento de Serviços

## 📋 Descrição

API REST desenvolvida em Java com Spring Boot para gerenciamento de agendamentos de serviços.

## 🛠️ Tecnologias Utilizadas

- **Java 17**
- **Spring Boot 3.1.5**
- **Spring Data JPA**
- **MySQL 8.0**
- **Maven**
- **Lombok**

## 📁 Estrutura do Projeto

```
src/main/java/com/agendamento/
├── model/              # Entidades JPA
│   ├── Prestador.java
│   ├── HorarioDisponivel.java
│   └── Agendamento.java
├── dto/                # Data Transfer Objects
│   ├── PrestadorDTO.java
│   ├── HorarioDisponivelDTO.java
│   └── AgendamentoDTO.java
├── repository/         # Interfaces JPA Repository
│   ├── PrestadorRepository.java
│   ├── HorarioDisponivelRepository.java
│   └── AgendamentoRepository.java
├── service/            # Lógica de negócio
│   ├── PrestadorService.java
│   ├── HorarioDisponivelService.java
│   └── AgendamentoService.java
├── controller/         # Endpoints REST
│   ├── PrestadorController.java
│   ├── HorarioDisponivelController.java
│   └── AgendamentoController.java
└── AgendamentoApplication.java  # Classe principal
```

## ⚙️ Configuração

### 1. Pré-requisitos

- JDK 17 ou superior
- Maven 3.6+
- MySQL 8.0
- IDE (IntelliJ IDEA, Eclipse ou VS Code)

### 2. Configurar Banco de Dados

Criar banco de dados MySQL:

```sql
CREATE DATABASE agendamento_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configurar application.properties

Editar `src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/agendamento_db?createDatabaseIfNotExist=true
spring.datasource.username=seu_usuario
spring.datasource.password=sua_senha
```

## 🚀 Como Executar

### Opção 1: Via Maven (Terminal)

```bash
# Navegar até o diretório do projeto
cd backend

# Compilar o projeto
mvn clean install

# Executar a aplicação
mvn spring-boot:run
```

### Opção 2: Via IDE

1. Importar o projeto como projeto Maven
2. Aguardar download das dependências
3. Executar a classe `AgendamentoApplication.java`

### Opção 3: JAR executável

```bash
# Gerar o JAR
mvn clean package

# Executar o JAR
java -jar target/agendamento-servicos-1.0.0.jar
```

## 📡 Endpoints da API

### Prestadores

- `GET /api/prestadores` - Listar todos os prestadores
- `GET /api/prestadores/ativos` - Listar prestadores ativos
- `GET /api/prestadores/{id}` - Buscar prestador por ID
- `POST /api/prestadores` - Criar novo prestador
- `PUT /api/prestadores/{id}` - Atualizar prestador
- `DELETE /api/prestadores/{id}` - Desativar prestador
- `GET /api/prestadores/buscar?termo=X` - Buscar prestadores

### Horários Disponíveis

- `GET /api/horarios/prestador/{id}` - Listar horários de um prestador
- `GET /api/horarios/prestador/{id}/data/{data}` - Horários em data específica
- `GET /api/horarios/prestador/{id}/periodo?dataInicio=X&dataFim=Y` - Horários em período
- `POST /api/horarios` - Criar horário disponível
- `DELETE /api/horarios/{id}` - Remover horário

### Agendamentos

- `GET /api/agendamentos` - Listar todos os agendamentos
- `GET /api/agendamentos/prestador/{id}` - Agendamentos de um prestador
- `GET /api/agendamentos/{id}` - Buscar agendamento por ID
- `POST /api/agendamentos` - Criar agendamento
- `PATCH /api/agendamentos/{id}/confirmar` - Confirmar agendamento
- `PATCH /api/agendamentos/{id}/cancelar` - Cancelar agendamento

## 📝 Exemplos de Requisições

### Criar Prestador

```json
POST /api/prestadores
{
  "nome": "Dr. João Silva",
  "especialidade": "Dentista",
  "email": "joao@email.com",
  "telefone": "(47) 99999-9999",
  "descricao": "Especialista em ortodontia",
  "precoHora": 150.00,
  "ativo": true
}
```

### Criar Horário Disponível

```json
POST /api/horarios
{
  "prestadorId": 1,
  "data": "2024-11-20",
  "horaInicio": "09:00:00",
  "horaFim": "10:00:00"
}
```

### Criar Agendamento

```json
POST /api/agendamentos
{
  "prestadorId": 1,
  "nomeCliente": "Maria Santos",
  "emailCliente": "maria@email.com",
  "telefoneCliente": "(47) 98888-8888",
  "data": "2024-11-20",
  "horaInicio": "09:00:00",
  "horaFim": "10:00:00",
  "observacoes": "Primeira consulta"
}
```

## 🔒 Regras de Negócio

1. **Gestão de Conflitos**: Sistema valida automaticamente conflitos de horários
2. **Status de Agendamento**: PENDENTE → CONFIRMADO → CONCLUIDO ou CANCELADO
3. **Disponibilidade**: Horários ficam indisponíveis ao serem agendados
4. **Cancelamento**: Libera automaticamente os horários

## 🧪 Testando a API

### Com cURL:

```bash
# Listar prestadores
curl http://localhost:8080/api/prestadores

# Criar prestador
curl -X POST http://localhost:8080/api/prestadores \
  -H "Content-Type: application/json" \
  -d '{"nome":"Dr. João","especialidade":"Dentista","email":"joao@email.com"}'
```

### Com Postman/Insomnia:

1. Importar collection com os endpoints acima
2. Configurar base URL: `http://localhost:8080`
3. Testar os endpoints

## 🐛 Troubleshooting

### Erro de conexão com MySQL

- Verificar se o MySQL está rodando
- Confirmar usuário e senha no `application.properties`
- Verificar se o banco foi criado

### Porta 8080 em uso

Alterar porta no `application.properties`:
```properties
server.port=8081
```

### Erro de compilação

```bash
mvn clean install -U
```

## 📚 Documentação Adicional

- [Spring Boot](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [MySQL](https://dev.mysql.com/doc/)

## 👥 Equipe

[Inserir nomes dos integrantes]

## 📄 Licença

Projeto acadêmico - [Nome da Instituição]