import socket
import threading
import pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0



def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except Exception:
        pass
    idCount -= 1
    conn.close()


while True:
    Conn, Addr = s.accept()
    print("Connected to:", Addr)

    idCount += 1
    P = 0
    GameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[GameId] = Game(GameId)
        print("Creating a new game...")
    else:
        games[GameId].ready = True
        P = 1

    thread = threading.Thread(target=threaded_client, args=(Conn, P, GameId))
    thread.start()

