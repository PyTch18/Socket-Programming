import socket
import threading

COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'

def handle_server(server_socket):
    while True:
        try:
            message = server_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{COLOR_RED}Server: {message}{COLOR_RESET}")
            else:
                break
        except:
            break
    server_socket.close()

def send_messages(server_socket):
    while True:
        message = input()
        server_socket.sendall(message.encode('utf-8'))

def start_client():
    host = '172.20.10.6'  # Replace with the server's IP address (IPv4 after ipconfig in the terminal) 
    port = 12345  # Must be the same as the server's port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        command = input("Type 'CONNECT' to connect to the server: ")
        if command == 'CONNECT':
            server_socket.connect((host, port))
            break

    print("Connected to the server")

    server_handler = threading.Thread(target=handle_server, args=(server_socket,))
    server_handler.start()

    send_messages(server_socket)

if __name__ == '__main__':
    start_client()
