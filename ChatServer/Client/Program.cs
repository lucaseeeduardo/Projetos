using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Client
{
    public class ChatClient
    {
        private TcpClient? _tcpClient;
        private NetworkStream? _stream;
        private string? _username;
        private bool _isConnected = false;
        private bool _userCreatedOnServer = false;

        public class Message
        {
            public string? Type { get; set; } // "text", "file", "command", "system"
            public string? From { get; set; }
            public string? To { get; set; }
            public string? Content { get; set; }
            public byte[]? FileData { get; set; }
            public string? FileName { get; set; }
        }

        public async Task<bool> ConnectAsync(string serverAddress, int port, string username)
        {
            try
            {
                _tcpClient = new TcpClient();
                await _tcpClient.ConnectAsync(serverAddress, port);
                _stream = _tcpClient.GetStream();
                _username = username;

                // Enviar nome de usuário
                var usernameBytes = Encoding.UTF8.GetBytes(username);
                await _stream.WriteAsync(usernameBytes, 0, usernameBytes.Length);

                // Aguardar resposta do servidor
                var buffer = new byte[1024];
                var bytesRead = await _stream.ReadAsync(buffer, 0, buffer.Length);
                var response = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                if (response == "OK")
                {
                    _isConnected = true;
                    _userCreatedOnServer = true; // Usuário criado no servidor após primeira mensagem
                    Console.WriteLine($"Conectado ao servidor como '{username}'");
                    Console.WriteLine("Digite '/help' para ver os comandos disponíveis");
                    
                    // Iniciar thread para receber mensagens
                    _ = Task.Run(ReceiveMessagesAsync);
                    
                    return true;
                }
                else
                {
                    Console.WriteLine($"Erro ao conectar: {response}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao conectar: {ex.Message}");
                return false;
            }
        }

        private async Task ReceiveMessagesAsync()
        {
            var buffer = new byte[8192];
            
            while (_isConnected && _tcpClient.Connected)
            {
                try
                {
                    var bytesRead = await _stream.ReadAsync(buffer, 0, buffer.Length);
                    if (bytesRead == 0) break;

                    var messageJson = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    var message = JsonSerializer.Deserialize<Message>(messageJson);

                    if (message != null)
                    {
                        await ProcessReceivedMessageAsync(message);
                    }
                }
                catch (Exception ex)
                {
                    if (_isConnected)
                    {
                        Console.WriteLine($"Erro ao receber mensagem: {ex.Message}");
                    }
                    break;
                }
            }
        }

        private async Task ProcessReceivedMessageAsync(Message message)
        {
            switch (message.Type)
            {
                case "text":
                    Console.WriteLine($"\n[{message.From}]: {message.Content}");
                    break;
                case "file":
                    await SaveReceivedFileAsync(message);
                    break;
                case "system":
                    Console.WriteLine($"\n[Sistema]: {message.Content}");
                    break;
            }
            
            // Mostrar prompt novamente
            Console.Write($"{_username}> ");
        }

        private async Task SaveReceivedFileAsync(Message message)
        {
            try
            {
                await File.WriteAllBytesAsync(message.FileName, message.FileData);
                Console.WriteLine($"\n[{message.From}] enviou o arquivo: {message.FileName} (salvo no diretório atual)");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nErro ao salvar arquivo {message.FileName}: {ex.Message}");
            }
        }

        public async Task SendMessageAsync(string input)
        {
            if (!_isConnected) return;

            try
            {
                if (input.StartsWith("/"))
                {
                    await ProcessCommandAsync(input);
                }
                else
                {
                    Console.WriteLine("Use o comando '/send message <destinatario> <mensagem>' para enviar mensagens");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao enviar mensagem: {ex.Message}");
            }
        }

        private async Task ProcessCommandAsync(string input)
        {
            var parts = input.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length == 0) return;

            var command = parts[0].ToLower();

            switch (command)
            {
                case "/help":
                    ShowHelp();
                    break;
                case "/users":
                    await SendCommandAsync("/users");
                    break;
                case "/sair":
                    await SendCommandAsync("/sair");
                    Disconnect();
                    break;
                case "/send":
                    await ProcessSendCommandAsync(parts);
                    break;
                default:
                    Console.WriteLine("Comando não reconhecido. Digite '/help' para ver os comandos disponíveis.");
                    break;
            }
        }

        private void ShowHelp()
        {
            Console.WriteLine("\nComandos disponíveis:");
            Console.WriteLine("/send message <destinatario> <mensagem> - Enviar mensagem de texto");
            Console.WriteLine("/send file <destinatario> <caminho_do_arquivo> - Enviar arquivo");
            Console.WriteLine("/users - Listar usuários conectados");
            Console.WriteLine("/sair - Sair do chat");
            Console.WriteLine("/help - Mostrar esta ajuda");
        }

        private async Task ProcessSendCommandAsync(string[] parts)
        {
            if (parts.Length < 4)
            {
                Console.WriteLine("Uso: /send message <destinatario> <mensagem> ou /send file <destinatario> <caminho_do_arquivo>");
                return;
            }

            var sendType = parts[1].ToLower();
            var recipient = parts[2];

            switch (sendType)
            {
                case "message":
                    var messageContent = string.Join(" ", parts, 3, parts.Length - 3);
                    await SendTextMessageAsync(recipient, messageContent);
                    break;
                case "file":
                    var filePath = parts[3];
                    await SendFileAsync(recipient, filePath);
                    break;
                default:
                    Console.WriteLine("Tipo de envio inválido. Use 'message' ou 'file'.");
                    break;
            }
        }

        private async Task SendTextMessageAsync(string recipient, string content)
        {
            var message = new Message
            {
                Type = "text",
                To = recipient,
                Content = content
            };

            await SendMessageToServerAsync(message);
        }

        private async Task SendFileAsync(string recipient, string filePath)
        {
            try
            {
                if (!File.Exists(filePath))
                {
                    Console.WriteLine($"Arquivo não encontrado: {filePath}");
                    return;
                }

                var fileData = await File.ReadAllBytesAsync(filePath);
                var fileName = Path.GetFileName(filePath);

                var message = new Message
                {
                    Type = "file",
                    To = recipient,
                    Content = $"Arquivo: {fileName}",
                    FileData = fileData,
                    FileName = fileName
                };

                await SendMessageToServerAsync(message);
                Console.WriteLine($"Arquivo '{fileName}' enviado para {recipient}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao enviar arquivo: {ex.Message}");
            }
        }

        private async Task SendCommandAsync(string command)
        {
            var message = new Message
            {
                Type = "command",
                Content = command
            };

            await SendMessageToServerAsync(message);
        }

        private async Task SendMessageToServerAsync(Message message)
        {
            try
            {
                var messageJson = JsonSerializer.Serialize(message);
                var messageBytes = Encoding.UTF8.GetBytes(messageJson);
                await _stream.WriteAsync(messageBytes, 0, messageBytes.Length);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao enviar para servidor: {ex.Message}");
            }
        }

        public void Disconnect()
        {
            _isConnected = false;
            _stream?.Close();
            _tcpClient?.Close();
            Console.WriteLine("Desconectado do servidor.");
        }

        public async Task SendExitCommandAsync()
        {
            System.Console.WriteLine("\nEnviando comando de saída ao servidor...");
            System.Console.WriteLine("user created on server: " + _userCreatedOnServer);
            System.Console.WriteLine("is connected: " + _isConnected);
            if (_userCreatedOnServer && _isConnected)
            {
                await SendCommandAsync("/sair");
                System.Console.WriteLine("Comando de saída enviado.");
            }
        }
    }

    class Program
    {
        private static ChatClient? _client;
        private static bool _exitRequested = false;
        private static readonly object _lockObject = new object();
        private static readonly ManualResetEventSlim _exitCompleted = new ManualResetEventSlim(false);

        static async Task Main(string[] args)
        {
            Console.WriteLine("=== Cliente de Chat ===");

            // Configurar manipulador de Ctrl+C
            Console.CancelKeyPress += async (sender, e) =>
            {
                lock (_lockObject)
                {
                    if (_exitRequested) return; // Evitar execução múltipla
                    _exitRequested = true;
                }
                e.Cancel = true;

                Console.WriteLine("\nInterrupção detectada. Enviando comando de saída...");
                if (_client != null)
                {
                    await _client.SendExitCommandAsync();
                }
                _exitCompleted.Set();
            };

            Console.Write("Digite seu nome de usuário: ");
            var username = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(username))
            {
                Console.WriteLine("Nome de usuário inválido.");
                return;
            }

            Console.Write("Digite o endereço do servidor (padrão: localhost): ");
            var serverAddress = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(serverAddress))
                serverAddress = "localhost";

            Console.Write("Digite a porta do servidor (padrão: 8080): ");
            var portInput = Console.ReadLine();
            if (!int.TryParse(portInput, out int port))
                port = 8080;

            _client = new ChatClient();

            if (await _client.ConnectAsync(serverAddress, port, username))
            {
                Console.WriteLine("\nDigite suas mensagens ou comandos:");

                string? input;
                while ((input = Console.ReadLine()) != null)
                {
                    if (input.ToLower() == "/sair")
                    {
                        await _client.SendMessageAsync(input);
                        break;
                    }

                    await _client.SendMessageAsync(input);
                    Console.Write($"{username}> ");
                }
                // aqui fiquei em dúvida, porque o ctrl + c ativa ao mesmo tempo a saída do while e as funções de cancel. 
                // O += imagino que seja por isso.
                await Task.Delay(200); 
                bool wasExitRequested;
                lock (_lockObject)
                {
                    wasExitRequested = _exitRequested;
                }

                if (wasExitRequested)
                {
                    Console.WriteLine("Aguardando processamento do comando de saída...");
                    _exitCompleted.Wait(); // Bloqueia até o manipulador terminar
                    Console.WriteLine("Comando de saída processado completamente.");
                }

            }
            else
            {
                Console.WriteLine("Não foi possível conectar ao servidor.");
            }

            if (!_exitRequested)
            {
                _client.Disconnect();
            }
            Console.WriteLine("Pressione qualquer tecla para sair...");
            Console.ReadKey();
        }
    }
}

