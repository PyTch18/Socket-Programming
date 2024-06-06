import socket
import threading

COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'

def handle_server(server_socket):
    while True:
        try:
            message = server_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{COLOR_RED}{message}{COLOR_RESET}")
            else:
                print("Server closed the connection.")
                break
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break
    server_socket.close()

def send_messages(server_socket):
    while True:
        try:
            message = input()
            server_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to server: {e}")
            break

def start_client():
    server_ip = input("Enter the server IP address: ")
    port = 5040  # Must be the same as the server's port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        command = input("Type 'CONNECT' to connect to the server: ")
        if command.strip().upper() == 'CONNECT':
            try:
                print(f"Attempting to connect to {server_ip}:{port}")
                server_socket.connect((server_ip, port))
                print("Connected to the server")

                server_handler = threading.Thread(target=handle_server, args=(server_socket,))
                server_handler.start()

                send_messages(server_socket)
            except Exception as e:
                print(f"Connection error: {e}")
            finally:
                server_socket.close()
                print("Disconnected from the server")
            break
        else:
            print("Invalid command. Please type 'CONNECT' to proceed.")

if __name__ == '__main__':
    start_client()
