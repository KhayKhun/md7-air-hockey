import pygame
import sys
import os
import time
import threading
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, PUCK_SPEED, PLAYER_INITIAL_X, PLAYER_INITIAL_Y, WINNING_SCORE, GOAL_WIDTH, GOAL_X_RANGE

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

class GameEngine:
    def __init__(self, winning_score=WINNING_SCORE):
        self.puck = {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT // 2, "dx": PUCK_SPEED, "dy": PUCK_SPEED}
        self.players = {
            1: {"x": PLAYER_INITIAL_X[1], "y": PLAYER_INITIAL_Y, "score": 0, "quit": False},
            2: {"x": PLAYER_INITIAL_X[2], "y": PLAYER_INITIAL_Y, "score": 0, "quit": False}
        }
        self.winning_score = winning_score
        self.game_over = False
        self.start_time = time.time()
        print("Game initialized")
    
    def track_puck(self):
        if self.game_over:
            return

        # Move puck
        self.puck["x"] += self.puck["dx"]
        self.puck["y"] += self.puck["dy"]

        # self._check_goals()
        self._check_bounce_borders()

        # Check for collision with players' paddles
        for player, data in self.players.items():
            if self._check_collision(data["x"], data["y"]):
                self.puck["dy"] *= -1  # Reverse puck direction
                print("---------------------")
                print(f"Puck collided with Player {player}")
                print("---------------------")

    def _check_bounce_borders(self):
        if self.puck["y"] <= PUCK_RADIUS:  # Top border
                self.puck["dy"] *= -1  # Bounce off the top
        elif self.puck["y"] >= SCREEN_HEIGHT - PUCK_RADIUS:  # Bottom border
                self.puck["dy"] *= -1  # Bounce off the bottom
        
        # Bounce off left and right walls
        if self.puck["x"] <= PUCK_RADIUS or self.puck["x"] >= SCREEN_WIDTH - PUCK_RADIUS:
            self.puck["dx"] *= -1
            print("---------------------")
            print("Puck bounced off wall")
            print("---------------------")
        


    def _check_goals(self):
        if self.puck["y"] <= PUCK_RADIUS:  # Top goal
            if GOAL_X_RANGE[0] <= self.puck["x"] <= GOAL_X_RANGE[1]:  # Check if within goal width
                print("---------------------")
                print("Player 2 scores!")
                print("---------------------")
                self.update_score(2)  # Player 2 scores
            else:
                self.puck["dy"] *= -1  # Bounce off the top

        elif self.puck["y"] >= SCREEN_HEIGHT - PUCK_RADIUS:  # Bottom goal
            if GOAL_X_RANGE[0] <= self.puck["x"] <= GOAL_X_RANGE[1]:  # Check if within goal width
                print("---------------------")
                print("Player 1 scores!")
                print("---------------------")
                self.update_score(1)  # Player 1 scores
            else:
                self.puck["dy"] *= -1  # Bounce off the bottom


    def _check_collision(self, handie_x, handie_y):
        return abs(self.puck["x"] - handie_x) < PUCK_RADIUS and abs(self.puck["y"] - handie_y) < PUCK_RADIUS


    def update_score(self, player):
        self.players[player]["score"] += 1
        if self.players[player]["score"] >= self.winning_score:
            self.game_over = True  # Mark game as over
            return  # Stop updating the puck, so the final frame is preserved

        # Reset puck in the center only if game is not over
        self.puck = {
            "x": SCREEN_WIDTH // 2, 
            "y": SCREEN_HEIGHT // 2, 
            "dy": PUCK_SPEED if player == 2 else -PUCK_SPEED, 
            "dx": PUCK_SPEED
        }

    def update_time(self):
        return round(time.time() - self.start_time, 1)

    def get_state(self):
        return {
            "puck": self.puck,
            "players": self.players,
            "time": self.update_time(),
            "game_over": self.game_over
        }

    def apply_inertia(self, player, target_x, target_y):
        speed = 5
        current_x, current_y = self.players[player]["x"], self.players[player]["y"]
        dx, dy = target_x - current_x, target_y - current_y
        distance = (dx**2 + dy**2) ** 0.5
        if distance > speed:
            ratio = speed / distance
            new_x, new_y = current_x + dx * ratio, current_y + dy * ratio
        else:
            new_x, new_y = target_x, target_y
        self.players[player]["x"], self.players[player]["y"] = new_x, new_y
    
    def mock_receive_mouse_data(self):
        while not self.game_over:
            new_x_me = random.randint(0, SCREEN_WIDTH)
            new_y_me = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
            new_x_opponent = random.randint(0, SCREEN_WIDTH)
            new_y_opponent = random.randint(0, SCREEN_HEIGHT // 2)

            # pygame.draw.circle(screen, GREEN, (new_x_me, new_y_me), 10)
            # pygame.draw.circle(screen, YELLOW, (new_x_opponent, new_y_opponent), 10)

            self.apply_inertia(1, new_x_me, new_y_me)
            self.apply_inertia(2, new_x_opponent, new_y_opponent)
            time.sleep(0.001)

        # Visualize the mouse tracking positions

        time.sleep(0.01)

    
    def run_game_loop(self):
        threading.Thread(target=self.mock_receive_mouse_data, daemon=True).start()
        while not self.game_over:
            self.track_puck()
            time.sleep(0.01)

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

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Restrict player movement to their half of the screen
    if mouse_y >= SCREEN_HEIGHT // 2:
        player_me.mouse_move(mouse_x, mouse_y)
    clock.tick(0)

pygame.quit()
sys.exit()
