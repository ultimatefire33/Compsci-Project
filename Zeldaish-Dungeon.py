from cmu_graphics import *

"""
onAppStart sets the amount of rows and cols for the board, it also gets the left of the border of the board in pixels
and gets the top edge of the border in pixels to set the border in place. It also sets the boardWidth and boardHeight of the board 
in pixels. It sets the board in a 2d list filled currently with None values. As of now we also have the loadCharacter(app).
"""
def onAppStart(app):
    app.stepsPerSecond = 2
    app.boardLeft = 25
    app.boardTop = 50
    app.boardWidth = 450
    app.boardHeight = 400
    app.direction = None

"""
This basically gives all the moves of the character and allows for extra stuff during different phrases of the program.
I will add those phases later.
"""
def onKeyPress(app, key):
    pass


"""
This checks if the piece given is legally within the board, or if it interacts with another block.
"""
def pieceIsLegal(app, piece, row, col):
    pass

"""
Draw the board outline (with double-thickness)
"""
def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black')
  
def redrawAll(app):
    drawBoardBorder(app)  

def main():
    runApp(width = 500, height = 500)

main()