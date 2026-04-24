import socket

HOST="192.168.18.26"
PORT=9003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST,PORT))

    while True:
        msg = cliente.recv(1024).decode("utf-8")
        print(msg)