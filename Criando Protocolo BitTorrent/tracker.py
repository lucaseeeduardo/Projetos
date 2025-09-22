#!/usr/bin/env python3

import socket
import threading
import time
import logging

# --- Configuration ---
TRACKER_HOST = '0.0.0.0' # Listen on all available interfaces
TRACKER_PORT = 10000      # Port for the tracker UDP server
PEER_TIMEOUT = 60       # Seconds before considering a peer inactive
LOG_LEVEL = logging.INFO
# ---------------------

# --- Logging Setup ---
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------

# --- Global Data Structure ---
# Stores peer info: { 'peer_id': {'ip': str, 'tcp_port': int, 'pieces': set(int), 'last_update': float} }
peers_db = {}
db_lock = threading.Lock() # To protect access to peers_db from multiple threads
# ---------------------------

def format_peer_list(exclude_peer_id=None):
    """Formats the current peer list for sending to peers.

    Args:
        exclude_peer_id (str, optional): Peer ID to exclude from the list (usually the requesting peer).

    Returns:
        str: Formatted string like "PEERLIST [<ip1>:<port1>:[p1,p2];<ip2>:<port2>:[p3];...]"
    """
    peer_strings = []
    with db_lock:
        for peer_id, data in peers_db.items():
            if peer_id == exclude_peer_id:
                continue
            pieces_str = ','.join(map(str, sorted(list(data['pieces']))))
            peer_strings.append(f"{data['ip']}:{data['tcp_port']}:[{pieces_str}]")
    return f"PEERLIST [{';'.join(peer_strings)}]"

def cleanup_inactive_peers():
    """Periodically checks for and removes inactive peers."""
    while True:
        time.sleep(PEER_TIMEOUT / 2) # Check periodically
        now = time.time()
        inactive_peers = []
        with db_lock:
            for peer_id, data in peers_db.items():
                if now - data['last_update'] > PEER_TIMEOUT:
                    inactive_peers.append(peer_id)

            if inactive_peers:
                logging.info(f"Removing inactive peers: {inactive_peers}")
                for peer_id in inactive_peers:
                    del peers_db[peer_id]

def handle_udp_message(data, addr, sock):
    """Parses and handles incoming UDP messages."""
    message = data.decode('utf-8')
    peer_ip, _ = addr # UDP source port is usually ephemeral, not the peer's listening TCP port
    logging.debug(f"Received message from {addr}: {message}")

    parts = message.split(' ', 2) # Split into command, args...
    command = parts[0]

    try:
        if command == 'JOIN' and len(parts) == 3:
            # JOIN <peer_ip> <peer_tcp_port>
            # Note: We use the source IP from the packet (peer_ip), not the one in the message
            #       as the one in the message might be wrong (e.g., behind NAT without config).
            #       However, the TCP port MUST come from the message.
            try:
                peer_tcp_port = int(parts[2])
                peer_id = f"{peer_ip}:{peer_tcp_port}"
                logging.info(f"JOIN request from {peer_id}")

                with db_lock:
                    peers_db[peer_id] = {
                        'ip': peer_ip,
                        'tcp_port': peer_tcp_port,
                        'pieces': set(),
                        'last_update': time.time()
                    }

                # Send peer list back (excluding the new peer itself initially)
                response = format_peer_list(exclude_peer_id=peer_id)
                logging.debug(f"Sending to {addr}: {response}")
                sock.sendto(response.encode('utf-8'), addr)

            except ValueError:
                logging.warning(f"Invalid port in JOIN from {addr}: {parts[2]}")

        elif command == 'UPDATE' and len(parts) == 3:
            # UPDATE <peer_ip> <peer_tcp_port> [p1,p2,...]
            try:
                peer_tcp_port = int(parts[1]) # Port is the second part here
                peer_id = f"{peer_ip}:{peer_tcp_port}"

                if peer_id not in peers_db:
                    logging.warning(f"UPDATE from unknown peer {peer_id}. Asking to JOIN first.")
                    # Optionally, send an error or ignore. For now, ignore.
                    return

                pieces_str = parts[2].strip('[]')
                pieces = set()
                if pieces_str: # Avoid error if list is empty '[]'
                    try:
                        pieces = set(map(int, pieces_str.split(',')))
                    except ValueError:
                        logging.warning(f"Invalid pieces format in UPDATE from {peer_id}: {parts[2]}")
                        return # Ignore invalid update

                logging.debug(f"UPDATE from {peer_id}: {len(pieces)} pieces")
                with db_lock:
                    if peer_id in peers_db: # Check again inside lock
                        peers_db[peer_id]['pieces'] = pieces
                        peers_db[peer_id]['last_update'] = time.time()
                    else:
                         logging.warning(f"Peer {peer_id} disappeared before UPDATE lock.")

            except ValueError:
                logging.warning(f"Invalid port in UPDATE from {addr}: {parts[1]}")
            except Exception as e:
                 logging.error(f"Error processing UPDATE from {peer_id}: {e}")


        else:
            logging.warning(f"Unknown command or format from {addr}: {message}")

    except Exception as e:
        logging.error(f"Error handling message from {addr}: {e}", exc_info=True)

def start_tracker():
    """Starts the UDP tracker server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((TRACKER_HOST, TRACKER_PORT))
        logging.info(f"Tracker UDP server started on {TRACKER_HOST}:{TRACKER_PORT}")

        # Start cleanup thread
        cleanup_thread = threading.Thread(target=cleanup_inactive_peers, daemon=True)
        cleanup_thread.start()

        while True:
            try:
                data, addr = sock.recvfrom(1024) # Buffer size 1024 bytes
                # Handle each message in a new thread to avoid blocking the main loop?
                # For UDP, it might be okay unless processing is very slow.
                # Let's keep it simple for now.
                handle_udp_message(data, addr, sock)
            except ConnectionResetError:
                 # Common on Windows when a previous send failed
                 logging.warning(f"Connection reset error from {addr}. Ignoring.")
            except Exception as e:
                logging.error(f"Error receiving data: {e}", exc_info=True)

    except OSError as e:
        logging.error(f"Failed to bind tracker to {TRACKER_HOST}:{TRACKER_PORT}. Error: {e}")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logging.info("Shutting down tracker server.")
        sock.close()

if __name__ == '__main__':
    start_tracker()

