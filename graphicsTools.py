from enum import Enum
from pyglet.shapes import Rectangle, Line
from pixelMathTools import *

class OpacityType(Enum):
    SOLID = 0
    CONSTANT = 1
    DATA_MATCH = 2
    COLOR_MATCH = 3
    DEFINE_TRANSPARENT = 4

##def drawGrid(rows, columns, gridWidth, gridHeight, \
##             marginSize, cellColor, marginColor, marginVisible=True):
##    ##calculating cells size and coordinates
##    width, height = getCellSize(gridWidth, gridHeight, rows, columns, marginSize)
##    cellsPositions = getCellsPositions(gridWidth, gridHeight, rows, columns, marginSize)
##    sprites = []
##    ## creating cell sprites
##    for i, position in enumerate(cellsPositions):
##        x, y = position
##        sprites.append(Rectangle(x, y, width, height, color=cellColor))
##    ## creating margin sprites
##    if marginVisible:
##        #if margins are enabled, calculate their positions and add them to the list
##        vertMarginPositions = getVerticalMarginsCentered(gridHeight, rows, marginSize)
##        horizMarginPositions = getHorizontalMarginsCentered(gridWidth, columns, marginSize)
##        for x, y in  horizMarginPositions: #horizontal
##            sprites.append(Line(x, y, gridWidth, y, thickness=marginSize,\
##                                color=marginColor))
##        for x, y in vertMarginPositions: #vertical
##            sprites.append(Line(x, y, x, gridHeight, thickness=marginSize,\
##                                color=marginColor))
##    return sprites
##
##

def drawMatrix(matrix, dataColorMatch, gridWidth, gridHeight, \
               marginSize, marginColor, opacityType=OpacityType.SOLID,\
               opacityData=None, marginVisible=True):
    
    rows = len(matrix)
    columns = len(matrix[0])
    
    ##calculating cells size and coordinates
    width, height = getCellSize(gridWidth, gridHeight, rows, columns, marginSize)
    cellsPositions = getCellsPositions(gridWidth, gridHeight, rows, columns, marginSize)

    # preparing empty list and defining opacity function based on opacity type
    sprites = []
    
    match opacityType:
        case OpacityType.SOLID:
            opacity = lambda x: 255
        case OpacityType.CONSTANT:
            opacity = lambda x: int(opacityData * 255)
        case OpacityType.DATA_MATCH:
            opacity = lambda x: int(opacityData[x] * 255)
        case OpacityType.COLOR_MATCH:
            opacity = lambda x: int(opacityData[dataColorMatch[x]] * 255)
        case OpacityType.DEFINE_TRANSPARENT:
            opacity = lambda x: int((opacityData[x] if x in opacityData else 1) * 255)
        case _: raise ValueError(f"opacity type is not specified or given value ({opacityType}) does not support")     
    
    unpackedMatrix = [value for row in matrix for value in row]
    ## creating cell sprites
    for i, (position, value) in enumerate(zip(cellsPositions, unpackedMatrix)):
        x, y = position
        rect = Rectangle(x, y, width, height, color=dataColorMatch[value])
        rect.opacity = opacity(value)
        sprites.append(rect)
    
    ## creating margin sprites
    if marginVisible:
        #if margins are enabled, calculate their positions and add them to the batch
        vertMarginPositions = getVerticalMarginsCentered(gridWidth, columns, marginSize)
        horizMarginPositions = getHorizontalMarginsCentered(gridHeight, rows, marginSize)

        for x, y in  horizMarginPositions: #horizontal
            sprites.append(Line(x, y, gridWidth, y, thickness=marginSize,\
                                color=marginColor))
        for x, y in vertMarginPositions: #vertical
            sprites.append(Line(x, y, x, gridHeight, thickness=marginSize,\
                                color=marginColor))
    return sprites
    






            
