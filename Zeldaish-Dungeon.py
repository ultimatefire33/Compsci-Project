from cmu_graphics import *
from PIL import Image
import os, pathlib
import math
import random
import csv
import pandas as pd


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
        self.meleeDamage = 1
        self.hasMelee = False
        self.canMove = False
        self.checkShoot = False
        self.shouldNotShoot = False

    def melee(self, user):
        if self.hasMelee:
            totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
            if totalDistance <= self.width:
                user.health -= self.meleeDamage
                user.hitCurr = True 

    def changePosition(self, user, obstacles):
        if user.health > 0:
            directionVectX =  self.cx - user.cx
            directionVectY = self.cy - user.cy
            totalDistance = math.hypot(directionVectX, directionVectY)
            self.checkShoot = False
            self.shouldNotShoot = False

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

            if self.cx + math.cos(angleToPlayer) * self.speed > 410:
                self.cx += - (math.cos(angleToPlayer) * self.speed)
            elif self.cy + math.sin(angleToPlayer) * self.speed > 255:
                self.cy += - (math.sin(angleToPlayer) * self.speed)
            elif self.cx + math.sin(angleToPlayer) * self.speed < 65:
                self.cx += - (math.cos(angleToPlayer) * self.speed)
            elif self.cy + math.sin(angleToPlayer) * self.speed < 65:
                self.cy += - (math.sin(angleToPlayer) * self.speed)

            for obstacle in obstacles:
                obstacleVectX = obstacle.cx - self.cx
                obstacleVectY = obstacle.cy - self.cy
                obstacleDistance = math.hypot(obstacleVectX, obstacleVectY)
                
                if abs(math.atan2(obstacleVectY, obstacleVectX) - angleToPlayer) < math.pi/4:
                    self.checkShoot = True

                if obstacleDistance < 60 and abs(math.atan2(obstacleVectY, obstacleVectX) - angleToPlayer) < math.pi/2 and angleToPlayer > math.pi/2:
                    changeAngle = math.atan2(obstacleVectY, obstacleVectX) + math.pi / 2
                    self.cx += math.cos(changeAngle) * self.speed * 2
                    self.cy += math.sin(changeAngle) * self.speed * 2

                elif obstacleDistance < 60 and abs(math.atan2(obstacleVectY, obstacleVectX) - angleToPlayer) < math.pi/2 and angleToPlayer < math.pi/2:
                    changeAngle = math.atan2(obstacleVectY, obstacleVectX) - math.pi / 2
                    self.cx += math.cos(changeAngle) * self.speed * 2
                    self.cy += math.sin(changeAngle) * self.speed * 2
            
            if self.checkShoot:
                self.shouldNotShoot = True
            else:
                self.shouldNotShoot = False

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
        self.fireballCDX = 0
        self.fireballCDY = 0
        self.fireballs = []
        self.spriteCounterEnemy = 0
        self.collision = False
        self.hasMelee = True
        self.canMove = True
        self.width = 38
        self.height = 39
        self.speed = 3
        self.meleeDamage = 2
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

    def createFireball(self, user):
        if self.shouldNotShoot == False:
            totalDistance = math.dist([self.cx, self.cy], [user.cx, user.cy])
            self.fireballCDX = ((user.cx - self.cx) / totalDistance)
            self.fireballCDY = ((user.cy - self.cy) / totalDistance) 
            newFireball = Fireball(self.cx, self.cy, self.fireballCDX, self.fireballCDY, True)
            self.fireballs.append(newFireball)

"""
Key spawns that leads to next room and happens every time the enemies in the room you
are currently in are defeated.
"""
class Key:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.taken = False
        spritestrip = Image.open('images/zelda_sprite_sheet.png')
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
Above is all classes
------------------------------------------------------------------------------------------
Below is methods relating to the game
"""

"""
onAppStart basically sets all of the elementary values for the game.
"""
def onAppStart(app):
    app.soundMelee = loadSound("sounds/sword_slash.wav")
    app.soundEnemyDie = loadSound("sounds/enemy_die.wav")
    app.soundLinkHurt = loadSound("sounds/link_hurt.wav")
    app.soundLinkDie = loadSound("sounds/link_die.wav")
    app.soundGetHeart = loadSound("sounds/get_heart.wav")
    app.soundOpenDoor = loadSound("sounds/door_unlock.wav")
    app.soundCreateFireball = loadSound("sounds/shoot_fireball.wav")
    app.soundWin = loadSound("sounds/win.wav")
    app.gameStarted = False
    app.createDungeonRoom = False
    app.changeButtonStart = False
    app.changeButtonRoom = False
    app.cx = 200
    app.cy = 200
    app.width = 505
    app.height = 351
    app.acceptDungeon = False
    app.dungeonName = ""
    app.goToDungeonScreen = False
    app.changeButtonLoad = False
    app.changeButtonCreate = False
    app.getDungeonName = False
    app.loadDungeon = False
    app.help = False
    app.allPositions = []
    
"""
Basically the restart method
"""

def startAdventure(app):
    app.width = 505
    app.height = 351
    app.gameWon = False
    app.levelClear = False
    app.level = 1
    app.positionLevel = 1
    app.stepsPerSecond = 20
    app.boardLeft = 57
    app.boardTop = 60
    app.boardWidth = 386
    app.boardHeight = 227
    app.user = Character()
    app.timerCounter = 0
    app.fireballShot = False
    app.enemies = []
    app.fireuserEnemies = []
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

def createRoom(app):
    app.tileset = Image.open('images/zelda_tileset.png')
    app.spritestrip = Image.open('images/zelda_sprite_sheet.png')
    app.enemysprite = Image.open('images/zelda_enemies_sheet.png')
    app.boardLeft = 57
    app.boardTop = 60
    app.boardWidth = 386
    app.boardHeight = 227
    app.width = 605
    app.height = 451
    app.enemy1 = CMUImage(app.enemysprite.crop((464, 113, 503, 149)))
    app.enemy2 = CMUImage(app.enemysprite.crop((231, 348, 266, 387)))
    app.enemy3 = CMUImage(app.enemysprite.crop((819, 172, 852, 210)))
    app.enemy4 = CMUImage(app.enemysprite.crop((638, 349, 679, 386)))
    app.enemy5 = CMUImage(app.enemysprite.crop((741, 350, 779, 384)))
    app.enemy6 = CMUImage(app.enemysprite.crop((227, 464, 267, 504)))
    app.obstacleImg = CMUImage(app.tileset.crop((2000, 22, 2035, 55)))
    app.enemy1Width = 39
    app.enemy1Height = 36
    app.enemy2Width = 35
    app.enemy2Height = 39
    app.enemy3Width = 33
    app.enemy3Height = 38
    app.enemy4Width = 41
    app.enemy4Height = 37
    app.enemy5Width = 38
    app.enemy5Height = 34
    app.enemy5Width = 40
    app.enemy5Height = 40
    app.enemy6Width = 40
    app.enemy6Height = 40
    app.obstacleWidth = 35
    app.obstacleHeight = 33
    app.dragEnemy = False
    app.timeToDraw = False
    app.drawOtherVer = False
    app.enemiesNeedDraw = []
    app.enemiesForFile = []


def startDungeon(app):
    app.tileset = Image.open('images/zelda_tileset.png')
    app.spritestrip = Image.open('images/zelda_sprite_sheet.png')
    app.enemysprite = Image.open('images/zelda_enemies_sheet.png')
    app.stepsPerSecond = 20
    app.width = 505
    app.height = 351
    app.boardLeft = 57
    app.boardTop = 60
    app.boardWidth = 386
    app.boardHeight = 227
    app.gameWon = False
    app.user = Character()
    app.timerCounter = 0
    app.fireballShot = False
    app.enemies = []
    app.fireuserEnemies = []
    app.obstacles = []
    app.hearts = []
    app.triforcePieces = []
    app.gameOver = False
    app.gameOverCounter = 0
    app.wait = False
    app.levelClear = False
    app.leftMostSpawn = app.boardLeft + 35
    app.rightMostSpawn = app.boardLeft + app.boardWidth - 35
    app.upMostSpawn = app.boardTop + 35
    app.lowMostSpawn = app.boardTop + app.boardHeight - 35
    spawnEnemiesDungeon(app)

def spawnEnemiesDungeon(app):
    for enemy in app.allPositions:
        if app.leftMostSpawn >= int(enemy[1]):
            continue
        elif int(enemy[1]) >= app.rightMostSpawn:
            continue
        elif app.upMostSpawn >= int(enemy[2]):
            continue
        elif int(enemy[2]) >= app.lowMostSpawn:
            continue
        else:
            spawnEnemyDungeon(app, enemy[0], int(enemy[1]), int(enemy[2]))
        

def spawnEnemyDungeon(app, enemyType, enemyCX, enemyCY):
    if enemyType == "knight":
        newEnemy = EnemyKnight(enemyCX, enemyCY)
        app.enemies.append(newEnemy)
    elif enemyType == "mage":
        newEnemy = EnemyMage(enemyCX, enemyCY)
        app.enemies.append(newEnemy)
        app.fireuserEnemies.append(newEnemy)
    elif enemyType == "slime":
        newEnemy = EnemySlime(enemyCX, enemyCY)
        app.enemies.append(newEnemy)
    elif enemyType == "mummy":
        newEnemy = EnemyMummy(enemyCX, enemyCY)
        app.enemies.append(newEnemy)
    elif enemyType == "lynel":
        newEnemy = EnemyLynel(enemyCX, enemyCY)
        app.enemies.append(newEnemy)
        app.fireuserEnemies.append(newEnemy)
    elif enemyType == "lightning":
        newEnemy = EnemyLightning(enemyCX, enemyCY)
        app.enemies.append(newEnemy)
    else:
        newObstacle = Obstacle(enemyCX, enemyCY)
        app.obstacles.append(newObstacle)


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
        cx = random.randint(app.leftMostSpawn + 75, app.rightMostSpawn - 75)
        cy = random.randint(app.upMostSpawn + 75, app.lowMostSpawn - 75)
        for i in range(len(app.enemies)):
            currEnemy = app.enemies[i]
            hypot = math.hypot(currEnemy.width, currEnemy.height)
            if math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) + 30 < hypot:
                while math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) + 30 < hypot == True:
                    cx = random.randint(app.leftMostSpawn + 75, app.rightMostSpawn - 75)
                    cy = random.randint(app.upMostSpawn + 75, app.lowMostSpawn - 75)
        newEnemy = enemyType(cx, cy)
        app.enemies.append(newEnemy)
        if isinstance(newEnemy, EnemyMage) or isinstance(newEnemy, EnemyLynel):
            app.fireuserEnemies.append(newEnemy)

"""
Spawns the obstacles so the enemy won't get clipped into them
"""        
def spawnObstacles(app):
    finish = False
    numMistakes = 0
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
            if (math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < 130):
                while (math.dist([cx, cy], [currEnemy.cx, currEnemy.cy]) < 130):
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)  
        
        for obstacle in app.obstacles:
            hypotObstacle = math.hypot(obstacle.width, obstacle.height)
            if (math.dist([cx, cy], [obstacle.cx, obstacle.cy]) < 130):
                while (math.dist([cx, cy], [obstacle.cx, obstacle.cy]) < 130):
                    cx = random.randint(leftMostSpawn, rightMostSpawn)
                    cy = random.randint(upMostSpawn, lowMostSpawn)

        newObstacle = Obstacle(cx, cy)
        app.obstacles.append(newObstacle) 

"""
This checks after an enemy is defeated whether a level is cleared or not
"""
def levelClearer(app):
    if app.gameStarted:
        if (app.levelClear == True) and (len(app.enemies) == 0) and (app.level != 8):
            spawnKeyAndHealth(app)
            app.levelClear = False
    else:
        if (app.levelClear) and len(app.enemies) == 0:
            gameDone(app)

"""
This checks whether the game is done and spawns the triforce shard if it is
"""
def gameDone(app):
    if app.gameStarted:
        if (app.levelClear == True) and (len(app.enemies) == 0) and (app.level == 8):
            spawnTriforce(app)
            app.soundWin.play()
            app.levelClear = False
    elif app.loadDungeon:
        if app.levelClear == True and len(app.enemies) == 0:
            spawnTriforce(app)
            app.soundWin.play()
            app.levelClear = False

"""
This spawns the triforce shard after all the enemies are cleared on level 8
"""
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

"""
This spawns the keys and health after each of the levels are cleared
"""
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

"""
This is for the user to progress through the rooms
"""
def goNewRoom(app):
    if len(app.keys) == app.level and app.level == 1:
        if 180 <= app.user.cx <= 253 and 65 <= app.user.cy <= 85:
            app.user.cx = 215
            app.user.cy = 235
            app.level = 2
            app.positionLevel = 2
            spawnEnemies(app)
            app.obstacles = []
            app.hearts = []
            spawnObstacles(app)

    elif len(app.keys) == app.level and app.level == 2:
        if 65 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 390
            app.user.cy = 160
            app.level = 3
            app.positionLevel = 3
            spawnEnemies(app)
            app.obstacles = []
            app.hearts = []
            spawnObstacles(app)

    elif app.level == 4 and app.positionLevel == 2:
        if 140 <= app.user.cy <= 175 and 395 <= app.user.cx <= 410:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 4 
            app.obstacles = []
            app.hearts = []
            spawnEnemies(app)
            spawnObstacles(app)    
            app.level = 5    

    elif app.positionLevel == 2 and app.level == 5:
        if 189 <= app.user.cx <= 253 and 65 <= app.user.cy <= 85:
            app.user.cx = 215
            app.user.cy = 235
            app.positionLevel = 5
            spawnEnemies(app)
            spawnObstacles(app) 
            
    elif app.level == 5 and app.positionLevel == 5 and len(app.keys) == 5:
        if 140 <= app.user.cy <= 175 and 385 <= app.user.cx <= 410:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 6 
            app.obstacles = []
            app.hearts = []
            app.level = 6
            spawnEnemies(app)
            spawnObstacles(app) 

    elif app.positionLevel == 5 and len(app.keys) == 6:
         if 65 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 390
            app.user.cy = 160
            app.level = 7
            app.positionLevel = 7
            app.obstacles = []
            app.hearts = []
            spawnEnemies(app)
            spawnObstacles(app)

    elif app.positionLevel == 5 and app.level == 7 and len(app.keys) == 7:
        if 180 <= app.user.cx <= 255 and 65 <= app.user.cy <= 85:
            app.user.cx = 215
            app.user.cy = 235
            app.level = 8
            app.positionLevel = 8
            app.obstacles = []
            app.hearts = []
            spawnEnemies(app)
    else:
        goBackPrevious(app)

"""
This is for the user to go back to the previous level to progress onto the next level
"""
def goBackPrevious(app): 
    if len(app.keys) == app.level and app.level == 3:
        if 140 <= app.user.cy <= 170 and 385 <= app.user.cx <= 410:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 2 
            app.obstacles = []
            app.hearts = []
            app.level = 4

    elif app.positionLevel == 3 and app.level > 3:
         if 145 <= app.user.cy <= 165 and 385 <= app.user.cx <= 410:
            app.user.cx = 75
            app.user.cy = 160
            app.positionLevel = 2 
            app.obstacles = []
            app.hearts = []

    elif app.positionLevel == 4 and app.level > 4:
        if 65 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 400
            app.user.cy = 160
            app.positionLevel = 2
            app.obstacles = []
            app.hearts = []

    elif app.level == 6 and app.positionLevel == 6 and len(app.keys) == 6:
        if 65 <= app.user.cx < 85 and 135 <= app.user.cy <= 170:
            app.user.cx = 400
            app.user.cy = 160
            app.positionLevel = 5
            app.obstacles = []
            app.hearts = []

    elif app.positionLevel == 7 and app.level == 7 and (len(app.keys)) == 7:
        if 145 <= app.user.cy <= 170 and 385 <= app.user.cx <= 410:
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
    if app.gameStarted or app.loadDungeon:
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
            for fireuser in app.fireuserEnemies:
                if app.user.health > 0:
                    if fireuser.shouldNotShoot == False:
                        fireuser.createFireball(app.user)  
                        app.soundCreateFireball.play()

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

                dist = math.dist([enemy.cx, enemy.cy], [app.user.cx, app.user.cy])
                if app.user.hitCurr == False and enemy.hasMelee and dist < enemy.width and app.gameOver == False:
                    enemy.melee(app.user)
                    if app.user.health <= 0:
                        app.soundLinkDie.play()
                    else:
                        app.soundLinkHurt.play()

                if app.user.meleeDone == True and app.wait == False:
                    app.user.melee(enemy)
                    if enemy.health <= 0:
                        app.enemies.remove(enemy)
                        app.soundEnemyDie.play()
                        if len(app.enemies) == 0:
                            app.levelClear = True
                        if enemy in app.fireuserEnemies:
                            app.fireuserEnemies.remove(enemy) 
                    app.wait = True

        for fireball in app.user.fireballs:
            if isLegal(app, fireball) and app.gameOver == False:
                fireball.changeFireballPos()  
            else:
                app.user.fireballs.remove(fireball) 

        for fireuser in app.fireuserEnemies:
            for fireball in fireuser.fireballs:
                if isLegal(app, fireball) and app.gameOver == False:
                    fireball.changeFireballPos()
                else:
                    fireuser.fireballs.remove(fireball)

        levelClearer(app)
        gameDone(app)


"""
This checks if a movement for an npc or the user is legal, can also apply to the moves of each
"""
def isLegal(app, character):
    if isinstance(character, EnemyLightning) == False:
        if character.cx + character.cdx  > 410:
            return False
        if character.cy + character.cdy > 255:
            return False
        if character.cx + character.cdx < 65:
            return False
        if character.cy + character.cdy < 65:
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
                        app.soundEnemyDie.play()
                        if len(app.enemies) == 0:
                            app.levelClear = True
                        if enemy in app.fireuserEnemies:
                            app.fireuserEnemies.remove(enemy) 
                    return False
        else:
            if math.dist([character.cx, character.cy], [app.user.cx, app.user.cy]) < app.user.width:
                app.user.health -= 1
                if app.user.health <= 0:
                    app.soundLinkDie.play()
                else:
                    app.soundLinkHurt.play()
                return False       
    return True

"""
Loads the sounds for the moves, character, and enemies
"""
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

"""
Writes to a file given a 2d list
"""
def writeFile(app):
    df = pd.DataFrame(app.enemiesForFile)
    df.to_csv(app.dungeonName, index = None, header = None)

"""
Reads from a file given a txt file
"""
def readFile(app):
    with open(app.dungeonName, 'r') as csv_file:
        csv_reader =  csv.reader(csv_file)
        for line in csv_reader:
            app.allPositions.append(line)

"""
Above is all the methods relating to the game
-----------------------------------------------------------------------------------------------------------------------------
Below is the app key and mouse movements/presses
"""

"""
This basically gives all the moves of the character and allows for extra stuff during different phrases of the program.
I will add those phases later.
"""
def onKeyHold(app, keys):
    if app.gameStarted or app.loadDungeon:
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
                    app.soundCreateFireball.play()

            if 'g' in keys:
                if app.user.meleeDone == False and app.wait == False:
                    app.soundMelee.play()
                    app.user.meleeDone = True

            if 'k' in keys and app.gameStarted:
                if len(app.keyNotPicked) != 0 and math.dist([app.user.cx, app.user.cy], [app.keyNotPicked[0].cx, app.keyNotPicked[0].cy]) < app.user.width * 2:
                    app.keys.append(app.keyNotPicked[0])
                    app.soundOpenDoor.play()
                    app.keyNotPicked[0].taken = True
                    app.keyNotPicked = []

            if 'space' in keys and app.gameStarted:
                goNewRoom(app)

            if 'h' in keys and app.hearts != [] and app.gameStarted:
                if math.dist([app.user.cx, app.user.cy], [app.hearts[0].cx, app.hearts[0].cy]) < app.user.width * 2:
                    app.user.health = 5
                    app.soundGetHeart.play()
                    app.hearts = []

            if 't' in keys and app.triforcePieces != []:
                if math.dist([app.user.cx, app.user.cy], [app.triforcePieces[0].cx, app.triforcePieces[0].cy]) < app.user.width * 2:
                    app.triforcePieces = []
                    app.gameWon = True
        
        elif app.gameOver and 'r' in keys and app.gameStarted:
            startAdventure(app)
        
        elif app.gameOver and 'r' in keys and app.loadDungeon:
            startDungeon(app)

"""
Gives user the ability to type and enter a filename
"""
def onKeyPress(app, key):
    if app.acceptDungeon or app.getDungeonName:
        if key.isalpha() and len(key) == 1:
            app.dungeonName += key
        elif key.isdigit() and len(key) == 1:
            app.dungeonName += key
        elif 'backspace' == key:
            app.dungeonName = app.dungeonName[:len(app.dungeonName) - 1]
        elif 'enter' == key:
            if app.acceptDungeon:
                writeFile(app)
                app.acceptDungeon = False
                app.createDungeonRoom = False
                app.dungeonName = ""
            elif app.getDungeonName:
                readFile(app)
                startDungeon(app)
                app.loadDungeon = True
                app.getDungeonName = False
                app.dungeonName = ""

    elif app.help == True:
        if key == 'h':
            app.help = False

    elif app.goToDungeonScreen == False and app.createDungeonRoom == False and app.loadDungeon == False and app.gameStarted == False:
        if key == 'h':
            app.help = True
                
"""
When the key is released the movement in the direction of that key is 0 now.
"""
def onKeyRelease(app, key):
    if app.gameStarted or app.loadDungeon:
        if key == 'a':
            app.user.cdx = 0
        if key == 's':
            app.user.cdy = 0
        if key == 'd':
            app.user.cdx = 0
        if key == 'w':
            app.user.cdy = 0

"""
Checks if the user is hovering over a button
"""
def onMouseMove(app, cx, cy):
    if app.gameStarted == False and app.goToDungeonScreen == False:
        app.cx = cx
        app.cy = cy
        if (152 <= app.cx <= 352) and (150 <= app.cy <= 200):
            app.changeButtonStart = True
        else:
            app.changeButtonStart = False

        if (152 <= app.cx <= 352) and (100 <= app.cy <= 150):
            app.changeButtonRoom = True
        else:
            app.changeButtonRoom = False

    if app.createDungeonRoom:
        app.cx = cx
        app.cy = cy
        if 252.5 <= cx <= 352.5 and 373.5 <= cy <= 428.5:
            app.drawOtherVer = True
        else:
            app.drawOtherVer = False
            
    if app.goToDungeonScreen:
        app.cx = cx
        app.cy = cy
        if (152 <= app.cx <= 352) and (150 <= app.cy <= 200):
            app.changeButtonCreate = True
        else:
            app.changeButtonCreate = False

        if (152 <= app.cx <= 352) and (100 <= app.cy <= 150):
            app.changeButtonLoad = True
        else:
            app.changeButtonLoad = False


"""
Checks if the user is pressing a button
"""
def onMousePress(app, mouseX, mouseY):
    if app.gameStarted == False and app.createDungeonRoom == False and app.goToDungeonScreen == False and app.loadDungeon == False and app.getDungeonName == False and app.help == False:
        if (152 <= mouseX <= 352) and (150 <= mouseY <= 200):
            startAdventure(app)
            app.gameStarted = True
        elif (152 <= mouseX <= 352) and (100 <= mouseY <= 150):
            app.goToDungeonScreen = True
        else:
            app.changeButtonStart = False
            app.changeButtonRoom = False
    
    elif app.goToDungeonScreen:
        if (152 <= mouseX <= 352) and (150 <= mouseY <= 200):
            createRoom(app)
            app.goToDungeonScreen = False
            app.createDungeonRoom = True
        elif (152 <= mouseX <= 352) and (100 <= mouseY <= 150):
            app.goToDungeonScreen = False
            app.getDungeonName = True
        else:
            app.changeButtonLoad = False
            app.changeButtonCreate = False

    elif app.createDungeonRoom:
        if 510 <= mouseX <= 510 + app.enemy1Width and 80 <= mouseY <= 80 + app.enemy1Height:
            app.dragEnemy = True
            app.dragger = app.enemy1
            app.dragCoordinates = None
        elif 560 <= mouseX <= 560 + app.enemy2Width and 80 <= mouseY <= 80 + app.enemy2Height:
            app.dragEnemy = True
            app.dragger = app.enemy2
            app.dragCoordinates = None
        elif 510 <= mouseX <= 510 + app.enemy3Width and 160 <= mouseY <= 160 + app.enemy3Height:
            app.dragEnemy = True
            app.dragger = app.enemy3
            app.dragCoordinates = None
        elif 560 <= mouseX <= 560 + app.enemy4Width and 160 <= mouseY <= 160 + app.enemy4Height:
            app.dragEnemy = True
            app.dragger = app.enemy4
            app.dragCoordinates = None
        elif 510 <= mouseX <= 510 + app.enemy5Width and 240 <= mouseY <= 240 + app.enemy5Height:
            app.dragEnemy = True
            app.dragger = app.enemy5
            app.dragCoordinates = None
        elif 560 <= mouseX <= 560 + app.enemy6Width and 240 <= mouseY <= 240 + app.enemy6Height:
            app.dragEnemy = True
            app.dragger = app.enemy6
            app.dragCoordinates = None
        elif 535 <= mouseX <= 535 + app.obstacleWidth and 310 <= mouseY <= 310 + app.obstacleHeight:
            app.dragEnemy = True
            app.dragger = app.obstacleImg
            app.dragCoordinates = None
        elif 252.5 <= mouseX <= 352.5 and 373.5 <= mouseY <= 428.5:
            app.width = 505
            app.height = 351
            app.acceptDungeon = True
        else:
            app.dragEnemy = False

"""
User can drag the enemies they want into the dungeon room
"""        
def onMouseDrag(app, cx, cy):
    if app.createDungeonRoom:
        app.dragCoordinates = (cx, cy)

"""
This places the enemy into the dungeon room and also appends the two lists for the enemies that will need to be drawn currently 
and the enemies that will be placed into the dungeon file
"""
def onMouseRelease(app, cx, cy):
    if app.createDungeonRoom and app.dragEnemy:
        app.enemiesNeedDraw.append([app.dragger, cx, cy])
        if app.dragger == app.enemy1:
            app.enemiesForFile.append(["mage", cx, cy])
        elif app.dragger == app.enemy2:
            app.enemiesForFile.append(["knight", cx, cy])
        elif app.dragger == app.enemy3:
            app.enemiesForFile.append(["lightning", cx, cy])
        elif app.dragger == app.enemy4:
            app.enemiesForFile.append(["mummy", cx, cy])
        elif app.dragger == app.enemy5:
            app.enemiesForFile.append(["slime", cx, cy])
        elif app.dragger == app.enemy6:
            app.enemiesForFile.append(["lynel", cx, cy])
        elif app.dragger == app.obstacleImg:
            app.enemiesForFile.append(["obstacle", cx, cy])
        app.dragEnemy = False

"""
Above is the events of key and mouse
----------------------------------------------------------------------------------------------------
Below is the drawing for the canvas
"""

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

"""
This draws the starting screen for the user
"""
def drawStartingScreen(app):
    image = Image.open('images/mainscreen.png')
    startImage = CMUImage(image.crop((0, 0, 505, 351)))
    drawImage(startImage, 0, 0)
    drawLabel("Zeldaish Quest", 258, 60, size = 60, font = 'The Wild Breath of Zelda', fill = 'green', bold = True)

"""
This is the button that shows up when the user is not hovering over start button
"""
def drawStartGameOne(app):
    drawRect(252, 185, 200, 50, fill = "black", align = "center")
    drawRect(252, 185, 195, 45, fill = "green", align = "center")
    drawLabel("Start Game", 252, 185, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

"""
This is the button that shows up when the user is hovering over the start button
"""
def drawStartGameTwo(app):
    drawRect(252, 185, 200, 50, fill = "white", align = "center")
    drawRect(252, 185, 195, 45, fill = "green", align = "center")
    drawLabel("Start Game", 252, 185, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

"""
This is the when the user hovers over the button on the start screen for room maker 
"""
def drawRoomMakerButton2(app):
    drawRect(252, 125, 200, 50, fill = "white", align = "center")
    drawRect(252, 125, 195, 45, fill = "green", align = "center")
    drawLabel("Room Maker", 252, 125, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

"""
This is a button which draws the help for users to get the help screen
"""
def drawHelpLabel(app):
    drawRect(425, 280, 150, 55, fill = "black", align = "center")
    drawRect(425, 280, 145, 50, fill = "green", align = "center")
    drawLabel("Press h to go to help", 425, 280, align = 'center', font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 15)


"""
This is when the user doesnt hover over the room maker button on the start screen
"""
def drawRoomMakerButton(app):
    drawRect(252, 125, 200, 50, fill = "black", align = "center")
    drawRect(252, 125, 195, 45, fill = "green", align = "center")
    drawLabel("Room Maker", 252, 125, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)
"""
This draws the triforce when the start game button is hovered over(Not mine)
"""
def drawSierpinskiTriangle(app, level, x, y, size):
    # (x,y) is the lower-left corner of the triangle
    # size is the length of a side
    # Need a bit of trig to calculate the top point
    if level == 0:
        topY = y - (size**2 - (size/2)**2)**0.5
        drawPolygon(x, y, x+size, y, x+size/2, topY, fill='yellow')
    else:
        # Bottom-left triangle
        drawSierpinskiTriangle(app, level-1, x, y, size/2)
        # Bottom-right triangle
        drawSierpinskiTriangle(app, level-1, x+size/2, y, size/2)
        # Top triangle
        midY = y - ((size/2)**2 - (size/4)**2)**0.5
        drawSierpinskiTriangle(app, level-1, x+size/4, midY, size/2)

"""
If the user beats the game then the game won screen will be drawn
"""
def drawGameWon(app):
    drawRect(0, 0, 505, 351, fill = 'yellow')
    image = Image.open('images/endscreen.png')
    endImage = CMUImage(image.crop((0, 0, 505, 351)))
    drawImage(endImage, 0, 0)
    drawLabel("You Won", 258, 290, size = 60, font = 'The Wild Breath of Zelda', fill = 'green')
  
"""
This draws the game over screen when the user has 0 health.
"""
def drawGameOver(app):
    drawRect(0, 0, 516, 355, fill = "black", opacity = app.gameOverCounter)
    drawLabel("You Died", 258, 178, size = 60, font = 'The Wild Breath of Zelda', fill = 'red', opacity = app.gameOverCounter, bold = True)
    drawRect(252, 250, 200, 50, fill = "white", align = "center", opacity = app.gameOverCounter)
    drawRect(252, 250, 195, 45, fill = "navy", align = "center", opacity = app.gameOverCounter)
    drawLabel("Press r to restart", 252, 250, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 25, opacity = app.gameOverCounter)

"""
Draws the dungeon doors for the build dungeon 
"""
def dungeonCreatorDoors(app):
    block1 = CMUImage(app.tileset.crop((1630, 88, 1695, 153)))
    block2 = CMUImage(app.tileset.crop((1630, 221, 1695, 286)))
    block3 = CMUImage(app.tileset.crop((1630, 154, 1694, 218)))
    block4 = CMUImage(app.tileset.crop((1630, 22, 1693, 86)))
    drawImage(block1, -3, 144)
    drawImage(block2, 222, 289)
    drawImage(block3, 444, 144)
    drawImage(block4, 221, 0)

"""
Draws the enemy images which the user will interact with on the build dungeon
"""
def drawEnemiesIdle(app):
    drawRect(505, 0, 100, 451, fill = "black")
    drawLabel("Enemies:", 555, 50, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 20)
    drawImage(app.enemy1, 510, 80)
    drawImage(app.enemy2, 560, 80)
    drawImage(app.enemy3, 510, 160)
    drawImage(app.enemy4, 560, 160)
    drawImage(app.enemy5, 510, 240)
    drawImage(app.enemy6, 560, 240)
    drawImage(app.obstacleImg, 535, 310)


"""
Places enemy on cx and cy of mouse when user is trying to get enemy for a dungeon
"""
def dragDrawEnemy(app, enemy, cx, cy):
    if app.dragEnemy:
        drawImage(enemy, cx, cy, align = 'center')

"""
Places enemy on cx and cy of the release of mouse when user is trying to get an enemy for the dungeon
"""
def drawReleaseEnemy(app):
    if app.dragEnemy == False and app.timeToDraw == True:
        enemyDrag = app.dragger
        releaseCx, releaseCy = app.releaseCoordinates
        drawImage(enemyDrag, releaseCx, releaseCy, align = 'center')

"""
This draws every enemy on the board that the user has placed
"""
def drawAllEnemies(app):
    for enemy in app.enemiesNeedDraw:
            drawImage(enemy[0], enemy[1], enemy[2], align = 'center')

"""
This draws the accept dungeon button on the create dungeon screen
"""
def drawAcceptButton(app):
    drawRect(0, 351, 605, 100, fill = "navy")
    drawRect(302.5, 401, 110, 55, fill = "black", align = "center")
    drawRect(302.5, 401, 100, 50, fill = "green", align = "center")
    drawLabel("Create Dungeon", 302.5, 401, align = 'center', font = "The Wild Breath of Zelda", fill = "Yellow", bold = True, size = 15)

"""
This draws the accept dungeon button on the create dungeon screen when the user hovers over it
"""
def drawAcceptButton2(app):
    drawRect(0, 351, 605, 100, fill = "navy")
    drawRect(302.5, 401, 110, 55, fill = "white", align = "center")
    drawRect(302.5, 401, 100, 50, fill = "green", align = "center")
    drawLabel("Create Dungeon", 302.5, 401, align = 'center', font = "The Wild Breath of Zelda", fill = "Yellow", bold = True, size = 15)

"""
This is for when the user is entering a name for reading or writing a file
"""
def drawDungeonNameScreen(app):
    loadImgNotMade = Image.open('images/loadingImage.jpg')
    loadImg = CMUImage(loadImgNotMade.crop((0, 0, 505, 351)))
    drawImage(loadImg, 0, 0)
    drawLabel("Loading...", 100, 40, fill = "white", font = "The Wild Breath of Zelda", bold = True, size = 50)
    drawRect(252.5, 175.5, 250, 55, fill = "white", align = "center")
    drawRect(252.5, 175.5, 240, 50, fill = "green", align = "center")
    drawLabel('Filename: ', 180, 175.5, align = 'center', font = "The Wild Breath of Zelda", fill = "Yellow", bold = True, size = 15)
    drawLabel(app.dungeonName, 275, 175.5, align = 'center', font = "The Wild Breath of Zelda", fill = "Yellow", bold = True, size = 15)

"""
This draws the button for create room on idle
"""
def drawCreateYourRoomButton1(app):
    drawRect(252, 185, 200, 50, fill = "black", align = "center")
    drawRect(252, 185, 195, 45, fill = "green", align = "center")
    drawLabel("Create Room", 252, 185, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

"""
This draws the button for create room when the user hovers over it
"""
def drawCreateYourRoomButton2(app):
    drawRect(252, 185, 200, 50, fill = "white", align = "center")
    drawRect(252, 185, 195, 45, fill = "green", align = "center")
    drawLabel("Create Room", 252, 185, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

"""
This draws the button for load room when on idle
"""
def drawLoadYourRoomButton1(app):
    drawRect(252, 125, 200, 50, fill = "black", align = "center")
    drawRect(252, 125, 195, 45, fill = "green", align = "center")
    drawLabel("Load Room", 252, 125, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

"""
This draws the button for load when when the user hovers over it
"""
def drawLoadYourRoomButton2(app):
    drawRect(252, 125, 200, 50, fill = "white", align = "center")
    drawRect(252, 125, 195, 45, fill = "green", align = "center")
    drawLabel("Load Room", 252, 125, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 30)

def drawHelpScreen(app):
    loadImgNotMade = Image.open('images/loadingImage.jpg')
    loadImg = CMUImage(loadImgNotMade.crop((0, 0, 505, 351)))
    drawImage(loadImg, 0, 0)
    for i in range(5):
        drawRect(150, 50 + i*60, 270, 55, fill = "white", align = "center")
        drawRect(150, 50 + i*60, 265, 50, fill = "green", align = "center")
    drawLabel("To walk in a dungeon use the keys wasd.", 150, 50, align = "center", font = 'The Wild Breath of Zelda', fill = 'Yellow', bold = True, size = 15)
    drawLabel("To shoot a fireball, walk in a direction and press f.", 20, 110, font = "The Wild Breath of Zelda", fill = "yellow", bold = True, size = 13, align = "left")
    drawLabel("To melee, press m", 150, 170, font = "The Wild Breath of Zelda", fill = "yellow", bold = True, size = 13)
    drawLabel("Press k,h, or t to grab a heart/key/triforce.", 150, 230, font = "The Wild Breath of Zelda", fill = "yellow", bold = True, size = 13)
    drawLabel("To go to the next dungeon", 150, 280, font = "The Wild Breath of Zelda", fill = "yellow", bold = True, size = 13)
    drawLabel("go to the newly opened door and press space.", 150, 300, font = "The Wild Breath of Zelda", fill = "yellow", bold = True, size = 13)
    
def redrawAll(app):
    if app.gameStarted:
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

        for fireuser in app.fireuserEnemies:
            for fireball in fireuser.fireballs:
                fireball.drawFireball()

        for obstacle in app.obstacles:
            obstacle.drawObstacle()
        
        for piece in app.triforcePieces:
            piece.drawTriforcePiece()

        if app.gameOver:
            drawGameOver(app)

        if app.gameWon:
            drawGameWon(app)
            
    elif app.loadDungeon:
        drawExterior(app)
        drawBackground(app)
        dungeonCreatorDoors(app)
        drawHealthBar(app)
        app.user.drawCharacter()
        for fireball in app.user.fireballs:
            fireball.drawFireball()

        for heart in app.hearts:
            heart.drawHeart()

        for enemy in app.enemies:
            enemy.drawEnemy()

        for fireuser in app.fireuserEnemies:
            for fireball in fireuser.fireballs:
                fireball.drawFireball()

        for obstacle in app.obstacles:
            obstacle.drawObstacle()
        
        for piece in app.triforcePieces:
            piece.drawTriforcePiece()

        if app.gameOver:
            drawGameOver(app)

        if app.gameWon:
            drawGameWon(app)

    elif app.goToDungeonScreen:
        drawStartingScreen(app)
        if app.changeButtonLoad:
            drawLoadYourRoomButton2(app)
            drawSierpinskiTriangle(app, 1, 210, 305, 100)
        else:
            drawLoadYourRoomButton1(app)
        if app.changeButtonCreate:
            drawCreateYourRoomButton2(app)
            drawSierpinskiTriangle(app, 1, 210, 305, 100)
        else:
            drawCreateYourRoomButton1(app)

    elif app.acceptDungeon or app.getDungeonName:
        drawDungeonNameScreen(app)

    elif app.createDungeonRoom:
        drawExterior(app)
        drawBackground(app)
        dungeonCreatorDoors(app)
        drawEnemiesIdle(app)
        if app.drawOtherVer:
            drawAcceptButton2(app)
        else:
            drawAcceptButton(app)
        if app.dragEnemy and app.dragCoordinates != None:
            enemyDrag = app.dragger
            dragCx, dragCy  = app.dragCoordinates
            dragDrawEnemy(app, enemyDrag, dragCx, dragCy)
        drawAllEnemies(app)

    elif app.help:
        drawHelpScreen(app)

    else:
        drawStartingScreen(app)
        drawHelpLabel(app)
        if app.changeButtonRoom:
            drawRoomMakerButton2(app)
            drawSierpinskiTriangle(app, 1, 210, 305, 100)
        else:
            drawRoomMakerButton(app)
        if app.changeButtonStart:
            drawStartGameTwo(app)
            drawSierpinskiTriangle(app, 1, 210, 305, 100)
        else:
            drawStartGameOne(app)

def main():
    runApp(width = app.width, height = app.height)

main()