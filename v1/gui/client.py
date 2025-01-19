import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS

# Initialize Pygame
pygame.init()

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Air Hockey Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game Elements
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Example game state data
example_game_state = {
    "puck": {
        "x": 420,
        "y": 310,
    },
    "players": {
        "me": {"x": 120, "y": 250, "score": 2, "quit" : False},
        "opponent": {"x": 680, "y": 50, "score": 3, "quit" : False}
    },
    "time": 45.6,
    "game_over": False
}

# Data Storage Classes
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
    
    def mouse_move(self, new_x, new_y): # sed the mouse coordinates to server
        self.apply_inertia(new_x, new_y)
        
        print(f"{self.color} player moved to ({self.x}, {self.y})")

    def apply_inertia(self, target_x, target_y):
        """ Move the handie gradually towards the target position. """
        speed = 5  # Adjust speed for inertia effect
        current_x, current_y = self.x, self.y

        dx, dy = target_x - current_x, target_y - current_y
        distance = (dx**2 + dy**2) ** 0.5

        if distance > speed:
            ratio = speed / distance # 1/time
            new_x, new_y = current_x + dx * ratio, current_y + dy * ratio
        else:
            new_x, new_y = target_x, target_y

        self.x = new_x
        self.y = new_y

# Initialize game objects
puck = Puck(example_game_state["puck"]["x"], example_game_state["puck"]["y"], PUCK_RADIUS)
player_me = Player(example_game_state["players"]["me"]["x"], example_game_state["players"]["me"]["y"], BLUE)
player_opponent = Player(example_game_state["players"]["opponent"]["x"], example_game_state["players"]["opponent"]["y"], RED)

# Drawing Functions
def draw_puck(puck):
    pygame.draw.circle(screen, WHITE, (int(puck.x), int(puck.y)), puck.radius)

def draw_player(player):
    pygame.draw.circle(screen, player.color, (int(player.x), int(player.y)), player.radius)

def draw_game():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, 10))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 10, SCREEN_WIDTH // 3, 10))
    
    draw_puck(puck)
    draw_player(player_me)
    draw_player(player_opponent)
    
    player_me_text = font.render(f"Player (You): {example_game_state['players']['me']['score']}", True, WHITE)
    player_opponent_text = font.render(f"Opponent: {example_game_state['players']['opponent']['score']}", True, WHITE)
    screen.blit(player_me_text, (20, 20))
    screen.blit(player_opponent_text, (20, SCREEN_HEIGHT - 40))

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Restrict player movement to their half of the screen
    if mouse_y >= SCREEN_HEIGHT // 2:
        player_me.mouse_move(mouse_x, mouse_y)
    
    # Opponent follows predefined state (simulated movement)
    player_opponent.mouse_move(example_game_state["players"]["opponent"]["x"], example_game_state["players"]["opponent"]["y"])
    
    draw_game()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
