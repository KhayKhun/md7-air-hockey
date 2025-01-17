import pygame
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, PUCK_SPEED, PLAYER_INITIAL_X, PLAYER_INITIAL_Y, WINNING_SCORE, GOAL_WIDTH, GOAL_Y_RANGE


# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
        1: {"x": 120, "y": 250, "score": 2}, # change 1 to me (me as blue color on the bottom)
        2: {"x": 680, "y": 350, "score": 3} # change 2 to opponent (opponent as red on the top)
    },
    "time": 45.6,
    "game_over": False
}

class Puck:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
    
    def _mock_update(self):
        self.x += example_game_state["puck"]["dx"]
        self.y += example_game_state["puck"]["dy"]
        if self.x <= PUCK_RADIUS or self.x >= SCREEN_WIDTH - PUCK_RADIUS:
            example_game_state["puck"]["dx"] *= -1
        if self.y <= PUCK_RADIUS or self.y >= SCREEN_HEIGHT - PUCK_RADIUS:
            example_game_state["puck"]["dy"] *= -1

class Handie:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = PUCK_RADIUS
        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        print(f"{self.color} player moved to ({self.x}, {self.y})")
    
    def _mock_move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))

# Initialize game objects
puck = Puck(example_game_state["puck"]["x"], example_game_state["puck"]["y"], example_game_state["puck"]["radius"])
player1 = Handie(example_game_state["players"][1]["x"], example_game_state["players"][1]["y"], RED)
player2 = Handie(example_game_state["players"][2]["x"], example_game_state["players"][2]["y"], BLUE)

def draw():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, 10))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 10, SCREEN_WIDTH // 3, 10))
    
    puck.draw()
    player1.draw()
    player2.draw()
    
    player1_text = font.render(f"Player 1: {example_game_state['players'][1]['score']}", True, WHITE)
    player2_text = font.render(f"Player 2: {example_game_state['players'][2]['score']}", True, WHITE)
    screen.blit(player1_text, (20, 20))
    screen.blit(player2_text, (20, SCREEN_HEIGHT - 40))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    puck._mock_update()
    player1._mock_move()
    player2._mock_move()
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_y < SCREEN_HEIGHT // 2:
        player1.move(mouse_x, mouse_y)
    else:
        player2.move(mouse_x, mouse_y)
    
    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
