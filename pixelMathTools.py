def get_grid_size(rows, columns, cell_width, cell_height, margin):
    return (cell_width + margin) * columns + margin, (cell_height + margin) * rows + margin


def calc_margin_on_average(cell_width, cell_height, divider):
    return int((cell_width + cell_height) / 2 / divider)


def get_grid_width(columns, cell_width, margin):
    return (cell_width + margin) * columns + margin


def get_grid_height(rows, cell_height, margin):
    return (cell_height + margin) * rows + margin


def get_cell_size(grid_width, grid_height, rows, columns, margin):
    return ((grid_width - margin) // columns) - margin, ((grid_height - margin) // rows) - margin


def get_cell_width(grid_width, columns, margin):
    return ((grid_width - margin) // columns) - margin


def get_cell_height(grid_height, rows, margin):
    return ((grid_height - margin) // rows) - margin


def get_cells_positions(grid_width, grid_height, rows, columns, margin):
    positions = []
    cell_width, cell_height = get_cell_size(grid_width, grid_height, rows, columns, margin)
    offset = margin
    for rowIndex in range(rows):
        y = offset + (cell_height + offset) * rowIndex
        for columnIndex in range(columns):
            x = offset + (cell_width + offset) * columnIndex
            positions.append((x, y))
    return positions


def get_horizontal_margins_centered(grid_height, rows, margin):
    positions = []
    cell_height = get_cell_height(grid_height, rows, margin)
    offset = margin // 2
    positions.append((0, int(offset)))
    for rowIndex in range(1, rows + 1):
        y = (margin + cell_height) * rowIndex + offset
        positions.append((0, y))
    return positions        

def get_vertical_margins_centered(grid_width, columns, margin):
    positions = []
    cell_width = get_cell_width(grid_width, columns, margin)
    offset = (margin + 1) // 2
    positions.append((int(offset), 0))
    for columnIndex in range(1, columns + 1):
        x = (cell_width + margin) * columnIndex + offset
        positions.append((x, 0))
    return positions
    

def get_cell_by_coordinates(x, y, grid_x, grid_y, grid_width, grid_height, rows, columns, margin, margin_blend=0):
    if margin_blend > margin / 2: raise ValueError("margin_blend cannot be more than half of margin itself")

    offset = margin - margin_blend

    x -= grid_x
    y -= grid_y

    if not(offset <= x <= (grid_width - offset)): return None
    if not(offset <= y <= (grid_height - offset)): return None

    cell_width, cell_height = get_cell_size(grid_width, grid_height, rows, columns, margin)

    period_x = cell_width + margin
    period_y = cell_height + margin

    clicked_col = int((x - offset) // period_x)
    clicked_row = int((y - offset) // period_y)

    if x > (period_x * (clicked_col + 1) + margin_blend) \
       or y > (period_y * (clicked_row + 1) + margin_blend): return None
    return clicked_row, clicked_col
    
    
    
    
