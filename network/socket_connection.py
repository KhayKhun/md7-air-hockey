import socket
from _thread import *
import sys

sever = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((sever, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for player 2")

def threaded_player(conn):
    conn.send()
    reply = ""
    while True:
        try:
            data = conn.recv(32 )
            reply = data.decode("utf-8")

            if not data:
                print("Player Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            
            conn.sendall(str.encode(reply))
        except:
            break
        
    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Player 2 joined!!!")

    start_new_thread(threaded_player, (conn, ))