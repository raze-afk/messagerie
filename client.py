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
            newmsg = ""
            for i in range(len(msg)):
                for y in range(len(cesar)):
                    if msg[i] == cesar[y]:
                        newmsg += cesar[y - key]
            print("\nMessage reçu:", newmsg)            
        except:
            break

def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        msg = input("Vous: ")
        client_socket.send(msg.encode())

if __name__ == "__main__":
    start_client()




