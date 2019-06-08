
# coding: utf-8

# In[82]:


import pyglet
from pyglet.gl import *
from pyglet.window import key


# In[83]:


class square:
    
    def __init__ (self,pos,dim,color):
        self.pos=pos
        self.dim=dim
        self.c=color
        
    
    def draw(self):
        
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,

        ('v2f', (self.pos.x, self.pos.y,
                 self.pos.x+self.dim[0],self.pos.y,
                 self.pos.x+self.dim[0], self.pos.y+self.dim[1],
                 self.pos.x, self.pos.y+self.dim[1])),
        ('c3B', (self.c[0],self.c[1],self.c[2],self.c[0],self.c[1],self.c[2],self.c[0],self.c[1],self.c[2],self.c[0],self.c[1],self.c[2]))         
        )
        


# In[84]:


class velocity:
    
    def __init__(self,x,y):
        self.x =x
        self.y=y
        
    def move_up (self,vel):
        self.x += vel.x
        self.y += vel.y
        
    def move_down (self,vel):
        self.x -= vel.x
        self.y -= vel.y
    
    def move_right (self,vel):
        self.x += vel.x
        self.y += vel.y
        
    def move_left (self,vel):
        self.x -= vel.x
        self.y -= vel.y
    
    def speed(self,scal):
        self.x *= scal
        self.y *= scal
    
    def cordinates(self):
        return (self.x,self.y)


# In[85]:


class Player:
    
    def __init__(self, pos, direction, color):
        self.pos = pos
        self.color = color
        self.dir=direction
        
    def draw(self):
        square(self.pos,(15,15),self.color).draw()
        
    def update(self):
        square(self.pos,(15,15),self.color).draw()
    
    def move(self):
        if self.dir == "UP":
            self.pos.y+=velocity_y
        
        if self.dir == "RIGHT":
            self.pos.x+=velocity_x
    
    def get_cordinates(self):
        m=velocity(self.pos.x,self.pos.y)
        return m.cordinates()
        
        
    def run(self):
        self.draw()
        self.move()
        self.update()
        

        


# In[86]:


def win(player_1,RL):
        a=player_1.get_cordinates()
        b=RL.get_cordinates()

        if(abs(a[0]-b[0])<15 and abs(a[1]-b[1])<15):
            global velocity_x,velocity_y
            velocity_x=0
            velocity_y=0
            #print("win")
            #print(a,b)
        
        


# In[87]:


def collide(player_1):
    if player_1.get_cordinates()[0] >= 585:
        
        global velocity_x
        velocity_x=0
        #print("collide")
        #print(player_1.get_cordinates()[0])


# In[90]:



class Main_Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(800,600,"pyglet Physics engin")

        pyglet.clock.schedule_interval(self.update, 1 / 60)

        #square(velocity(400,350),(10,150),(0,200,0)).draw()
        self.player1 = Player(velocity(10, 400), "RIGHT", (255,0,0))
        self.player2 = Player(velocity(300, 10), "UP", (0, 0, 255))
        
    def on_draw(self):
        self.clear()
        pyglet.gl.glClearColor(1, 1, 1, 1)
        square(velocity(600,350),(10,150),(0,200,0)).draw()
        self.player1.run()
        self.player2.run()
        self.player1
        win(self.player1,self.player2)
        collide(self.player1)
        
    def update(self, dt):
        pass


# In[92]:

##
##velocity_x=1
##velocity_y=1
##global velocity_x,velocity_y
##window=Main_Window()
##pyglet.app.run()

