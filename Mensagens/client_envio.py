import socket

HOST="192.168.18.26"
PORT=9002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST,PORT))

    nome=input("Seu nome: ")

    cliente.sendall(nome.encode("utf-8"))

    while True:
        msg=input("Mensagem: ")

        cliente.sendall(msg.encode("utf-8"))