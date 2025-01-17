import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 400
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
paddle_radius = 30
puck_radius = 15

# Paddle Positions
player1_pos = [WIDTH // 2, HEIGHT // 4]
player2_pos = [WIDTH // 2, 3 * HEIGHT // 4]

# Puck Position
puck_pos = [WIDTH // 2, HEIGHT // 2]

# Score
player1_score = 0
player2_score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Draw Elements
def draw():
    screen.fill(BLACK)
    # Draw the Table
    pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)  # Center line
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 50, 2)  # Center circle
    
    # Goals
    pygame.draw.rect(screen, RED, (WIDTH // 3, 0, WIDTH // 3, 10))  # Top goal
    pygame.draw.rect(screen, BLUE, (WIDTH // 3, HEIGHT - 10, WIDTH // 3, 10))  # Bottom goal
    
    # Paddles and Puck
    pygame.draw.circle(screen, RED, player1_pos, paddle_radius)
    pygame.draw.circle(screen, BLUE, player2_pos, paddle_radius)
    pygame.draw.circle(screen, WHITE, puck_pos, puck_radius)
    
    # Scores
    player1_text = font.render(f"Player 1: {player1_score}", True, WHITE)
    player2_text = font.render(f"Player 2: {player2_score}", True, WHITE)
    screen.blit(player1_text, (20, 20))
    screen.blit(player2_text, (20, HEIGHT - 40))

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Mouse Movement
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Update Player 1 Position (Top Half)
    if mouse_y < HEIGHT // 2:
        player1_pos[0] = mouse_x
        player1_pos[1] = mouse_y
        # Boundary Check for Player 1
        if player1_pos[0] - paddle_radius < 0:
            player1_pos[0] = paddle_radius
        if player1_pos[0] + paddle_radius > WIDTH:
            player1_pos[0] = WIDTH - paddle_radius
        if player1_pos[1] - paddle_radius < 0:
            player1_pos[1] = paddle_radius
    
    # Update Player 2 Position (Bottom Half)
    elif mouse_y >= HEIGHT // 2:
        player2_pos[0] = mouse_x
        player2_pos[1] = mouse_y
        # Boundary Check for Player 2
        if player2_pos[0] - paddle_radius < 0:
            player2_pos[0] = paddle_radius
        if player2_pos[0] + paddle_radius > WIDTH:
            player2_pos[0] = WIDTH - paddle_radius
        if player2_pos[1] + paddle_radius > HEIGHT:
            player2_pos[1] = HEIGHT - paddle_radius
    
    # Redraw Elements
    draw()
    
    # Update Display
    pygame.display.flip()
    
    # Frame Rate
    clock.tick(60)

pygame.quit()
sys.exit()