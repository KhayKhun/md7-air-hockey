import pygame
from network import Network


width = 300
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Air Hockey")

clients_num = 0

class player:
    def __init__(self, radius, x, y, color):
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x, self.y = pygame.mouse.get_pos()
        #print(self.x, self.y)
        self.x = max(self.radius, min(self.x, width - self.radius))
        self.y = max(self.radius, min(self.y, height - self.radius))


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def draw_window(window, player, player2):
    window.fill((130, 56, 165))
    player.draw(window)
    player2.draw(window)
    pygame.display.update()

def main():
    running = True
    n = Network()
    startPos = read_pos(n.pygame.mouse.get_pos())
    clock = pygame.time.Clock()
    circle1 = player(20, startPos[0], startPos[1], (250, 0, 0))
    circle2 = player(20, startPos[0], startPos[1], (250, 0, 0))
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        circle2Pos = read_pos(n.send(make_pos((circle1.x, circle1.y))))
        circle2.x = circle2Pos[0]
        circle2.y = circle2Pos[1]
        circle2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        circle1.move()
        draw_window(window, circle1, circle2)
    

main()