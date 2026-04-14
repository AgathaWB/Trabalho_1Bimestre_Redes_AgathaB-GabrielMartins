import socket
import threading
import random
import time

HOST = "192.168.248.116"
PORT = 9002
U = "utf-8"
N_J = 2  # Quantidade de jogadores para iniciar / Numero de Jogadores
N_R = 3  # Quantidade de rodadas / Numero de Rodadas
ALFABETO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


NOME = []
CEP = []
MEU_PROFESSOr = []
COR = []
PONTOS = []
CONEXOES = []
LETRA_COMPARTILHADA = []

barreira = threading.Barrier(N_J)

def verificar_ocorrencia_pontos(lista, j):
    # x = 1 se for repetido ou vazio, x = 3 se for único
    x = 3
    # Se o campo estiver vazio, não ganha pontos
    if lista[j] == "":
        x = 0
    # Se a resposta aparece mais de uma vez na lista da rodada
    elif lista.count(lista[j]) > 1:
        x = 1
    
    PONTOS[j] += x
    return x

def jogo(conn, addr, jogador_id):
    print(f"[Server] Jogador {jogador_id} conectado: {addr}")
    
    j = 0
    while j < N_R:
        # O Jogador 0 sorteia a letra para todos
        if jogador_id == 0:
            LETRA_COMPARTILHADA[0] = random.choice(ALFABETO)
        
        barreira.wait() # Aguarda sorteio da letra
        
        letra = LETRA_COMPARTILHADA[0]
        conn.sendall(f"\n--- RODADA {j+1} --- \nLetra da rodada: {letra}\n".encode(U))
        
        # .strip() remove espaços extras e o \n do terminal
        NOME[jogador_id] = conn.recv(1024).decode(U).strip()
        CEP[jogador_id] = conn.recv(1024).decode(U).strip()
        MEU_PROFESSOr[jogador_id] = conn.recv(1024).decode(U).strip()
        COR[jogador_id] = conn.recv(1024).decode(U).strip()
        
        # BARREIRA 1: Espera todos os jogadores enviarem as respostas
        barreira.wait()
        
        # Calcula pontos chamando seu método para cada lista
        v1 = verificar_ocorrencia_pontos(NOME, jogador_id)
        v2 = verificar_ocorrencia_pontos(CEP, jogador_id)
        v3 = verificar_ocorrencia_pontos(MEU_PROFESSOr, jogador_id)
        v4 = verificar_ocorrencia_pontos(COR, jogador_id)
        
        total_da_rodada = v1 + v2 + v3 + v4
        
        # Barreira 2: Espera todos calcularem antes de enviar o status
        barreira.wait()
        
        msg_status = f"Voce fez {total_da_rodada} pontos nesta rodada. Total acumulado: {PONTOS[jogador_id]}\n"
        conn.sendall(msg_status.encode(U))
        
        j += 1

    # --- Final do Jogo
    barreira.wait() # Garante que todos saíram do loop de rodadas
    
    #Vencedor
    maior_pontuacao = max(PONTOS)
    vencedor_id = PONTOS.index(maior_pontuacao)
    
    anuncio = f"FIM DE JOGO!\nO VENCEDOR FOI O JOGADOR {vencedor_id} COM {maior_pontuacao} PONTOS!"
    conn.sendall(anuncio.encode(U))
    
    print(f"[Server] Conexão com Jogador {jogador_id + 1} encerrada.")
    conn.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        
        print(f"Servidor STOP rodando em {HOST}:{PORT}")
        print(f"Aguardando {N_J} jogadores...")
        
        idx = 0
        while idx < N_J:
            conn, addr = server.accept()
            CONEXOES[idx] = conn 
            
            thread = threading.Thread(
                target=jogo, 
                args=(conn, addr, idx)
            )
            thread.start()
            idx += 1
            
        print("[Server] Todos os jogadores conectaram. Partida iniciada!")

if __name__ == "__main__":
    iniciar_servidor()