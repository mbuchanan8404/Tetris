# Matthew Buchanan
# Programming Languages
# Homework 8
# Uses starter code from https://www.cs.cmu.edu/~112/notes/notes-tetris/2_1_DesignOverview.html

# Updated Animation Starter Code

from tkinter import *
import random
import copy

# Seven "standard" pieces (tetrominoes)

iPiece = [
    [True, True, True, True]
]

jPiece = [
    [True, False, False],
    [True, True, True]
]

lPiece = [
    [False, False, True],
    [True, True, True]
]

oPiece = [
    [True, True],
    [True, True]
]

sPiece = [
    [False, True, True],
    [True, True, False]
]

tPiece = [
    [False, True, False],
    [True, True, True]
]

zPiece = [
    [True, True, False],
    [False, True, True]
]


####################################
# customize these functions
####################################

def init(data):
    tetrisPieces = [iPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    data.tetrisPieces = tetrisPieces
    data.tetrisPiecesColors = tetrisPieceColors
    data.emptyColor = "blue"
    data.rows, data.cols, data.cellSize, data.margin = gameDimensions()
    board = []
    for i in range(0, data.rows):
        new = []
        for j in range(0, data.cols):
            new.append("blue")
        board.append(new)
    data.board = board

    data.isGameOver = FALSE
    data.score = 0
    newFallingPiece(data)


def mousePressed(event, data):
    # use event.x and event.y
    pass


def keyPressed(canvas, event, data):
    if (event.char == 'r'):
        init(data)
    if (data.isGameOver == TRUE):
        return
    if (event.char == 's'):
        moveFallingPiece(canvas, data, 1, 0)
    elif (event.char == 'a'):
        moveFallingPiece(canvas, data, 0, -1)
    elif (event.char == 'd'):
        moveFallingPiece(canvas, data, 0, 1)
    elif (event.char == 'w'):
        rotateFallingPiece(canvas, data)


def drawBoard(canvas, data):
    for i in range(0, data.rows):
        for j in range(0, data.cols):
            drawCell(canvas, data, i, j, data.board[i][j])


def drawCell(canvas, data, y, x, color):
    x1 = x * data.cellSize + data.margin
    y1 = y * data.cellSize + data.margin
    x2 = (x + 1) * data.cellSize + data.margin
    y2 = (y + 1) * data.cellSize + data.margin
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)


def timerFired(canvas, data):
    if (data.isGameOver == TRUE):
        return
    if (fallingPieceIsLegal(canvas, data, 0, 0) == FALSE):
        data.isGameOver = TRUE
        temp = str(data.score) + "\nGAME OVER"
        data.score = temp;
    elif (moveFallingPiece(canvas, data, +1, 0) == FALSE):
        placeFallingPiece(canvas, data)
        removeFullRows(canvas, data)
        newFallingPiece(data)  # here


def placeFallingPiece(canvas, data):
    for i in range(0, len(data.fallingPiece)):
        for j in range(0, len(data.fallingPiece[i])):
            if (data.fallingPiece[i][j] == TRUE):
                data.board[data.fallingPieceRow + i][data.fallingPieceCol + j] = data.fallingPieceColor


def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)


def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    randomIndex = random.randint(0, len(data.tetrisPiecesColors) - 1)
    data.fallingPieceColor = data.tetrisPiecesColors[randomIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = (data.cols // 2) - (len(data.fallingPiece[0]) // 2)


def drawFallingPiece(canvas, data):
    for i in range(0, len(data.fallingPiece)):
        for j in range(0, len(data.fallingPiece[i])):
            if (data.fallingPiece[i][j] == TRUE):
                drawCell(canvas, data, data.fallingPieceRow + i, data.fallingPieceCol + j, data.fallingPieceColor)


def moveFallingPiece(canvas, data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    return fallingPieceIsLegal(canvas, data, drow, dcol)


def fallingPieceIsLegal(canvas, data, drow, dcol):
    if ((data.fallingPieceRow + len(data.fallingPiece) > data.rows) |
            (data.fallingPieceCol < 0)):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return FALSE
    for i in range(0, len(data.fallingPiece)):
        if ((data.fallingPieceCol + len(data.fallingPiece[i])) > data.cols):
            data.fallingPieceRow -= drow
            data.fallingPieceCol -= dcol
            return FALSE
    for i in range(0, len(data.fallingPiece)):
        for j in range(0, len(data.fallingPiece[0])):
            if (data.fallingPiece[i][j] == TRUE and (
                    data.board[data.fallingPieceRow + i][data.fallingPieceCol + j] != "blue")):
                data.fallingPieceRow -= drow
                data.fallingPieceCol -= dcol
                return FALSE
    return TRUE


def rotateFallingPiece(canvas, data):
    temp = data.fallingPiece
    oldNumRows = len(data.fallingPiece)
    oldNumCols = len(data.fallingPiece[0])
    oldFPC = data.fallingPieceCol
    oldFPR = data.fallingPieceRow
    data.fallingPiece = list(zip(*data.fallingPiece[::-1]))
    data.fallingPiece = list(zip(*data.fallingPiece[::-1]))
    data.fallingPiece = list(zip(*data.fallingPiece[::-1]))
    data.fallingPieceRow = oldFPR + oldNumRows // 2 - len(data.fallingPiece) // 2
    data.fallingPieceCol = oldFPC + oldNumCols // 2 - len(data.fallingPiece[0]) // 2
    if (data.fallingPieceRow < 0):
        data.fallingPieceRow = 0
    if (fallingPieceIsLegal(canvas, data, 0, 0)):
        redrawAll(canvas, data)
    else:
        data.fallingPiece = temp
        data.fallingPieceCol = oldFPC
        data.fallingPieceRow = oldFPR


def removeFullRows(canvas, data):
    totalRowsRemoved = 0
    for i in range(0, data.rows):
        rowFilled = i
        for j in range(0, data.cols):
            if (data.board[i][j] == "blue"):
                rowFilled = -1
                break
        if (rowFilled >= 0):
            for k in range(rowFilled, 1, -1):
                data.board[k] = copy.copy(data.board[k - 1])
            for k in range(0, len(data.board[0])):
                data.board[0][k] = "blue"
            totalRowsRemoved += 1
    data.score += totalRowsRemoved ** 2


def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 25
    margin = 32
    return rows, cols, cellSize, margin


def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    x = (cols * cellSize) + (2 * margin)
    y = (rows * cellSize) + (2 * margin)
    run(x, y)


####################################
# use the run function as-is
####################################
def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height, fill='purple', width=0)
        canvas.create_text(((data.cols * data.cellSize) + (2 * data.margin)) // 2, data.margin // 2, fill="darkblue",
                           font="Times 10 italic bold", text="Score: " + str(data.score), justify='center')
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(canvas, event, data)
        redrawAll(canvas, data)
        # redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        redrawAllWrapper(canvas, data)
        timerFired(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object):
        pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 250  # milliseconds
    root = Tk()
    root.resizable(width=False, height=False)  # prevents resizing window
    init(data)

    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


playTetris()
