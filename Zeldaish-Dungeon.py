from cmu_graphics import *
from PIL import Image
import os, pathlib
import math
import random

"""
This is the main projectile that the user uses, used when 'f' is pressed
user can shoot a fireball every 0.5 seconds, also contains enemy fireball
"""
class Fireball:
    def __init__(self, cx, cy, cdx, cdy, enemyFireball):
        if enemyFireball:
            self.speed = 6
        else:
            self.speed = 6

        if not (enemyFireball):
            self.cdx , self.cdy = self.getDirection(cdx, cdy) 
            self.cdx = self.cdx * self.speed
            self.cdy = self.cdy * self.speed
        else:
            self.cdy = cdy * self.speed
            self.cdx = cdx * self.speed

        self.cx = cx + self.cdx
        self.cy = cy + self.cdy
        self.width = 43
        self.height = 35
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.enemyFireball = enemyFireball
        self.sprites = []
        self.spriteCounterFire = 0
        for i in range(2):
            self.sprite = CMUImage(spritestrip.crop((577, 0 + 60*i, 620, 35 + 60*i)))
            self.sprites.append(self.sprite)
    
    def drawFireball(self):
        sprite = self.sprites[self.spriteCounterFire]
        drawImage(sprite, self.cx, self.cy)

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
        self.speed = 5
        self.height = 15
        self.width = 16
        self.cx = 100
        self.cy = 100
        self.cdx = 0
        self.cdy = 0
        self.hitCurr = False
        self.meleeDone = False
        self.fireballs = []
        spritestrip = Image.open('images/zelda_sprite_sheet.png')
        self.sprites = []
        self.currSprites = []
        self.spriteCounter = 0
        self.meleeSprites = []

        for i in range(4):
            for j in range(2):
                self.sprite = CMUImage(spritestrip.crop((0+60*i, 0 + 60*j, 29+60*i, 31 + 60*j)))
                self.sprites.append(self.sprite)

        self.sprite = CMUImage(spritestrip.crop((0, 160, 30, 219)))
        self.meleeSprites.append(self.sprite)
        self.sprite = CMUImage(spritestrip.crop((40, 170, 103, 208)))
        self.meleeSprites.append(self.sprite)
        self.sprite = CMUImage(spritestrip.crop((108, 158, 150, 219)))
        self.meleeSprites.append(self.sprite)
        self.sprite = CMUImage(spritestrip.crop((159, 169, 219, 206)))
        self.meleeSprites.append(self.sprite)

    def drawCharacter(self):
        if not self.meleeDone:
            if self.cdx == 0 and self.cdy == 0:
                self.currSprites = self.sprites[0]
                sprite = self.currSprites
                drawImage(sprite, self.cx, self.cy)

            if self.cdy > 0:
                self.currSprites = self.sprites[0:2]
                sprite = self.currSprites[self.spriteCounter]
                drawImage(sprite, self.cx, self.cy)
            
            elif self.cdy < 0:
                self.currSprites = self.sprites[4:6]
                sprite = self.currSprites[self.spriteCounter]
                drawImage(sprite, self.cx, self.cy)
            
            elif self.cdx > 0:
                self.currSprites = self.sprites[6:]
                sprite = self.currSprites[self.spriteCounter]
                drawImage(sprite, self.cx, self.cy)

            elif self.cdx < 0:
                self.currSprites = self.sprites[2:4]
                sprite = self.currSprites[self.spriteCounter]
                drawImage(sprite, self.cx, self.cy)
        else:
            if self.cdx > 0:
                self.currSprites = self.meleeSprites[3]
                sprite = self.currSprites
                drawImage(sprite, self.cx, self.cy)

            elif self.cdx < 0:
                self.currSprites = self.meleeSprites[1]
                sprite = self.currSprites
                drawImage(sprite, self.cx, self.cy)

            elif self.cdy > 0 or (self.cdy == 0 and self.cdx == 0):
                self.currSprites = self.meleeSprites[0]
                sprite = self.currSprites
                drawImage(sprite, self.cx, self.cy)

            elif self.cdy < 0:
                self.currSprites = self.meleeSprites[2]
                sprite = self.currSprites
                drawImage(sprite, self.cx, self.cy)

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
        if totalDistance <= self.width * 2:
            enemy.health -= 2

"""
This is another enemy type that shoots projectiles and doesnt chase the user.
It will back away when the user gets into a certain distance with the enemy.
"""          
class EnemyMage:
    def __init__(self, cx, cy):
        self.health = 1
        self.cx = cx
        self.cy = cy
        self.cdx = 0
        self.cdy = 0
        self.fireballCDX = 0
        self.fireballCDY = 0
        self.height = 30
        self.width = 30
        self.speed = 0
        self.fireballs = []
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.currSprites = []
        for i in range(3):
            self.sprite = CMUImage(spritestrip.crop((460+60*i, 110, 499+60*i, 146)))
            self.sprites.append(self.sprite)
    
    def drawEnemy(self):
        if self.fireballCDY >= 0 and self.fireballCDX <= 0:
            self.currSprites = self.sprites[0]
            sprite = self.currSprites
            drawImage(sprite, self.cx, self.cy)

        if self.fireballCDY >= 0 and self.fireballCDX > 0:
            self.currSprites = self.sprites[2]
            sprite = self.currSprites
            drawImage(sprite, self.cx, self.cy)
        
        if self.fireballCDY < 0:
            self.currSprites = self.sprites[1]
            sprite = self.currSprites
            drawImage(sprite, self.cx, self.cy)

    def createFireball(self, user):
        totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
        self.fireballCDX = ((user.cx - self.cx) / totalDistance)
        self.fireballCDY = ((user.cy - self.cy) / totalDistance) 
        newFireball = Fireball(self.cx, self.cy, self.fireballCDX, self.fireballCDY, True)
        self.fireballs.append(newFireball)
          
"""
This is a melee type of enemy that removes one health from the user every second in range
"""   
class EnemyKnight:
    def __init__(self, cx, cy):
        self.health = 2
        self.cx = cx
        self.cy = cy
        self.cdx = 0
        self.cdy = 0
        self.height = 20
        self.width = 20
        self.speed = 0
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.currSprites = []
        self.spriteCounterEnemy = 0
        self.collision = False
        for i in range(4):
            for j in range(2):
                self.sprite = CMUImage(spritestrip.crop((224+60*i, 349 + 60*j, 262+60*i, 386 + 60*j)))
                self.sprites.append(self.sprite)
    
    def drawEnemy(self):
        if self.cdx == 0 and self.cdy == 0:
            self.currSprites = self.sprites[0]
            sprite = self.currSprites
            drawImage(sprite, self.cx, self.cy)

        elif abs(self.cdy) > abs(self.cdx) and self.cdy < 0:
            self.currSprites = self.sprites[0:2]
            sprite = self.currSprites[self.spriteCounterEnemy]
            drawImage(sprite, self.cx, self.cy)
        
        elif abs(self.cdy) > abs(self.cdx) and self.cdy > 0:
            self.currSprites = self.sprites[4:6]
            sprite = self.currSprites[self.spriteCounterEnemy]
            drawImage(sprite, self.cx, self.cy)
        
        elif abs(self.cdx) >= abs(self.cdy) and self.cdx < 0:
            self.currSprites = self.sprites[6:]
            sprite = self.currSprites[self.spriteCounterEnemy]
            drawImage(sprite, self.cx, self.cy)

        elif abs(self.cdx) >= abs(self.cdy) and self.cdx > 0:
            self.currSprites = self.sprites[2:4]
            sprite = self.currSprites[self.spriteCounterEnemy]
            drawImage(sprite, self.cx, self.cy)

    def changePosition(self, user, obstacles):
        if user.health > 0:
            directionVectX =  self.cx - user.cx
            directionVectY = self.cy - user.cy
            totalDistance = math.hypot(directionVectX, directionVectY)
            if totalDistance > self.width:
                self.speed = 2
                self.cdx = directionVectX / totalDistance
                self.cdy = directionVectY / totalDistance
            else:
                self.speed = 0
                self.cdx = 0
                self.cdy = 0
            
            angleToPlayer = math.atan2(-directionVectY, -directionVectX)
            self.cx += math.cos(angleToPlayer) * self.speed
            self.cy += math.sin(angleToPlayer) * self.speed

            for obstacle in obstacles:
                obstacleVectX = obstacle.cx - self.cx
                obstacleVectY = obstacle.cy - self.cy
                obstacleDistance = math.hypot(obstacleVectX, obstacleVectY)
                if obstacleDistance < 100 and abs(math.atan2(obstacleVectY, obstacleVectX) - angleToPlayer) < math.pi/2:
                    changeAngle = math.atan2(obstacleVectY, obstacleVectX) + math.pi / 2
                    self.cx += math.cos(changeAngle) * self.speed * 2
                    self.cy += math.sin(changeAngle) * self.speed * 2
        else:
            self.cdx = 0
            self.cdy = 0
            self.speed = 0

    def melee(self, user):
        totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
        if totalDistance <= self.width:
            user.health -= 1
            user.hitCurr = True
"""
Obstacle that makes it so player and enemies cant move in that square
"""
class Obstacle:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.width = 33
        self.height = 32
        self.tileset = Image.open('images/zelda_tileset.png')
        self.sprite = CMUImage(self.tileset.crop((2000, 22, 2033, 54)))

    def drawObstacle(self):
        drawImage(self.sprite, self.cx, self.cy)

"""
onAppStart basically sets all of the elementary values for the game.
"""
def onAppStart(app):
    app.stepsPerSecond = 20
    app.boardLeft = 57
    app.boardTop = 60
    app.boardWidth = 386
    app.boardHeight = 227
    app.globalCounter = 0
    app.fireCounter = 30
    app.user = Character()
    app.timerCounter = 0
    app.fireballShot = False
    app.enemies = []
    app.mageEnemies = []
    app.obstacles = []
    app.gameOver = False
    app.gameOverCounter = 0
    app.wait = False
    app.tileset = Image.open('images/zelda_tileset.png')
    app.spritestrip = Image.open('images/zelda_sprite_sheet.png')
    spawnEnemies(app)
    spawnObstacles(app)

"""
Spawns knight enemies and makes sure they dont spawn on top of eachother, also spawns random amount
from 1-3 and mages from 1-2
"""
def spawnEnemies(app):
    numEnemyKnight = random.randint(1,2)
    numEnemyMage = random.randint(1,2)
    enemyWidth = 35
    enemyHeight = 35
    leftMostSpawn = app.boardLeft + enemyWidth
    rightMostSpawn = app.boardLeft + app.boardWidth - enemyWidth
    upMostSpawn = app.boardTop + enemyHeight 
    lowMostSpawn = app.boardTop + app.boardHeight - enemyHeight

    for i in range(numEnemyKnight):
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = math.hypot(currEnemy.width, currEnemy.height)
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        knightEnemy = EnemyKnight(cx, cy)
        app.enemies.append(knightEnemy)

    for i in range(numEnemyMage):
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = math.hypot(currEnemy.width, currEnemy.height)
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        mageEnemy = EnemyMage(cx, cy)
        app.enemies.append(mageEnemy)
        app.mageEnemies.append(mageEnemy)

"""
Spawns the obstacles so the enemy won't get clipped into them
"""        

def spawnObstacles(app):
    numObstacles = random.randint(1,2)
    numObstacles = 1
    obstacleWidth = 35
    obstacleHeight = 35
    padding = 50
    leftMostSpawn = app.boardLeft + obstacleWidth + padding
    rightMostSpawn = app.boardLeft + app.boardWidth - obstacleWidth - padding
    upMostSpawn = app.boardTop + obstacleHeight + padding
    lowMostSpawn = app.boardTop + app.boardHeight - obstacleHeight - padding
    for i in range(numObstacles):
        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypotEnemy = math.hypot(currEnemy.width, currEnemy.height)
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypotEnemy * 8:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypotEnemy * 8 == True:
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        newObstacle = Obstacle(cx, cy)
        app.obstacles.append(newObstacle)

        

"""
This keeps track of all timed events and movement of main character, npcs, and 
projectiles
"""
def onStep(app):
    app.timerCounter += 1

    if app.user.health <= 0:
        app.gameOver = True

    if app.gameOver and app.gameOverCounter < 100:
        app.gameOverCounter += 1

    if app.user.meleeDone != True:
        if app.user.cdx == 0 and app.user.cdy == 0:
            app.user.spriteCounter = (1 + app.user.spriteCounter) % 1
        else:
            app.user.spriteCounter = (1 + app.user.spriteCounter) % len(app.user.currSprites)
    else:
        app.user.spriteCounter = (1 + app.user.spriteCounter) % 1

    for enemy in app.enemies:
        if isinstance(enemy, EnemyKnight):
            if enemy.cdx == 0 and enemy.cdy == 0:
                enemy.spriteCounterEnemy = (1 + enemy.spriteCounterEnemy) % 1
            else:
                enemy.spriteCounterEnemy = (1 + enemy.spriteCounterEnemy) % len(enemy.currSprites)
        elif isinstance(enemy, EnemyMage):
            for fireball in enemy.fireballs:
                fireball.spriteCounterFire = (1 + fireball.spriteCounterFire) % len(fireball.sprites)
    
    for fireball in app.user.fireballs:
        fireball.spriteCounterFire = (1 + fireball.spriteCounterFire) % len(fireball.sprites) 

    if app.timerCounter % 15 == 0:
        app.fireballShot = False
        app.user.meleeDone = False
        app.wait = False

    if app.timerCounter % 30 == 0:
        app.user.hitCurr = False
        for mage in app.mageEnemies:
            mage.createFireball(app.user)  

    if isLegal(app, app.user)and app.user.health > 0:
        app.user.changePosition()
    
    for enemy in app.enemies:
        if isLegal(app, enemy):
            if isinstance(enemy, EnemyKnight):
                enemy.changePosition(app.user, app.obstacles)
            if app.user.hitCurr == False and isinstance(enemy, EnemyKnight):
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

    if character.cx + character.cdx + character.width/2 + 15 > app.boardWidth + app.boardLeft:
        return False
    if character.cy + character.cdy + character.height/2 + 15 > app.boardHeight + app.boardTop:
        return False
    if character.cx - character.width/2  + character.cdx < app.boardLeft:
        return False
    if character.cy - character.height/2 + character.cdy < app.boardTop:
        return False
    
    for obstacle in app.obstacles:
        if isinstance(character, Fireball):
            if math.dist([character.cx + character.cdx , character.cy + character.cdy], [obstacle.cx, obstacle.cy]) + character.width <= ((obstacle.width**2 + obstacle.height**2) ** 0.5) * 1.3:
                return False
            
        else:
            if math.dist([character.cx + character.cdx , character.cy + character.cdy], [obstacle.cx, obstacle.cy]) + character.width <= ((obstacle.width**2 + obstacle.height**2) ** 0.5) * 0.9:
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
    if app.user.health > 0:
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
            if app.user.meleeDone == False and app.wait == False:
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
Draws healthbar for the user.
"""
def drawHealthBar(app):
    drawRect(0, 0, 240, 30) 
    drawLabel("Health: ", 30, 15, fill = "white")
    heart = CMUImage(app.spritestrip.crop((467, 382, 487, 402)))
    for i in range(app.user.health):
        drawImage(heart, 50 + i*40, 5)
"""
Draws the base plate where the character walks on.
"""
def drawBackground(app):
    background = CMUImage(app.tileset.crop((3, 384, 386, 608)))
    drawImage(background, app.boardLeft + 4, app.boardTop + 4)
"""
Draws the walls of the room
"""
def drawExterior(app):
    exterior = CMUImage(app.tileset.crop((1045, 22, 1550, 375)))
    drawImage(exterior, 0, 0)

"""
Draw the board outline (with double-thickness).
"""
def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black')
  
"""
Draws the doors of the room
"""
def drawDoorBlocks(app):
    block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
    block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
    block3 = CMUImage(app.tileset.crop((1630, 154, 1695, 218)))
    block4 = CMUImage(app.tileset.crop((1696, 23, 1760, 86)))
    drawImage(block1, -3, 144)
    drawImage(block2, 221, 289)
    drawImage(block3, 445, 144)
    drawImage(block4, 221, 1)
  
"""
This draws the game over screen when the user has 0 health.
"""
def drawGameOver(app):
    drawRect(0, 0, 516, 355, fill = "black", opacity = app.gameOverCounter)
    drawLabel("You Died", 258, 178, size = 30, font = 'Honoka Mincho', fill = 'red', opacity = app.gameOverCounter)
  
def redrawAll(app):
    drawBoardBorder(app)
    drawExterior(app)
    drawBackground(app)
    drawDoorBlocks(app)
    drawHealthBar(app)
    app.user.drawCharacter()
    for fireball in app.user.fireballs:
        fireball.drawFireball()
    for enemy in app.enemies:
        enemy.drawEnemy()
    for mage in app.mageEnemies:
        for fireball in mage.fireballs:
            fireball.drawFireball()  
    for obstacle in app.obstacles:
        obstacle.drawObstacle()
    if app.gameOver:
        drawGameOver(app) 
        drawGameOver(app)    

def main():
    runApp(width = 505, height = 351)

main()