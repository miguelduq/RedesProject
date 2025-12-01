from websocket_server import WebsocketServer

# guarda todos os jogadores conectados
players = {}

def new_client(client, server):
    print(f"Novo jogador conectado: id={client['id']}")
    players[client['id']] = client
    server.send_message(client, "Bem-vindo! Você entrou no servidor do jogo.")

def client_left(client, server):
    print(f"Jogador saiu: id={client['id']}")
    if client['id'] in players:
        del players[client['id']]

def message_received(client, server, message):
    print(f"Mensagem do {client['id']}: {message}")

    # exemplo: repassar mensagem para TODOS os outros jogadores
    for pid, pclient in players.items():
        if pid != client['id']:
            server.send_message(pclient, f"Jogador {client['id']}: {message}")

def main():
    # 0.0.0.0 = aceita conexões externas (não só localhost)
    server = WebsocketServer(
        host="0.0.0.0",   # importante para servidor não local
        port=8765
    )

    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)

    print("Servidor de jogo rodando na porta 8765...")
    server.run_forever()

if __name__ == "__main__":
    main()