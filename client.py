import socket
import threading
import random

cesar = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            key = int(msg.split("#")[0])
            msg = msg.split("#")[1]
            decrypt_msg = ""
            for i in range(len(msg)):
                for y in range(len(cesar)):
                    if msg[i] == cesar[y]:
                        decrypt_msg += cesar[(y - key) % 26]
            print("\nMessage reçu:", decrypt_msg)            
        except:
            break

def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        msg = input("Vous: ")
        key = random.randint(2,25)
        crypt_msg = ""
        for i in range(len(msg)):
            for y in range(len(cesar)):
                if msg[i] == cesar[y]:
                    crypt_msg += cesar[(y + key) % 26]
        to_send = str(key) + "#" + crypt_msg
        print("sender : ", to_send)
        client_socket.send(to_send.encode())

if __name__ == "__main__":
    start_client()




