import socket
import threading
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key
private_key, public_key = generate_keys()
def public_key_to_base64(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return base64.b64encode(pem).decode()
def encrypt_rsa(text, public_key):
    ciphertext = public_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode()
def decrypt_rsa(ciphertext, private_key):
    ciphertext_bytes = base64.b64decode(ciphertext)
    plaintext = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()
SENDER_PUBLIC = None
clients = []
def stole_client_from_server(client_socket, addr):
    print(f"[+] Nouvelle connexion : {addr}")
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"[{addr}] {msg}")
            send_to_reel_client(msg, client_socket)
        except:
            break
    print(f"[-] Déconnexion : {addr}")
    clients.remove(client_socket)
    client_socket.close()
def send_to_reel_client(msg, sender_socket):
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
