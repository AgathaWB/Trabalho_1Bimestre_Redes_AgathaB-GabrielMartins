import socket  # Importa a biblioteca socket

HOST = "127.0.0.1" # Endereço IP do servidor
PORT = 9007  # Porta usada para receber mensagens

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Conecta ao servidor

    while True:
        m = s.recv(1024).decode("utf-8")  
        # Recebe até 1024 bytes do servidor e decodifica para string
        
        print(m)  # Exibe a mensagem recebida no terminal