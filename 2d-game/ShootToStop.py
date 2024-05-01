#Code is strongly influenced by the documentation of pyglet and their concrete game example: https://pyglet.readthedocs.io/en/latest/programming_guide/examplegame.html#checking-for-collisions
#The formular how to get a normed vector between two points came from ChatGPT. This was used to set the movement direction of the ShootEnemy towards the player: Thoug adapted to different uses, the Prompt was: I want to be able to move in 8 directions. I have an xspeed nad a yspeed. how can i calculate the xspeed and yspeed so that the total speed is always the same speed?
    #Part of that equasion was used to check distance/collision between player and enemies, as well as Bullets and enemies.
#ChatGPT was used for Debuging 
#The content of the __del__(self): functions was based on the ChatGPT prompt: i have an object in a python array. The object has a function that should remove it from the array it is in


import os
import sys
import random

import pyglet
from pyglet import shapes
import numpy as np

from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

#setup pyglet
window_size_x = 704
window_size_y = 704
config = pyglet.gl.Config(double_buffer=True, depth_size=24)
window = pyglet.window.Window(window_size_x, window_size_y)
current_dir = os.path.dirname(__file__)
batch = pyglet.graphics.Batch()
event_loop = pyglet.app.EventLoop()


#seting up global variables
level_speed = 10
point_counter = 0
life_counter = 3
count_down = 40
input_x = 0
move_x = 0
input_threshold = 4
player_speed = 10  
minimum_distance_bullet_hit = 30
minimum_distance_player_hit = 32  
side_space = 120
bullets = []
enemies = []
backgrounds=[]
gameOver = False
spawnEnemie = False
doShoot = False

#Score Label
score_label = pyglet.text.Label(text="Score:", x=100, y=50,color=(0,0,0,255),rotation=-90)
score_number = pyglet.text.Label(text="0", x=100, y=100,color=(0,0,0,255),rotation=-90)
life_label = pyglet.text.Label(text="Lifes:", x=600, y=120,color=(0,0,0,255),rotation=90)
life_number = pyglet.text.Label(text=str(life_counter), x=600, y=70,color=(0,0,0,255),rotation=90)


#Other game Objects, like the player and the enemies are based on this class 
class GameObject():
    x = 0
    y = 0
    offsetX = 0
    offsetY = 0
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        
    def update(self):
        #ensure that the sprite is located where the game object is.
        self.sprite.x = self.x - self.offsetX
        self.sprite.y = self.y - self.offsetY



class Player(GameObject): 
    def __init__(self):
        #seting up the run animation for the player
        frames = []
        for i in range(1,15):
            imageName = "f"+str(i)+".png"            
            image_p = os.path.join(current_dir,'images',imageName)
            frame = pyglet.image.load(image_p)
            frames.append(frame)
        animation = pyglet.image.Animation.from_image_sequence(frames, 1/15)
        self.sprite = pyglet.sprite.Sprite(animation)

        #setting other variables
        self.x = 350
        self.y = 200
        self.offsetX = self.sprite.width/2
        self.offsetY = self.sprite.height/2
         
    def update(self):
        super().update()
        
          
    
class Bullet():
    def __init__(self,x,y,xSpeed,ySpeed,array):
        self.array = array        
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.sprite = shapes.Circle(self.x,self.y,10,color=(100,100,100), batch=batch) 
        
               
    def update(self):
        
        self.x = self.x + self.xSpeed
        self.y = self.y + self.ySpeed
        self.sprite.y = self.y

        #check if the enemy should despawn
        if self.y>window_size_y:
            self.__del__()
        
    def __del__(self):
        #deletes itself from the array of bullets
        if self in self.array:
            self.sprite.delete()
            self.array.remove(self)
        

#Shoot enemy is based on this. 
class Enemy(GameObject):
    def __init__(self,x,y,array):  
        self.x = x
        self.y = y          
        self.sprite = shapes.Circle(self.x,self.y,20,color=(80,80,100), batch=batch)
        self.targetX = 0    
        self.targetY = 0
        self.despawnSizePadding = 300
        self.array = array
    def moveLogic(self):
        pass
    def move(self):
        pass

    def update(self):
        self.moveLogic()
        self.move()
        
    def __del__(self):
        #deletes itself from the array of enemies
        if self in self.array:
                self.array.remove(self)
                self.sprite.delete()
                
                
#An Enemy Type that targets the PLayers location at spawn.
class ShootEnemy(Enemy):
    def __init__(self,x,y,array,speed):         
        super().__init__(x,y,array)
        self.speed = speed
        self.targetX = random.randint(side_space+10, window_size_x-side_space-10)
        self.targetY = 0
        
        self.dx = 0
        self.dy = 0
        self.calculateDirection()
        
        
    #calculate and starting direction towards the player
    def calculateDirection(self):
        self.dx = self.targetX - self.x
        self.dy = self.targetY - self.y
        dxy = np.sqrt(self.dx**2 + self.dy**2)      
        if dxy != 0:
            self.dx /=dxy
            self.dy /=dxy
            
    def move(self):
        global life_counter
        if self.sprite is not None and self.sprite._vertex_list is not None:
            self.x += self.dx*self.speed    
            self.y += self.dy*self.speed
            self.sprite.x = self.x
            self.sprite.y = self.y
            #despawn if outside of bottom screen 
            if self.y < -10:
                life_counter -=1
                self.__del__()
            
    
    
#The looping background image.
class BackgroundImage():
    def __init__(self,imageName,speed,y): 
        image_path = os.path.join(current_dir, 'images',imageName)
        image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(img=image)
        self.speed = speed
        self.y = y
    def update(self):
        self.y -= self.speed
        if(self.y < (-window_size_y)):
            self.y = window_size_y
        self.sprite.y = self.y



#Trying to filter input to improve controls.
#This code is from ChatGPT: The Prompt was: I use the input from my smartphone gyroscop to control my game. The input is rather jittery. SHould i filter it and if yes, what is a simple method to do so in python?
class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.filtered_value = None

    def update(self, new_value):
        if self.filtered_value is None:
            self.filtered_value = new_value
        else:
            self.filtered_value = self.alpha * new_value + (1 - self.alpha) * self.filtered_value
        return self.filtered_value

#initiate the lowpassfilter
alpha = 0.2 
low_pass_filter = LowPassFilter(alpha)

#initiate the player and background        
player = Player()
backgrounds.append(BackgroundImage("Background.png",level_speed,704))
backgrounds.append(BackgroundImage("Background.png",level_speed,0))
 




#main logic update loop
def update(dt):
    global player
    global doShoot
    global spawnEnemie
    global level_speed 
    global point_counter
    global gameOver
    
    point_counter += 1
    score_number.text = str(point_counter)
    life_number.text = str(life_counter)
    #update player    
    handleInput()
    handleMovement()   
    player.update()

    #update bullets, enemies and backgrounds
    for b in bullets:
        b.update()    
    for e in enemies:
        e.update()
    for ba in backgrounds:
        ba.update()        
    
    enemieSpawner()
    

    
    #Check for collisions
    enemyBulletCollision()
    playerEnemyCollision()
    
    #Spawn bullet
    if doShoot == True:
        bullets.append(Bullet(player.x,player.y,0,10,bullets))
        point_counter -= 10
        doShoot = False
        
    #Spawn Enemie
    if spawnEnemie == True:
        enemies.append(ShootEnemy(random.randint(side_space, window_size_x-side_space),750,enemies,level_speed))
        spawnEnemie = False
    
    checkIfEndGame()
    
def enemieSpawner():
    global count_down
    global spawnEnemie
    #check if enemies should be spawned. can have multiple cooldowns at once.
    if(count_down <= 0):
        spawnEnemie = True
        count_down = 30+ random.randint(0, 30)
    else:
        count_down -= 1
        


def handleInput():
    global input_x
    global low_pass_filter
    # check if the sensor has the 'accelerometer' capability
    if(sensor.has_capability('gyroscope')):   
        #check if x is over certain threshold and set xInput
        
        input_x += low_pass_filter.update(sensor.get_value('gyroscope')['x'])
        
        #if(input_x + sensor.get_value('gyroscope')['x']<= 10):
        #    input_x += sensor.get_value('gyroscope')['x']
        
    
def handleMovement():
    global input_x
    global move_x
    global player
    
    global input_threshold
    global player_speed 
    global side_space
    
    if input_x > input_threshold:
        move_x = 1
    elif input_x < -input_threshold:
        move_x = -1
    else:
        move_x = 0    
       
    
    if player.x + player.offsetX + move_x *player_speed < window_size_x-side_space and  player.x - player.offsetX + move_x *player_speed >side_space:       
        player.x += move_x *player_speed
    else: player.x -= move_x

#React to the Button Press and decide if to shoot
def shootInput(data):
    global doShoot
    if int(data) == 1:
        doShoot = True   
        


def enemyBulletCollision():

    global point_counter
    global minimum_distance_bullet_hit
    
    for b in bullets:
        matchedEnemy = None
        matchD = minimum_distance_bullet_hit
        for e in enemies:
           
            distance = (b.x-e.x)**2 + (b.y-e.y)**2
            
            if distance <= minimum_distance_bullet_hit**2:
                e.__del__()
                b.__del__()
                break
            
def playerEnemyCollision():
    global point_counter
    global minimum_distance_player_hit
    global life_counter
    for e in enemies:
        distance = (player.x-e.x)**2 + (player.y-e.y)**2
        if distance < minimum_distance_player_hit**2:
            #player was hit and game is lost. Print Points and close game
            e.__del__()
            life_counter-= 1

        
def checkIfEndGame():
    global life_counter
    if(life_counter<=0):
        try:
            print("Points: " + str(point_counter))      
            window.close()
            event_loop.exit()  
            pyglet.app.exit()
            os._exit(0)
            
        except Exception as e:
            print(e)
            pass
    
    
    
        
        

#When the window gets closed. Print Points into Terminal. and close the aplication.        
@window.event  
def on_close():
    print("Points: " + str(point_counter))
    pyglet.app.exit()
    window.close()
    os._exit(0)
        
        
#Draw the game elements.       
@window.event
def on_draw():
    global score_label
    global score_number
    window.clear()
    drawBackground()
    drawProjectiles()
    drawPlayer()
    drawEnemies()
    score_label.draw()
    score_number.draw()
    life_label.draw()
    life_number.draw()

def drawBackground():
    for ba in backgrounds:
        ba.sprite.draw()   

def drawProjectiles():
    for b in bullets:
        b.sprite.draw()
    
def drawPlayer():
    player.sprite.draw()
        
def drawEnemies():
    for e in enemies:
        if e.sprite != None:
            e.sprite.draw()


#register button1 event handler
sensor.register_callback('button_1', shootInput)    

#Setup main logic update loop
pyglet.clock.schedule_interval(update, 1/30.0)

#Start Game    
pyglet.app.run()







#TODO

        




#fix stuck
#Can only move side to side and shoot up. Maybe bullet hell but running TEST
#Add Shadow for player
#fix overlap issiue DONE
#Straight down enemie


#Cleanup code
#Add comments
#PEP8 complient
#LowerSleepTime -> les debugable but more realistic
#virtual environment and a requirements.txt


#DONE
#Add Animation DONE
#Draw Level DONE
#background can loop and if one background is out of framenext one jumps up DONE
#Make Bullet speed calculation better DONE
#https://pyglet.readthedocs.io/en/latest/programming_guide/examplegame.html#basic-graphics
#Correct inport of Resources DONE
#Handle input DONE
#Create Movement DONE
#collision with wall DONE
#Shooting DONE
    #Bullet sprite DONE
    #Bullet Movement DONE
    #Bullet Distruction DONE
    #Bullet list DONE
    #Update Bullet list DONE
#Collision enemie player DONE
#Collision shots enemies DONE

#Create Enemies DONE
    #Test enemy 1 DONE
    #enemy list DONE


#Ein shooter?
    #Tilt to move.
    #Avoid enemies
    #Shoot enemies
    #Mit lauf animation
    

#Welche spiele würden sich gut eignen?
#Space invaders?
#Tetris
#Snake?