import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

AES_KEY = b'5t8MVNIi199RlALz' 
AES_IV = b't3q2Orv4tjm9QY9d'  

def encrypt_aes(plaintext):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()  
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode()

def decrypt_aes(ciphertext):
    ciphertext = base64.b64decode(ciphertext)  
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

def receive_messages(client_socket):

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:

                break
            decrypt_msg = decrypt_aes(msg)
            print("\nMessage reçu:", decrypt_msg)            
        except:
            break

def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    
    while True:
        msg = input("Vous: ")
        encrypted_msg = encrypt_aes(msg)
        client_socket.send(encrypted_msg.encode())

if __name__ == "__main__":
    start_client()
