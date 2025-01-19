import pygame
import sys
import os
import time
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, WINNING_SCORE
from engine.v2_game_engine import GameEngine

# Initialize Pygame
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

class Puck:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = PUCK_RADIUS
        self.color = color

def draw_winner(players):
    winner = None
    for k, v in players.items():
        if v["score"] >= WINNING_SCORE:  # Check if a player has won
            winner = k
            break  # Stop checking after finding the winner

    if winner:
        winner_text = font.render(f"Player {winner} Won!", True, WHITE)
        text_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Draw the text OVER the existing gameplay screen (no black background)
        screen.blit(winner_text, text_rect)
        pygame.display.flip()  # Update display to show winner text

        time.sleep(3)  # Pause for 3 seconds
        # pygame.quit()  # Quit Pygame
        # sys.exit()  # Exit the program


def draw_game(game_engine):
    screen.fill(BLACK)
    state = game_engine.get_state()

    # Draw game elements (gameplay state)
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, 10))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 10, SCREEN_WIDTH // 3, 10))
    
    pygame.draw.circle(screen, WHITE, (int(state['puck']['x']), int(state['puck']['y'])), PUCK_RADIUS)
    pygame.draw.circle(screen, BLUE, (int(state['players'][1]['x']), int(state['players'][1]['y'])), PUCK_RADIUS)
    pygame.draw.circle(screen, RED, (int(state['players'][2]['x']), int(state['players'][2]['y'])), PUCK_RADIUS)

    player_me_text = font.render(f"Player (You): {state['players'][1]['score']}", True, WHITE)
    player_opponent_text = font.render(f"Opponent: {state['players'][2]['score']}", True, WHITE)
    screen.blit(player_me_text, (20, 20))
    screen.blit(player_opponent_text, (20, SCREEN_HEIGHT - 40))

    pygame.display.flip()  # Update display

    # If the game is over, show the winner text over the final frame
    if state["game_over"]:
        draw_winner(state["players"])

game = GameEngine()
game_thread = threading.Thread(target=game.run_game_loop)
game_thread.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    draw_game(game)
    clock.tick(0)

pygame.quit()
sys.exit()
