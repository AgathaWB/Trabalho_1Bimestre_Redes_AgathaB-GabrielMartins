# Jogo STOP (Sockets e Threads)

## 1. Introdução

Este projeto implementa o jogo STOP em um ambiente distribuído utilizando Python. Um servidor central coordena múltiplos jogadores conectados via sockets.

---

## 2. Objetivo

O sistema tem como finalidade:
- Permitir múltiplos jogadores simultâneos
- Controlar rodadas automaticamente
- Coletar respostas dos jogadores
- Calcular pontuações
- Determinar o vencedor final

---

## 3. Arquitetura do Sistema

### Servidor (servidor.py)
- Aguarda conexões dos jogadores
- Controla número de jogadores
- Sorteia letras
- Recebe respostas
- Calcula pontuação
- Envia resultados

### Cliente (cliente.py)
- Conecta ao servidor
- Envia nome
- Recebe letra da rodada
- Permite entrada de respostas
- Envia respostas
- Exibe resultados

---

## 4. Funcionamento do Jogo

1. Jogadores conectam ao servidor
2. Servidor aguarda número mínimo de jogadores
3. Servidor sorteia uma letra
4. Jogadores enviam respostas
5. Servidor aguarda todos
6. Servidor calcula pontuação:
   - Única: 3 pontos
   - Repetida: 1 ponto
   - Nenhuma: 0 pontos
7. Servidor envia resultados
8. Processo se repete por várias rodadas
9. Ao final, o vencedor é exibido

---

## 5. Regras do Jogo

- Respostas devem iniciar com a letra sorteada
- Todos os temas devem ser preenchidos
- Pontuação:
  - Resposta única: 3 pontos
  - Resposta repetida: 1 ponto
  - Resposta nula: 0 pontos 

---

## 6. Concorrência

O servidor utiliza:
- `threading.Thread` para múltiplos jogadores
- `threading.Semaphore` para controle de acesso às respostas

---

### 7. Configuração de Rede
### Mesmo computador
localhost

### Computadores diferentes
IP_DO_SERVIDOR

### Exemplo:

192.168.0.10

### 8. Como Executar
### Requisitos
Python 3 instalado

### Executar servidor
python servidor.py

### Executar clientes
python cliente.py

### Executar um cliente para cada jogador.

### 9. Exemplo de Execução
Letra sorteada: A

Jogador 1:
Animal: Anta
Cidade: Arapongas

Jogador 2:
Animal: Anta
Cidade: Americana

Pontuação:
Jogador 1: 4 pontos
Jogador 2: 4 pontos

---

### 10. Observações Importantes
- Todos os jogadores devem estar conectados antes do início
- O número de jogadores é fixo no servidor
- A porta deve estar disponível
- Pode ser necessário liberar firewall
- Pode ser testado com múltiplos terminais no mesmo computador
