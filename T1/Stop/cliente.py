import socket
HOST = "192.168.248.116"
PORT = 9002
U = "utf-8"
N_R = 3 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print(f"[*] Conectado ao servidor {HOST}:{PORT}")

    j = 0
    while j < N_R:
        # 1. Recebe a letra da rodada
        mensagem_servidor = cliente.recv(1024).decode(U)
        print(mensagem_servidor)

        # 2. Envia as respostas na ordem exata dos recvs do servidor
        NOME = input("NOME: ")
        cliente.sendall(NOME.encode(U))

        CEP = input("CEP: ")
        cliente.sendall(CEP.encode(U))

        MEU_PROFESSOr = input("MEU PROFESSOR: ")
        cliente.sendall(MEU_PROFESSOr.encode(U))

        COR = input("COR: ")
        cliente.sendall(COR.encode(U))

        print("\n[*] Aguardando processamento da rodada...")

        # 3. Recebe a parcial de pontos
        status_pontos = cliente.recv(1024).decode(U)
        print(status_pontos)

        j += 1

    # 4. Recebe o anúncio final do vencedor
    anuncio_final = cliente.recv(1024).decode(U)
    print(anuncio_final)

