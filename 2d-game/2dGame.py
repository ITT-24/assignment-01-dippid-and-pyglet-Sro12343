from DIPPID import SensorUDP
import os
import pyglet




# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

windowSizeX = 704
windowSizeY = 704
config = pyglet.gl.Config(double_buffer=True, depth_size=24)
window = pyglet.window.Window(windowSizeX, windowSizeY)
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, 'images','redSquare.png')
redSquare = pyglet.image.load(image_path)
sprite = pyglet.sprite.Sprite(img=redSquare, x=100,y=100)




class gameObject():
    #Has a sprite
    #Has a Update function
    #Update first aplies condition updates and 
    print("not implemented")

class player(gameObject): 
    #Set Sprite/Animation Sprites
    #update function moves and draws    
    print("not implemented")
    
class enemy(gameObject):
    #initialize with sprite
    #update calles movement logic to determin movement direction
    #then moves
    #then draws
    #this means different enemies only have to have different movement logic and sprites
    print("not implemented")
    
def update(dt):
    #for the list of game objects execute update.
    enemieSpawner()
    print("not implemented")
    
def enemieSpawner():
    #check if enemies should be spawned. can have multiple cooldowns at once.
    #Spawn enemies
        
@window.event
def on_draw():
    window.clear()
    #draw background
    #draw Projectiles
    #draw Player
    #draw Enemies
    
    sprite.draw()

def drawBackground():
    print("not implemented")

def drawProjectiles():
    print("not implemented")
    
def drawPlayer():
    print("not implemented")
def drawEnemies():
    print("not implemented")    

def handleInput():
    #check if x is over certain threshold and set xInput
    #check if y is over certain threshold and set yInput
    #check if fire button is pressed and can fire 
    print("not implemented")
    
def handleMovement(xInput,yInput):
    #check x direction if position + sprite space is free
        #If so then move in x direction else get differance and move that much
    #check y direction if position + sprite space is free
        #If so then move in y direction else get differance and move that much     
    
    print("not implemented")   


def shooting():
    #spawn bullet
    #apply offset according to which direction player faces. But there Where the lines of fire directions intersect should be where Enemies target, to make Shooting easier
    #set can shoot to false
    
    print("not implemented")


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
    checkCollision()
    print("not implemented")
    
def playerEnemyCollision():
    #Transmits list of player and Enemies
    checkCollision()
    print("not implemented")
    
pyglet.app.run()

pyglet.clock.schedule_interval(update, 1/30.0)

#TODO
#https://pyglet.readthedocs.io/en/latest/programming_guide/examplegame.html#basic-graphics
#Correct inport of Resources
#Handle input
#Create Movement
#collision with wall
#Shooting
#Create Enemies
#Collision enemie player
#Collision shots enemies
#Add Animation
#Draw Level
#Cleanup code
#Add comments
#PEP8 complient
#LowerSleepTime -> les debugable but more realistic
#virtual environment and a requirements.txt







#Ein shooter?
    #Tilt to move.
    #Avoid enemies
    #Shoot enemies
    #Mit lauf animation
    

#Welche spiele würden sich gut eignen?
#Space invaders?
#Tetris
#Snake?