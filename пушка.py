from random import randrange as rnd, choice
from tkinter import *
import math
 
#print (dir(math))
 
import time
import random
root = Tk()
fr = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg = 'white')
canv.pack(fill=BOTH,expand=1)

class ball():
    """ Класс ball описывает мяч. """

    def __init__(self,x=40,y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 10
        self.vy = 10
        self.color = choice(['blue','green','red','brown'])
        self.id = canv.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color)
        self.live = 30
        def set_coords(self):
              canv.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

    def move(self):
        """ Метод move описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения 
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        canv.delete(self.id)
        self.id = canv.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color)

    def hittest(self,ob):
        if (((ob.x - self.x)**2 + (ob.y - self.y)**2)**(1/2) - self.r - ob.r ) <=0:
            return True
        return False

class figures_list:

    def init(self):
        self.figures = []

    def add(self, other):
        self.figures.append(other)
        
    def delet(self, other):
        self.figures.pop(self.figures.index(other))

    def draw(self, screen):
        for i in self.figures:
            i.draw(screen)

    def update(self, width, height):
        for i in self.figures:
            i.update(width, height)

class balls_list(figures_list):
    def catch(self, x, y):
        su = 0 
        for i in self.figures:
            if i.catch(x, y, 0):
                self.delet(i)
                su += i.cost
        return su
    
    def generate(self,WIDTH, HEIGHT):
        a = random.randint(1, 8)
        for i in range(a):
            x = random.randint(50, WIDTH-50)
            y = random.randint(50, HEIGHT-50)
            vx = random.randint(-5, 5)
            vy = random.randint(-5, 5)
            color = COLORS_LIST[random.randint(1, len(COLORS_LIST)-1)]
            scale = random.randint(1, 7)
            ball = Ball(x, y, scale, color, vx, vy)
            self.add(ball)  

    def update(self, width, height):
        sc = 0
        for i in self.figures:
            for j in self.figures:
                if i.collapses < 1 and j.collapses < 1:
                    if i.centre.dist(j.centre) <= i.radius + j.radius and i.centre.dist(j.centre)>0:
                        i.collapse(j)
        for i in self.figures:
            if i.ftype == 'Ball':
                i.update(width, height)
            else:
                sc += i.update(width, height, self)
        for i in self.figures:
            i.collapses = 0
        return sc

class gun():
    """ Класс gun описывает пушку. """
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...
         
    def fire2_start(self,event):
        self.f2_on = 1

    
 
    def fire2_end(self,event):
        """ Выстрел мячом происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y)/(event.x-new_ball.x))
        new_ball.vx = self.f2_power*math.cos(self.an)
        new_ball.vy = -self.f2_power*math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10
 
 
    def targetting (self,event=0):
        """ Прицеливание. Зависит от положения мыши.
        """
        if event:
            self.an = math.atan((event.y-450)/(event.x-20))    
        if self.f2_on:
            canv.itemconfig(self.id,fill = 'orange')
        else:
            canv.itemconfig(self.id,fill = 'black')
        canv.coords(self.id, 20, 450, 20 + max(self.f2_power, 20) * math.cos(self.an), 450 + max(self.f2_power, 20) * math.sin(self.an))
         

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id,fill = 'orange')
        else:
            canv.itemconfig(self.id,fill = 'black')
        
class target():
    """ Класс target описывает цель. """ 
    def __init__(self):
        self.points = 0
        self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
        self.id = canv.create_oval(0,0,0,0)
        self.id_points = canv.create_text(30,30,text = self.points,font = '28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600,780)
        y = self.y = rnd(300,550)
        r = self.r = rnd(2,50)
        color = self.color = 'red'
        canv.coords(self.id, x-r,y-r,x+r,y+r)
        canv.itemconfig(self.id, fill = color)
         
    def hit(self, t2,points = 1):
        """ Попадание шарика в цель. """
        # canv.coords(self.id,-10,-10,-10,-10)
        self.points += points
        # canv.itemconfig(self.id_points, text = self.points)
        canv.coords(self.id, -200,-200,-200,-200)
        canv.itemconfig(self.id, fill = self.color)

        t2.new_target1()

t1 = target()
screen1 = canv.create_text(400,300, text = '',font = '28')
g1 = gun()
bullet = 0
balls = []      

class target1():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canv.create_rectangle(0,0,0,0)
        self.id_points = canv.create_text(20,20,text = self.points,font = '28')
        self.new_target1()
        
    def new_target1(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600,780)
        y = self.y = rnd(300,550)
        r = self.r = rnd(2,50)
        color = self.color = 'red'
        canv.coords(self.id, x-r,y-r,x+r,y+r)
        canv.itemconfig(self.id, fill = color)
         
    def hit(self,t1,points = 1):
        """ Попадание шарика в цель. """
        # canv.coords(self.id,-10,-10,-10,-10)
        self.points += points
        # canv.itemconfig(self.id_points, text = self.points)
        
        canv.coords(self.id, -200,-200,-200,-200)
        canv.itemconfig(self.id, fill = self.color)
        t1.new_target()


t2 = target1()



def new_game(event=''):
    global gun, t1, t2, screen1, balls, bullet
    t1.new_target()
    t2.new_target1()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
 
    z = 0.03
    t1.live = 1
    while t1.live or balls or t2.live:
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 1
                t1.hit(t2)
                canv.bind('<Button-1>', '')
                # canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text = 'Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
            if b.hittest(t2) and t2.live:
                t2.live = 1
                t2.hit(t1)
                canv.bind('<Button-1>', '')
                # canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text = 'Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text = '')
    canv.delete(gun)
    root.after(750,new_game)

new_game()   
 
mainloop()
