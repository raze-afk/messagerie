import socket

s = socket.socket()
s.connect(('127.0.0.1', 2222))

while True:
    user_input = input("S: ")
    s.send(user_input.encode())

    if user_input == "Bye" or user_input == "bye":
        break

    print("N:", s.recv(1024).decode())

s.close()

