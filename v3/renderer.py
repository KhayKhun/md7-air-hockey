import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, WINNING_SCORE

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

def get_mouse_position():
    """ Tracks mouse position and sends it to the server, restricting movement based on player ID. """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return mouse_x, mouse_y

def draw_winner(state):
    """ Displays the winner when the game is over. """
    if state and state["game_over"]:
        winner = "You" if state["players"]["me"]["score"] >= WINNING_SCORE else "Opponent"
        winner_text = font.render(f"{winner} Won!", True, WHITE)
        text_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(winner_text, text_rect)
        pygame.display.flip()

def draw_game(get_state_fnc):
    """ Renders the game state received from the server, including puck movement. """
    state, player_id = get_state_fnc()
    if state is None:
        return  # Skip rendering if no game state

    screen.fill(BLACK)

    # Draw arena elements
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, 10))  # Red goal (Top)
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 10, SCREEN_WIDTH // 3, 10))  # Blue goal (Bottom)

    # Draw puck
    puck_x = int(state['puck']['x'])
    puck_y = int(state['puck']['y'])
    pygame.draw.circle(screen, WHITE, (puck_x, puck_y), PUCK_RADIUS)

    # Get player positions
    me_x, me_y = int(state['players']['me']['x']), int(state['players']['me']['y'])
    opponent_x, opponent_y = int(state['players']['opponent']['x']), int(state['players']['opponent']['y'])

    # Flip opponent's Y-position to match POV (opponent should always be at the top)
    opponent_y = SCREEN_HEIGHT - opponent_y
    opponent_x = SCREEN_WIDTH - opponent_x  # Mirror left-right

    # Draw players
    pygame.draw.circle(screen, BLUE if player_id == 1 else RED, (me_x, me_y), PUCK_RADIUS)
    pygame.draw.circle(screen, RED if player_id == 1 else BLUE, (opponent_x, opponent_y), PUCK_RADIUS)

    # Draw scores
    player_me_text = font.render(f"Player (You): {state['players']['me']['score']}", True, WHITE)
    player_opponent_text = font.render(f"Opponent: {state['players']['opponent']['score']}", True, WHITE)
    screen.blit(player_me_text, (20, SCREEN_HEIGHT - 40))  # Always at the bottom
    screen.blit(player_opponent_text, (20, 20))  # Always at the top

    # Check for winner
    draw_winner(state)

    pygame.display.flip()

def run_game(get_state_fnc):
    """ Runs the game loop and continuously fetches the latest game state. """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        draw_game(get_state_fnc)
        clock.tick(60)  # Limit FPS
