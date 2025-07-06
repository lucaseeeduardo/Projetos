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

# --- Configuration ---
PIECE_SIZE = 100 * 1024  # 512 KB per piece
UPDATE_INTERVAL = 30     # Seconds between tracker updates
REQUEST_TIMEOUT = 60     # Seconds to wait for a piece response
MAX_CONNECTIONS = 5      # Max concurrent downloads/uploads
LOG_LEVEL = logging.INFO
# ---------------------

# --- Logging Setup ---
logging.basicConfig(level=LOG_LEVEL,
                    format="%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s")
# ---------------------

# --- Global State ---
known_peers = {}  # { peer_id: {"ip": ip, "tcp_port": port, "pieces": set()} }
owned_pieces = set()
total_pieces = 0
target_file_path = ""
output_file_path = ""
piece_hashes = [] # Optional: For verifying pieces
my_tcp_port = 0
my_ip = ""
tracker_addr = None
peer_id = ""
shutdown_flag = threading.Event()
state_lock = threading.Lock() # Lock for known_peers and owned_pieces
# --------------------

def get_my_ip():
    """Attempts to determine the primary local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def parse_peer_list(peer_list_str):
    """Parses the PEERLIST string from the tracker."""
    peers = {}
    content = peer_list_str.strip("PEERLIST []")
    if not content:
        return peers

    peer_entries = content.split(";")
    for entry in peer_entries:
        try:
            parts = entry.split(":")
            ip = parts[0]
            port = int(parts[1])
            pieces_str = parts[2].strip("[]")
            pieces = set()
            if pieces_str:
                pieces = set(map(int, pieces_str.split(",")))

            entry_peer_id = f"{ip}:{port}"
            # Don't add ourselves to the known peers list
            if entry_peer_id != peer_id:
                peers[entry_peer_id] = {"ip": ip, "tcp_port": port, "pieces": pieces}
        except (IndexError, ValueError) as e:
            logging.warning(f"Failed to parse peer entry 	{entry}	: {e}")
    return peers

def update_known_peers(new_peers):
    """Updates the global known_peers dictionary safely."""
    with state_lock:
        # Simple merge: Update existing, add new ones.
        # More sophisticated logic could handle peer removal if not present in new list.
        known_peers.update(new_peers)
        # Remove self if accidentally added
        if peer_id in known_peers:
            del known_peers[peer_id]
    logging.debug(f"Known peers updated: {len(known_peers)} peers")

def send_tracker_update(udp_sock):
    """Sends the current list of owned pieces to the tracker."""
    with state_lock:
        pieces_str = ",".join(map(str, sorted(list(owned_pieces))))
    message = f"UPDATE {my_tcp_port} [{pieces_str}]"
    try:
        udp_sock.sendto(message.encode("utf-8"), tracker_addr)
        logging.debug(f"Sent UPDATE to tracker: {len(owned_pieces)} pieces")
    except socket.error as e:
        logging.error(f"Socket error sending UPDATE to tracker: {e}")
    except Exception as e:
        logging.error(f"Error sending UPDATE to tracker: {e}")

def tracker_update_thread(udp_sock):
    """Thread function to periodically send updates to the tracker."""
    logging.info("Tracker update thread started.")
    while not shutdown_flag.is_set():
        send_tracker_update(udp_sock)
        shutdown_flag.wait(UPDATE_INTERVAL)
    logging.info("Tracker update thread stopped.")

def handle_peer_connection(conn, addr):
    """Handles an incoming TCP connection from another peer requesting a piece."""
    logging.debug(f"Incoming connection from {addr}")
    try:
        conn.settimeout(REQUEST_TIMEOUT)
        data = conn.recv(1024)
        if not data:
            logging.warning(f"No data received from {addr}")
            return

        message = data.decode("utf-8")
        logging.debug(f"Received request from {addr}: {message}")
        if message.strip() == "SIZE":
            file_size = os.path.getsize(target_file_path)
            conn.sendall(str(file_size).encode("utf-8"))
            return
        # se a mensagem começar com GET, então tá mandando um pedido de pedaço, daí manda esse pedaço no sendall ali embaixo
        # notar que o sendall é um loop que itera sobre os bytes até enviar todos os bytes, mesmo que sejam muitos bytes
        # o ideal aqui não seria ele fazer só um chamada? já que cada piece é um pacote de bytes fechado. 
        # avaliar a diff do buffer do sendall ali com o buffer máximo do socket
        if message.startswith("GET "):
            try:
                piece_index = int(message.split(" ")[1])
                logging.info(f"Peer {addr} requested piece {piece_index}")

                with state_lock:
                    has_piece = piece_index in owned_pieces

                if has_piece:
                    piece_data = read_piece(piece_index)
                    if piece_data:
                        logging.info(f"Sending piece {piece_index} ({len(piece_data)} bytes) to {addr}")
                        # sendall significa que envia todos os dados, mesmo que sejam muitos bytes
                        # Isso é importante para garantir que o peer receba o arquivo completo
                        conn.sendall(piece_data)
                    else:
                        logging.error(f"Failed to read piece {piece_index} for {addr}")
                        # Optionally send an error message back
                else:
                    logging.warning(f"Don't have piece {piece_index} requested by {addr}")
                    # Optionally send a message indicating piece not found

            except (IndexError, ValueError):
                logging.warning(f"Invalid GET request format from {addr}: {message}")
        else:
            logging.warning(f"Unknown command from {addr}: {message}")

    except socket.timeout:
        logging.warning(f"Timeout handling connection from {addr}")
    except socket.error as e:
        logging.error(f"Socket error with {addr}: {e}")
    except Exception as e:
        logging.error(f"Error handling connection from {addr}: {e}", exc_info=True)
    finally:
        conn.close()
        logging.debug(f"Connection from {addr} closed")

def tcp_server_thread():
    """Thread function to listen for incoming TCP connections from peers."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_sock.bind((my_ip, my_tcp_port))
        server_sock.listen(MAX_CONNECTIONS)
        logging.info(f"TCP server listening on {my_ip}:{my_tcp_port}")

        while not shutdown_flag.is_set():
            # Use select for non-blocking accept with timeout
            readable, _, _ = select.select([server_sock], [], [], 1.0) # 1 second timeout
            if server_sock in readable:
                try:
                    conn, addr = server_sock.accept()
                    # Handle connection in a new thread to allow multiple uploads
                    handler_thread = threading.Thread(target=handle_peer_connection, args=(conn, addr), daemon=True)
                    handler_thread.start()
                except socket.error as e:
                    if not shutdown_flag.is_set(): # Avoid error message during shutdown
                         logging.error(f"Socket error accepting connection: {e}")
                except Exception as e:
                    if not shutdown_flag.is_set():
                         logging.error(f"Error accepting connection: {e}", exc_info=True)

    except OSError as e:
        logging.error(f"Failed to bind TCP server to {my_ip}:{my_tcp_port}. Error: {e}")
        shutdown_flag.set() # Signal other threads to stop
    except Exception as e:
        logging.critical(f"TCP server unexpected error: {e}", exc_info=True)
        shutdown_flag.set()
    finally:
        logging.info("TCP server thread stopping.")
        server_sock.close()
        logging.info("TCP server socket closed.")

def calculate_rarity():
    """Calculates the rarity of each piece based on known_peers."""
    rarity = {i: 0 for i in range(total_pieces)}
    with state_lock:
        if not known_peers:
             # If no peers known, assume all pieces are equally rare (or un-acquirable)
             # This prevents division by zero or weirdness if tracker returns empty list initially
             return rarity
        for peer_data in known_peers.values():
            for piece_index in peer_data["pieces"]:
                if piece_index in rarity:
                    rarity[piece_index] += 1
    return rarity

def choose_piece_to_download():
    """Chooses the next piece to download based on rarity (rarest first)."""
    rarity = calculate_rarity()
    with state_lock:
        needed_pieces = list(set(range(total_pieces)) - owned_pieces)

    if not needed_pieces:
        return None, None # All pieces downloaded

    # Sort needed pieces by rarity (ascending), then randomly for ties
    needed_pieces.sort(key=lambda i: (rarity.get(i, 0), random.random()))

    rarest_needed_piece = needed_pieces[0]

    # Find peers who have this piece
    peers_with_piece = []
    with state_lock:
        for p_id, data in known_peers.items():
            if rarest_needed_piece in data["pieces"]:
                peers_with_piece.append(p_id)

    if not peers_with_piece:
        logging.warning(f"No known peers have the rarest needed piece {rarest_needed_piece}. Will retry.")
        return None, None # Cannot download this piece right now

    # Choose a random peer from those who have the piece
    chosen_peer_id = random.choice(peers_with_piece)
    with state_lock:
        # Make sure peer still exists (could be removed between checks)
        if chosen_peer_id in known_peers:
             chosen_peer_info = known_peers[chosen_peer_id]
        else:
             logging.warning(f"Peer {chosen_peer_id} disappeared before selection.")
             return None, None

    logging.info(f"Chosen piece {rarest_needed_piece} (rarity: {rarity.get(rarest_needed_piece, 0)}) from peer {chosen_peer_id}")
    return rarest_needed_piece, chosen_peer_info

def download_piece(piece_index, peer_info, udp_sock):
    """Attempts to download a specific piece from a given peer."""
    peer_addr = (peer_info["ip"], peer_info["tcp_port"])
    logging.info(f"Attempting to download piece {piece_index} from {peer_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(REQUEST_TIMEOUT)
    try:
        sock.connect(peer_addr)
        message = f"GET {piece_index}"
        sock.sendall(message.encode("utf-8"))
        # Receive the piece data
        received_data = b""
        expected_size = get_piece_size(piece_index)
        while len(received_data) < expected_size:
            chunk = sock.recv(4096) # Read in chunks
            print("received chunk: ", len(chunk))
            if not chunk:
                logging.error(f"Connection closed by {peer_addr} while downloading piece {piece_index}. Received {len(received_data)}/{expected_size} bytes.")
                break # Connection broken
            received_data += chunk

        if len(received_data) != expected_size:
             logging.warning(f"Dados recebidos ({len(received_data)}) é diferente do esperado ({expected_size}) para o pedaço {piece_index} from {peer_addr}. Truncating.")
             received_data = received_data[:expected_size]
        logging.info(f"Recebido {len(received_data)} de {expected_size}")

        logging.info(f"Successfully received piece {piece_index} ({len(received_data)} bytes) from {peer_addr}")

        # --- Optional: Verify piece hash here --- #

        # Write piece to file
        if write_piece(piece_index, received_data):
            with state_lock:
                owned_pieces.add(piece_index)
            logging.info(f"Successfully saved piece {piece_index}. Owned: {len(owned_pieces)}/{total_pieces}")
            # Immediately inform tracker about the new piece
            # Consider doing this less frequently if it causes too much traffic
            send_tracker_update(udp_sock) # Need udp_sock here
            if len(owned_pieces) == total_pieces:
                logging.info("All pieces downloaded! Download complete.")
                # Optionally, send a final update to tracker
                # Renomeia o arquivo após o download completo
                novo_nome = target_file_path.replace('incompleto', '')
                try:
                    os.rename(target_file_path, novo_nome)
                    logging.info(f"Arquivo renomeado para: {novo_nome}")
                except Exception as e:
                    logging.error(f"Erro ao renomear arquivo: {e}")

            return True
        else:
            logging.error(f"Failed to write piece {piece_index} to file.")
            return False

    except socket.timeout:
        logging.warning(f"Timeout connecting to or downloading from {peer_addr} for piece {piece_index}")
        return False
    except socket.error as e:
        logging.error(f"Socket error downloading piece {piece_index} from {peer_addr}: {e}")
        return False
    except Exception as e:
        logging.error(f"Error downloading piece {piece_index} from {peer_addr}: {e}", exc_info=True)
        return False
    finally:
        sock.close()

def get_piece_size(piece_index):
    """Calculates the size of a specific piece, handling the last piece."""
    global total_pieces
    try:
        file_size = os.path.getsize(target_file_path)
        if piece_index < total_pieces - 1:
            return PIECE_SIZE
        else:
            # Last piece might be smaller
            return file_size - (piece_index * PIECE_SIZE)
    except OSError as e:
        logging.error(f"Error getting file size for {target_file_path}: {e}")
        # Return default piece size as a fallback, might cause issues
        return PIECE_SIZE

def read_piece(piece_index):
    """Reads a specific piece from the target file."""
    try:
        with open(target_file_path, "rb") as f:
            start_offset = piece_index * PIECE_SIZE
            f.seek(start_offset)
            size_to_read = get_piece_size(piece_index)
            piece_data = f.read(size_to_read)
            if len(piece_data) != size_to_read:
                 logging.warning(f"Read incomplete data for piece {piece_index}. Expected {size_to_read}, got {len(piece_data)}.")
                 # Decide how to handle this - maybe return None or raise error
            return piece_data
    except OSError as e:
        logging.error(f"Error reading piece {piece_index} from {target_file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading piece {piece_index}: {e}", exc_info=True)
        return None

def write_piece(piece_index, data):
    """Writes a downloaded piece to the correct position in the output file."""
    try:
        # Use r+b to allow writing without truncating
        with open(target_file_path, "r+b") as f:
            start_offset = piece_index * PIECE_SIZE
            f.seek(start_offset)
            f.write(data)
        return True
    except OSError as e:
        logging.error(f"Error writing piece {piece_index} to {target_file_path}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error writing piece {piece_index}: {e}", exc_info=True)
        return False

def initialize_output_file(file_size):
    """Creates or ensures the output file exists with the correct size, filled with null bytes."""
    try:
        os.makedirs(os.path.dirname(target_file_path) or ".", exist_ok=True)
        if not os.path.exists(target_file_path) or os.path.getsize(target_file_path) != file_size:
            with open(target_file_path, "wb") as f:
                f.seek(file_size-1)
                f.write(b"\0")
        logging.info(f"Output criado/completo: {target_file_path} ({file_size} bytes)")


    except OSError as e:
        logging.critical(f"Failed to initialize output file {target_file_path}: {e}")
        return False
    except Exception as e:
        logging.critical(f"Unexpected error initializing output file: {e}", exc_info=True)
        return False
    return True

def download_manager(udp_sock):
    """Main logic for managing the download process."""
    logging.info("Download manager started.")
    while not shutdown_flag.is_set():
        with state_lock:
            if len(owned_pieces) == total_pieces:
                logging.info("Download complete! All pieces acquired.")
                
                is_seeder = True
                send_tracker_update(udp_sock) # Final update to tracker
                break # Exit download loop

        piece_index, peer_info = choose_piece_to_download()

        if piece_index is not None and peer_info is not None:
            if download_piece(piece_index, peer_info, udp_sock):
                # Success, loop will continue to choose next piece
                # Send update immediately after getting a piece
                send_tracker_update(udp_sock)
                pass
            else:
                # Failure, wait a bit before retrying
                logging.warning(f"Failed to download piece {piece_index}. Waiting before retry.")
                shutdown_flag.wait(5) # Wait 5 seconds before trying next piece
        else:
            # No piece available or no peers have it, wait before checking again
            with state_lock:
                 needed_count = total_pieces - len(owned_pieces)
            if needed_count > 0:
                 logging.info(f"No suitable piece/peer found. Still need {needed_count} pieces. Waiting...")
                 shutdown_flag.wait(10) # Wait 10 seconds
            else:
                 # Should have been caught by the check at the start of the loop
                 logging.info("Download appears complete, but loop continued. Exiting.")
                 break

    logging.info("Download manager stopped.")
    if not is_seeder:
       logging.info("Download manager started.")
       download_manager()
       logging.info("Download manager stopped.")

    else:
        logging.info("Modo Seeder: servindo até Ctrl+C")
        try:
            while not shutdown_flag.is_set():
                shutdown_flag.wait(timeout=1.0)
        except KeyboardInterrupt:
            logging.info("Ctrl+C recebido no seeder. Finalizando...")
            shutdown_flag.set()


def main():
    global total_pieces, target_file_path, my_tcp_port, my_ip, tracker_addr, peer_id, is_seeder

    parser = argparse.ArgumentParser(description="P2P File Sharing Client (BitTorrent Simulation)")
    parser.add_argument("target_file", help="Path to the file to share/download.")
    parser.add_argument("--tracker", required=True, help="Tracker address HOST:PORT")
    parser.add_argument("--listen-port", type=int, required=True, help="TCP port for peer connections")
    args = parser.parse_args()
    # pra diferenciar leecher de seeder, eu verifico se o arquivo de entrada existe.
    # se existir, verifico se existe algum outro peer que já tenha esse arquivo e mando um SIZE pra ele
    # caso esse size seja menor que o meu, eu sou seeder.

    my_tcp_port = args.listen_port 
    target_file_path = args.target_file
    is_seeder = os.path.exists(target_file_path)
    
    if not is_seeder:
        target_file_path += 'incompleto'


    # Validate target file
    if not os.path.isfile(target_file_path) and is_seeder:
        logging.critical(f"Target file not found or is not a file: {target_file_path}")
        return
    if is_seeder:
        try:
            file_size = os.path.getsize(target_file_path)


            if file_size == 0:
                logging.critical(f"Target file is empty: {target_file_path}")
                return
            
            total_pieces = math.ceil(file_size / PIECE_SIZE)
            logging.info(f"Arquivo local: {target_file_path}, Tamanho: {file_size} bytes, Pedaços: {total_pieces}")

            # se eu passar o arg de output é pq eu to sendo o seeder.
            if(is_seeder):
                owned_pieces.update(range(total_pieces))
        except OSError as e:
            logging.critical(f"Cannot access target file: {e}")
            return

    # Parse tracker address
    try:
        tracker_host, tracker_port_str = args.tracker.split(":")
        tracker_port = int(tracker_port_str)
        tracker_addr = (tracker_host, tracker_port)
    except (ValueError, IndexError):
        logging.critical(f"Endereço do tracker inválido. Precisa ser HOST:PORT. Retorno: {args.tracker}")
        return

    # Determine own IP and Peer ID
    my_ip = get_my_ip()
    peer_id = f"{my_ip}:{my_tcp_port}"
    logging.info(f"Peer starting with ID: {peer_id}")
        # --- UDP Socket for Tracker Communication ---
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.settimeout(5.0) # Timeout for recvfrom

    # --- Initial JOIN to Tracker ---
    join_message = f"JOIN {my_ip} {my_tcp_port}"
    try:
        logging.info(f"Sending JOIN to tracker {tracker_addr}")
        udp_sock.sendto(join_message.encode("utf-8"), tracker_addr)

        # aqui entendo que 2048 seja suficiente, sabendo que pode haver muitos peers e dar erro por buffer overflow
        data, _ = udp_sock.recvfrom(2048) # Larger buffer for peer list
        response = data.decode("utf-8")
        print("<<< Lista de peeer recebida do trackr ", response)
        if response.startswith("PEERLIST"):
            initial_peers = parse_peer_list(response)
            update_known_peers(initial_peers)
            logging.info(f"Received initial peer list from tracker: {len(initial_peers)} peers")
        else:
            logging.warning(f"Unexpected response from tracker after JOIN: {response}")

    except socket.timeout:
        logging.error("Timeout waiting for initial response from tracker after JOIN.")
        # Decide whether to retry or exit
        udp_sock.close()
        return
    except socket.error as e:
        logging.error(f"Socket error during initial JOIN: {e}")
        udp_sock.close()
        return
    except Exception as e:
        logging.error(f"Error during initial JOIN: {e}")
        udp_sock.close()
        return
    
    if not is_seeder:

        first_peer = next(iter(known_peers.values()), None)
        if not first_peer:
            logging.critical("Nenhum seeder disponível para metadata. Abortando.")
            return

        size_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        size_sock.settimeout(REQUEST_TIMEOUT)
        size_sock.connect((first_peer["ip"], first_peer["tcp_port"]))
        size_sock.sendall(b"SIZE")
        resp = size_sock.recv(64)
        file_size = int(resp.decode("utf-8"))
        size_sock.close()

        # atualize total_pieces e recrie output com esse tamanho
        total_pieces = math.ceil(file_size / PIECE_SIZE)
        logging.info(f"Dynamic file size received: {file_size} bytes, Pieces: {total_pieces}")
        # agora re-initialize passando o tamanho em vez de ler do target
        if not initialize_output_file(file_size):
            logging.critical("Erro ao criar arquivo no leecher.")
            return
        
    # --- Determine initially owned pieces (if file exists and matches target) ---
    # For simplicity, assume we start with zero pieces unless output == target
    if is_seeder:
         logging.info("Acting as a seeder (output file is the target file). Assuming all pieces are owned.")
         with state_lock:
              owned_pieces.update(range(total_pieces))
    else:
         # TODO: Implement piece checking for resuming downloads if needed
         logging.info("Starting download. Assuming zero pieces initially.")
         pass


    # --- Start Threads ---
    threads = []
    try:
        # TCP Server Thread
        # essa thread tcp_server_thread escuta na porta TCP especificada e aceita conexões de outros peers

        tcp_server = threading.Thread(target=tcp_server_thread, name="TCPServer", daemon=True)
        #entender melhor esse threads.append, pra que serve
        threads.append(tcp_server)
        tcp_server.start()

        # Tracker Update Thread
        tracker_updater = threading.Thread(target=tracker_update_thread, args=(udp_sock,), name="TrackerUpdate", daemon=True)
        threads.append(tracker_updater)
        tracker_updater.start()

        # Download Manager (runs in main thread or its own thread)
        # Running in main thread for simplicity here
        if not is_seeder:
            download_manager(udp_sock)
        else:
            logging.info("Modo Seeder: servindo até Ctrl+C")
            try:
                while not shutdown_flag.is_set():
                    shutdown_flag.wait(timeout=1.0)
            except KeyboardInterrupt:
                logging.info("Ctrl+C recebido no seeder. Finalizando...")
                shutdown_flag.set()


    except KeyboardInterrupt:
        logging.info("Apertou CTRL + C --- DESLIGANDO...")
        shutdown_flag.set()
    except Exception as e:
        logging.critical(f"Fatal error in main loop: {e}", exc_info=True)
        shutdown_flag.set()
    finally:
        logging.info("Waiting for threads to finish...")
        shutdown_flag.set() # Ensure flag is set
        # No need to join daemon threads explicitly
        time.sleep(1) # Give threads a moment to react
        udp_sock.close()
        logging.info("UDP socket closed.")
        logging.info("Peer shutdown complete.")

if __name__ == "__main__":
    main()