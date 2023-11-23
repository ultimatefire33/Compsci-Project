from cmu_graphics import *

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

    def drawCharacter(self):
        drawRect(self.cx, self.cy, self.width, self.height, fill = "blue", align = "center")

    def changePosition(self):
        self.cx += self.cdx
        self.cy += self.cdy

"""
onAppStart sets the amount of rows and cols for the board, it also gets the left of the border of the board in pixels
and gets the top edge of the border in pixels to set the border in place. It also sets the boardWidth and boardHeight of the board 
in pixels. It sets the board in a 2d list filled currently with None values. As of now we also have the loadCharacter(app).
"""
def onAppStart(app):
    app.stepsPerSecond = 30
    app.boardLeft = 25
    app.boardTop = 50
    app.boardWidth = 450
    app.boardHeight = 400
    app.borderWidth = 5
    app.direction = None
    app.user = Character()

"""
This keeps track of all timed events and movement of main character and npcs
"""
def onStep(app):
    if isLegal(app, app.user):
        app.user.changePosition()

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
    if len(keys) == 2:
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

def main():
    runApp(width = 500, height = 500)

main()