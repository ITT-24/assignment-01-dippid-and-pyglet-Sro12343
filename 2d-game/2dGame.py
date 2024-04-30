from DIPPID import SensorUDP
import os
import pyglet
from pyglet import shapes
import numpy as np
import random



# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

windowSizeX = 704
windowSizeY = 704
config = pyglet.gl.Config(double_buffer=True, depth_size=24)
window = pyglet.window.Window(windowSizeX, windowSizeY)
current_dir = os.path.dirname(__file__)
batch = pyglet.graphics.Batch()
LevelSpeed = 10
countDown = 40
spawnEnemie = False
inputX = 0
inputY = 0
moveX = 0
moveY = 0
bullets = []
enemies = []
backgrounds=[]
doShoot = False

levelCountdown = 300


shootButtonPressed = False
canShoot = True

class GameObject():
    x = 0
    y = 0
    offsetX = 0
    offsetY = 0
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x
        self.y
    #Has a sprite
    #Has a Update function
    def update(self):
        self.sprite.x = self.x - self.offsetX
        self.sprite.y = self.y - self.offsetY

    #Update first aplies condition updates and then moves
    print("not implemented")

class Player(GameObject): 
    def __init__(self):
        image_path = os.path.join(current_dir, 'images','redSquare.png')
        #image = pyglet.image.load(image_path)
        frames = []
        for i in range(1,15):
            imageName = "f"+str(i)+".png"            
            image_p = os.path.join(current_dir,'images',imageName)
            print(image_p)
            frame = pyglet.image.load(image_p)
            frames.append(frame)
        animation = pyglet.image.Animation.from_image_sequence(frames, 1/15)
        self.sprite = pyglet.sprite.Sprite(animation)
        #self.sprite = pyglet.sprite.Sprite(img=image)
        #self.sprite = pyglet.shapes.Box(300,300,64,64,color=(255,0,0),batch=batch)
        self.x = 300
        self.y = 300
        self.offsetX = self.sprite.width/2
        self.offsetY = self.sprite.height/2
         
    def update(self):
        super().update()
        
        
    #Set Sprite/Animation Sprites
    #update function moves and draws    
    print("not implemented")
    
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

        if self.y>windowSizeY:
            self.deleteSelf()
        pass
    def __del__(self):
        if self in self.array:
            self.sprite.delete()
            self.array.remove(self)
        
    #Movement is simple directional shift
    #if position gets to small/large in x/y direction bullet deletes itself.

class Enemy(GameObject):
    def __init__(self,x,y,array):  
        self.x = x
        self.y = y          
        self.sprite = shapes.Circle(self.x,self.y,20,color=(255,100,100), batch=batch)
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
        if self in self.array:
                self.array.remove(self)
                self.sprite.delete()
                
                
class ShootEnemy(Enemy):
    def __init__(self,x,y,array,speed, playerX, playerY):         
        super().__init__(x,y,array)
        self.speed = speed
        self.targetX = playerX
        self.targetY = playerY
        
        self.dx = 0
        self.dy = 0
        self.calculateDirection()
        
        
        #calculate direction between two points
    def calculateDirection(self):
        self.dx = self.targetX - self.x
        self.dy = self.targetY - self.y
        
        dxy = np.sqrt(self.dx**2 + self.dy**2)
        
        if dxy != 0:
            self.dx /=dxy
            self.dy /=dxy
    def move(self):
        if self.sprite is not None and self.sprite._vertex_list is not None:

            self.x += self.dx*self.speed    
            self.y += self.dy*self.speed
            #if self.x<0-self.despawnSizePadding or self.x>windowSizeX+self.despawnSizePadding or self.y<0-self.despawnSizePadding or self.y>windowSizeY+self.despawnSizePadding:
            self.sprite.x = self.x
            self.sprite.y = self.y
            if self.y < -10:
                self.__del__()
            
        
            
    #initialize with sprite
    #update calles movement logic to determin movement direction
    #then moves
    #then draws
    #this means different enemies only have to have different movement logic and sprites
    

class backgroundImage():
    def __init__(self,imageName,speed,y): 
        image_path = os.path.join(current_dir, 'images',imageName)
        image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(img=image)
        self.speed = speed
        self.y = y
    def update(self):
        self.y -= self.speed
        if(self.y < (-windowSizeY)):
            self.y = windowSizeY
        self.sprite.y = self.y
        
player = Player()
backgrounds.append(backgroundImage("Background.png",LevelSpeed,704))
backgrounds.append(backgroundImage("Background.png",LevelSpeed,0))
 
ticker = 0;
    
def update(dt):
    global player
    global doShoot
    global spawnEnemie
    global levelCountdown
    global LevelSpeed 
#     ticker += 10
    if doShoot == True:
        bullets.append(Bullet(ticker,200,0,10,bullets))
        doShoot = False
    
    if spawnEnemie == True:
        enemies.append(ShootEnemy(random.randint(52, 652),800,enemies,LevelSpeed,player.x,player.y))
        spawnEnemie = False
    
    handleInput()
    handleMovement()
    
    player.update()

    for b in bullets:
        b.update()
    
    for e in enemies:
        e.update()
    for ba in backgrounds:
        ba.update()        

    enemieSpawner()
    enemieBulletCollision()
    playerEnemyCollision()
    
    if levelCountdown <=0:
        #LevelSpeed += 1
        levelCountdown = 300
        #for ba in backgrounds:
        #    ba.speed = LevelSpeed
    else:
        levelCountdown -= 1
    
    #for the list of game objects execute update.
    #print("not implemented")
    
def enemieSpawner():
    #check if enemies should be spawned. can have multiple cooldowns at once.
    #Spawn enemies
    global countDown
    global spawnEnemie
    if(countDown <= 0):
        spawnEnemie = True
        countDown = 30+ random.randint(0, 30)
    else:
        countDown -= 1
        
        
@window.event
def on_draw():
    window.clear()
    drawBackground()

    #batch.draw()
    drawProjectiles()
    drawPlayer()
    drawEnemies()
    
    

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




inputX = 0

def handleInput():
    global inputX
    global inputY

    
    # check if the sensor has the 'accelerometer' capability
    if(sensor.has_capability('gyroscope')):   
        #print('gyroscope X: ', sensor.get_value('gyroscope')['x']) 
        if(inputX + sensor.get_value('gyroscope')['x']<= 10):
            inputX += sensor.get_value('gyroscope')['x']
#        if(np.abs(sensor.get_value('gyroscope')['x'])>=0.001):
 #           inputX += sensor.get_value('gyroscope')['x']
        #    print('gyroscope X: ', sensor.get_value('gyroscope')['x'])    
        if(inputY + sensor.get_value('gyroscope')['y']<= 10):
            inputY += sensor.get_value('gyroscope')['y']
        #check if x is over certain threshold and set xInput
        #check if y is over certain threshold and set yInput
        
        
        
    #print(str(inputX) +" "+ str(inputY))
        
    #check if fire button is pressed and can fire 
    
    
def handleMovement():
    global inputX
    global inputY
    global moveX
    global moveY
    global player
    
    inputThreshold = 4
    speed = 10
    
    
    if inputX > inputThreshold:
        moveX = 1
    elif inputX < -inputThreshold:
        moveX = -1
    else:
        moveX = 0    
        
    #if inputY > inputThreshold:
    #    moveY = 1
    #elif inputY < -inputThreshold:
    #    moveY = -1
    #else:
    #    moveY = 0
    
    if player.x + player.offsetX + moveX *speed < windowSizeX and  player.x - player.offsetX + moveX *speed >0:       
        player.x += moveX *speed
    else: player.x -= moveX
        
    #if player.y + player.offsetY + moveY *speed < windowSizeY and  player.y - player.offsetY + moveY *speed >0:       
    #    player.y += moveY *speed
 
        
        
        
        
        
        
    #check x direction if position + sprite space is free
    
        #If so then move in x direction else get differance and move that much
    #check y direction if position + sprite space is free
        #If so then move in y direction else get differance and move that much     
    
    #print("not implemented")   


def shootInput(data):
    global canShoot
    print(data)
    if int(data) == 1:
        #wants to shoot
        if canShoot == True:
            #shoot
            shoot()
    else:
        if canShoot == False:
            canShoot = True    
        
    
def shoot():
    #calculate shot direction.
    global moveX
    global moveY
   # global bullets
    global canShoot
    global ticker
    global doShoot
    
    print(canShoot)
    xdir= 0
    ydir= 0
    speed = 10
    
    
        
    #print("test->")     
    #print(xdir)     
    #print(ydir)
    #print("<-test")
    #xSpeed = xdir*speed
    #ySpeed = ydir*speed
    #bullets.append(Bullet(player.x,player.y,xSpeed,ySpeed,bullets))
    
    doShoot = True
    #bullets.append(Bullet(len(bullets)*30,10,0,10,bullets))             
    canShoot = False
    


    #spawn bullet
    #apply offset according to which direction player faces. But there Where the lines of fire directions intersect should be where Enemies target, to make Shooting easier
    #set can shoot to false
    
    print("not implemented")


#for i in range(300):
#        bullets.append(Bullet(player.x,player.y,0,10,bullets))        
    
#bullets.append(Bullet(10,player.y,0,10,bullets))

#bullets.append(Bullet(20,player.y,0,10,bullets))

#bullets.append(Bullet(30,player.y,0,10,bullets))

#bullets.append(Bullet(40,player.y,0,10,bullets))

#bullets.append(Bullet(50,player.y,0,10,bullets))

#bullets.append(Bullet(60,player.y,0,10,bullets))
     
#enemies.append(ShootEnemy(100,500,enemies,10,player.x,player.y))

def checkCollision():
    #gets two lists of objects
    #checks for all variations if they collide. 
    # Returns a list of all colliding objects
    print("not implemented")

def enemieBulletCollision():
    #Transmits list of Bullets and enemies
    #For the list of collisions it sorts it to have for each bullet the minimal distance to an enemy.
    #Delets the Colliding Bullets and enemies from their lists
    #Make the hit threthshold large enough so it is easyer.
    #checkCollision()
    #print("not implemented")
    minimumDistance = 10
    
    for b in bullets:
        matchedEnemy = None
        matchD = minimumDistance
        for e in enemies:
            #check distance     
            dx = b.x -e.x
            dy = b.y -e.y
            distance = np.sqrt(dx**2 + dy**2)
            if distance < minimumDistance and distance < matchD:
                matchedEnemy = e
        if matchedEnemy != None:
            e.__del__()
            b.__del__()
            
def playerEnemyCollision():
    minimumDistance = 32
    for e in enemies:
        dx = player.x - e.x
        dy = player.y - e.y
        distance = np.sqrt(dx**2 + dy**2)
        if distance < minimumDistance:
            pass
#            window.close() 
    #Transmits list of player and Enemies
    #checkCollision()
    #print("not implemented")
    
    
    

    
sensor.register_callback('button_1', shootInput)    
pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.app.run()



#TODO

        




#fix stuck
#Can only move side to side and shoot up. Maybe bullet hell but running TEST
#Add Shadow for player
#fix overlap issiue


#add enemy following player
#add enemy zig zag

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