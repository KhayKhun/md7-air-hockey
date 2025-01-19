import threading
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from v3.client_socket import start_client, receive_game_state, send_mouse_position, get_latest_game_state_and_player_id
from v3.renderer import run_game, get_mouse_position

def game_loop():
    """ Main game loop to manage game state, rendering, and user input. """

    # Start networking threads
    threading.Thread(target=receive_game_state, daemon=True).start()
    threading.Thread(target=send_mouse_position, args=(get_mouse_position,), daemon=True).start()

    # Wait until game_state and player_id are initialized
    while True:
        gs, pid = get_latest_game_state_and_player_id()
        if gs is not None and pid is not None:
            break  # Proceed when valid game state & player ID are received

        print("Waiting for game state...")
        time.sleep(0.1)

    print("Game state received, starting renderer...")

    run_game(get_latest_game_state_and_player_id)  # Now dynamically retrieves state
    

if __name__ == "__main__":
    start_client()  # Connect to the server
    game_loop()  # Start the game loop
