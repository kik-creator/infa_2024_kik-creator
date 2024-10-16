import pygame
from pygame.draw import *
from random import randint
pygame.init()

sysfont = pygame.font.get_default_font()
print('system font :', sysfont)
font = pygame.font.SysFont(None, 48)

FPS = 1
screen = pygame.display.set_mode((1000, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

global balls
balls = []

def add_ball():
    global balls
    balls.append([randint(100,700), randint(100,500), randint(10,70) - 40,\
    randint(10,50) - 30, randint(30,50), COLORS[randint(0, 5)]])

add_ball()
#print(balls)



def new_ball():
    '''creates new ball datastructure x,y,vx,vy,r,COLOR'''
    
    global balls
    x = randint(100,700)
    y = randint(100,500)
    vx = randint(10,70) - 40
    vy = randint(10,50) - 30 
    r = randint(30,50)
    color = COLORS[randint(0, 5)]
    #circle(screen, color, (x, y), r)
    balls.append([x, y, vx, vy, r, color])

def del_ball(numbr):
    """
    deleting ball by number 
    """
    global balls
    del balls[numbr]


def click(event):
    print(x, y, r)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    

def compare(coords1, radius, coords2):
    return radius*radius >= (coords1[0] - coords2[0])*(coords1[0] - coords2[0]) + \
            (coords1[1] - coords2[1])*(coords1[1] - coords2[1])

pygame.display.update()
clock = pygame.time.Clock()
finished = False
events = []
score = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        #events.append(event)
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            img1 = font.render('score:' + str(score), True, BLUE)
            screen.blit(img1, (20, 50))
            i = 0
            while i < len(balls):
                if compare(event.pos, balls[i][2], (balls[i][0], balls[i][1])):
                    score += 1
                    del_ball(i)
                    print(balls)
                else:
                    i+=1
                    # drawing title
                    img1 = font.render('score:' + str(score), True, BLUE)
                    screen.blit(img1, (20, 50))
                    # -----------------
    # new coordinates for balls
    for b in balls:
        b[0] += b[2]
        b[1] += b[3]
    # TO DO !  

    #add reflection from walls
    #---------------------------
    add_ball() 
    #print(balls)
   
    for b in balls:
        circle(screen, b[5], (b[0], b[1]), b[2])

    pygame.display.update()
    screen.fill(BLACK)

print(score)
pygame.quit()