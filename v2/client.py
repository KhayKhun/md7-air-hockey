import pygame
import socket
import threading
import json
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, WINNING_SCORE

# Network Setup
HOST = '127.0.0.1'
PORT = 21003
client_socket = None
player_id = None
game_state = None  # Stores the latest game state

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Air Hockey Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


def send_mouse_position():
    """ Tracks mouse position and sends it to the server, restricting movement based on player ID. """
    global client_socket, player_id

    while True:
        if player_id is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Restrict movement to bottom half (regardless of player_id)
            mouse_y = max(SCREEN_HEIGHT // 2, mouse_y)

            data = json.dumps({"player": player_id, "x": mouse_x, "y": mouse_y})
            try:
                client_socket.send((data + "\n").encode())  # Send movement data
            except:
                print("Lost connection to server.")
                break

        pygame.time.delay(10)  # Limit update rate




def receive_game_state():
    """ Continuously receives and updates the game state from the server. """
    global client_socket, player_id, game_state
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
                    game_state = json.loads(json_data)  # Parse JSON

                    if player_id is None:  # Assign player ID when first received
                        player_id = game_state.get("player_id", None)
                        print("Assigned Player ID:", player_id)

                except json.JSONDecodeError:
                    print("Received invalid JSON:", json_data)
        except:
            print("Error receiving game state.")
            break


def draw_winner():
    """ Displays the winner when the game is over. """
    if game_state and game_state["game_over"]:
        winner = "You" if game_state["players"]["me"]["score"] >= WINNING_SCORE else "Opponent"
        winner_text = font.render(f"{winner} Won!", True, WHITE)
        text_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(winner_text, text_rect)
        pygame.display.flip()
        time.sleep(3)  # Pause for 3 seconds before quitting
        pygame.quit()
        sys.exit()

def draw_game():
    """ Renders the game state received from the server, including puck movement. """
    screen.fill(BLACK)

    if game_state is None:
        pygame.display.flip()
        return  # Skip rendering if no game state
    print(game_state['puck'])
    if(player_id == 2):
        print("Player 2", game_state['players']['me']['x'], game_state['players']['me']['y'])
    # Draw arena elements
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, 10))  # Red goal (Top)
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 10, SCREEN_WIDTH // 3, 10))  # Blue goal (Bottom)

    # ✅ **Draw puck using server's updated position**
    puck_x = int(game_state['puck']['x'])
    puck_y = int(game_state['puck']['y'])
    pygame.draw.circle(screen, WHITE, (puck_x, puck_y), PUCK_RADIUS)

    # Get player positions
    me_x, me_y = int(game_state['players']['me']['x']), int(game_state['players']['me']['y'])
    opponent_x, opponent_y = int(game_state['players']['opponent']['x']), int(game_state['players']['opponent']['y'])

    # Flip opponent's Y-position to match POV (opponent should always be at the top)
    opponent_y = SCREEN_HEIGHT - opponent_y

    # Mirror opponent’s movement (left-right inversion)
    opponent_x = SCREEN_WIDTH - opponent_x

    # Draw players
    pygame.draw.circle(screen, BLUE if player_id == 1 else RED, (me_x, me_y), PUCK_RADIUS)
    pygame.draw.circle(screen, RED if player_id == 1 else BLUE, (opponent_x, opponent_y), PUCK_RADIUS)

    # Draw scores
    player_me_text = font.render(f"Player (You): {game_state['players']['me']['score']}", True, WHITE)
    player_opponent_text = font.render(f"Opponent: {game_state['players']['opponent']['score']}", True, WHITE)
    screen.blit(player_me_text, (20, SCREEN_HEIGHT - 40))  # Always at the bottom
    screen.blit(player_opponent_text, (20, 20))  # Always at the top

    # Check for winner
    draw_winner()

    pygame.display.flip()



def start_client():
    """ Connects to the server and keeps running. """
    global client_socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to the game server.")

    # Start networking threads
    threading.Thread(target=receive_game_state, daemon=True).start()
    threading.Thread(target=send_mouse_position, daemon=True).start()

    # Run the Pygame loop
    run_game()


def run_game():
    """ Runs the Pygame loop and handles rendering. """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        draw_game()
        clock.tick(60)  # Limit FPS


if __name__ == "__main__":
    start_client()
