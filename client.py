import socket
import threading
import random

def cesar_cipher(text, key, encrypt=True):
    cesar = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    shift = key if encrypt else -key
    
    for char in text:
        if char == " ":
            result += " "
        elif char in cesar:
            new_index = (cesar.index(char) + shift) % 26
            result += cesar[new_index]
        else:
            result += char 
    
    return result

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            key, encrypted_msg = msg.split("#", 1)
            decrypt_msg = cesar_cipher(encrypted_msg, int(key), encrypt=False)
            print("\nMessage reçu:", decrypt_msg)            
        except:
            break

def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    
    while True:
        msg = input("Vous: ")
        key = random.randint(2, 25)
        encrypted_msg = cesar_cipher(msg, key)
        to_send = f"{key}#{encrypted_msg}"
        print("Sender:", to_send)
        client_socket.send(to_send.encode())

if __name__ == "__main__":
    start_client()
