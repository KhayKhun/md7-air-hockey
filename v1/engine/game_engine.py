import time
import threading
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PUCK_RADIUS, PUCK_SPEED, PLAYER_INITIAL_X, PLAYER_INITIAL_Y, WINNING_SCORE, GOAL_WIDTH, GOAL_Y_RANGE


class GameEngine:
    def __init__(self, winning_score=WINNING_SCORE):
        self.puck = {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT // 2, "dx": PUCK_SPEED, "dy": PUCK_SPEED}
        self.players = {
            1: {"x": PLAYER_INITIAL_X[1], "y": PLAYER_INITIAL_Y, "score": 0, "quit" : False},
            2: {"x": PLAYER_INITIAL_X[2], "y": PLAYER_INITIAL_Y, "score": 0, "quit" : False}
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

        # Bounce off left and right walls
        if self.puck["x"] <= PUCK_RADIUS or self.puck["x"] >= SCREEN_WIDTH - PUCK_RADIUS:
            self.puck["dx"] *= -1
            print("---------------------")
            print("Puck bounced off wall")
            print("---------------------")

        # Check for goals (top or bottom side)
        if self.puck["y"] <= PUCK_RADIUS:  # Top goal
            if GOAL_WIDTH[0] <= self.puck["x"] <= GOAL_WIDTH[1]:
                print("---------------------")
                print("Player 2 scores!")
                print("---------------------")
                self.update_score(2)  # Player 2 scores
            else:
                self.puck["dy"] *= -1  # Bounce off the top

        elif self.puck["y"] >= SCREEN_HEIGHT - PUCK_RADIUS:  # Bottom goal
            if GOAL_WIDTH[0] <= self.puck["x"] <= GOAL_WIDTH[1]:
                print("---------------------")
                print("Player 1 scores!")
                print("---------------------")
                self.update_score(1)  # Player 1 scores
            else:
                self.puck["dy"] *= -1  # Bounce off the bottom

        # Check for collision with players' paddles
        for player, data in self.players.items():
            if self._check_collision(data["x"], data["y"]):
                self.puck["dy"] *= -1  # Reverse puck direction
                print("---------------------")
                print(f"Puck collided with Player {player}")
                print("---------------------")


    def _check_collision(self, handie_x, handie_y):
        return abs(self.puck["x"] - handie_x) < PUCK_RADIUS and abs(self.puck["y"] - handie_y) < PUCK_RADIUS

    def update_score(self, player):
        self.players[player]["score"] += 1
        print(f"Player {player} scores! Current score: {self.players}")
        
        if self.players[player]["score"] >= self.winning_score:
            self.game_over = True
            print(f"Player {player} wins!")

        self.puck = {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT // 2, "dx": PUCK_SPEED if player == 2 else -PUCK_SPEED, "dy": PUCK_SPEED}

    def update_time(self):
        return round(time.time() - self.start_time, 1)

    def get_state(self):
        game_state =  {
            "puck": self.puck,
            "players": self.players,
            "time": self.update_time(),
            "game_over": self.game_over
        }
        print(game_state)
        return game_state

    def set_player_position(self, player, x, y):
        self.players[player]["x"], self.players[player]["y"] = x, y
    
    def apply_inertia(self, player, target_x, target_y):
        """ Move the handie gradually towards the target position. """
        speed = 5  # Adjust speed for inertia effect
        current_x, current_y = self.players[player]["x"], self.players[player]["y"]
        dx, dy = target_x - current_x, target_y - current_y
        distance = (dx**2 + dy**2) ** 0.5

        if distance > speed:
            ratio = speed / distance # 1/time
            new_x, new_y = current_x + dx * ratio, current_y + dy * ratio
        else:
            new_x, new_y = target_x, target_y

        self.set_player_position(player, new_x, new_y) # update player position

    def mock_receive_mouse_data(self):
        while not self.game_over:
            new_x_me = random.randint(0, SCREEN_WIDTH)
            new_y_me = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
            new_x_opponent = random.randint(0, SCREEN_WIDTH)
            new_y_opponent = random.randint(0, SCREEN_HEIGHT // 2)

            self.apply_inertia(1, new_x_me, new_y_me)
            self.apply_inertia(2, new_x_opponent, new_y_opponent)
            
            time.sleep(0.1)

    def mock_receive_players_quit(self, player1_quits, player2_quits):
        if player1_quits:
            print("Player 1 quits")
        if player2_quits:
            print("Player 2 quits")

    def run_game_loop(self):
        threading.Thread(target=self.mock_receive_mouse_data, daemon=True).start() # run mock data
        while not self.game_over:
            self.track_puck()
            self.get_state()
            time.sleep(0.1)

if __name__ == "__main__":
    game = GameEngine()
    game_thread = threading.Thread(target=game.run_game_loop)
    game_thread.start()
