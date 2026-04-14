import socket  # Importa a biblioteca socket, usada para comunicação em rede

HOST = "127.0.0.1"  # Define o endereço IP do servidor HOST = "127.0.0.1"
PORT = 9015  # Define a porta de conexão do servidor

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))  # Conecta ao servidor usando IP e porta

    nome = input("[Cliente] Digite seu nome: ")  # Solicita o nome do usuário
    
    cliente.sendall(nome.encode("utf-8"))  
    # Envia o nome para o servidor codificado em UTF-8

    while True:
        mensagem = input("Digite sua mensagem: ")  # Lê mensagem digitada pelo usuário
        cliente.sendall(mensagem.encode("utf-8"))  
        # Envia a mensagem para o servidor