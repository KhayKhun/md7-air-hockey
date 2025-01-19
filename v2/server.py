import socket
import threading
import json
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from v2.game_engine import GameEngine
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT


HOST = '0.0.0.0'
PORT = 21003

clients = {}  # Dictionary to store connected clients {addr: socket}
players = {}  # Stores player assignment {addr: player_number}
game = GameEngine()


def handle_client(client_socket, addr):  # Own thread
    """ Handles incoming messages from clients and updates game state. """
    global clients, players, game

    # Assign player ID (1 or 2)
    player_number = 1 if len(players) == 0 else 2
    players[addr] = player_number
    print(f"Player {player_number} connected from {addr}")

    # Send initial game state with player_id
    initial_state = game.get_state()
    # Include player ID in first message
    initial_state["player_id"] = player_number
    print(initial_state)
    initial_state["players"] = {
        "me": initial_state["players"][player_number],
        "opponent": initial_state["players"][2 if player_number == 1 else 1]
    }
    # Send directly to the new client
    client_socket.send((json.dumps(initial_state) + "\n").encode())

    buffer = ""

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                print("Client disconnected:", addr)
                break

            buffer += data  # Append received data to buffer

            while "\n" in buffer:  # Ensure we have a complete JSON object
                json_data, buffer = buffer.split(
                    "\n", 1)  # Extract one JSON object
                try:
                    player_data = json.loads(json_data)  # Parse JSON
                    player_id = player_data["player"]
                    x, y = player_data["x"], player_data["y"]

                    # Apply movement to the correct player
                    game.apply_inertia(player_id, x, y)

                    # Send updated game state to all clients
                    send_game_state()

                except json.JSONDecodeError:
                    print("Received invalid JSON:", json_data)

            time.sleep(0.05)  # Reduce CPU usage

    except (ConnectionResetError, BrokenPipeError):
        print(f"Player {player_id} disconnected.")

    # Remove client from the game
    del clients[addr]
    del players[addr]
    client_socket.close()


def send_game_state():
    """ Sends the current game state to all clients. """
    global clients, players, game

    game_state = game.get_state()

    for addr, client_socket in clients.items():
        player_id = players[addr]

        # **Normal for Player 1, Mirrored for Player 2**
        puck_x, puck_y = game_state["puck"]["x"], game_state["puck"]["y"]

        if player_id == 2:  # Mirror for Player 2
            puck_x = SCREEN_WIDTH - puck_x  # Left-right inversion
            puck_y = SCREEN_HEIGHT - puck_y  # Flip y-position
        print('Player 1:', game_state["players"][1]['x'], game_state["players"][1]['y'])
        print('Player 2:', game_state["players"][2]['x'], game_state["players"][2]['y'])
        print('Puck:', game_state["puck"]["x"], game_state["puck"]["y"])
        print("##################")
        # Send transformed game state
        state_for_client = {
            "puck": {"x": puck_x, "y": puck_y},  # Send adjusted puck position
            "players": {
                "me": game_state["players"][player_id],
                "opponent": game_state["players"][2 if player_id == 1 else 1]
            },
            "game_over": game_state["game_over"],
            "player_id": player_id  # Ensure player_id is always sent
        }

        try:
            client_socket.send((json.dumps(state_for_client) + "\n").encode())
        except:
            print(f"Failed to send data to {addr}")



def start_server():
    """ Starts the game server and listens for client connections. """
    global clients, players, game

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)  # Max 2 players
    print(f"Server running on {HOST}:{PORT}")

    while len(clients) < 2:  # Wait for two players
        client_socket, addr = server_socket.accept()
        clients[addr] = client_socket
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

    print("Game started!")

    # 🔹 **Start a separate thread to move the puck continuously**
    threading.Thread(target=move_puck_loop, daemon=True).start()

    # 🔹 Keep the main thread running indefinitely
    while True:
        time.sleep(1)  # Prevents CPU from running at 100% usage


def move_puck_loop():
    """ Moves the puck continuously in the game engine and updates clients. """
    while not game.game_over:
        game.track_puck()  # Move the puck based on game physics
        send_game_state()  # Send updated puck position to clients
        time.sleep(0.05)  # Limit update rate (100 FPS)



if __name__ == "__main__":
    start_server()
