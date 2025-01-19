import socket
import json
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_HEIGHT

# Global variables
HOST = '127.0.0.1'
PORT = 21002
client_socket = None
game_state = None
player_id = None

def start_client():
    """ Connects to the server and initializes global client_socket. """
    global client_socket
    if client_socket is None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print("Connected to the game server.")

def receive_game_state():
    """ Continuously receives and updates the game state. """
    global game_state, player_id, client_socket

    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("Server closed connection.")
                break

            buffer += data  # Append received data to buffer

            while "\n" in buffer:  # Ensure we have a complete JSON object
                json_data, buffer = buffer.split("\n", 1)  # Extract one JSON object
                try:
                    game_state = json.loads(json_data)
                    if player_id is None and "player_id" in game_state:  # Assign player ID when received
                        player_id = game_state["player_id"]
                        print("Assigned Player ID:", player_id)

                except json.JSONDecodeError:
                    print("Received invalid JSON:", json_data)
        except:
            print("Error receiving game state.")
            break

def send_mouse_position(get_mouse_position):
    """ Continuously sends the player's mouse position to the server. """
    global client_socket, player_id

    while True:
        if player_id is not None:
            mouse_x, mouse_y = get_mouse_position()
            mouse_y = max(SCREEN_HEIGHT // 2, mouse_y)  # Restrict movement

            data = json.dumps({"player": player_id, "x": mouse_x, "y": mouse_y})
            try:
                client_socket.send((data + "\n").encode())  # Send movement data
            except:
                print("Lost connection to server.")
                break

        time.sleep(0.01)  # Limit update rate

def get_latest_game_state_and_player_id():
    """ Returns the latest game state and player ID. """
    return game_state, player_id
