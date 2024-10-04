import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 100
screen = pygame.display.set_mode((500, 500))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
count = 0

class ball:

    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
    def draw(self, screen):
        circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if (self.x) >= 500 or (self.x) <= 0:
            self.vx = -self.vx
        if (self.y) >= 500 or (self.y) <= 0:
            self.vy = -self.vy

number_of_ball = 100
steps_of_time_number = 100

pool = [ball(randint(-200, 200), randint(-200, 200), randint(-5, 5), randint(-5, 5), 20, COLORS[randint(0, len(COLORS)-1)]) for i in range(number_of_ball)]



# def click(event):        
#     global count     
#     x1, y1 = pygame.mouse.get_pos()
#     if (y - y1)**2 + (x-x1)**2 <= r**2:
#         print("Click!")
#         count += 1
#     print(x, y, r)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #  click(event)
            pass

    for unit in pool:
        unit.update()
        unit.draw(screen)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
print(count)