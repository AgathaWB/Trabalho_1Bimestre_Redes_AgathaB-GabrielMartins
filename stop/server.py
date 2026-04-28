import socket
import threading
import random
import datetime

HOST = "192.168.18.26"
PORT = 9002
UTF = "utf-8"

n_jogadores = 2
n_rodadas = 3
ALFABETO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Estruturas compartilhadas
jogadores = [""] * n_jogadores
nomes = [""] * n_jogadores
ceps = [""] * n_jogadores
frutas = [""] * n_jogadores
animais = [""] * n_jogadores
pontos = [0] * n_jogadores

conexoes = [None] * n_jogadores
letra_compartilhada = [""]

# Sincronização
barreira = threading.Barrier(n_jogadores)
semaforo = threading.Semaphore(1)

# registra as mensagem do chat
mensagens = []
def registrar_mensagem(jogador_id, categoria, resposta, addr):
    horario = datetime.datetime.now().strftime("%H:%M:%S")
    msg = (
        f"[{horario}] {jogadores[jogador_id]} "
        f"({addr[0]}) enviou {categoria}: {resposta}"
    )
    with semaforo: 
        mensagens.append(msg)
    print(msg)

# verifica quantos pontos o jogador fez 
def pontuar(lista, jogador_id):
    if lista[jogador_id] == "":
        valor = 0
    elif lista.count(lista[jogador_id]) > 1:
        valor = 1
    else:
        valor = 3

    with semaforo:
        pontos[jogador_id] += valor

    return valor


def jogo(conn, addr, jogador_id):
    print(f"Jogador {jogador_id+1} conectado: {addr}")

    # Recebe nome inicial do jogador
    nome_cliente = conn.recv(1024).decode(UTF).strip()
    jogadores[jogador_id] = nome_cliente

    for rodada in range(n_rodadas):

        # jogador 0 sorteia letra
        if jogador_id == 0:
            letra_compartilhada[0] = random.choice(ALFABETO)

        barreira.wait()

        letra = letra_compartilhada[0]

        conn.sendall(
            f"\n--- RODADA {rodada+1} ---\nLetra da rodada: {letra}\n".encode(UTF)
        )

        # recebe tudo em uma mensagem só 
        dados = conn.recv(1024).decode(UTF).strip()
        nome_resp, cep_resp, fruta_resp, animal_resp = dados.split("|")

        with semaforo:
            nomes[jogador_id] = nome_resp
            ceps[jogador_id] = cep_resp
            frutas[jogador_id] = fruta_resp
            animais[jogador_id] = animal_resp

        registrar_mensagem(jogador_id,"Nome",nome_resp,addr)
        registrar_mensagem(jogador_id,"CEP",cep_resp,addr)
        registrar_mensagem(jogador_id,"Fruta",fruta_resp,addr)
        registrar_mensagem(jogador_id,"Cor",animal_resp,addr)

        # espera todos responderem
        barreira.wait()

        p1 = pontuar(nomes,jogador_id)
        p2 = pontuar(ceps,jogador_id)
        p3 = pontuar(frutas,jogador_id)
        p4 = pontuar(animais,jogador_id)

        rodada_total = p1+p2+p3+p4

        barreira.wait()

        placar = "\nPLACAR ATUAL:\n"
        for i in range(n_jogadores):
            placar += f"{jogadores[i]}: {pontos[i]} pontos\n"

        msg = (
            f"Você fez {rodada_total} pontos nesta rodada.\n"
            f"Total acumulado: {pontos[jogador_id]}\n"
            + placar
        )

        conn.sendall(msg.encode(UTF))

    barreira.wait()

    # verefica a maior pontuacao
    maior = max(pontos)
    vencedores = []

    for i in range(n_jogadores):
        if pontos[i] == maior:
            vencedores.append(i + 1)


    final = "\n=== FIM DE JOGO ===\n"

    for i in range(n_jogadores):
        final += (
            f"Jogador {i+1} ({jogadores[i]}): "
            f"{pontos[i]} pontos\n"
        )


    if len(vencedores) == 1:
        final += (
            f"VENCEDOR: {jogadores[vencedores[0]-1]} "
            f"com {maior} pontos\n"
        )
    else:
        final += "EMPATE ENTRE: "

        for v in vencedores:
            final += f"{jogadores[v-1]} "

        final += f"com {maior} pontos\n"


    conn.sendall(final.encode(UTF))

    conn.close()


def iniciar_servidor():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind((HOST,PORT))
        server.listen()

        print(f"Servidor em {HOST}:{PORT}")
        print(f"Aguardando {n_jogadores} jogadores...")

        for i in range(n_jogadores):
            conn,addr = server.accept()
            conexoes[i]=conn

            t = threading.Thread(
                target=jogo,
                args=(conn,addr,i)
            )
            t.start()

        print("Partida iniciada.")


if __name__ == "__main__":
    iniciar_servidor()