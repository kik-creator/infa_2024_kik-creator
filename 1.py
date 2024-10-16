import pygame
from pygame.draw import *
from random import randint
pygame.init()
print("Your name")
name = input()
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
class rectangle:
    def __init__(self, x, y, vx, vy, a, color):
        self.figurtip = "rectangle"
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.a = a
        self.color = color

    def draw(self, screen):
        rect(screen, self.color, pygame.Rect(self.x, self.y, self.a, self.a))
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if (self.x) >= 500 or (self.x) <= 0:
            self.vx = -self.vx
        if (self.y) >= 500 or (self.y) <= 0:
            self.vy = -self.vy

    def click(self, x, y):
        if abs(self.x+-x) < self.a/2 and abs(self.y-y) < self.a/2:
            print("Click!")
            return True
        return False


class ball:

    def __init__(self, x, y, vx, vy, radius, color):
        self.figurtip = 'ball'
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

    def click(self, x, y):
        if (y - self.y)**2 + (x-self.x)**2 <= self.radius**2:
            print("Click!")
            return True
        return False


number_of_ball = 100
number_of_rectangle = 100
steps_of_time_number = 100

pool = [ball(randint(-200, 200), randint(-200, 200), randint(-3, 3), randint(-3, 3), randint(10,25), COLORS[randint(0, len(COLORS)-1)]) for i in range(number_of_ball)]
pool1 = [rectangle(randint(-200, 200), randint(-200, 200), randint(-3, 3), randint(-3, 3), randint(15,25), COLORS[randint(0, len(COLORS)-1)]) for i in range(number_of_rectangle)]
for u in pool1:
    pool.append(u)
def drawText(surface, color, text, where, font_name = "Arial", font_size = 16):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if type(where) is pygame.Rect:
        text_rect.center = where.center
    else:
        text_rect.topleft = where
    surface.blit(text_surface, text_rect)
    
f = open("newgammer.txt", 'w')
f.write(name)
f.close()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for ball in pool:
                if ball.click (x, y) and ball.figurtip=="ball":
                    count+=1
                    pool.pop(pool.index(ball))
                elif ball.click (x,y) and ball.figurtip=="rectangle":
                    count+=2
                    pool.pop(pool.index(ball))
            #  click(event)
            pass

    for unit in pool:
        unit.update()
        unit.draw(screen)
    pygame.draw.rect(screen, YELLOW, pygame.Rect(20, 10, 450, 20))
    drawText(screen, BLUE, str(count), pygame.Rect(20, 10, 450, 20))
    pygame.display.update()
    screen.fill(BLACK)

f = open("newgammer.txt", 'w')
f.write(str(count))
f.close()

pygame.quit()
print(count)