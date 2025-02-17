import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print("\nMessage reçu:", msg)
        except:
            break

def start_client(host='127.0.0.1', port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        msg = input("Vous: ")
        client_socket.send(msg.encode())

if __name__ == "__main__":
    start_client()
