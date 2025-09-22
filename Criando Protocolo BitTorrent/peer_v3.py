#!/usr/bin/env python3

import socket
import threading
import time
import argparse
import os
import math
import random
import logging
import select

# --- Configuração ---
PIECE_SIZE = 100 * 1024  # Tamanho de cada pedaço em bytes (100 KB)
UPDATE_INTERVAL = 30     # Segundos entre as atualizações do tracker
REQUEST_TIMEOUT = 60     # Segundos para esperar por uma resposta de pedaço
MAX_CONNECTIONS = 5      # Máximo de downloads/uploads simultâneos
LOG_LEVEL = logging.INFO # Nível de log para exibição de mensagens
# ---------------------

# --- Configuração de Log ---
logging.basicConfig(level=LOG_LEVEL,
                    format="%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s")
# ---------------------

# --- Estado Global ---
# Dicionário para armazenar informações dos peers conhecidos. A chave é o ID do peer (IP:Porta).
# Cada valor contém o IP, a porta TCP e um conjunto de índices dos pedaços que o peer possui.
known_peers = {}  # { peer_id: {"ip": ip, "tcp_port": port, "pieces": set()} }
owned_pieces = set() # Conjunto de índices dos pedaços que este peer possui.
total_pieces = 0     # Número total de pedaços do arquivo alvo.
target_file_path = "" # Caminho para o arquivo que está sendo compartilhado ou baixado.
output_file_path = "" # Caminho para o arquivo de saída (onde os pedaços baixados são salvos).
piece_hashes = [] # Opcional: Para verificar a integridade dos pedaços (não implementado neste exemplo).
my_tcp_port = 0      # Porta TCP que este peer está escutando.
my_ip = ""           # Endereço IP deste peer.
tracker_addr = None  # Endereço (IP, Porta) do tracker.
peer_id = ""         # ID único deste peer (IP:Porta).
shutdown_flag = threading.Event() # Flag para sinalizar o encerramento das threads.
state_lock = threading.Lock() # Lock para proteger o acesso a `known_peers` e `owned_pieces` (recursos compartilhados).
# --------------------

def get_my_ip():
    """Determina qual é o IP local."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # esse jeito de pegar o ip é tipo fazer o sistema operacional definir qual é a interface de rede e o ip local utilizados para se conectar ao servidor dns do google.
        # a conexão em si não acontece, porque é udp em uma porta pra tcp, mas é útil pra que o SO me mostre o ip local e eu possa obter esse valor.
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        if ip == "127.0.0.1" :
            ip = "0.0.0.0"
        
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def parse_peer_list(peer_list_str):
    """Converte a lista de peers (string) que o tracker manda para um dicionário de peers.
    A string PEERLIST é formatada como: PEERLIST [ip1:porta1:[pedacos];ip2:porta2:[pedacos]]
    """
    peers = {}
    # Remove o prefixo "PEERLIST " e os colchetes externos.
    content = peer_list_str.strip("PEERLIST []")
    if not content:
        return peers

    # Divide a string em entradas individuais de peer.
    peer_entries = content.split(";")
    for entry in peer_entries:
        try:
            # Divide cada entrada em IP, porta e lista de pedaços.
            parts = entry.split(":")
            ip = parts[0]
            port = int(parts[1])
            # Remove os colchetes da string de pedaços e divide por vírgula.
            pieces_str = parts[2].strip("[]")
            pieces = set()
            if pieces_str:
                # Converte os pedaços para um conjunto de inteiros.
                pieces = set(map(int, pieces_str.split(",")))

            entry_peer_id = f"{ip}:{port}"
            # Não adiciona a si mesmo à lista de peers conhecidos.
            if entry_peer_id != peer_id:
                peers[entry_peer_id] = {"ip": ip, "tcp_port": port, "pieces": pieces}
        except (IndexError, ValueError) as e:
            logging.warning(f"Falha ao analisar a entrada do peer \t{entry}\t: {e}")
    return peers

def update_known_peers(new_peers):
    """Atualiza o dicionário `known_peers` com novas informações de peers.
    Utiliza um lock para garantir a segurança da thread ao acessar `known_peers`.
    """
    # o state lock é para travar o acesso ao "known_peers";
    with state_lock:
        known_peers.update(new_peers)
        # esse if aqui é pra tirar eu mesmo da lista e não criar conexão de eu com eu.
        if peer_id in known_peers:
            del known_peers[peer_id]
    logging.debug(f"Peers conhecidos atualizado: {len(known_peers)} peers")

def send_tracker_update(udp_sock):
    """Envia a lista atual de pedaços possuídos para o tracker.
    A mensagem é formatada como: UPDATE <minha_porta_tcp> [<pedacos_possuidos>]
    """
    print("Etrnou aqui - 1")
    with state_lock:
        # Converte o conjunto de pedaços possuídos para uma string separada por vírgulas.
        pieces_str = ",".join(map(str, sorted(list(owned_pieces))))
    message = f"UPDATE {my_tcp_port} [{pieces_str}]"
    try:
        # Envia a mensagem UDP para o tracker.
        udp_sock.sendto(message.encode("utf-8"), tracker_addr)
        logging.info(f"Enviado UPDATE para o tracker: {len(owned_pieces)} pedaços")
    except socket.error as e:
        logging.error(f"Erro de socket ao enviar UPDATE para o tracker: {e}")
    except Exception as e:
        logging.error(f"Erro ao enviar UPDATE para o tracker: {e}")

def tracker_update_thread(udp_sock):
    """Função da thread para enviar periodicamente atualizações para o tracker.
    Esta thread executa em loop, enviando atualizações e esperando por um intervalo definido.
    """
    logging.info("Thread de atualização do tracker iniciada.")
    while not shutdown_flag.is_set():
        send_tracker_update(udp_sock)
        # Espera pelo intervalo de atualização ou até que a flag de desligamento seja ativada.
        shutdown_flag.wait(UPDATE_INTERVAL)
    logging.info("Thread de atualização do tracker parada.")

def handle_peer_connection(conn, addr):
    """Lida com uma conexão TCP de entrada de outro peer solicitando um pedaço.
    Recebe a solicitação, verifica se o pedaço é possuído e o envia de volta.
    """
    logging.debug(f"Conexão de entrada de {addr}")
    try:
        # Define um timeout para a conexão.
        conn.settimeout(REQUEST_TIMEOUT)
        # Recebe os dados da solicitação.
        data = conn.recv(1024)
        if not data:
            logging.warning(f"Nenhum dado recebido de {addr}")
            return

        message = data.decode("utf-8")
        logging.debug(f"Requisição recebida de {addr}: {message}")
        # Se a mensagem for "SIZE", envia o tamanho total do arquivo.
        if message.strip() == "SIZE":
            file_size = os.path.getsize(target_file_path)
            conn.sendall(str(file_size).encode("utf-8"))
            return
        # se a mensagem começar com GET, então tá mandando um pedido de pedaço, daí manda esse pedaço no sendall ali embaixo
        # notar que o sendall é um loop que itera sobre os bytes até enviar todos os bytes, mesmo que sejam muitos bytes
        # o ideal aqui não seria ele fazer só um chamada? já que cada piece é um pacote de bytes fechado. 
        # avaliar a diff do buffer do sendall ali com o buffer máximo do socket
        # Se a mensagem for uma solicitação GET para um pedaço.
        if message.startswith("GET "):
            try:
                # Extrai o índice do pedaço da mensagem.
                piece_index = int(message.split(" ")[1])
                logging.info(f"Peer {addr} solicitou o pedaço {piece_index}")

                with state_lock:
                    # Verifica se o pedaço solicitado é possuído por este peer.
                    has_piece = piece_index in owned_pieces

                if has_piece:
                    # Lê os dados do pedaço do arquivo.
                    piece_data = read_piece(piece_index)
                    if piece_data:
                        logging.info(f"Enviando pedaço {piece_index} ({len(piece_data)} bytes) para {addr}")
                        # sendall significa que envia todos os dados, mesmo que sejam muitos bytes
                        # Isso é importante para garantir que o peer receba o arquivo completo
                        conn.sendall(piece_data)
                    else:
                        logging.error(f"Falha ao ler o pedaço {piece_index} para {addr}")
                        # Opcionalmente, enviar uma mensagem de erro de volta.
                else:
                    logging.warning(f"Não possui o pedaço {piece_index} solicitado por {addr}")
                    # Opcionalmente, enviar uma mensagem indicando que o pedaço não foi encontrado.

            except (IndexError, ValueError):
                logging.warning(f"Formato de requisição GET inválido de {addr}: {message}")
        else:
            logging.warning(f"Comando desconhecido de {addr}: {message}")

    except socket.timeout:
        logging.warning(f"Timeout ao lidar com a conexão de {addr}")
    except socket.error as e:
        logging.error(f"Erro de socket com {addr}: {e}")
    except Exception as e:
        logging.error(f"Erro ao lidar com a conexão de {addr}: {e}", exc_info=True)
    finally:
        # Fecha a conexão.
        conn.close()
        logging.debug(f"Conexão de {addr} fechada")

def tcp_server_thread():
    """Função da thread para escutar conexões TCP de entrada de outros peers.
    Aceita novas conexões e as delega para threads separadas para lidar com as solicitações.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        # Vincula o socket do servidor ao IP e porta especificados.
        server_sock.bind(("0.0.0.0", my_tcp_port))
        # Começa a escutar por conexões de entrada.
        server_sock.listen(MAX_CONNECTIONS)
        logging.info(f"Servidor TCP escutando em {my_ip}:{my_tcp_port}")

        while not shutdown_flag.is_set():
            # Usa select para aceitar conexões de forma não bloqueante com timeout.
            readable, _, _ = select.select([server_sock], [], [], 1.0) # Timeout de 1 segundo
            if server_sock in readable:
                try:
                    # Aceita uma nova conexão.
                    conn, addr = server_sock.accept()
                    # Lida com a conexão em uma nova thread para permitir múltiplos uploads simultâneos.
                    handler_thread = threading.Thread(target=handle_peer_connection, args=(conn, addr), daemon=True)
                    handler_thread.start()
                except socket.error as e:
                    # Evita mensagem de erro durante o desligamento.
                    if not shutdown_flag.is_set():
                         logging.error(f"Erro de socket ao aceitar conexão: {e}")
                except Exception as e:
                    if not shutdown_flag.is_set():
                         logging.error(f"Erro ao aceitar conexão: {e}", exc_info=True)

    except OSError as e:
        logging.critical(f"Falha ao vincular o servidor TCP a {my_ip}:{my_tcp_port}. Erro: {e}")
        # Sinaliza outras threads para parar em caso de erro crítico.
        shutdown_flag.set() 
    except Exception as e:
        logging.critical(f"Erro inesperado do servidor TCP: {e}", exc_info=True)
        shutdown_flag.set()
    finally:
        logging.info("Thread do servidor TCP parando.")
        # Fecha o socket do servidor.
        server_sock.close()
        logging.info("Socket do servidor TCP fechado.")

def calculate_rarity():
    """Calcula a raridade de cada pedaço com base nos peers conhecidos.
    A raridade é o número de peers que possuem um determinado pedaço.
    """
    rarity = {i: 0 for i in range(total_pieces)}
    with state_lock:
        if not known_peers:
             # Se nenhum peer for conhecido, assume que todos os pedaços são igualmente raros (ou inatingíveis).
             # Isso evita divisão por zero ou comportamento estranho se o tracker retornar uma lista vazia inicialmente.
             return rarity
        for peer_data in known_peers.values():
            for piece_index in peer_data["pieces"]:
                if piece_index in rarity:
                    rarity[piece_index] += 1
    return rarity

def choose_piece_to_download():
    """Escolhe o próximo pedaço para baixar com base na raridade (o mais raro primeiro).
    Prioriza pedaços que são possuídos por menos peers.
    """
    rarity = calculate_rarity()
    with state_lock:
        # Identifica os pedaços que ainda não foram baixados.
        needed_pieces = list(set(range(total_pieces)) - owned_pieces)

    if not needed_pieces:
        return None, None # Todos os pedaços foram baixados.

    # Ordena os pedaços necessários por raridade (ascendente), e aleatoriamente para desempate.
    needed_pieces.sort(key=lambda i: (rarity.get(i, 0), random.random()))

    rarest_needed_piece = needed_pieces[0]

    # Encontra peers que possuem este pedaço.
    peers_with_piece = []
    with state_lock:
        for p_id, data in known_peers.items():
            if rarest_needed_piece in data["pieces"]:
                peers_with_piece.append(p_id)

    if not peers_with_piece:
        logging.warning(f"Nenhum peer conhecido possui o pedaço mais raro necessário {rarest_needed_piece}. Tentando novamente.")
        return None, None # Não é possível baixar este pedaço agora.

    # Escolhe um peer aleatório entre aqueles que possuem o pedaço.
    chosen_peer_id = random.choice(peers_with_piece)
    with state_lock:
        # Garante que o peer ainda existe (pode ter sido removido entre as verificações).
        if chosen_peer_id in known_peers:
             chosen_peer_info = known_peers[chosen_peer_id]
        else:
             logging.warning(f"Peer {chosen_peer_id} desapareceu antes da seleção.")
             return None, None

    logging.info(f"Pedaço escolhido {rarest_needed_piece} (raridade: {rarity.get(rarest_needed_piece, 0)}) do peer {chosen_peer_id}")
    return rarest_needed_piece, chosen_peer_info

def download_piece(piece_index, peer_info, udp_sock):
    """Tenta baixar um pedaço específico de um determinado peer.
    Estabelece uma conexão TCP com o peer, solicita o pedaço e o recebe.
    """
    global target_file_path

    peer_addr = (peer_info["ip"], peer_info["tcp_port"])
    logging.info(f"Tentando baixar o pedaço {piece_index} de {peer_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(REQUEST_TIMEOUT)
    try:
        if peer_addr == "127.0.0.1":
            peer_addr = "0.0.0.0"
            
        # Conecta-se ao peer.
        sock.connect(peer_addr)
        # Envia a solicitação GET para o pedaço.
        message = f"GET {piece_index}"
        sock.sendall(message.encode("utf-8"))
        # Recebe os dados do pedaço.
        received_data = b""
        expected_size = get_piece_size(piece_index)
        while len(received_data) < expected_size:
            # Lê os dados em blocos.
            chunk = sock.recv(4096) 
            print("received chunk: ", len(chunk))
            if not chunk:
                logging.error(f"Conexão fechada por {peer_addr} durante o download do pedaço {piece_index}. Recebido {len(received_data)}/{expected_size} bytes.")
                break # Conexão interrompida.
            received_data += chunk

        if len(received_data) != expected_size:
             logging.warning(f"Dados recebidos ({len(received_data)}) é diferente do esperado ({expected_size}) para o pedaço {piece_index} from {peer_addr}. Truncating.")
             received_data = received_data[:expected_size]
        logging.info(f"Recebido {len(received_data)} de {expected_size}")

        logging.info(f"Pedaço {piece_index} ({len(received_data)} bytes) recebido com sucesso de {peer_addr}")

        # --- Opcional: Verificar o hash do pedaço aqui --- #

        # Escreve o pedaço no arquivo.
        if write_piece(piece_index, received_data):
            with state_lock:
                # Adiciona o pedaço aos pedaços possuídos.
                owned_pieces.add(piece_index)
            logging.info(f"Pedaço {piece_index} salvo com sucesso. Possuídos: {len(owned_pieces)}/{total_pieces}")
            # Informa imediatamente o tracker sobre o novo pedaço.
            # Considerar fazer isso com menos frequência se causar muito tráfego.
            send_tracker_update(udp_sock) # Precisa do udp_sock aqui.
            if len(owned_pieces) == total_pieces:
                logging.info("Todos os pedaços baixados! Download completo.")
                # Opcionalmente, enviar uma atualização final para o tracker.
                # Renomeia o arquivo após o download completo.

                novo_nome = target_file_path.replace("incompleto", "")
                
                try:
                    os.rename(target_file_path, novo_nome)
                    logging.info(f"Arquivo renomeado para: {novo_nome}")
                    target_file_path = novo_nome
                except Exception as e:
                    logging.error(f"Erro ao renomear arquivo: {e}")

            return True
        else:
            logging.error(f"Falha ao escrever o pedaço {piece_index} no arquivo.")
            return False

    except socket.timeout:
        logging.warning(f"Timeout ao conectar ou baixar de {peer_addr} para o pedaço {piece_index}")
        return False
    except socket.error as e:
        logging.error(f"Erro de socket ao baixar o pedaço {piece_index} de {peer_addr}: {e}")
        return False
    except Exception as e:
        logging.error(f"Erro ao baixar o pedaço {piece_index} de {peer_addr}: {e}", exc_info=True)
        return False
    finally:
        # Fecha o socket.
        sock.close()

def get_piece_size(piece_index):
    """Calcula o tamanho de um pedaço específico, lidando com o último pedaço que pode ser menor.
    """
    global total_pieces
    try:
        file_size = os.path.getsize(target_file_path)
        if piece_index < total_pieces - 1:
            return PIECE_SIZE
        else:
            # O último pedaço pode ser menor que PIECE_SIZE.
            return file_size - (piece_index * PIECE_SIZE)
    except OSError as e:
        logging.error(f"Erro ao obter o tamanho do arquivo para {target_file_path}: {e}")
        # Retorna o tamanho padrão do pedaço como fallback, pode causar problemas.
        return PIECE_SIZE

def read_piece(piece_index):
    """Lê um pedaço específico do arquivo alvo.
    Abre o arquivo, busca a posição inicial do pedaço e lê a quantidade de bytes correspondente.
    """
    try:
        with open(target_file_path, "rb") as f:
            # Calcula o deslocamento inicial do pedaço no arquivo.
            start_offset = piece_index * PIECE_SIZE
            f.seek(start_offset)
            # Obtém o tamanho exato do pedaço a ser lido.
            size_to_read = get_piece_size(piece_index)
            # Lê os dados do pedaço.
            piece_data = f.read(size_to_read)
            if len(piece_data) != size_to_read:
                 logging.warning(f"Dados incompletos lidos para o pedaço {piece_index}. Esperado {size_to_read}, obtido {len(piece_data)}.")
                 # Decide como lidar com isso - talvez retornar None ou levantar um erro.
            return piece_data
    except OSError as e:
        logging.error(f"Erro ao ler o pedaço {piece_index} de {target_file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao ler o pedaço {piece_index}: {e}", exc_info=True)
        return None

def write_piece(piece_index, data):
    """Escreve um pedaço baixado na posição correta no arquivo de saída.
    Abre o arquivo em modo de leitura/escrita binária e busca a posição para escrever.
    """
    try:
        # Usa r+b para permitir a escrita sem truncar o arquivo.
        with open(target_file_path, "r+b") as f:
            # Calcula o deslocamento inicial para escrever o pedaço.
            start_offset = piece_index * PIECE_SIZE
            f.seek(start_offset)
            # Escreve os dados do pedaço.
            f.write(data)
        return True
    except OSError as e:
        logging.error(f"Erro ao escrever o pedaço {piece_index} em {target_file_path}: {e}")
        return False
    except Exception as e:
        logging.error(f"Erro inesperado ao escrever o pedaço {piece_index}: {e}", exc_info=True)
        return False

def initialize_output_file(file_size):
    """Cria ou garante que o arquivo de saída exista com o tamanho correto, preenchido com bytes nulos.
    Isso pré-aloca o espaço necessário para o arquivo.
    """
    try:
        # Cria os diretórios pai se não existirem.
        os.makedirs(os.path.dirname(target_file_path) or ".", exist_ok=True)
        # Se o arquivo não existir ou tiver um tamanho diferente, ele é criado/redimensionado.
        if not os.path.exists(target_file_path) or os.path.getsize(target_file_path) != file_size:
            with open(target_file_path, "wb") as f:
                # Busca a posição final do arquivo e escreve um byte nulo para pré-alocar o espaço.
                f.seek(file_size-1)
                f.write(b"\0")
        logging.info(f"Output criado/completo: {target_file_path} ({file_size} bytes)")


    except OSError as e:
        logging.critical(f"Falha ao inicializar o arquivo de saída {target_file_path}: {e}")
        return False
    except Exception as e:
        logging.critical(f"Erro inesperado ao inicializar o arquivo de saída: {e}", exc_info=True)
        return False
    return True

def download_manager(udp_sock):
    """Lógica principal para gerenciar o processo de download.
    Em um loop, escolhe um pedaço para baixar, tenta baixá-lo e atualiza o estado.
    """
    logging.info("Gerenciador de download iniciado.")
    is_seeder = False # Inicializa como não seeder para o loop de download
    while not shutdown_flag.is_set():
        with state_lock:
            # Verifica se todos os pedaços foram baixados.
            if len(owned_pieces) == total_pieces:
                logging.info("Download completo! Todos os pedaços adquiridos.")
                
                is_seeder = True # Se todos os pedaços foram baixados, este peer se torna um seeder.
                send_tracker_update(udp_sock) # Atualização final para o tracker.
                logging.info("Enviado pro tracker update")
                break # Sai do loop de download.

        # Escolhe o próximo pedaço para baixar e o peer de quem baixar.
        piece_index, peer_info = choose_piece_to_download()

        if piece_index is not None and peer_info is not None:
            # Tenta baixar o pedaço.
            if download_piece(piece_index, peer_info, udp_sock):
                # Sucesso, o loop continuará para escolher o próximo pedaço.
                # Envia atualização imediatamente após obter um pedaço.
                send_tracker_update(udp_sock)
                pass
            else:
                # Falha, espera um pouco antes de tentar novamente.
                logging.warning(f"Falha ao baixar o pedaço {piece_index}. Esperando antes de tentar novamente.")
                shutdown_flag.wait(5) # Espera 5 segundos antes de tentar o próximo pedaço.
        else:
            # Nenhum pedaço disponível ou nenhum peer o possui, espera antes de verificar novamente.
            with state_lock:
                 needed_count = total_pieces - len(owned_pieces)
            if needed_count > 0:
                 logging.info(f"Nenhum pedaço/peer adequado encontrado. Ainda faltam {needed_count} pedaços. Esperando...")
                 shutdown_flag.wait(10) # Espera 10 segundos.
            else:
                 # Deveria ter sido capturado pela verificação no início do loop.
                 logging.info("Download parece completo, mas o loop continuou. Saindo.")
                 break

    logging.info("Gerenciador de download parado.")
    # Se o download foi concluído (peer se tornou seeder), entra no modo seeder.
    if is_seeder:
        logging.info("Modo Seeder: servindo até Ctrl+C")
        try:
            while not shutdown_flag.is_set():
                shutdown_flag.wait(timeout=1.0)
        except KeyboardInterrupt:
            logging.info("Ctrl+C recebido no seeder. Finalizando...")
            shutdown_flag.set()


def main():
    global total_pieces, target_file_path, my_tcp_port, my_ip, tracker_addr, peer_id, is_seeder

    parser = argparse.ArgumentParser(description="P2P File Sharing Client (Simulação do BitTorrent).")
    parser.add_argument("target_file", help="Caminho do arquivo alvo pra compartilhar/baixar.")
    parser.add_argument("--tracker", required=True, help="Tracker IP:PORTA.")
    parser.add_argument("--listen-port", type=int, required=True, help="Porta TCP para comunicação entre peers.")
    args = parser.parse_args()

    my_tcp_port = args.listen_port 
    target_file_path = args.target_file
    # Verifica se o arquivo alvo já existe, indicando que este peer é um seeder.
    is_seeder = os.path.exists(target_file_path)
    
    # Leecher: o nome passa a ser teste2.pdfincompleto
    # Se não for um seeder (leecher), adiciona "incompleto" ao nome do arquivo.
    if not is_seeder:
        target_file_path += "incompleto"

    # Validar arquivo alvo
    # Se for um seeder, verifica se o arquivo alvo existe e é um arquivo válido.
    if not os.path.isfile(target_file_path) and is_seeder:
        logging.critical(f"Arquivo alvo não existe ou não é um arquivo: {target_file_path}")
        return
    
    # Se for um seeder, calcula o número total de pedaços e marca todos como possuídos.
    if is_seeder:
        try:
            file_size = os.path.getsize(target_file_path)

            if file_size == 0:
                logging.critical(f"Arquivo alvo está vazio: {target_file_path}")
                return
            
            # Calcula o número total de pedaços com base no tamanho do arquivo e PIECE_SIZE.
            total_pieces = math.ceil(file_size / PIECE_SIZE)
            logging.info(f"Arquivo local compartilhado: {target_file_path}, Tamanho: {file_size} bytes, Pedaços: {total_pieces}")

            # Assim que identifica que é seeder, já manda update pro tracker de quantos pedaços possui.
            # Marca todos os pedaços como possuídos por este seeder.
            owned_pieces.update(range(total_pieces))
        except OSError as e:
            logging.critical(f"Não foi possível encontrar o arquivo alvo: {e}")
            return

    # Aqui pega a tring de IP:PORTA e faz split da string pra obter ambos em variáveis separadas.
    # Analisa o endereço do tracker fornecido na linha de comando.
    try:
        tracker_host, tracker_port_str = args.tracker.split(":")
        tracker_port = int(tracker_port_str)
        tracker_addr = (tracker_host, tracker_port)
    except (ValueError, IndexError):
        logging.critical(f"Endereço do tracker inválido. Precisa ser HOST:PORT. Retorno: {args.tracker}")
        return

    # Aqui eu pego o meu ip e a porta 
    # Obtém o IP local e define o ID do peer.
    my_ip = get_my_ip()
    peer_id = f"{my_ip}:{my_tcp_port}"
    logging.info(f"Peer local (EU) com IP: {peer_id}")
    
    # --- Criação do socket UDP para comunicação com o tracker ---
    # Cria um socket UDP para enviar e receber mensagens do tracker.
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.settimeout(5.0) # Timeout para esperar a resposta do tracker.

    # --- JOIN inicial com o Tracker ---
    # Envia uma mensagem JOIN para o tracker para se registrar na rede.
    join_message = f"JOIN {my_ip} {my_tcp_port}"
    try:
        logging.info(f"TRK1: Enviando JOIN para o tracker {tracker_addr}")
        udp_sock.sendto(join_message.encode("utf-8"), tracker_addr)

        # aqui entendo que 2048 seja suficiente, sabendo que pode haver muitos peers e dar erro por buffer overflow talvez?
        # Recebe a resposta do tracker, que deve conter a lista de peers (PEERLIST).
        data, _ = udp_sock.recvfrom(2048) # Buffer maior para a lista de peers.
        response = data.decode("utf-8")
        print("Lista de peeer recebida do trackr ", response)
        
        if response.startswith("PEERLIST"):
            # Analisa a lista de peers recebida e atualiza os peers conhecidos.
            initial_peers = parse_peer_list(response)
            update_known_peers(initial_peers)
            logging.info(f"TRK 2: Tracker respondeu: {len(initial_peers)} peers")
        else:
            logging.warning(f"Resposta inesperada do tracker após JOIN: {response}")

    except socket.timeout:
        logging.error("Timeout esperando a resposta inicial do tracker após JOIN.")
        # Decide se deve tentar novamente ou sair.
        udp_sock.close()
        return
    except socket.error as e:
        logging.error(f"Erro de socket durante o JOIN inicial: {e}")
        udp_sock.close()
        return
    except Exception as e:
        logging.error(f"Erro durante o JOIN inicial: {e}")
        udp_sock.close()
        return
    
    # Se não for um seeder, precisa obter o tamanho total do arquivo de um peer.
    if not is_seeder:
        # Tenta obter o tamanho do arquivo de um peer disponível.
        first_peer = next(iter(known_peers.values()), None)
        if not first_peer:
            logging.critical("Nenhum seeder disponível para metadata. Abortando.")
            return

        # Conecta-se ao primeiro peer para solicitar o tamanho do arquivo.
        size_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        size_sock.settimeout(REQUEST_TIMEOUT)
        size_sock.connect((first_peer["ip"], first_peer["tcp_port"]))
        size_sock.sendall(b"SIZE")
        resp = size_sock.recv(64)
        file_size = int(resp.decode("utf-8"))
        size_sock.close()

        # atualize total_pieces e recrie output com esse tamanho
        # Atualiza o número total de pedaços e inicializa o arquivo de saída com o tamanho correto.
        total_pieces = math.ceil(file_size / PIECE_SIZE)
        logging.info(f"Tamanho do arquivo dinâmico recebido: {file_size} bytes, Pedaços: {total_pieces}")
        # agora re-initialize passando o tamanho em vez de ler do target
        if not initialize_output_file(file_size):
            logging.critical("Erro ao criar arquivo no leecher.")
            return
        
    # --- Determina os pedaços inicialmente possuídos (se o arquivo existir e corresponder ao alvo) ---
    # Para simplificar, assume-se que começamos com zero pedaços, a menos que a saída seja igual ao alvo.
    if is_seeder:
         logging.info("Atuando como um seeder (arquivo de saída é o arquivo alvo). Assumindo que todos os pedaços são possuídos.")
         with state_lock:
              # Se for um seeder, todos os pedaços são marcados como possuídos.
              owned_pieces.update(range(total_pieces))
    else:
         # TODO: Implementar verificação de pedaços para retomar downloads, se necessário.
         logging.info("Iniciando download. Assumindo zero pedaços inicialmente.")
         pass


    # --- Iniciar Threads ---
    threads = []
    try:
        # Thread do Servidor TCP
        # essa thread tcp_server_thread escuta na porta TCP especificada e aceita conexões de outros peers
        # Inicia a thread que escuta por conexões TCP de outros peers.
        tcp_server = threading.Thread(target=tcp_server_thread, name="TCPServer", daemon=True)
        #entender melhor esse threads.append, pra que serve
        threads.append(tcp_server)
        tcp_server.start()

        # Thread de Atualização do Tracker
        # Inicia a thread que periodicamente envia atualizações para o tracker.
        tracker_updater = threading.Thread(target=tracker_update_thread, args=(udp_sock,), name="TrackerUpdate", daemon=True)
        threads.append(tracker_updater)
        tracker_updater.start()

        # Gerenciador de Download (executa na thread principal ou em sua própria thread)
        # Running in main thread for simplicity here
        # Se não for um seeder, inicia o gerenciador de download.
        if not is_seeder:
            download_manager(udp_sock)
        else:
            # Se for um seeder, permanece ativo servindo arquivos até ser interrompido.
            logging.info("Modo Seeder: servindo até Ctrl+C")
            try:
                while not shutdown_flag.is_set():
                    shutdown_flag.wait(timeout=1.0)
            except KeyboardInterrupt:
                logging.info("Ctrl+C recebido no seeder. Finalizando...")
                shutdown_flag.set()


    except KeyboardInterrupt:
        logging.info("Apertou CTRL + C --- DESLIGANDO...")
        # Ativa a flag de desligamento para encerrar todas as threads.
        shutdown_flag.set()
    except Exception as e:
        logging.critical(f"Erro fatal no loop principal: {e}", exc_info=True)
        shutdown_flag.set()
    finally:
        logging.info("Esperando as threads terminarem...")
        shutdown_flag.set() # Garante que a flag esteja ativada.
        # Não é necessário juntar threads daemon explicitamente.
        time.sleep(1) # Dá um momento para as threads reagirem.
        udp_sock.close()
        logging.info("Socket UDP fechado.")
        logging.info("Desligamento do peer completo.")

if __name__ == "__main__":
    main()

