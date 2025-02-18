import socket
import threading
import random
import string 
def vigenere_cipher(text, key, encrypt=True):
    vige = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    key_index = 0
    
    for char in text:
        if char == " ":
            result += " "
        elif char in vige:
            shift = vige.index(key[key_index % len(key)])
            shift = shift if encrypt else -shift
            new_index = (vige.index(char) + shift) % 26
            result += vige[new_index]
            key_index += 1
        else:
            result += char  
    
    return result

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print("message reçu: ", msg)
            key, encrypted_msg = msg.split("#", 1)
            decrypt_msg = vigenere_cipher(encrypted_msg, key, encrypt=False)
            print("\nMessage reçu:", decrypt_msg)            
        except:
            break

def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    
    while True:
        msg = input("Vous: ")
        key = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        encrypted_msg = vigenere_cipher(msg, key)
        to_send = f"{key}#{encrypted_msg}"
        print("Sender:", to_send)
        client_socket.send(to_send.encode())

if __name__ == "__main__":
    start_client()
