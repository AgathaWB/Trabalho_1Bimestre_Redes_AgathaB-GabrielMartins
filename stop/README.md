Jogo de STOP

O jogo funciona de forma síncrona, onde o servidor coordena as rodadas e a pontuação entre os jogadores conectados.

Arquivos:

server.py: Realiza o sorteio das letras, utiliza barreiras para sincronizar os jogadores e calcula os pontos de cada rodada.

client.py: Interface onde o jogador recebe a letra e envia as respostas dos campos solicitados.

Como rodar:

Configuração: Ajuste o HOST para o IP do servidor. O código está configurado para 2 jogadores (N_J) e 3 rodadas (N_R). Alterar nas decalrações das constantes no topo do código

Servidor: Execute python3 server.py. Ele aguardará a conexão de todos os jogadores antes de iniciar.

Jogadores: Execute python3 client.py em terminais separados para cada participante.

Regras e Fluxo:

Após a conexão de todos, o servidor envia a letra sorteada.

Os jogadores preenchem NOME, CEP, PROFESSOR e COR.

A pontuação é de 3 pontos para respostas únicas, 1 ponto para repetidas e 0 para campos vazios.

O resultado acumulado é exibido após cada rodada e o vencedor é anunciado ao final.