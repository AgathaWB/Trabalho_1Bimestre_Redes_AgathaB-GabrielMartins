# Sistema de Mensagens em Grupo (Sockets e Threads)

## 1. Introdução

Este projeto implementa um sistema distribuído de mensagens em grupo utilizando sockets TCP em Python. Um servidor central é responsável por receber mensagens de múltiplos clientes e distribuí-las para todos os demais.

O cliente foi dividido em duas aplicações distintas:
- Um cliente responsável pelo envio de mensagens
- Um cliente responsável pelo recebimento de mensagens

Essa separação permite execução simultânea e contínua, simulando aplicações reais de comunicação.

---

## 2. Objetivo

O sistema tem como objetivos:
- Permitir comunicação entre múltiplos clientes
- Garantir acesso concorrente seguro no servidor
- Distribuir mensagens para todos os clientes conectados
- Identificar cada mensagem com nome, IP e horário

---

## 3. Arquitetura do Sistema

O sistema é composto por três programas:

### Servidor (servidor.py)
Responsável por:
- Aceitar múltiplas conexões simultâneas
- Criar threads para cada cliente
- Receber mensagens
- Armazenar mensagens em uma fila compartilhada
- Controlar acesso à fila com semáforos
- Distribuir mensagens aos clientes

### Cliente de Envio (cliente_envio.py)
- Recebe entrada do usuário via terminal
- Envia nome ao conectar
- Envia mensagens ao servidor

### Cliente de Recebimento (cliente_recebimento.py)
- Solicita mensagens ao servidor
- Exibe mensagens no terminal
- Executa continuamente em loop

---

## 4. Funcionamento do Sistema

1. O servidor é iniciado e aguarda conexões
2. Os clientes se conectam ao servidor
3. Cada cliente envia seu nome
4. O cliente de envio permite digitar mensagens
5. O servidor:
   - Recebe a mensagem
   - Armazena na fila
   - Adiciona nome, IP e horário
6. O cliente de recebimento solicita mensagens
7. O servidor envia as mensagens disponíveis
8. O processo ocorre continuamente

---

## 5. Estrutura das Mensagens

Formato padrão:
[Nome (IP) HH:MM:SS]
Mensagem

---

## 6. Concorrência

O servidor utiliza:
- `threading.Thread` para múltiplos clientes
- `threading.Semaphore` para proteger a fila de mensagens

Isso evita problemas de acesso simultâneo e garante integridade dos dados.

---

### 7. Configuração de Rede

### Porta utilizada
Exemplo no código:
PORTA = 12345
Execução no mesmo computador:
127.0.0.1

---

### 8. Como Executar
### Requisitos
Python 3 instalado

### Verificar versão:
python --version

### Executar o cliente:
python client_envio.py

python client_recebe.py

### Executar o servidor:
python server.py

### 9. Observações Importantes
- O servidor deve ser iniciado antes dos clientes
- Cliente de envio e recebimento são processos separados
- Cada cliente pode enviar várias mensagens
- A porta deve estar livre
- Pode ser necessário liberar firewall
- Para testes, utilizar múltiplos terminais
- Funciona em rede local ou entre computadores