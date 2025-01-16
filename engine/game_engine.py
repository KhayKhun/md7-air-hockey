import time
import threading
import random

# Global Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PUCK_RADIUS = 20
PUCK_SPEED = 5
PLAYER_INITIAL_X = {1: 100, 2: 700}
PLAYER_INITIAL_Y = SCREEN_HEIGHT // 2
WINNING_SCORE = 5
GOAL_WIDTH = 200
GOAL_Y_RANGE = ((SCREEN_HEIGHT - GOAL_WIDTH) // 2, (SCREEN_HEIGHT + GOAL_WIDTH) // 2)

class GameEngine:
    def __init__(self, winning_score=WINNING_SCORE):
        self.puck = {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT // 2, "dx": PUCK_SPEED, "dy": PUCK_SPEED}
        self.players = {
            1: {"x": PLAYER_INITIAL_X[1], "y": PLAYER_INITIAL_Y, "score": 0},
            2: {"x": PLAYER_INITIAL_X[2], "y": PLAYER_INITIAL_Y, "score": 0}
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
        print(f"Puck position: {self.puck}")
        
        # Bounce off top and bottom walls
        if self.puck["y"] <= PUCK_RADIUS or self.puck["y"] >= SCREEN_HEIGHT - PUCK_RADIUS:
            self.puck["dy"] *= -1
            print("Puck bounced off wall")
        
        # Check for goals (left or right side)
        if self.puck["x"] <= PUCK_RADIUS:
            if GOAL_Y_RANGE[0] <= self.puck["y"] <= GOAL_Y_RANGE[1]:
                self.update_score(2)  # Player 2 scores
            else:
                self.puck["dx"] *= -1  # Bounce off the side
        elif self.puck["x"] >= SCREEN_WIDTH - PUCK_RADIUS:
            if GOAL_Y_RANGE[0] <= self.puck["y"] <= GOAL_Y_RANGE[1]:
                self.update_score(1)  # Player 1 scores
            else:
                self.puck["dx"] *= -1  # Bounce off the side

        # Check for collision with players' handies
        for player, data in self.players.items():
            if self._check_collision(data["x"], data["y"]):
                self.puck["dx"] *= -1  # Reverse puck direction
                print(f"Puck collided with Player {player}")

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
        return {
            "puck": self.puck,
            "players": self.players,
            "time": self.update_time(),
            "game_over": self.game_over
        }

    def set_player_position(self, player, x, y):
        self.players[player]["x"], self.players[player]["y"] = x, y
        print(f"Player {player} moved to: ({x}, {y})")
    
    def mock_receive_data(self):
        while not self.game_over:
            for player in self.players:
                new_x = random.randint(0, SCREEN_WIDTH // 2) if player == 1 else random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH)
                new_y = random.randint(0, SCREEN_HEIGHT)
                self.set_player_position(player, new_x, new_y)
            time.sleep(0.1)

    def run_game_loop(self):
        threading.Thread(target=self.mock_receive_data, daemon=True).start()
        while not self.game_over:
            self.track_puck()
            time.sleep(0.5)

if __name__ == "__main__":
    game = GameEngine()
    game_thread = threading.Thread(target=game.run_game_loop)
    game_thread.start()
