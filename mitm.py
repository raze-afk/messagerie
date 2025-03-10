import socket
import threading

clients = []

def stole_client_from_server(client_socket, addr):
    print(f"[+] Nouvelle connexion : {addr}")
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"[{addr}] {msg}")
            broadcast(msg, client_socket)
        except:
            break
    print(f"[-] Déconnexion : {addr}")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(msg, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(msg.encode())
            except:
                client.close()
                clients.remove(client)

def start_server(host='0.0.0.0', port=1111):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Serveur démarré sur {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=stole_client_from_server, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
