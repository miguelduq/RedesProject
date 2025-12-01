from websocket import create_connection
import threading

def receber(ws):
    while True:
        try:
            msg = ws.recv()
            print("Recebido:", msg)
        except Exception as e:
            print("Conexão encerrada:", e)
            break

def main():
    # troque pelo IP público ou domínio do seu servidor
    ws = create_connection("ws://SEU_IP_PUBLICO:8765")

    print("Conectado ao servidor.")

    # thread separada só para ouvir as mensagens
    t = threading.Thread(target=receber, args=(ws,))
    t.daemon = True
    t.start()

    # loop de envio
    try:
        while True:
            texto = input("Você: ")
            if not texto:
                continue
            ws.send(texto)
    except KeyboardInterrupt:
        print("\nSaindo...")
    finally:
        ws.close()

if __name__ == "__main__":
    main()