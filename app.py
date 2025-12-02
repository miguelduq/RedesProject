# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "segredo-maneiro"
socketio = SocketIO(app, cors_allowed_origins="*")  # usa eventlet por baixo

# rooms[room_code] = { "host_id": sid, "players": { sid: player_name } }
rooms = {}


@app.route("/")
def index():
    return render_template("index.html")


def gerar_codigo_sala():
    """Gera um código simples de 4 dígitos para a sala."""
    return str(random.randint(1000, 9999))


@socketio.on("connect")
def handle_connect():
    print("Novo cliente conectado:", request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado:", request.sid)
    sid = request.sid

    # Percorre salas para remover host/jogador
    salas_para_apagar = []

    for room_code, room in rooms.items():
        mudou = False

        # Se era o host, derruba a sala
        if room["host_id"] == sid:
            salas_para_apagar.append(room_code)
            emit(
                "errorMessage",
                "O host saiu. A sala foi encerrada.",
                to=room_code,
            )
            mudou = True

        # Se era jogador, remove da lista
        if sid in room["players"]:
            del room["players"][sid]
            mudou = True
            emit(
                "playersUpdate",
                {"players": room["players"]},
                to=room_code,
            )

        if mudou:
            print(f"Atualização na sala {room_code}")

    for room_code in salas_para_apagar:
        print(f"Removendo sala {room_code}")
        del rooms[room_code]


@socketio.on("createRoom")
def handle_create_room():
    sid = request.sid
    room_code = gerar_codigo_sala()

    rooms[room_code] = {
        "host_id": sid,
        "players": {},
    }

    join_room(room_code)
    print(f"Sala criada: {room_code} (host: {sid})")

    emit("roomCreated", {"roomCode": room_code})


@socketio.on("joinRoom")
def handle_join_room(data):
    room_code = data.get("roomCode")
    player_name = data.get("playerName", "Jogador")

    room = rooms.get(room_code)
    if not room:
        emit("errorMessage", "Sala não encontrada.")
        return

    sid = request.sid
    join_room(room_code)
    room["players"][sid] = player_name

    print(f"{player_name} entrou na sala {room_code}")

    emit("playersUpdate", {"players": room["players"]}, to=room_code)


@socketio.on("startGame")
def handle_start_game(data):
    room_code = data.get("roomCode")
    room = rooms.get(room_code)
    if not room:
        return

    sid = request.sid
    if sid != room["host_id"]:
        emit("errorMessage", "Apenas o host pode iniciar o jogo.")
        return

    print(f"Jogo iniciado na sala {room_code}")
    emit("gameStarted", to=room_code)


@socketio.on("sendQuestion")
def handle_send_question(data):
    room_code = data.get("roomCode")
    option_a = data.get("optionA")
    option_b = data.get("optionB")

    room = rooms.get(room_code)
    if not room:
        return

    sid = request.sid
    if sid != room["host_id"]:
        emit("errorMessage", "Apenas o host pode enviar perguntas.")
        return

    print(f"Pergunta enviada na sala {room_code}: A) {option_a}  B) {option_b}")
    emit("newQuestion", {"optionA": option_a, "optionB": option_b}, to=room_code)


@socketio.on("submitAnswer")
def handle_submit_answer(data):
    room_code = data.get("roomCode")
    choice = data.get("choice")

    room = rooms.get(room_code)
    if not room:
        return

    sid = request.sid
    print(f"Resposta na sala {room_code}: jogador={sid}, escolha={choice}")

    # Aqui dá pra armazenar respostas, fazer contagem, etc.
    # Por enquanto só confirma para o jogador
    emit("answerReceived", {"choice": choice})


if __name__ == "__main__":
    # socketio.run substitui app.run e já configura o servidor com WebSocket
    socketio.run(app, host="0.0.0.0", port=5000)
