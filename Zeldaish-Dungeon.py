from cmu_graphics import *
from PIL import Image
import os, pathlib
import math
import random

"""
This is the parent enemy class that is used for all enemies.
"""
class Enemy:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.cdx = 0
        self.cdy = 0
        self.height = 30
        self.width = 30
        self.speed = 0
        self.hasMelee = False
        self.canMove = False

    def melee(self, user):
        if self.hasMelee:
            totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
            if totalDistance <= self.width:
                user.health -= 1
                user.hitCurr = True 

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
                
                if obstacleDistance < 100 and abs(math.atan2(obstacleVectY, obstacleVectX) - angleToPlayer) < math.pi/2 and angleToPlayer > math.pi/2:
                    changeAngle = math.atan2(obstacleVectY, obstacleVectX) + math.pi / 2
                    self.cx += math.cos(changeAngle) * self.speed * 2
                    self.cy += math.sin(changeAngle) * self.speed * 2

                elif obstacleDistance < 100 and abs(math.atan2(obstacleVectY, obstacleVectX) - angleToPlayer) < math.pi/2 and angleToPlayer < math.pi/2:
                    changeAngle = math.atan2(obstacleVectY, obstacleVectX) - math.pi / 2
                    self.cx += math.cos(changeAngle) * self.speed * 2
                    self.cy += math.sin(changeAngle) * self.speed * 2
        else:
            self.cdx = 0
            self.cdy = 0
            self.speed = 0

"""
This is the main projectile that the user/mage uses, used when 'f' is pressed
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
        self.height = 31
        self.width = 29
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
class EnemyMage(Enemy):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.health = 2
        self.fireballCDX = 0
        self.fireballCDY = 0
        self.fireballs = []
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.hasMelee = False
        self.canMove = False
        self.height = 39
        self.width = 36
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
class EnemyKnight(Enemy):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.health = 3
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.currSprites = []
        self.spriteCounterEnemy = 0
        self.collision = False
        self.hasMelee = True
        self.canMove = True
        self.width = 38
        self.height = 36
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

"""
Weaker melee enemy class that also moves slower
"""
class EnemyMummy(Enemy):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.health = 1
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.spriteCounterEnemy = 0
        self.collision = False
        self.hasMelee = True
        self.canMove = True
        self.width = 39
        self.height = 39
        for i in range(2):
            self.sprite = CMUImage(spritestrip.crop((638, 345 + 60*i, 677, 384 + 60*i)))
            self.sprites.append(self.sprite)

    def drawEnemy(self):
        sprite = self.sprites[self.spriteCounterEnemy]
        drawImage(sprite, self.cx, self.cy)

"""
Very basic enemy that cant move much and still melees the user if they get too close
"""
class EnemySlime(Enemy):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.health = 1
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.spriteCounterEnemy = 0
        self.hasMelee = True
        self.canMove = True
        self.width = 34
        self.height = 33
        for i in range(2):
            self.sprite = CMUImage(spritestrip.crop((740, 350 + 60*i, 774, 383 + 60*i)))
            self.sprites.append(self.sprite)

    def drawEnemy(self):
        sprite = self.sprites[self.spriteCounterEnemy]
        drawImage(sprite, self.cx, self.cy)

    def changePosition(self, user, obstacles):
        if user.health > 0:
            angle = random.randint(0, 360)
            self.speed = 10
            self.cdx = math.cos(angle) * self.speed
            self.cdy = math.sin(angle) * self.speed
            self.cx += self.cdx
            self.cy += self.cdy
        else:
            self.speed = 0
            self.cdx = 0
            self.cdy = 0

"""
This is another enemy type that moves around the edge of a room and hits the player
taking 1 health from them.
"""            
class EnemyLightning(Enemy):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.health = 2
        self.speed = 10
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.spriteCounterEnemy = 0
        self.hasMelee = True
        self.canMove = True
        self.height = 40
        self.width = 33
        self.startingWall = random.randint(1,4)
        self.currWall = 0
        for i in range(2):
            self.sprite = CMUImage(spritestrip.crop((820, 114 + 60*i, 853, 154 + 60*i)))
            self.sprites.append(self.sprite)
    
    def drawEnemy(self):
        sprite = self.sprites[self.spriteCounterEnemy]
        drawImage(sprite, self.cx, self.cy)

    def changePosition(self):
        if self.startingWall != None:
            if self.startingWall == 1:
                self.cx = 65
                self.cy = 100
                self.cdx = 0
                self.cdy = -10
                self.currWall = self.startingWall
                self.startingWall = None

            elif self.startingWall == 2:
                self.cx = 150
                self.cy = 67
                self.cdx = 10
                self.cdy = 0
                self.currWall = self.startingWall
                self.startingWall = None

            elif self.startingWall == 3:
                self.cx = 397
                self.cy = 100
                self.cdx = 0
                self.cdy = -10
                self.currWall = self.startingWall
                self.startingWall = None

            elif self.startingWall == 4:
                self.cx = 150
                self.cy = 252
                self.cdx = -10
                self.cdy = 0
                self.currWall = self.startingWall
                self.startingWall = None
        else:
            if self.isLegalLightning() == False:
                self.getNextVals()
            else:
                self.cx += self.cdx
                self.cy += self.cdy

    def isLegalLightning(self):
        if self.cdx == 0 and self.cdy < 0:
            if self.cy + self.cdy < 55:
                return False
            else:
                return True
        elif self.cdx > 0 and self.cdy == 0:
            if self.cdx + self.cx > 415:
                return False
            else:
                return True
        elif self.cdx == 0 and self.cdy > 0:
            if self.cy + self.cdy > 255:
                return False
            else:
                return True
        elif self.cdx < 0 and self.cdy == 0:
            if self.cx + self.cdx < 60:
                return False
            else:
                return True
            
    def getNextVals(self):
        if self.currWall == 1:
            self.currWall = 2
            self.cdx = 10
            self.cdy = 0

        elif self.currWall == 2:
            self.currWall = 3
            self.cdx = 0
            self.cdy = 10

        elif self.currWall == 3:
            self.currWall = 4
            self.cdx = -10
            self.cdy = 0

        elif self.currWall == 4:
            self.currWall = 1
            self.cdx = 0
            self.cdy = -10

"""
Miniboss with 7 health and moves the same way as the mummy and knight ai
"""
class EnemyLynel(Enemy):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.health = 7
        spritestrip = Image.open('images/zelda_enemies_sheet.png')
        self.sprites = []
        self.currSprites = []
        self.spriteCounterEnemy = 0
        self.collision = False
        self.hasMelee = True
        self.canMove = True
        self.width = 38
        self.height = 39
        for i in range(4):
            for j in range(2):
                self.sprite = CMUImage(spritestrip.crop((230+60*i, 465 + 60*j, 268+60*i, 504 + 60*j)))
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

"""
Key spawns that leads to next room and happens every time the enemies in the room you
are currently in are defeated.
"""
class Key:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.taken = False
        spritestrip = spritestrip = Image.open('images/zelda_sprite_sheet.png')
        self.sprite = CMUImage(spritestrip.crop((693, 489, 723, 527)))

    def drawKey(self):
        drawImage(self.sprite, self.cx, self.cy)

"""
Heart spawns that gives back all health and happens when all the enemies in the room you are
in are defeated. If not picked up and user goes to the next room, it will disappear.
"""
class Heart:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.taken = False
        spritestrip = spritestrip = Image.open('images/zelda_sprite_sheet.png')
        self.sprite = CMUImage(spritestrip.crop((570, 376, 611, 410)))
    
    def drawHeart(self):
        drawImage(self.sprite, self.cx, self.cy)

"""
Triforce Piece spawns whenever all enemies in level 8 are defeated. When picked up the game is over.
"""
class TriforcePiece:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.taken = False
        spritestrip = spritestrip = Image.open('images/zelda_sprite_sheet.png')
        self.sprite = CMUImage(spritestrip.crop((636, 550, 669, 579)))
    
    def drawTriforcePiece(self):
        drawImage(self.sprite, self.cx, self.cy)
      
"""
Obstacle that makes it so player and enemies cant move in that square.
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
    app.gameWon = False
    app.levelClear = False
    app.positionLevel = 8
    app.level = 8
    app.stepsPerSecond = 20
    app.boardLeft = 57
    app.boardTop = 60
    app.boardWidth = 386
    app.boardHeight = 227
    app.user = Character()
    app.timerCounter = 0
    app.fireballShot = False
    app.enemies = []
    app.mageEnemies = []
    app.obstacles = []
    app.keys = []
    app.hearts = []
    app.keyNotPicked = []
    app.triforcePieces = []
    app.gameOver = False
    app.gameOverCounter = 0
    app.wait = False
    app.leftMostSpawn = app.boardLeft + 35
    app.rightMostSpawn = app.boardLeft + app.boardWidth - 35
    app.upMostSpawn = app.boardTop + 35 
    app.lowMostSpawn = app.boardTop + app.boardHeight - 35
    app.tileset = Image.open('images/zelda_tileset.png')
    app.spritestrip = Image.open('images/zelda_sprite_sheet.png')
    spawnEnemies(app)

"""
This spawns the enemies for each level
"""
def spawnEnemies(app):
    if app.level == 1:
        spawnSpecificEnemy(app, 1, EnemyMummy)
        spawnSpecificEnemy(app, 1, EnemySlime)
    if app.level == 2:
        spawnSpecificEnemy(app, 2, EnemyMummy)
        spawnSpecificEnemy(app, 2, EnemySlime)
    if app.level == 3:
        spawnSpecificEnemy(app, 1, EnemyMage)
        spawnSpecificEnemy(app, 1, EnemyLightning)
    if app.level == 4:
        spawnSpecificEnemy(app, 2, EnemyMage)
        spawnSpecificEnemy(app, 1, EnemyMummy)
    if app.level == 5:
        spawnSpecificEnemy(app, 1, EnemyMage)
        spawnSpecificEnemy(app, 1, EnemyKnight)
    if app.level == 6:
        spawnSpecificEnemy(app, 1, EnemyLightning)
        spawnSpecificEnemy(app, 2, EnemyKnight)
    if app.level == 7:
        spawnSpecificEnemy(app, 2, EnemyMage)
        spawnSpecificEnemy(app, 1, EnemyKnight)
    if app.level == 8:
        spawnSpecificEnemy(app, 1, EnemyMage)
        spawnSpecificEnemy(app, 1, EnemyLynel)

"""
This spawns the specific enemy types
"""
def spawnSpecificEnemy(app, numEnemy, enemyType):
    for i in range(numEnemy):
        cx = random.randint(app.leftMostSpawn + 50, app.rightMostSpawn - 50)
        cy = random.randint(app.upMostSpawn + 50, app.lowMostSpawn - 50)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = math.hypot(currEnemy.width, currEnemy.height)
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypot == True:
                    cx = random.randint(app.leftMostSpawn + 50, app.rightMostSpawn - 50)
                    cy = random.randint(app.upMostSpawn + 50, app.lowMostSpawn - 50)
        newEnemy = enemyType(cx, cy)
        app.enemies.append(newEnemy)
        if isinstance(newEnemy, EnemyMage):
            app.mageEnemies.append(newEnemy)

"""
Spawns the obstacles so the enemy won't get clipped into them
"""        
def spawnObstacles(app):
    numObstacles = 1
    padding = 35
    leftMostSpawn = app.leftMostSpawn + padding
    rightMostSpawn = app.rightMostSpawn - padding
    upMostSpawn = app.upMostSpawn + padding
    lowMostSpawn = app.lowMostSpawn - padding
    for i in range(numObstacles):

        cx = random.randint(leftMostSpawn, rightMostSpawn)
        cy = random.randint(upMostSpawn, lowMostSpawn)

        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypotEnemy = math.hypot(currEnemy.width, currEnemy.height)
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypotEnemy * 8 or math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < currEnemy.width * 8:
                while (math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < hypotEnemy * 8 == True) and (math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < currEnemy.width * 8 == True):
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)
        
        for obstacle in app.obstacles:
            hypotObstacle = math.hypot(obstacle.width, obstacle.height)
            if (math.dist([cx, cy], [obstacle.cx, obstacle.cy]) < hypotObstacle * 8 == True):
                while (math.dist([cx, cy], [obstacle.cx, obstacle.cy]) < hypotObstacle * 8):
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)

        newObstacle = Obstacle(cx, cy)
        app.obstacles.append(newObstacle) 

def levelClearer(app):
    if (app.levelClear == True) and (len(app.enemies) == 0) and (app.level != 8):
        spawnKeyAndHealth(app)
        app.levelClear = False

def gameDone(app):
    if (app.levelClear == True) and (len(app.enemies) == 0) and (app.level == 8):
        spawnTriforce(app)
        app.levelClear = False

def spawnTriforce(app):
    padding = 35
    imageHeight = 35
    imageWidth = 35
    padding = 35
    leftMostSpawn = app.boardLeft + imageWidth + padding
    rightMostSpawn = app.boardLeft + app.boardWidth - imageWidth - padding
    upMostSpawn = app.boardTop + imageHeight + padding
    lowMostSpawn = app.boardTop + app.boardHeight - imageHeight - padding

    if app.levelClear:
        cxTri = random.randint(leftMostSpawn, rightMostSpawn)
        cyTri = random.randint(upMostSpawn, lowMostSpawn)
        tri = TriforcePiece(cxTri, cyTri)
        app.triforcePieces = [tri]

def spawnKeyAndHealth(app):
    padding = 35
    imageHeight = 35
    imageWidth = 35
    padding = 35
    leftMostSpawn = app.boardLeft + imageWidth + padding
    rightMostSpawn = app.boardLeft + app.boardWidth - imageWidth - padding
    upMostSpawn = app.boardTop + imageHeight + padding
    lowMostSpawn = app.boardTop + app.boardHeight - imageHeight - padding

    if app.levelClear:
        cxKey = random.randint(leftMostSpawn, rightMostSpawn)
        cyKey = random.randint(upMostSpawn, lowMostSpawn)
        key = Key(cxKey, cyKey)
        app.keyNotPicked = [key]
        cxHeart = random.randint(leftMostSpawn, rightMostSpawn)
        cyHeart = random.randint(upMostSpawn, lowMostSpawn)
        heart = Heart(cxHeart, cyHeart)
        app.hearts = [heart]

def goNewRoom(app):
    if len(app.keys) == app.level and app.level == 1:
        if 189 <= app.user.cx <= 253 and 70 <= app.user.cy <= 85:
            app.user.cx = 215
            app.user.cy = 235
            app.level = 2
            app.positionLevel = 2
            spawnEnemies(app)
            app.obstacles = []
            app.hearts = []
            spawnObstacles(app)

    elif len(app.keys) == app.level and app.level == 2:
        if 75 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 390
            app.user.cy = 160
            app.level = 3
            app.positionLevel = 3
            spawnEnemies(app)
            app.obstacles = []
            app.hearts = []
            spawnObstacles(app)

    elif app.level == 4 and app.positionLevel == 2:
        if 140 <= app.user.cy <= 175 and 385 <= app.user.cx <= 395:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 4 
            app.obstacles = []
            app.hearts = []
            spawnEnemies(app)
            spawnObstacles(app)    
            app.level = 5    

    elif app.positionLevel == 2 and app.level == 5:
        if 189 <= app.user.cx <= 253 and 70 <= app.user.cy <= 85:
            app.user.cx = 215
            app.user.cy = 235
            app.positionLevel = 5
            spawnEnemies(app)
            spawnObstacles(app) 
            
    elif app.level == 5 and app.positionLevel == 5 and len(app.keys) == 5:
        if 140 <= app.user.cy <= 175 and 385 <= app.user.cx <= 395:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 6 
            app.obstacles = []
            app.hearts = []
            app.level = 6
            spawnEnemies(app)
            spawnObstacles(app) 

    elif app.positionLevel == 5 and len(app.keys) == 6:
         if 75 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 390
            app.user.cy = 160
            app.level = 7
            app.positionLevel = 7
            app.obstacles = []
            app.hearts = []
            spawnEnemies(app)
            spawnObstacles(app)

    elif app.positionLevel == 5 and app.level == 7 and len(app.keys) == 7:
        if 189 <= app.user.cx <= 253 and 70 <= app.user.cy <= 85:
            app.user.cx = 215
            app.user.cy = 235
            app.level = 8
            app.positionLevel = 8
            app.obstacles = []
            app.hearts = []
            spawnEnemies(app)
    else:
        goBackPrevious(app)

def goBackPrevious(app):
    if app.positionLevel == 2 and len(app.keys) >= 2 and 200 <= app.user.cx <= 230 and 240 <= app.user.cy <= 260:
        app.positionLevel = 1
        app.obstacles = []
        app.hearts = []
        app.user.cx = 235
        app.user.cy = 75  

    elif len(app.keys) == app.level and app.level == 3:
        if 145 <= app.user.cy <= 165 and 385 <= app.user.cx <= 395:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 2 
            app.obstacles = []
            app.hearts = []
            app.level = 4

    elif app.positionLevel == 3 and app.level > 3:
         if 145 <= app.user.cy <= 165 and 385 <= app.user.cx <= 395:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 2 
            app.obstacles = []
            app.hearts = []

    elif app.positionLevel == 4 and app.level > 4:
        if 75 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 400
            app.user.cy = 160
            app.positionLevel = 2
            app.obstacles = []
            app.hearts = []

    elif app.level == 6 and app.positionLevel == 6 and len(app.keys) == 6:
        if 75 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 400
            app.user.cy = 160
            app.positionLevel = 5
            app.obstacles = []
            app.hearts = []

    elif app.positionLevel == 7 and app.level == 7 and (len(app.keys)) == 7:
        if 145 <= app.user.cy <= 165 and 385 <= app.user.cx <= 395:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 5
            app.obstacles = []
            app.hearts = []

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
            if app.timerCounter % 2 == 0:
                app.user.spriteCounter = (1 + app.user.spriteCounter) % len(app.user.currSprites)
    else:
        app.user.spriteCounter = (1 + app.user.spriteCounter) % 1

    for enemy in app.enemies:
        if isinstance(enemy, EnemyKnight) or isinstance(enemy, EnemyLynel):
            if enemy.cdx == 0 and enemy.cdy == 0:
                enemy.spriteCounterEnemy = (1 + enemy.spriteCounterEnemy) % 1
            else:
                if app.timerCounter % 2 == 0:
                    enemy.spriteCounterEnemy = (1 + enemy.spriteCounterEnemy) % len(enemy.currSprites)

        elif isinstance(enemy, EnemyMage):
            for fireball in enemy.fireballs:
                fireball.spriteCounterFire = (1 + fireball.spriteCounterFire) % len(fireball.sprites)

        elif isinstance(enemy, EnemyMummy):
            if app.timerCounter % 2 == 0:
                enemy.spriteCounterEnemy = (1 + enemy.spriteCounterEnemy) % len(enemy.sprites)

        elif isinstance(enemy, EnemySlime) or isinstance(enemy, EnemyLightning):
            if app.timerCounter % 15 == 0:
                enemy.spriteCounterEnemy = (1 + enemy.spriteCounterEnemy) % len(enemy.sprites)
    
    for fireball in app.user.fireballs:
        fireball.spriteCounterFire = (1 + fireball.spriteCounterFire) % len(fireball.sprites) 

    if app.timerCounter % 30 == 0:
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
            if enemy.canMove:
                if isinstance(enemy, EnemySlime):
                    if app.timerCounter % 15 == 0:
                        enemy.changePosition(app.user, app.obstacles)
                elif isinstance(enemy, EnemyLightning):
                    if app.timerCounter % 2 == 0:
                        enemy.changePosition()
                else:
                    enemy.changePosition(app.user, app.obstacles)

            if app.user.hitCurr == False and enemy.hasMelee:
                enemy.melee(app.user)

            if app.user.meleeDone == True and app.wait == False:
                app.user.melee(enemy)
                if enemy.health <= 0:
                    app.enemies.remove(enemy)
                    if len(app.enemies) == 0:
                        app.levelClear = True
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
    
    levelClearer(app)
    gameDone(app)

"""
This checks if a movement for an npc or the user is legal, can also apply to the moves of each
"""
def isLegal(app, character):
    if isinstance(character, EnemyLightning) == False:
        if character.cx + character.cdx + character.width > 427:
            return False
        if character.cy + character.cdy + character.height > 270:
            return False
        if character.cx - character.width/2  + character.cdx < app.boardLeft:
            return False
        if character.cy - character.height/2 + character.cdy < app.boardTop:
            return False
        
        for obstacle in app.obstacles:
            if math.dist([character.cx + character.cdx, character.cy + character.cdy], [obstacle.cx, obstacle.cy]) <= math.hypot(obstacle.width, obstacle.height) * 0.6:
                return False     
        
    if isinstance(character, Fireball):
        if character.enemyFireball == False:
            for enemy in app.enemies:
                if math.dist([character.cx, character.cy], [enemy.cx, enemy.cy]) < enemy.width:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        app.enemies.remove(enemy)
                        if len(app.enemies) == 0:
                            app.levelClear = True
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
    if app.user.health > 0 or app.gameWon:
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

        if 'k' in keys:
            if len(app.keyNotPicked) != 0 and math.dist([app.user.cx, app.user.cy], [app.keyNotPicked[0].cx, app.keyNotPicked[0].cy]) < app.user.width * 2:
                app.keys.append(app.keyNotPicked[0])
                app.keyNotPicked[0].taken = True
                app.keyNotPicked = []

        if 'space' in keys:
            goNewRoom(app)

        if 'h' in keys and app.hearts != []:
            if math.dist([app.user.cx, app.user.cy], [app.hearts[0].cx, app.hearts[0].cy]) < app.user.width * 2:
                app.user.health = 5
                app.hearts = []

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
    drawLabel("Health ", 30, 15, fill = "white", font = "The Wild Breath of Zelda", bold = True)
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
    if app.level == 1 and len(app.keys) == 0:
        block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
        block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
        block3 = CMUImage(app.tileset.crop((1630, 154, 1695, 218)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -3, 144)
        drawImage(block2, 221, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 221, 1)
    elif (app.level == 1 and len(app.keys) == 1) or (app.positionLevel == 1 and app.keys >= 2):
        block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
        block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
        block3 = CMUImage(app.tileset.crop((1630, 154, 1695, 218)))
        block4 = CMUImage(app.tileset.crop((1696, 23, 1760, 86)))
        drawImage(block1, -3, 144)
        drawImage(block2, 221, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 221, 1)
    elif app.level == 2 and len(app.keys) == 1:
        block1 = CMUImage(app.tileset.crop((1763, 88, 1825, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1763, 156, 1826, 220)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 221, 1)
    elif app.level == 2 and len(app.keys) == 2:
        block1 = CMUImage(app.tileset.crop((1695, 88, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1763, 156, 1826, 220)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 221, 1)
    elif (app.level == 3 and len(app.keys) == 2) or app.positionLevel == 3:
        block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
        block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1630, 22, 1693, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif (app.level == 3 and len(app.keys) == 3) or app.positionLevel == 3:
        block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
        block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1630, 22, 1693, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif (len(app.keys) == 3 and app.level == 4) and app.positionLevel == 2:
        block1 = CMUImage(app.tileset.crop((1695, 88, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 4:
        block1 = CMUImage(app.tileset.crop((1696, 89, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1629, 222, 1693, 284)))
        block3 = CMUImage(app.tileset.crop((1630, 154, 1695, 218)))
        block4 = CMUImage(app.tileset.crop((1630, 22, 1693, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 2 and app.level >= 5:
        block1 = CMUImage(app.tileset.crop((1695, 88, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1696, 23, 1760, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 5 and app.level == 5 and (len(app.keys)) == 4:
        block1 = CMUImage(app.tileset.crop((1763, 88, 1825, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1763, 156, 1826, 220)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 221, 1)
    elif app.positionLevel == 5 and app.level == 5 and len(app.keys) == 5:
        block1 = CMUImage(app.tileset.crop((1763, 88, 1825, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1696, 155, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 221, 1)
    elif app.positionLevel == 6:
        block1 = CMUImage(app.tileset.crop((1696, 89, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1629, 222, 1693, 284)))
        block3 = CMUImage(app.tileset.crop((1630, 154, 1695, 218)))
        block4 = CMUImage(app.tileset.crop((1630, 22, 1693, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 5 and app.level == 6:
        block1 = CMUImage(app.tileset.crop((1695, 88, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1761, 23, 1825, 87)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 7 and app.level == 7:
        block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
        block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1630, 22, 1693, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 5 and app.level == 7:
        block1 = CMUImage(app.tileset.crop((1695, 88, 1759, 152)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1696, 154, 1759, 218)))
        block4 = CMUImage(app.tileset.crop((1696, 23, 1760, 86)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)
    elif app.positionLevel == 8 and app.level == 8:
        block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
        block2 = CMUImage(app.tileset.crop((1697, 221, 1759, 284)))
        block3 = CMUImage(app.tileset.crop((1630, 154, 1695, 218)))
        block4 = CMUImage(app.tileset.crop((1630, 22, 1692, 85)))
        drawImage(block1, -1, 144)
        drawImage(block2, 222, 289)
        drawImage(block3, 445, 144)
        drawImage(block4, 222, 1)


def drawStartingScreen(app):
    pass

def drawGameWon(app):
    image = Image.open('images/end_screen.png')
    endImage = CMUImage(image.crop((0,0, 505, 351)))
    drawImage(endImage, 0, 0)
    drawLabel("You Won", 258, 178, size = 60, font = 'The Wild Breath of Zelda', fill = 'green')
  
"""
This draws the game over screen when the user has 0 health.
"""
def drawGameOver(app):
    drawRect(0, 0, 516, 355, fill = "black", opacity = app.gameOverCounter)
    drawLabel("You Died", 258, 178, size = 60, font = 'The Wild Breath of Zelda', fill = 'red', opacity = app.gameOverCounter, bold = True)
  
def redrawAll(app):
    print(app.triforcePieces)
    drawBoardBorder(app)
    drawExterior(app)
    drawBackground(app)
    drawDoorBlocks(app)
    drawHealthBar(app)
    app.user.drawCharacter()
    for fireball in app.user.fireballs:
        fireball.drawFireball()

    for key in app.keyNotPicked:
        key.drawKey()

    for heart in app.hearts:
        heart.drawHeart()

    for enemy in app.enemies:
        enemy.drawEnemy()

    for mage in app.mageEnemies:
        for fireball in mage.fireballs:
            fireball.drawFireball()

    for obstacle in app.obstacles:
        obstacle.drawObstacle()
    
    for piece in app.triforcePieces:
        piece.drawTriforcePiece()

    if app.gameOver:
        drawGameOver(app)

    if app.gameWon:
        drawGameWon(app) 

def main():
    runApp(width = 505, height = 351)

main()