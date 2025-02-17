import socket

s = socket.socket()
port = 2222
s.bind(('127.0.0.1', port))
s.listen()
print("Socket Up and running")

c, addr = s.accept()
print("Connection from", addr)

while True:
    rcvdData = c.recv(1024).decode()
    print("S:", rcvdData)

    sendData = input("N: ")
    c.send(sendData.encode())

    if sendData == "Bye" or sendData == "bye":
        break

c.close()

