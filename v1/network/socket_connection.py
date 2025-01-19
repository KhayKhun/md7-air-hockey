import socket
from _thread import *
import sys

sever = "192.168.1.67"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((sever, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for player 2")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(50, 50), (100, 100)]
def threaded_player(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Player Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending: ", reply)
            
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
        
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Player 2 joined!!!", addr)

    start_new_thread(threaded_player, (conn, currentPlayer))
    currentPlayer += 1