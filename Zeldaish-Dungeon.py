from cmu_graphics import *

"""
This class is a move for the user. The move is meant to be a 1x1 red block which goes in the direction of where 
the user is facing and is meant to stop at where the block reaches the edges of the screen or where the block hits
an enemy.
"""
class fireball():

    def __init__(self, direction, row, col):
        self.direction = direction
        self.row = row
        self.col = col
        self.projColor = "red"
        self.projPiece = [[True]]
    

"""
onAppStart sets the amount of rows and cols for the board, it also gets the left of the border of the board in pixels
and gets the top edge of the border in pixels to set the border in place. It also sets the boardWidth and boardHeight of the board 
in pixels. It sets the board in a 2d list filled currently with None values. As of now we also have the loadCharacter(app).
"""
def onAppStart(app):
    app.stepsPerSecond = 2
    app.rows = 15
    app.cols = 15
    app.boardLeft = 25
    app.boardTop = 50
    app.boardWidth = 450
    app.boardHeight = 400
    app.cellBorderWidth = 2
    app.direction = None
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadCharacter(app)

"""
This basically gives all the moves of the character and allows for extra stuff during different phrases of the program.
I will add those phases later.
"""
def onKeyPress(app, key):
    if key == 'left':
        movePiece(app, -1, 0)
        app.direction = "left"
    elif key == 'down':
        movePiece(app, 0, 1)
        app.direction = "down"
    elif key == 'right':
        movePiece(app, 1, 0)
        app.direction = "right"
    elif key == 'up':
        movePiece(app, 0, -1)
        app.direction = "up"
    elif key == 'f':
        app.projFire = True

"""
Changes the row and column of the character based on the key press and
checks if it interferes with the border edges.
"""
def movePiece(app, dcol, drow):
    app.pieceRow += drow
    app.pieceCol += dcol
    if pieceIsLegal(app, app.piece, app.pieceRow, app.pieceCol):
        return True
    else:
        app.pieceRow -= drow
        app.pieceCol -= dcol
        return False

"""
This checks if the piece given is legally within the board, or if it interacts with another block.
"""
def pieceIsLegal(app, piece, row, col):
    if row + len(piece) > app.rows:
        return False
    if col + len(piece[0]) > app.cols:
        return False
    if col < 0:
        return False
    if row < 0:
        return False
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if app.board[row + i][col + j] != None and app.piece[i][j] == True:
                return False
    return True

"""
Gets each cell width from the board width (in pixels) divided by the total columns.
Gets each cell height from the board height (in pixels) divided by the total rows.
"""
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

"""
Makes each cell size from the getCellSize(app) function.
It will get the cellLeft from the left edge of the board in addition with the column we are on times the cell width.
It will get the cellTop from the top edge of the board in addition with the row of the board we are on times each cell height.
"""
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

"""
Loads the character with an initial row, column, color, and the 2d list of the piece. (As of right now it is just a 1x1 piece, may change later)
"""
def loadCharacter(app):
    app.pieceRow = 7
    app.pieceCol = 7
    app.pieceColor = 'green'
    app.piece = [[True]]

"""
Draw the board outline (with double-thickness)
"""
def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

"""
Draws each cell on the board using the getCellLeftTop function given the row and col the drawCell is given. It then uses the drawRect
function to draw the 'cell'/ rectangle.
"""
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

"Draws the boarder using the drawCell function and going through each row and column."    
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

"Draws each piece/character on the board."   
def drawPiece(app):
    numRows = len(app.piece)
    numCols = len(app.piece[0])
    for i in range(numRows):
        for j in range(numCols):
            if app.piece[i][j] == True:
                drawCell(app, app.pieceRow + i, app.pieceCol + j, app.pieceColor)  

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)  
    drawPiece(app)

def main():
    runApp(width = 500, height = 500)

main()