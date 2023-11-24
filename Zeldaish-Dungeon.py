from cmu_graphics import *
import math
import random
<<<<<<< HEAD

"""
This is the main projectile that the user uses, used when 'f' is pressed
user can shoot a fireball every 0.5 seconds
=======


"""
This is the main projectile that the user uses, used when 'f' is pressed
>>>>>>> New-Features
"""
class Fireball:
    def __init__(self, cx, cy, cdx, cdy):
        self.speed = 5
        self.radius = 5
        self.cdx , self.cdy = self.getDirection(cdx, cdy) 
        self.cdx = self.cdx * self.speed
        self.cdy = self.cdy * self.speed
        self.cx = cx + self.cdx
        self.cy = cy + self.cdy
        self.width = self.radius
        self.height = self.radius
    
    def drawFireball(self):
        drawCircle(self.cx, self.cy, self.radius, fill = "red")

    def changeFireballPos(self):
        self.cx += self.cdx
        self.cy += self.cdy
    
    def getDirection(self, cdx, cdy):
        if cdx > 0 and cdy > 0:
            return 1, 1
        elif cdx > 0 and cdy == 0:
            return 1, 0
        elif cdx > 0 and cdy < 0:
            return 1, -1
        elif cdx == 0 and cdy > 0:
            return 0, 1
        elif cdx == 0 and cdy < 0:
            return 0, -1
        elif cdx < 0 and cdy > 0:
            return -1, 1
        elif cdx < 0 and cdy == 0:
            return -1, 0
        else:
            return -1, -1
<<<<<<< HEAD

"""
This is the main character class, user moves with 'wasd'
=======


"""
This is the main character class
>>>>>>> New-Features
"""
class Character:
    def __init__(self):
        self.health = 5
        self.speed = 3
        self.height = 20
        self.width = 20
        self.cx = 100
        self.cy = 100
        self.cdx = 0
        self.cdy = 0
        self.charMoving = False
        self.hitCurr = False
        self.fireballs = []

    def drawCharacter(self):
        drawRect(self.cx, self.cy, self.width, self.height, fill = "blue", align = "center")

    def changePosition(self):
        self.cx += self.cdx
        self.cy += self.cdy

    def createFireball(self):
        if len(self.fireballs) < 3 and self.ifBothZero() == False:
            newFireball = Fireball(self.cx, self.cy, self.cdx, self.cdy)
            self.fireballs.append(newFireball)

    def ifBothZero(self):
        if self.cdx == 0 and self.cdy == 0:
            return True
        return False
    
<<<<<<< HEAD
"""
This is a melee type of enemy that removes one health from the user every second in range
"""   
=======
>>>>>>> New-Features
class EnemyDog:
    def __init__(self, cx, cy):
        self.health = 2
        self.cx = cx
        self.cy = cy
        self.cdx = 0
        self.cdy = 0
        self.height = 20
        self.width = 20
        self.speed = 5
    
    def drawEnemy(self):
        drawRect(self.cx, self.cy, self.width, self.height, fill = "green", align = "center")

    def changePosition(self, user):
        if user.health > 0:
            totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
            if totalDistance > (self.width):
                self.speed = 1
            else:
                self.speed = 0
            self.cdx = ((user.cx - self.cx) / totalDistance) * self.speed
            self.cdy = ((user.cy - self.cy) / totalDistance) * self.speed
            self.cx += self.cdx
            self.cy += self.cdy
        else:
            self.cdx = 0
            self.cdy = 0
    
    def melee(self, user):
        totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
        if totalDistance < self.width:
            user.health -= 1
            user.hitCurr = True

<<<<<<< HEAD
=======

>>>>>>> New-Features
"""
onAppStart basically sets all of the elementary values for the game.
"""
def onAppStart(app):
    app.stepsPerSecond = 30
    app.boardLeft = 25
    app.boardTop = 50
    app.boardWidth = 450
    app.boardHeight = 400
    app.borderWidth = 5
    app.direction = None
    app.globalCounter = 0
    app.fireCounter = 30
    app.user = Character()
    app.timerCounter = 0
    app.fireballShot = False
    app.enemies = []
    app.gameOver = False
    app.gameOverCounter = 0
    spawnEnemies(app)

"""
<<<<<<< HEAD
Spawns dog enemies and makes sure they dont spawn on top of eachother, also spawns random amount
from 2-5
"""
def spawnEnemies(app):
    numEnemies = random.randint(2,5)
    for i in range(numEnemies):
        enemyWidth = 20
        enemyHeight = 20
        leftMostSpawn = app.boardLeft + (app.borderWidth//2 + 1) + enemyWidth
        rightMostSpawn = app.boardLeft + app.boardWidth - (app.borderWidth//2 + 1) - enemyWidth
        upMostSpawn = app.boardTop + (app.borderWidth//2 + 1) + enemyHeight 
        lowMostSpawn = app.boardTop + app.boardHeight - (app.borderWidth//2 + 1) - enemyHeight
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = (currEnemy.width**2 + currEnemy.height**2) ** 0.5
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        newEnemy = EnemyDog(cx, cy)
        app.enemies.append(newEnemy)

"""
=======
>>>>>>> New-Features
This keeps track of all timed events and movement of main character, npcs, and 
projectiles
"""
def onStep(app):
    if app.user.health <= 0:
        app.gameOver = True

    if app.gameOver and app.gameOverCounter < 100:
        app.gameOverCounter += 1

    app.timerCounter += 1

    if app.timerCounter % 15 == 0:
        app.fireballShot = False

    if app.timerCounter % 30 == 0:
        app.user.hitCurr = False

    if isLegal(app, app.user)and app.user.health > 0:
        app.user.changePosition()
    
    for enemy in app.enemies:
        if isLegal(app, enemy):
            enemy.changePosition(app.user)
            if app.user.hitCurr == False:
                enemy.melee(app.user)

    for fireball in app.user.fireballs:
        if isLegal(app, fireball):
            fireball.changeFireballPos()  
        else:
            app.user.fireballs.remove(fireball) 

"""
<<<<<<< HEAD
This checks if a movement for an npc or the user is legal, can also apply to the moves of each
=======
This checks if a move for an npc or the user is legal, can also apply to moves
>>>>>>> New-Features
"""
def isLegal(app, character):
    if character.cx + character.cdx + character.width//2 + app.borderWidth/2 > app.boardWidth + app.boardLeft:
        return False
    if character.cy + character.cdy + character.height//2 + app.borderWidth/2 > app.boardHeight + app.boardTop:
        return False
    if character.cx - character.width//2  + character.cdx - app.borderWidth/2 < app.boardLeft:
        return False
    if character.cy - character.height//2 + character.cdy - app.borderWidth/2 < app.boardTop:
        return False
    
    if isinstance(character, Fireball):
        for enemy in app.enemies:
            if math.dist([character.cx, character.cy], [enemy.cx, enemy.cy]) < enemy.width:
                enemy.health -= 1
                if enemy.health == 0:
                    app.enemies.remove(enemy)
                return False
    return True
<<<<<<< HEAD
=======

"""
Spawns dog enemies and makes sure they dont spawn on top of eachother
"""
def spawnEnemies(app):
    numEnemies = random.randint(2,5)
    for i in range(numEnemies):
        enemyWidth = 20
        enemyHeight = 20
        leftMostSpawn = app.boardLeft + (app.borderWidth//2 + 1) + enemyWidth
        rightMostSpawn = app.boardLeft + app.boardWidth - (app.borderWidth//2 + 1) - enemyWidth
        upMostSpawn = app.boardTop + (app.borderWidth//2 + 1) + enemyHeight 
        lowMostSpawn = app.boardTop + app.boardHeight - (app.borderWidth//2 + 1) - enemyHeight
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = (currEnemy.width**2 + currEnemy.height**2) ** 0.5
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        newEnemy = EnemyDog(cx, cy)
        app.enemies.append(newEnemy)

def drawGameOver(app):
    drawRect(0, 0, 500, 500, fill = "black", opacity = app.gameOverCounter)
    drawLabel("You Died", 250, 250, size = 30, font = 'Honoka Mincho', fill = 'red', opacity = app.gameOverCounter)
>>>>>>> New-Features

"""
This basically gives all the moves of the character and allows for extra stuff during different phrases of the program.
I will add those phases later.
"""
def onKeyHold(app, keys):
    if len(keys) >= 2:
        if 'a' in keys and 's' in keys:
            app.user.cdx = -app.user.speed
            app.user.cdy = app.user.speed
        elif 's' in keys and 'd' in keys:
            app.user.cdx = app.user.speed
            app.user.cdy = app.user.speed
        elif 'w' in keys and 'd' in keys:
            app.user.cdx = app.user.speed
            app.user.cdy = -app.user.speed
        elif 'a' in keys and 'w' in keys:
            app.user.cdx = -app.user.speed
            app.user.cdy = -app.user.speed
        elif 'a' in keys and 'd' in keys:
            app.user.cdx = 0
            app.user.cdy = 0
        elif 'w' in keys and 's' in keys:
            app.user.cdx = 0 
            app.user.cdy = 0

    elif len(keys) == 1:
        if 'a' in keys:
            app.user.cdx = -app.user.speed
            app.user.cdy = 0
        elif 's' in keys:
            app.user.cdy = app.user.speed
            app.user.cdx = 0
        elif 'd' in keys:
            app.user.cdx = app.user.speed
            app.user.cdy = 0
        elif 'w' in keys:
            app.user.cdy = -app.user.speed
            app.user.cdx = 0
    if 'f' in keys:
        if app.fireballShot == False:
            app.user.createFireball()
            app.fireballShot = True

"""
When the key is released the movement in the direction of that key is 0 now.
"""
def onKeyRelease(app, key):
    if key == 'a':
       app.user.cdx = 0
    if key == 's':
        app.user.cdy = 0
    if key == 'd':
        app.user.cdx = 0
    if key == 'w':
        app.user.cdy = 0

"""
Draw the board outline (with double-thickness)
"""

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black', borderWidth = app.borderWidth)
  
<<<<<<< HEAD
"This draws the game over screen when the user has 0 health"
def drawGameOver(app):
    drawRect(0, 0, 500, 500, fill = "black", opacity = app.gameOverCounter)
    drawLabel("You Died", 250, 250, size = 30, font = 'Honoka Mincho', fill = 'red', opacity = app.gameOverCounter)
=======
>>>>>>> New-Features
  
def redrawAll(app):
    drawBoardBorder(app)
    drawRect(0, 0, 190, 20, fill = "black")
    drawLabel("Health: ", 30, 10, fill = "white") 
    app.user.drawCharacter()
    for fireball in app.user.fireballs:
        fireball.drawFireball()
    for enemy in app.enemies:
        enemy.drawEnemy()
    for i in range(app.user.health):
        drawRect(60 + i*30, 10, 10, 10, fill = "pink", align = "center")
    if app.gameOver:
<<<<<<< HEAD
        drawGameOver(app) 
=======
        drawGameOver(app)
    
>>>>>>> New-Features

def main():
    runApp(width = 500, height = 500)

main()