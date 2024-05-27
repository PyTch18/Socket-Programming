import socket
import threading

COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{COLOR_YELLOW}Client: {message}{COLOR_RESET}")
            else:
                break
        except:
            break
    client_socket.close()

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.sendall(message.encode('utf-8'))

def start_server():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 12345  # Use any port in the range 1024-49151

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

    send_messages(client_socket)

if __name__ == '__main__':
    start_server()
