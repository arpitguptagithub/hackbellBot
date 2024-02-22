import paramiko
import threading
import socket
import logging
import os

logging.basicConfig(filename='ssh_snake_detector.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s')

class SSHHoneypot(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        return paramiko.OPEN_FAILED_UNKNOWN_CHANNEL_TYPE

    def check_auth_password(self, username, password):
        logging.info(f"Password login attempt: {username}")
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        logging.info(f"Public key login attempt: {username}")
        return paramiko.AUTH_FAILED

    def check_auth_none(self, username):
        logging.info(f"None authentication attempt: {username}")
        return paramiko.AUTH_FAILED

def start_ssh_honeypot(port):
    host_key = paramiko.RSAKey(filename='/path/to/your/private/key')

    server = None

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(100)

        logging.info(f"SSH honeypot listening on port {port}")

        while True:
            client, addr = server.accept()
            logging.info(f"Connection from {addr}")

            transport = paramiko.Transport(client)
            transport.add_server_key(host_key)

            honeypot = SSHHoneypot()
            transport.start_server(server=honeypot)

            channel = transport.accept(1)
            if channel is None:
                transport.close()
            else:
                channel.close()

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        if server:
            server.close()

# Replace these values with your own
ssh_honeypot_port = 2222

honeypot_thread = threading.Thread(target=start_ssh_honeypot, args=(ssh_honeypot_port,))
honeypot_thread.start()

# Keep the main thread running
honeypot_thread.join()
