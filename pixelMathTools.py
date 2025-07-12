def getGridSize(rows, columns, cellWidth, cellHeight, margin):
    return ((cellWidth + margin) * columns + margin, \
            (cellHeight + margin) * rows + margin)


def calcMarginOnAverage(cellWidth, cellHeight, divider):
    return int((cellWidth + cellHeight) / 2 / divider)


def getGridWidth(columns, cellWidth, margin):
    return (cellWidth + margin) * columns + margin


def getGridHeight(rows, cellHeight, margin):
    return (cellHeight + margin) * rows + margin


def getCellSize(gridWidth, gridHeight, rows, columns, margin):
    return (((gridWidth - margin) // columns) - margin, \
            ((gridHeight - margin) // rows) - margin)


def getCellWidth(gridWidth, columns, margin):
    return ((gridWidth - margin) // columns) - margin


def getCellHeight(gridHeight, rows, margin):
    return ((gridHeight - margin) // rows) - margin


def getCellsPositions(gridWidth, gridHeight, rows, columns, margin):
    positions = []
    cellWidth, cellHeight = getCellSize(gridWidth, gridHeight, rows, columns, margin)
    offset = margin
    for rowIndex in range(rows):
        y = offset + (cellHeight + offset) * rowIndex
        for columnIndex in range(columns):
            x = offset + (cellWidth + offset) * columnIndex
            positions.append((x, y))
    return positions


def getHorizontalMarginsCentered(gridHeight, rows, margin):
    positions = []
    cellHeight = getCellHeight(gridHeight, rows, margin)
    offset = (margin) // 2
    positions.append((0, int(offset)))
    for rowIndex in range(1, rows + 1):
        y = (margin + cellHeight) * rowIndex + offset
        positions.append((0, y))
    return positions        

def getVerticalMarginsCentered(gridWidth, columns, margin):
    positions = []
    cellWidth = getCellWidth(gridWidth, columns, margin)
    offset = (margin + 1) // 2
    positions.append((int(offset), 0))
    for columnIndex in range(1, columns + 1):
        x = (cellWidth + margin) * columnIndex + offset
        positions.append((x, 0))
    return positions
    

def getCellByCoordinates(x, y, grid_x, grid_y, grid_width, grid_height, rows, columns, margin, margin_blend=0):
    if margin_blend > margin / 2: raise ValueError("margin_blend cannot be more, than half of margin itself")

    offset = margin - margin_blend
    strict = margin - 2 * margin_blend

    x -= grid_x
    y -= grid_y

    if not((offset <= x <= (grid_width - offset))): return None
    if not((offset <= y <= (grid_height - offset))): return None

    cell_width, cell_height = getCellSize(grid_width, grid_height, rows, columns, margin)

    period_x = cell_width + margin
    period_y = cell_height + margin

    clicked_col = int((x - offset) // period_x)
    clicked_row = int((y - offset) // period_y)

    if x > (period_x * (clicked_col + 1) + margin_blend) \
       or y > (period_y * (clicked_row + 1) + margin_blend): return None
    return (clicked_row, clicked_col)
    
    
    
    
