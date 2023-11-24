from cmu_graphics import *
import math


"""
This is the main projectile that the user uses, used when 'f' is pressed
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


"""
This is the main character class
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
    
class EnemyDog:
    def __init__(self):
        self.health = 3
        self.cx = None
        self.cy = None
        self.cdx = 0
        self.cdy = 0
        self.height = 20
        self.width = 20
    
    def drawCharacter(self):
        drawRect(self.cx, self.cy, self.width, self.height, fill = "black", align = "center")

    def changePosition(self):
        self.cx += self.cdx
        self.cy += self.cdy






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

"""
This keeps track of all timed events and movement of main character, npcs, and 
projectiles
"""
def onStep(app):
    app.timerCounter += 1
    if app.timerCounter % 15 == 0:
        app.timerCounter = 0
        app.fireballShot = False

    if isLegal(app, app.user):
        app.user.changePosition()

    for fireball in app.user.fireballs:
        if isLegal(app, fireball):
            fireball.changeFireballPos()  
        else:
            app.user.fireballs.remove(fireball) 

"""
This checks if a move for an npc or the user is legal, can also apply to moves
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
  
  
def redrawAll(app):
    drawBoardBorder(app)
    drawLabel(f"{app.user.cx} cx", 20, 10) 
    app.user.drawCharacter()
    for fireball in app.user.fireballs:
        fireball.drawFireball()

def main():
    runApp(width = 500, height = 500)

main()