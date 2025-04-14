import socket
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///gamers.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
main_socket.bind(("192.168.1.12", 10000))  # IP и порт привязываем к порту
main_socket.setblocking(False)  # Непрерывность, не ждём ответа
main_socket.listen(5)  # Прослушка входящих соединений, 5 одновременных подключений
print("Сокет создался")


def find(data):
    first = None
    for num, sign in enumerate(data):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num

            result = data[first + 1:second].split(",")
    return result


players = []


# Декларативный класс таблицы игроков
class Player(Base):
    __tablename__ = "gamers"
    name = Column(String, primary_key=True)
    password = Column(String(250))
    score = Column(Integer, default=0)

    def __init__(self, name, passw):
        self.name = name
        self.password = passw


Base.metadata.create_all(engine)

while True:
    try:
        new_socket, addr = main_socket.accept()  # принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)
        players.append(new_socket)
    except BlockingIOError:
        pass

    for sock in players:
        try:
            data = sock.recv(1024).decode()

            data = find(data)
            if data[0] == "final":
                data.remove("final")
                print(data)
                player = s.get(Player, data[0])
                print(player.score)
                if player.score < int(data[2]):
                    print("рекорд")
                    player.score = int(data[2])
                    s.merge(player)
                    s.commit()
            else:
                player = s.get(Player, data[0])
                if player:
                    if data[1] == player.password:
                        print("Welcome!")
                        sock.send(f"<{player.score}>".encode())
                    else:
                        print("Пароль неверен!")
                        sock.send("<-1>".encode())
                else:

                    player = Player(data[0], data[1])
                    s.add(player)
                    s.commit()
                    sock.send("<0>".encode())
            sock.close()
            players.remove(sock)
        except:
            pass

    time.sleep(1)
