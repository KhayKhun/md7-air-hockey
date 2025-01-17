import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        "dx": 5,
        "dy": -5,
        "radius": 15
    },
    "players": {
        1: {"x": 120, "y": 250, "score": 2},
        2: {"x": 680, "y": 350, "score": 3}
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

class Handie:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 30
        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        print(f"{self.color} player moved to ({self.x}, {self.y})")

# Initialize game objects
puck = Puck(example_game_state["puck"]["x"], example_game_state["puck"]["y"], example_game_state["puck"]["radius"])
player1 = Handie(example_game_state["players"][1]["x"], example_game_state["players"][1]["y"], RED)
player2 = Handie(example_game_state["players"][2]["x"], example_game_state["players"][2]["y"], BLUE)

def draw():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 50, 2)
    pygame.draw.rect(screen, RED, (WIDTH // 3, 0, WIDTH // 3, 10))
    pygame.draw.rect(screen, BLUE, (WIDTH // 3, HEIGHT - 10, WIDTH // 3, 10))
    
    puck.draw()
    player1.draw()
    player2.draw()
    
    player1_text = font.render(f"Player 1: {example_game_state['players'][1]['score']}", True, WHITE)
    player2_text = font.render(f"Player 2: {example_game_state['players'][2]['score']}", True, WHITE)
    screen.blit(player1_text, (20, 20))
    screen.blit(player2_text, (20, HEIGHT - 40))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_y < HEIGHT // 2:
        player1.move(mouse_x, mouse_y)
    else:
        player2.move(mouse_x, mouse_y)
    
    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
