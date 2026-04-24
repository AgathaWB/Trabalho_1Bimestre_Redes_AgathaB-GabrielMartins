import socket
import threading
from datetime import datetime

HOST = "192.168.18.26"
PORT_ENVIO = 9002
PORT_RECEPTOR = 9003

fila_mensagens = []
clientes_receptores = []
semaforo_fila = threading.Semaphore(1)

#coloca a mensagem dentro da fila
def inserir_mensagem(msg):
    with semaforo_fila:
        fila_mensagens.append(msg)

def distribuir_mensagens():
    while True:
        semaforo_fila.acquire()

        if len(fila_mensagens) > 0:
            mensagens = list(fila_mensagens)
            fila_mensagens.clear()
        else:
            mensagens = []
            
        semaforo_fila.release()

        # envia cada mensagem para todos
        for msg in mensagens:
            dados = msg.encode("utf-8")

            for cliente in clientes_receptores:
                try:
                    cliente.sendall(dados)
                except:
                    pass

def cerificar_mensagem_cliente(conn,addr):
    print(f"Cliente conectado: {addr}")

    nome = conn.recv(1024).decode("utf-8")

    while True:
        texto = conn.recv(1024).decode("utf-8")

        if not texto:
            break

        horario = datetime.now().strftime("%H:%M:%S")


        mensagem_formatada = (
            f"[{nome} ({addr[0]}) {horario}]\n"
            f"{texto}\n"
        )

        print(mensagem_formatada)
        inserir_mensagem(mensagem_formatada)

def receber_mensagem():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((HOST,PORT_ENVIO))
        servidor.listen()

        print(f"Servidor envio em {PORT_ENVIO}")

        while True:
            conn,addr = servidor.accept()

            thread_cliente = threading.Thread(target=cerificar_mensagem_cliente,args=(conn,addr), daemon=True)

            thread_cliente.start()


def receber_receptores():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

        servidor.bind((HOST,PORT_RECEPTOR))
        servidor.listen()

        print(f"Servidor receptores em {PORT_RECEPTOR}")

        while True:

            conn,addr = servidor.accept()

            # guarda conexão do receptor
            clientes_receptores.append(conn)

            print(f"Receptor conectado {addr}")

def main():
    t1 = threading.Thread(target=receber_mensagem)
    t2 = threading.Thread(target=receber_receptores)
    t3 = threading.Thread( target=distribuir_mensagens)

    t1.start()
    t2.start()
    t3.start()

if __name__=="__main__":
    main()