import socket
import threading

COLOR_YELLOW = '\033[93m'
COLOR_MAGENTA = '\033[95m'
COLOR_RESET = '\033[0m'

clients = []  # List to store client sockets
client_names = {}  # Dictionary to store client names
client_count = 0  # Counter to assign unique names to clients

def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                formatted_message = f"{COLOR_MAGENTA}{client_name}: {message}{COLOR_RESET}"
                print(formatted_message)
                broadcast(formatted_message, client_socket)
            else:
                break
        except:
            break
    client_socket.close()
    clients.remove(client_socket)
    del client_names[client_socket]

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(f"{COLOR_MAGENTA}{message}{COLOR_RESET}".encode('utf-8'))
            except:
                client.close()
                clients.remove(client)
                del client_names[client]

def send_messages():
    while True:
        message = input()
        formatted_message = f"{message}"
        broadcast(f"{COLOR_YELLOW}{formatted_message}{COLOR_RESET}", None)

def start_server():
    global client_count

    host = '0.0.0.0'  # Listen on all interfaces
    port = 12345  # Use any port in the range 1024-49151

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_count += 1
        client_name = f"Client {client_count}"
        print(f"Connection from {client_address} as {client_name}")
        clients.append(client_socket)
        client_names[client_socket] = client_name

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_handler.start()

if __name__ == '__main__':
    send_thread = threading.Thread(target=send_messages)
    send_thread.start()
    start_server()
