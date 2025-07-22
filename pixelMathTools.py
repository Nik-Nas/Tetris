def grid_size(rows: int, columns: int, cell_width: int, cell_height: int, margin: int):
    return (cell_width + margin) * columns + margin, (cell_height + margin) * rows + margin


def margin_on_average(cell_width: int, cell_height: int, divider: float):
    return int((cell_width + cell_height) / 2 / divider)


def grid_width(columns: int, cell_width: int, margin: int):
    return (cell_width + margin) * columns + margin


def grid_height(rows: int, cell_height: int, margin: int):
    return (cell_height + margin) * rows + margin


def cell_size(grid_width: int, grid_height: int, rows, columns, margin):
    return ((grid_width - margin) // columns) - margin, ((grid_height - margin) // rows) - margin


def cell_width(grid_width: int, columns: int, margin):
    return ((grid_width - margin) // columns) - margin


def cell_height(grid_height, rows, margin):
    return ((grid_height - margin) // rows) - margin


def cell_position(grid_x: int, grid_y: int, row: int, col: int, cell_width: int, cell_height: int, margin: int):
    return margin + (cell_width + margin) * col + grid_x, margin + (cell_height + margin) * row + grid_y


def cells_positions_list(grid_x: int, grid_y: int, grid_width: int, grid_height: int,
                         rows: int, columns: int, margin: int):
    positions = []
    cell_width_, cell_height_ = cell_size(grid_width, grid_height, rows, columns, margin)
    offset = margin
    for rowIndex in range(rows):
        y = offset + (cell_height_ + offset) * rowIndex + grid_y
        for columnIndex in range(columns):
            x = offset + (cell_width_ + offset) * columnIndex + grid_x
            positions.append((x, y))
    return positions


def horiz_margins_positions_list(grid_height, rows, margin):
    positions = []
    cell_height_ = cell_height(grid_height, rows, margin)
    offset = margin // 2
    positions.append((0, int(offset)))
    for rowIndex in range(1, rows + 1):
        y = (margin + cell_height_) * rowIndex + offset
        positions.append((0, y))
    return positions

def vert_margins_position_list(grid_width, columns, margin):
    positions = []
    cell_width_ = cell_width(grid_width, columns, margin)
    offset = (margin + 1) // 2
    positions.append((int(offset), 0))
    for columnIndex in range(1, columns + 1):
        x = (cell_width_ + margin) * columnIndex + offset
        positions.append((x, 0))
    return positions
    

def cell_by_coordinates(x, y, grid_x, grid_y, grid_width, grid_height, rows, columns, margin, margin_blend=0):
    if margin_blend > margin / 2: raise ValueError("margin_blend cannot be more than half of margin itself")

    offset = margin - margin_blend

    x -= grid_x
    y -= grid_y

    if not(offset <= x <= (grid_width - offset)): return None
    if not(offset <= y <= (grid_height - offset)): return None

    cell_width_, cell_height_ = cell_size(grid_width, grid_height, rows, columns, margin)

    period_x = cell_width_ + margin
    period_y = cell_height_ + margin

    clicked_col = int((x - offset) // period_x)
    clicked_row = int((y - offset) // period_y)

    if x > (period_x * (clicked_col + 1) + margin_blend) \
       or y > (period_y * (clicked_row + 1) + margin_blend): return None
    return clicked_row, clicked_col
    
    
    
    
