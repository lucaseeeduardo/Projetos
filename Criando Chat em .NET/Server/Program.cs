using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Server
{
    public class ChatServer
    {
        private TcpListener _listener;
        private readonly Dictionary<string, ClientInfo> _clients = new();
        private readonly object _clientsLock = new();
        private readonly string _logFile = "server.log";
        private bool _isRunning = false;

        public class ClientInfo
        {
            public string Username { get; set; }
            public TcpClient TcpClient { get; set; }
            public NetworkStream Stream { get; set; }
            public string IPAddress { get; set; }
            public DateTime ConnectedAt { get; set; }
        }

        public class Message
        {
            public string Type { get; set; } // "text", "file", "command", "system"
            public string From { get; set; }
            public string To { get; set; }
            public string Content { get; set; }
            public byte[] FileData { get; set; }
            public string FileName { get; set; }
        }

        public async Task StartAsync(int port = 8080)
        {
            _listener = new TcpListener(IPAddress.Any, port);
            _listener.Start();
            _isRunning = true;

            Console.WriteLine($"Servidor iniciado na porta {port}");
            LogToFile($"Servidor iniciado na porta {port}");

            while (_isRunning)
            {
                try
                {
                    var tcpClient = await _listener.AcceptTcpClientAsync();
                    _ = Task.Run(() => HandleClientAsync(tcpClient));
                }
                catch (ObjectDisposedException)
                {
                    break;
                }
            }
        }

        private async Task HandleClientAsync(TcpClient tcpClient)
        {
            var clientEndpoint = tcpClient.Client.RemoteEndPoint as IPEndPoint;
            var clientIP = clientEndpoint?.Address.ToString() ?? "Unknown";
            
            Console.WriteLine($"Cliente conectado: {clientIP}");
            LogToFile($"Cliente conectado: {clientIP} em {DateTime.Now}");

            var stream = tcpClient.GetStream();
            var buffer = new byte[4096];

            try
            {
                // Primeiro, receber o nome de usuário
                var bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                if (bytesRead == 0) return;

                var username = Encoding.UTF8.GetString(buffer, 0, bytesRead).Trim();
                
                bool userExists = false;
                lock (_clientsLock)
                {
                    if (_clients.ContainsKey(username))
                    {
                        userExists = true;
                    }
                    else
                    {
                        _clients[username] = new ClientInfo
                        {
                            Username = username,
                            TcpClient = tcpClient,
                            Stream = stream,
                            IPAddress = clientIP,
                            ConnectedAt = DateTime.Now
                        };
                    }
                }

                if (userExists)
                {
                    // Nome de usuário já existe
                    var errorMsg = Encoding.UTF8.GetBytes("ERROR: Nome de usuário já existe");
                    await stream.WriteAsync(errorMsg, 0, errorMsg.Length);
                    return;
                }

                Console.WriteLine($"Usuário '{username}' conectado de {clientIP}");
                LogToFile($"Usuário '{username}' conectado de {clientIP} em {DateTime.Now}");

                // Confirmar conexão
                var welcomeMsg = Encoding.UTF8.GetBytes("OK");
                await stream.WriteAsync(welcomeMsg, 0, welcomeMsg.Length);

                // Loop principal para receber mensagens
                while (tcpClient.Connected)
                {
                    bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                    if (bytesRead == 0) break;

                    var messageJson = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    var message = JsonSerializer.Deserialize<Message>(messageJson);
                    
                    if (message != null)
                    {
                        message.From = username;
                        await ProcessMessageAsync(message);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao processar cliente: {ex.Message}");
            }
            finally
            {
                // Remover cliente da lista
                lock (_clientsLock)
                {
                    if (_clients.ContainsKey(clientEndpoint?.Address.ToString() ?? ""))
                    {
                        var username = _clients.Values.FirstOrDefault(c => c.IPAddress == clientIP)?.Username;
                        if (!string.IsNullOrEmpty(username))
                        {
                            _clients.Remove(username);
                            Console.WriteLine($"Usuário '{username}' desconectado");
                            LogToFile($"Usuário '{username}' desconectado em {DateTime.Now}");
                        }
                    }
                }
                
                tcpClient.Close();
            }
        }

        private async Task ProcessMessageAsync(Message message)
        {
            switch (message.Type)
            {
                case "command":
                    await ProcessCommandAsync(message);
                    break;
                case "text":
                case "file":
                    await RouteMessageAsync(message);
                    break;
            }
        }

        private async Task ProcessCommandAsync(Message message)
        {
            var parts = message.Content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length == 0) return;

            var command = parts[0].ToLower();

            switch (command)
            {
                case "/users":
                    await SendUserListAsync(message.From);
                    break;
                case "/sair":
                    await DisconnectUserAsync(message.From);
                    break;
            }
        }

        private async Task SendUserListAsync(string requestingUser)
        {
            ClientInfo clientInfo;
            string userList;
            
            lock (_clientsLock)
            {
                if (!_clients.ContainsKey(requestingUser)) return;
                clientInfo = _clients[requestingUser];
                userList = string.Join(", ", _clients.Keys);
            }

            var response = new Message
            {
                Type = "system",
                From = "Server",
                To = requestingUser,
                Content = $"Usuários conectados: {userList}"
            };

            var responseJson = JsonSerializer.Serialize(response);
            var responseBytes = Encoding.UTF8.GetBytes(responseJson);
            
            try
            {
                await clientInfo.Stream.WriteAsync(responseBytes, 0, responseBytes.Length);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao enviar lista de usuários para {requestingUser}: {ex.Message}");
            }
        }

        private async Task DisconnectUserAsync(string username)
        {
            lock (_clientsLock)
            {
                if (_clients.ContainsKey(username))
                {
                    try
                    {
                        _clients[username].TcpClient.Close();
                    }
                    catch { }
                    
                    _clients.Remove(username);
                    Console.WriteLine($"Usuário '{username}' desconectado por comando /sair");
                    LogToFile($"Usuário '{username}' desconectado por comando /sair em {DateTime.Now}");
                }
            }
        }

        private async Task RouteMessageAsync(Message message)
        {
            ClientInfo targetClient = null;
            ClientInfo senderClient = null;
            
            lock (_clientsLock)
            {
                if (!_clients.ContainsKey(message.To))
                {
                    // Destinatário não encontrado - preparar resposta de erro
                    if (_clients.ContainsKey(message.From))
                    {
                        senderClient = _clients[message.From];
                    }
                }
                else
                {
                    targetClient = _clients[message.To];
                }
            }

            if (targetClient == null)
            {
                // Enviar erro para o remetente
                if (senderClient != null)
                {
                    var errorResponse = new Message
                    {
                        Type = "system",
                        From = "Server",
                        To = message.From,
                        Content = $"Erro: Usuário '{message.To}' não encontrado"
                    };

                    var errorJson = JsonSerializer.Serialize(errorResponse);
                    var errorBytes = Encoding.UTF8.GetBytes(errorJson);
                    
                    try
                    {
                        await senderClient.Stream.WriteAsync(errorBytes, 0, errorBytes.Length);
                    }
                    catch { }
                }
                return;
            }

            // Enviar mensagem para o destinatário
            var messageJson = JsonSerializer.Serialize(message);
            var messageBytes = Encoding.UTF8.GetBytes(messageJson);
            
            try
            {
                await targetClient.Stream.WriteAsync(messageBytes, 0, messageBytes.Length);
                Console.WriteLine($"Mensagem roteada de '{message.From}' para '{message.To}'");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao rotear mensagem para {message.To}: {ex.Message}");
            }
        }

        private void LogToFile(string message)
        {
            try
            {
                File.AppendAllText(_logFile, $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} - {message}\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao escrever no log: {ex.Message}");
            }
        }

        public void Stop()
        {
            _isRunning = false;
            _listener?.Stop();
        }
    }

    class Program
    {
        static async Task Main(string[] args)
        {
            var server = new ChatServer();
            
            Console.WriteLine("Pressione Ctrl+C para parar o servidor");
            Console.CancelKeyPress += (sender, e) =>
            {
                e.Cancel = true;
                server.Stop();
            };

            try
            {
                await server.StartAsync();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro no servidor: {ex.Message}");
            }
        }
    }
}

