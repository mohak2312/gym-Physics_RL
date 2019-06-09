import gym
from random import randint
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet import image 


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

class Player:
    def __init__(self, pos, direction, color):
        self.pos = pos
        self.color = color
        self.dir=direction
        self.velocity_x =0 
        self.velocity_y =0
        
    def draw(self):
        square(self.pos,(15,15),self.color).draw()
        
    def update(self):
        square(self.pos,(15,15),self.color).draw()
        
        
    def move(self):        
        if self.dir == "UP":
            self.pos.y+= self.velocity_y
        
        if self.dir == "RIGHT":
            self.pos.x += self.velocity_x
    
    def get_cordinates(self):
        m=velocity(self.pos.x,self.pos.y)
        return m.cordinates()
        
        
    def run(self):
        self.draw()
        self.move()
        self.update()
    

class Main_Window():
#class Main_Window(pyglet.window.Window):
    def __init__(self,y_pos,x_pos):
        #super().__init__(800,600,"pyglet Physics engine",vsync=True,)
        #self.win = pyglet.window.Window(width=800, height=600)
        super().__init__()
        self.player1_Y_pos = y_pos
        self.player2_X_pos = x_pos
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        self.player1 = Player(velocity(10, self.player1_Y_pos), "RIGHT", (255,0,0))
        self.player2 = Player(velocity(self.player2_X_pos, 10), "UP", (0, 0, 255))

    #@self.win.event    
    def on_draw(self):
        self.clear()
        pyglet.gl.glClearColor(1, 1, 1, 1)
        square(velocity(600,0),(10,800),(0,200,0)).draw()
        self.player1.run()
        self.player2.run()
        #pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

    def update(self, dt):
        pass

#class Main_Window():
class Main_Window_1(pyglet.window.Window):
    def __init__(self):
        super().__init__(800,600,"pyglet Physics engin")
        #super().__init__()
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        Main_Window.player1 = Player(velocity(10, Physics_RLEnv.player1_Y_pos), "RIGHT", (255,0,0))
        Main_Window.player2 = Player(velocity(Physics_RLEnv.player2_X_pos, 10), "UP", (0, 0, 255))
        
    def on_draw(self):
        self.clear()
        pyglet.gl.glClearColor(1, 1, 1, 1)
        square(velocity(600,0),(10,800),(0,200,0)).draw()
        Main_Window.player1.run()
        Main_Window.player2.run()
        rawimage=pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
        format = 'RGB'
        pitch = rawimage.width * len(format)
        pixels = rawimage.get_data(format, pitch)
        #print(pixels)

    def update(self, dt):
        pass


class Physics_RLEnv(gym.Env,Main_Window):
  metadata = {'render.modes': ['human']}
  def __init__(self):
      #global velocity_x,velocity_y
      self.player_val=randint(1,10)
      self.player1_Y_pos=randint(120,580)
      self.player2_X_pos=randint(120,580)
      #self.player1 = Player(velocity(10, self.player1_Y_pos), "RIGHT", (255,0,0))
      #self.player2 = Player(velocity(self.player2_X_pos, 10), "UP", (0, 0, 255))
      self.action_space = spaces.Discrete(100)
      high =np.array(((800,600),(800,600)),dtype=np.int32)
      low = np.array(((0,0),(0,0)),dtype=np.int32)
      self.observation_space = spaces.Box(low=low, high=high,dtype=np.int32)
      self.window=Main_Window(self.player1_Y_pos,self.player2_X_pos)
      self.window.player1.velocity_x=0
      self.window.player2.velocity_y=self.player_val
      self.action_list=[]
      #pyglet.app.run()

  def step(self, action):
      #global velocity_x,velocity_y
      self.window.player1.velocity_x = action
      self.window.player2.velocity_y=self.player_val
      self.window.player1.run()
      self.window.player2.run()
      a=self.window.player1.get_cordinates()
      b=self.window.player2.get_cordinates()
      observation= self.get_state()
      reward=self.get_reward(a,b)
      done= self.episode_over(a,b)
      #self.action_list.append(self.window.player1.velocity_x) ###'actions':self.action_list,
      info = {'actions':len(self.action_list),'Y_Pos_1':self.window.player1_Y_pos,'Velocity_y':self.window.player2.velocity_y,'X_pos_2':self.player2_X_pos}
      #self.info.append([,])
      #pyglet.app.run()
      return observation, reward, done, info

  def get_reward(self,a,b):
        if(abs(a[0]-b[0])<15 and abs(a[1]-b[1])<15):
            return 10
        elif (a[0] >= 585 or b[1] >= 600):
            return -10
        else:
            return 1
        
  def episode_over(self,a,b):
        if a[0] >= 585 or (abs(a[0]-b[0])<15 and abs(a[1]-b[1])<15) or b[1] >= 600 :
            return True
        else:
            return False

  def get_state(self,):
      a,b=self.window.player1.get_cordinates()
      c,d=self.window.player2.get_cordinates()
      return (a,b,c,d)

  def reset(self):
      self.player_val=randint(1,10)
      self.player1_Y_pos=randint(120,580)
      self.player2_X_pos=randint(120,580)
      self.window.player1 = Player(velocity(10, self.player1_Y_pos), "RIGHT", (255,0,0))
      self.window.player2 = Player(velocity(self.player2_X_pos, 10), "UP", (0, 0, 255))
      self.window.player1.velocity_x=0
      self.window.player2.velocity_y=self.player_val
      self.action_list=[]
      return self.get_state()
      #self.window=Main_Window()
    
  def render(self, mode='human'):
      window=Main_Window_1()
      pyglet.app.run()

  def close(self):
    pass
