import pygame

width = 1000
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
        self.x = max(self.radius, min(self.x, width - self.radius))
        self.y = max(self.radius, min(self.y, height - self.radius))



def draw_window(window, player):
    window.fill((130, 56, 165))
    player.draw(window)
    pygame.display.update()

def main():
    running = True
    clock = pygame.time.Clock()
    circle = player(20, 0, 0, (250, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        circle.move()
        draw_window(window, circle)
        clock.tick(60)
    pygame.quit()

main()