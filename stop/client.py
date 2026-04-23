import socket

HOST = "192.168.18.26"
PORT = 9002
UTF = "utf-8"
N_R = 3

# verifica se a letra está certa (deixando passar se a resposta for nula)
def verificar_entrada(campo, letra):
    while True:
        valor = input(f"{campo}: ").strip().upper()

        if valor == "":
            return valor
        if valor and valor[0] == letra:
            return valor
        
        print(
            f"Entrada inválida! Deve começar com {letra}."
        )


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST,PORT))

    print(f"Conectado em {HOST}:{PORT}")

    nome_jogador = input("Digite seu nome: ")
    cliente.sendall(nome_jogador.encode(UTF))

    for rodada in range(N_R):

        msg = cliente.recv(1024).decode(UTF)
        print(msg)

        # vai pegar a primeira letra da palavra e coloca na variavel "letra" para enviar ao método 
        letra = msg.split(":")[-1].strip().upper()

        nome = verificar_entrada("NOME",letra)
        cep = verificar_entrada("CEP",letra)
        fruta = verificar_entrada("FRUTA",letra)
        animal = verificar_entrada("ANIMAL",letra)

        # envia tudo em uma mensagem só
        pacote = f"{nome}|{cep}|{fruta}|{animal}"
        cliente.sendall(pacote.encode(UTF))

        print("\nAguardando pontuação...")

        retorno = cliente.recv(2048).decode(UTF)
        print(retorno)

    fim = cliente.recv(4096).decode(UTF)
    print(fim)