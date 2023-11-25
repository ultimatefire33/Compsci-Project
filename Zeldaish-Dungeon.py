from cmu_graphics import *
import math
import random

"""
This is the main projectile that the user uses, used when 'f' is pressed
user can shoot a fireball every 0.5 seconds, also contains enemy fireball
"""
class Fireball:
    def __init__(self, cx, cy, cdx, cdy, enemyFireball):
        self.speed = 5
        self.radius = 5
        if not (enemyFireball):
            self.cdx , self.cdy = self.getDirection(cdx, cdy) 
            self.cdx = self.cdx * self.speed
            self.cdy = self.cdy * self.speed
        else:
            self.cdy = cdy * self.speed
            self.cdx = cdx * self.speed

        self.cx = cx + self.cdx
        self.cy = cy + self.cdy
        self.width = self.radius
        self.height = self.radius
        self.enemyFireball = enemyFireball
    
    def drawFireball(self):
        if self.enemyFireball == False:
            drawCircle(self.cx, self.cy, self.radius, fill = "red")
        else:
            drawCircle(self.cx, self.cy, self.radius, fill = "blue")

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

"""
This is the main character class, user moves with 'wasd'
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
        self.meleeDone = False
        self.fireballs = []

    def drawCharacter(self):
        if self.meleeDone:
            drawRect(self.cx, self.cy, self.width, self.height, fill = "red", align = "center")
        else:
            drawRect(self.cx, self.cy, self.width, self.height, fill = "blue", align = "center")

    def changePosition(self):
        self.cx += self.cdx
        self.cy += self.cdy

    def createFireball(self):
        if len(self.fireballs) < 3 and self.ifBothZero() == False:
            newFireball = Fireball(self.cx, self.cy, self.cdx, self.cdy, False)
            self.fireballs.append(newFireball)

    def ifBothZero(self):
        if self.cdx == 0 and self.cdy == 0:
            return True
        return False
    
    def melee(self, enemy):
        totalDistance = math.dist([self.cx, self.cy], [enemy.cx, enemy.cy])
        if totalDistance < self.width * 2:
            enemy.health -= 2

"""
This is another enemy type that shoots projectiles and doesnt chase the user.
It will back away when the user gets into a certain distance with the enemy.
"""          
class EnemyMage:
    def __init__(self, cx, cy):
        self.health = 2
        self.cx = cx
        self.cy = cy
        self.cdx = 0
        self.cdy = 0
        self.fireballCDX = 0
        self.fireballCDY = 0
        self.height = 20
        self.width = 20
        self.speed = 0
        self.fireballs = []
    
    def drawEnemy(self):
        drawRect(self.cx, self.cy, self.width, self.height, fill = "purple", align = "center")

    def changePosition(self, user):
        if user.health > 0:
            totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
            if totalDistance < self.width * 2:
                self.speed = 2
            else:
                self.speed = 0
            self.cdx = -((user.cx - self.cx) / totalDistance) * self.speed
            self.cdy = -((user.cy - self.cy) / totalDistance) * self.speed
            self.cx += self.cdx
            self.cy += self.cdy
        else:
            self.cdx = 0
            self.cdy = 0

    def createFireball(self, user):
        totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
        self.fireballCDX = ((user.cx - self.cx) / totalDistance)
        self.fireballCDY = ((user.cy - self.cy) / totalDistance) 
        newFireball = Fireball(self.cx, self.cy, self.fireballCDX, self.fireballCDY, True)
        self.fireballs.append(newFireball)
          
"""
This is a melee type of enemy that removes one health from the user every second in range
"""   
class EnemyDog:
    def __init__(self, cx, cy):
        self.health = 3
        self.cx = cx
        self.cy = cy
        self.cdx = 0
        self.cdy = 0
        self.height = 20
        self.width = 20
        self.speed = 0
    
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
    app.mageEnemies = []
    app.gameOver = False
    app.gameOverCounter = 0
    app.wait = False
    spawnEnemies(app)

"""
Spawns dog enemies and makes sure they dont spawn on top of eachother, also spawns random amount
from 1-3 and mages from 1-2
"""
def spawnEnemies(app):
    numEnemyDog = random.randint(1,3)
    numEnemyMage = random.randint(1,2)
    enemyWidth = 20
    enemyHeight = 20
    leftMostSpawn = app.boardLeft + (app.borderWidth//2 + 1) + enemyWidth
    rightMostSpawn = app.boardLeft + app.boardWidth - (app.borderWidth//2 + 1) - enemyWidth
    upMostSpawn = app.boardTop + (app.borderWidth//2 + 1) + enemyHeight 
    lowMostSpawn = app.boardTop + app.boardHeight - (app.borderWidth//2 + 1) - enemyHeight

    for i in range(numEnemyDog):
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = (currEnemy.width**2 + currEnemy.height**2) ** 0.5
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        dogEnemy = EnemyDog(cx, cy)
        app.enemies.append(dogEnemy)

    for i in range(numEnemyMage):
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = (currEnemy.width**2 + currEnemy.height**2) ** 0.5
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        mageEnemy = EnemyMage(cx, cy)
        app.enemies.append(mageEnemy)
        app.mageEnemies.append(mageEnemy)

"""
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

    if app.timerCounter % 60 == 0:
        app.user.meleeDone = False
        app.wait = False
        for mage in app.mageEnemies:
            mage.createFireball(app.user)

    if isLegal(app, app.user)and app.user.health > 0:
        app.user.changePosition()
    
    for enemy in app.enemies:
        if isLegal(app, enemy):
            enemy.changePosition(app.user)
            if app.user.hitCurr == False and isinstance(enemy, EnemyDog):
                enemy.melee(app.user)
            if app.user.meleeDone == True and app.wait == False:
                app.user.melee(enemy)
                if enemy.health <= 0:
                    app.enemies.remove(enemy)
                    if enemy in app.mageEnemies:
                        app.mageEnemies.remove(enemy) 
                app.wait = True

    for fireball in app.user.fireballs:
        if isLegal(app, fireball) and app.gameOver == False:
            fireball.changeFireballPos()  
        else:
            app.user.fireballs.remove(fireball) 

    for mage in app.mageEnemies:
        for fireball in mage.fireballs:
            if isLegal(app, fireball) and app.gameOver == False:
                fireball.changeFireballPos()
            else:
                mage.fireballs.remove(fireball)

"""
This checks if a movement for an npc or the user is legal, can also apply to the moves of each
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
        if character.enemyFireball == False:
            for enemy in app.enemies:
                if math.dist([character.cx, character.cy], [enemy.cx, enemy.cy]) < enemy.width:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        app.enemies.remove(enemy)
                        if enemy in app.mageEnemies:
                            app.mageEnemies.remove(enemy) 
                    return False
        else:
            if math.dist([character.cx, character.cy], [app.user.cx, app.user.cy]) < app.user.width:
                app.user.health -= 1
                return False       
    return True

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
    if 'g' in keys:
        if app.user.meleeDone == False:
            app.user.meleeDone = True

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
  
"This draws the game over screen when the user has 0 health"
def drawGameOver(app):
    drawRect(0, 0, 500, 500, fill = "black", opacity = app.gameOverCounter)
    drawLabel("You Died", 250, 250, size = 30, font = 'Honoka Mincho', fill = 'red', opacity = app.gameOverCounter)
  
def redrawAll(app):
    drawBoardBorder(app)
    drawRect(0, 0, 190, 20, fill = "black")
    drawLabel("Health: ", 30, 10, fill = "white") 
    app.user.drawCharacter()

    for fireball in app.user.fireballs:
        fireball.drawFireball()

    for enemy in app.enemies:
        enemy.drawEnemy()

    for mage in app.mageEnemies:
        for fireball in mage.fireballs:
            fireball.drawFireball()
    
    for i in range(app.user.health):
        drawRect(60 + i*30, 10, 10, 10, fill = "pink", align = "center")
        
    if app.gameOver:
        drawGameOver(app) 
        drawGameOver(app) 

def main():
    runApp(width = 500, height = 500)

main()