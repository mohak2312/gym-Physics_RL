import gym
from random import randint
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
        
    def draw(self):
        square(self.pos,(15,15),self.color).draw()
        
    def update(self):
        square(self.pos,(15,15),self.color).draw()
        
        
    def move(self):
        global velocity_x,velocity_y
        
        if self.dir == "UP":
            self.pos.y+=velocity_y
        
        if self.dir == "RIGHT":
            self.pos.x +=  velocity_x
    
    def get_cordinates(self):
        m=velocity(self.pos.x,self.pos.y)
        return m.cordinates()
        
        
    def run(self):
        self.draw()
        self.move()
        self.update()
    

class Main_Window():
#class Main_Window(pyglet.window.Window):
    
    def __init__(self):
        
        #super().__init__(800,600,"pyglet Physics engin")
        super().__init__()
        pyglet.clock.schedule_interval(self.update, 1 / 60)

        
        Main_Window.player1 = Player(velocity(10, Physics_RLEnv.player1_Y_pos), "RIGHT", (255,0,0))
        Main_Window.player2 = Player(velocity(Physics_RLEnv.player2_X_pos, 10), "UP", (0, 0, 255))
        
    def on_draw(self):
    
        self.clear()
        pyglet.gl.glClearColor(1, 1, 1, 1)
        square(velocity(600,0),(10,800),(0,200,0)).draw()
        Main_Window.player1.run()
        Main_Window.player2.run()
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
      global velocity_x,velocity_y
      velocity_x=0
      self.player_val=randint(1,10)
      velocity_y=self.player_val
      Physics_RLEnv.player1_Y_pos=randint(120,580)
      Physics_RLEnv.player2_X_pos=randint(120,580)
      self.window=Main_Window()
      self.info=[]
      #pyglet.app.run()

 
  def step(self, action):
      global velocity_x,velocity_y
      velocity_x = action
      velocity_y=self.player_val
      Main_Window.player1.run()
      Main_Window.player2.run()
      a=Main_Window.player1.get_cordinates()
      b=Main_Window.player2.get_cordinates()
      observation= self.get_state(a,b)
      reward=self.get_reward(a,b)
      done= self.episode_over(a,b)
      self.info.append([velocity_x,Physics_RLEnv.player1_Y_pos,velocity_y,Physics_RLEnv.player2_X_pos])
      #pyglet.app.run()
      
      return observation, reward, done, self.info
       
    
  
  def get_reward(self,a,b):
        if(abs(a[0]-b[0])<15 and abs(a[1]-b[1])<15):
            return 1
        elif (a[0] >= 585 or b[1] >= 600):
            return -1
        else:
            return 0
        
  def episode_over(self,a,b):
        if a[0] >= 585 or (abs(a[0]-b[0])<15 and abs(a[1]-b[1])<15) or b[1] >= 600 :
            return True
        else:
            return False

  def get_state(self,a,b):
      return (a,b)
      

  def reset(self):
      global velocity_x,velocity_y
      velocity_x=0
      velocity_y=0
      self.info=[]
      #self.window=Main_Window()
    
  def render(self, mode='human'):
      
      window=Main_Window_1()
      
      pyglet.app.run()

  def close(self):
    pass
