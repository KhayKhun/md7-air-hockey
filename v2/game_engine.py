import sys
import os
import time
import threading
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, PUCK_SPEED, PLAYER_INITIAL_X, PLAYER_INITIAL_Y, WINNING_SCORE, GOAL_X_RANGE


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

        self._check_goals()
        self._check_bounce_borders()

        # ✅ Check for collision with both players
        for player, data in self.players.items():
            if self._check_collision(data["x"], data["y"], player):  # Pass `player` to fix for Player 2
                self.puck["dy"] *= -1  # Reverse puck direction
                print("---------------------")
                print(f"Puck collided with Player {player}")
                print("---------------------")


    def _check_collision(self, handie_x, handie_y, player_id):
        """ Checks if the puck collides with a player's handie. """
        
        # ✅ If Player 2, FLIP THE PUCK POSITION instead of flipping the paddle
        puck_x, puck_y = self.puck["x"], self.puck["y"]
        if player_id == 2:
            puck_x = SCREEN_WIDTH - puck_x
            puck_y = SCREEN_HEIGHT - puck_y

        return abs(puck_x - handie_x) < PUCK_RADIUS and abs(puck_y - handie_y) < PUCK_RADIUS


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

            self.apply_inertia(1, new_x_me, new_y_me)
            self.apply_inertia(2, new_x_opponent, new_y_opponent)
            time.sleep(0.001)

        time.sleep(0.01)

    
    def run_game_loop(self):
        threading.Thread(target=self.mock_receive_mouse_data, daemon=True).start()
        while not self.game_over:
            self.track_puck()
            time.sleep(0.01)
