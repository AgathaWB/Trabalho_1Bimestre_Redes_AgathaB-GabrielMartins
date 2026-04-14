Sistema de Chat (Mensagens)
O sistema é composto por um servidor que gerencia as mensagens e dois tipos de clientes: um para envio e outro para visualização.

Arquivos:

Server.py: Centraliza as conexões, gerencia a fila de mensagens e faz o broadcast para os visualizadores.

Client.py: Interface para o usuário identificar-se e enviar textos.

Client1.py: Terminal focado apenas em receber e exibir as mensagens formatadas.

Como rodar:

Configuração de rede: O endereço em HOST deve ser o mesmo em todos os arquivos.

Execução do Servidor: Execute python Server.py. O sistema utiliza as portas 9002 para entrada e 9003 para saída.

Visualização: Execute python Client1.py para abrir a tela de recebimento.

Envio: Execute python Client.py, insira o nome e digite as mensagens no terminal.