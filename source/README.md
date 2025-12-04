## 📦 Instalação (local)

### 1. Clone o repositório
```
bash
git clone https://github.com/user/RedesProject.git
cd SEU-REPO
```
### 2. Instale as dependências
```
pip install -r requirements.txt
```
### 3. Execute o servidor
```
python app.py
```
### 4. Acesse em: http://localhost:5000

# Como Funciona o Jogo

## 👑 1. Papel do Host

O Host é o criador da sala e responsável por conduzir toda a partida.  
Ele pode:

- Criar uma sala (um código único é gerado automaticamente)
- Visualizar a lista de jogadores conectados
- Iniciar uma rodada
- Enviar a pergunta “Would You Rather…?”
- Acompanhar as respostas em tempo real
- Finalizar a rodada e revelar os resultados

O Host **não vota**, apenas administra o jogo.

---

## 👥 2. Papel dos Jogadores

Os Jogadores participam da sala criada pelo Host.  
Eles podem:

- Escolher um nome para entrar no jogo
- Digitar o código da sala para participar
- Visualizar a pergunta enviada pelo Host
- Votar entre as opções A ou B
- Acompanhar as estatísticas de votos ao final da rodada

Jogadores **não podem**:
- Criar sala  
- Enviar perguntas  
- Finalizar rodada  

---

## 🔄 3. Fluxo Completo da Partida

### **1. Host cria a sala**
- O servidor gera um código automático, ex: `F9K42`.
- O Host compartilha esse código com os Jogadores.

### **2. Jogadores entram na sala**
- Cada jogador digita seu nome e o código da sala.
- O servidor confirma a entrada e todos os jogadores são listados na tela do Host.

### **3. Host inicia a rodada**
- A interface do Host permite enviar uma pergunta no formato:
  - *"Would you rather Option A or Option B?"*

### **4. Jogadores votam**
- Cada jogador vê os dois botões (A e B).
- O voto é enviado instantaneamente via WebSocket.

### **5. Votos aparecem em tempo real**
- O Host (e opcionalmente todos) veem a contagem crescer ao vivo.

### **6. Host encerra a rodada**
- O servidor bloqueia novos votos.
- O resultado final da votação é exibido para todos.

### **7. Novo round ou finalizar jogo**
- O Host pode enviar outra pergunta ou encerrar a partida.

---

## ⚡ Funcionamento em Tempo Real

A comunicação do jogo usa **WebSockets**, permitindo:

- Entrada imediata de novos jogadores  
- Votos atualizando sem recarregar a página  
- Resultados instantâneos  
- Sincronização entre Host e todos os participantes  