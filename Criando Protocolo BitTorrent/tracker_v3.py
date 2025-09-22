#!/usr/bin/env python3

import socket
import threading
import time
import logging

# --- Configuração ---
TRACKER_HOST = '0.0.0.0' # O tracker escutará em todas as interfaces disponíveis.
TRACKER_PORT = 10000      # Porta UDP para o servidor do tracker.
PEER_TIMEOUT = 60       # Tempo em segundos antes de considerar um peer inativo e removê-lo.
LOG_LEVEL = logging.INFO # Nível de log para exibição de mensagens.
# ---------------------

# --- Configuração de Log ---
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------

# --- Estrutura de Dados Global ---
# Armazena informações dos peers: { 'peer_id': {'ip': str, 'tcp_port': int, 'pieces': set(int), 'last_update': float} }
# 'peer_id' é uma string no formato 'IP:porta_tcp'.
# 'ip' é o endereço IP do peer.
# 'tcp_port' é a porta TCP que o peer está escutando.
# 'pieces' é um conjunto de índices dos pedaços de arquivo que o peer possui.
# 'last_update' é o timestamp da última vez que o peer se comunicou com o tracker.
peers_db = {}
# Lock para proteger o acesso a 'peers_db' de múltiplas threads, garantindo a segurança dos dados.
db_lock = threading.Lock() 
# ---------------------------

def format_peer_list(exclude_peer_id=None):
    """Formata a lista atual de peers para envio aos peers.

    Args:
        exclude_peer_id (str, optional): ID do peer a ser excluído da lista (geralmente o peer solicitante).

    Returns:
        str: String formatada como "PEERLIST [<ip1>:<porta1>:[p1,p2];<ip2>:<porta2>:[p3];...]"
    """
    peer_strings = []
    with db_lock:
        # Itera sobre todos os peers no banco de dados.
        for peer_id, data in peers_db.items():
            # Exclui o peer que fez a solicitação, se especificado.
            if peer_id == exclude_peer_id:
                continue
            # Converte o conjunto de pedaços para uma string separada por vírgulas e ordenada.
            pieces_str = ','.join(map(str, sorted(list(data['pieces']))))
            # Adiciona a string formatada do peer à lista.
            peer_strings.append(f"{data['ip']}:{data['tcp_port']}:[{pieces_str}]")
    # Retorna a lista de peers formatada com o prefixo "PEERLIST ".
    return f"PEERLIST [{' ; '.join(peer_strings)}]"

def cleanup_inactive_peers():
    """Verifica periodicamente e remove peers inativos.
    Um peer é considerado inativo se não enviar uma atualização dentro do PEER_TIMEOUT.
    """
    while True:
        # Espera por um período antes de verificar novamente.
        time.sleep(PEER_TIMEOUT / 2) 
        now = time.time()
        inactive_peers = []
        with db_lock:
            # Identifica peers que não foram atualizados dentro do tempo limite.
            for peer_id, data in peers_db.items():
                if now - data['last_update'] > PEER_TIMEOUT:
                    inactive_peers.append(peer_id)

            # Remove os peers inativos do banco de dados.
            if inactive_peers:
                logging.info(f"Removendo peers inativos: {inactive_peers}")
                for peer_id in inactive_peers:
                    del peers_db[peer_id]

def handle_udp_message(data, addr, sock):
    """Analisa e lida com as mensagens UDP de entrada.
    Processa comandos como JOIN e UPDATE enviados pelos peers.
    """
    message = data.decode('utf-8')
    # O IP de origem UDP é geralmente efêmero, não a porta TCP de escuta do peer.
    peer_ip, _ = addr 
    logging.debug(f"Mensagem recebida de {addr}: {message}")

    # Divide a mensagem em comando e argumentos.
    parts = message.split(' ', 2) 
    command = parts[0]

    try:
        # Lida com o comando JOIN.
        if command == 'JOIN' and len(parts) == 3:
            # Formato: JOIN <peer_ip> <peer_tcp_port>
            # Nota: Usamos o IP de origem do pacote (peer_ip), não o que está na mensagem,
            #       pois o da mensagem pode estar incorreto (ex: atrás de NAT sem configuração).
            #       No entanto, a porta TCP DEVE vir da mensagem.
            try:
                peer_tcp_port = int(parts[2])
                peer_id = f"{peer_ip}:{peer_tcp_port}"
                logging.info(f"Requisição JOIN de {peer_id}")

                with db_lock:
                    # Adiciona ou atualiza as informações do peer no banco de dados.
                    peers_db[peer_id] = {
                        'ip': peer_ip,
                        'tcp_port': peer_tcp_port,
                        'pieces': set(), # Inicialmente, o peer não possui pedaços conhecidos.
                        'last_update': time.time() # Registra o tempo da última atualização.
                    }

                # Envia a lista de peers de volta (excluindo o próprio peer recém-chegado inicialmente).
                response = format_peer_list(exclude_peer_id=peer_id)
                logging.debug(f"Enviando para {addr}: {response}")
                sock.sendto(response.encode('utf-8'), addr)

            except ValueError:
                logging.warning(f"Porta inválida no JOIN de {addr}: {parts[2]}")

        # Lida com o comando UPDATE.
        elif command == 'UPDATE' and len(parts) == 3:
            # Formato: UPDATE <peer_tcp_port> [p1,p2,...]
            try:
                peer_tcp_port = int(parts[1]) # A porta é a segunda parte aqui.
                peer_id = f"{peer_ip}:{peer_tcp_port}"

                if peer_id not in peers_db:
                    logging.warning(f"UPDATE de peer desconhecido {peer_id}. Pedindo para JOIN primeiro.")
                    # Opcionalmente, enviar um erro ou ignorar. Por enquanto, ignorar.
                    return

                # Extrai a string de pedaços e a converte para um conjunto de inteiros.
                pieces_str = parts[2].strip('[]')
                pieces = set()
                if pieces_str: # Evita erro se a lista estiver vazia '[]'.
                    try:
                        pieces = set(map(int, pieces_str.split(',')))
                    except ValueError:
                        logging.warning(f"Formato de pedaços inválido no UPDATE de {peer_id}: {parts[2]}")
                        return # Ignora atualização inválida.

                logging.debug(f"UPDATE de {peer_id}: {len(pieces)} pedaços")
                with db_lock:
                    if peer_id in peers_db: # Verifica novamente dentro do lock.
                        # Atualiza os pedaços possuídos e o tempo da última atualização do peer.
                        peers_db[peer_id]['pieces'] = pieces
                        peers_db[peer_id]['last_update'] = time.time()
                    else:
                         logging.warning(f"Peer {peer_id} desapareceu antes do lock de UPDATE.")

            except ValueError:
                logging.warning(f"Porta inválida no UPDATE de {addr}: {parts[1]}")
            except Exception as e:
                 logging.error(f"Erro ao processar UPDATE de {peer_id}: {e}")


        else:
            logging.warning(f"Comando ou formato desconhecido de {addr}: {message}")

    except Exception as e:
        logging.error(f"Erro ao lidar com a mensagem de {addr}: {e}", exc_info=True)

def start_tracker():
    """Inicia o servidor UDP do tracker.
    Cria um socket UDP, vincula-o a um endereço e porta, e começa a escutar por mensagens.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Vincula o socket do tracker ao host e porta configurados.
        sock.bind((TRACKER_HOST, TRACKER_PORT))
        logging.info(f"Servidor UDP do Tracker iniciado em {TRACKER_HOST}:{TRACKER_PORT}")

        # Inicia a thread de limpeza de peers inativos.
        cleanup_thread = threading.Thread(target=cleanup_inactive_peers, daemon=True)
        cleanup_thread.start()

        while True:
            try:
                # Recebe dados de qualquer peer.
                data, addr = sock.recvfrom(1024) # Tamanho do buffer: 1024 bytes.
                # Lida com cada mensagem em uma nova thread para evitar bloquear o loop principal?
                # Para UDP, pode ser aceitável, a menos que o processamento seja muito lento.
                # Por enquanto, vamos manter simples.
                handle_udp_message(data, addr, sock)
            except ConnectionResetError:
                 # Comum no Windows quando um envio anterior falhou.
                 logging.warning(f"Erro de redefinição de conexão de {addr}. Ignorando.")
            except Exception as e:
                logging.error(f"Erro ao receber dados: {e}", exc_info=True)

    except OSError as e:
        logging.error(f"Falha ao vincular o tracker a {TRACKER_HOST}:{TRACKER_PORT}. Erro: {e}")
    except Exception as e:
        logging.critical(f"Ocorreu um erro inesperado: {e}", exc_info=True)
    finally:
        logging.info("Encerrando o servidor do tracker.")
        sock.close()

if __name__ == '__main__':
    start_tracker()



