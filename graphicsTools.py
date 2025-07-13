import enum
from pyglet.shapes import Rectangle, Line
from pixelMathTools import *


class OpacityType(enum.Enum):
    SOLID = 0
    CONSTANT = 1
    DATA_MATCH = 2
    COLOR_MATCH = 3
    DEFINE_TRANSPARENT = 4


def draw_matrix(matrix, data_color_match, grid_width, grid_height, margin_size, margin_color,
                opacity_type=OpacityType.SOLID, opacity_data=None, margin_visible=True):
    rows = len(matrix)
    columns = len(matrix[0])

    ##calculating cells size and coordinates
    width, height = get_cell_size(grid_width, grid_height, rows, columns, margin_size)
    cells_positions = get_cells_positions(grid_width, grid_height, rows, columns, margin_size)

    # preparing empty list and defining opacity function based on opacity type
    sprites = []

    match opacity_type:
        case OpacityType.SOLID:
            opacity = lambda inp: 255
        case OpacityType.CONSTANT:
            opacity = lambda inp: int(opacity_data * 255)
        case OpacityType.DATA_MATCH:
            opacity = lambda inp: int(opacity_data[inp] * 255)
        case OpacityType.COLOR_MATCH:
            opacity = lambda inp: int(opacity_data[data_color_match[inp]] * 255)
        case OpacityType.DEFINE_TRANSPARENT:
            opacity = lambda inp: int((opacity_data[inp] if inp in opacity_data else 1) * 255)
        case _:
            raise ValueError(f"opacity type is not specified or given value ({opacity_type}) does not support")

    unpacked_matrix = [value for row in matrix for value in row]
    ## creating cell sprites
    for i, (position, value) in enumerate(zip(cells_positions, unpacked_matrix)):
        x, y = position
        rect = Rectangle(x, y, width, height, color=data_color_match[value])
        rect.opacity = opacity(value)
        sprites.append(rect)

    ## creating margin sprites
    if margin_visible:
        # if margins are enabled, calculate their positions and add them to the batch
        vert_margin_positions = get_vertical_margins_centered(grid_width, columns, margin_size)
        horiz_margin_positions = get_horizontal_margins_centered(grid_height, rows, margin_size)

        for x, y in horiz_margin_positions:  # horizontal
            sprites.append(Line(x, y, grid_width, y, thickness=margin_size, color=margin_color))
        for x, y in vert_margin_positions:  # vertical
            sprites.append(Line(x, y, x, grid_height, thickness=margin_size, color=margin_color))
    return sprites
