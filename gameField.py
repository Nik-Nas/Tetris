from vector2D import *
from pieceManager import *


def copy(iterable):
    result = []
    for i in iterable:
        result.append([item for item in i])
    return result


class GameField:

    def __init__(self, rows, columns):
        ##dimensions of field (in cells)
        self._rows = rows
        self._columns = columns
        self._matrix = []
        for i in range(rows):
            self._matrix.append([0] * columns)
        self._stationary_matrix = copy(self._matrix)
        self._current_piece = None
        self._hold_piece = None
        self._piece_manager = PieceManager()

        self._current_piece = self._piece_manager.get_next()
        self._cur_width = len(self._current_piece.rotated[0])
        self._cur_height = len(self._current_piece.rotated)
        self._cur_col = columns // 2 - 1
        self._cur_row = rows - self._cur_height
        self.update_current(self._cur_row, self._cur_col)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    def tick_current(self):
        self.move_current(Vector2dPresets.DOWN)

    def rotate_current(self, is_clockwise=False):
        if self._current_piece is None: return False
        if self.fit(self._cur_row, self._cur_col, Vector2dPresets.DEFAULT, self._current_piece.next_rotation) != 0:
            return False
        self._current_piece.rotate(is_clockwise)
        self._cur_width = len(self._current_piece.rotated[0])
        self._cur_height = len(self._current_piece.rotated)
        self.update_current(self._cur_row, self._cur_col)
        return True

    def move_current(self, direction) -> bool:
        if not direction: raise ValueError("direction is not specified")
        old_pos = (self._cur_row, self._cur_col)
        row, col = old_pos
        match direction:
            case Vector2dPresets.DOWN:
                row -= 1
            case Vector2dPresets.LEFT:
                col -= 1
            case Vector2dPresets.RIGHT:
                col += 1
            case _:
                raise ValueError(f"wtf is going on? Direction {direction} is not supported")

        fit_status = self.fit(row, col, direction, rotation=self._current_piece._rotation_index)
        if fit_status != 0: row, col = old_pos

        self.update_current(row, col)
        if fit_status == 2:
            self._stationary_matrix = copy(self._matrix)
            self.next_current()
        return fit_status == 0

    def fit(self, row: int, col: int, direction: Vector2dPresets, rotation:int) -> int:
        if self._current_piece is None: return 0
        if row < 0:
            return 2
        if col < 0 or col > self._columns - self._cur_width:
            return 1
        can_end = direction == Vector2dPresets.DOWN
        piece = self._current_piece.rotations[rotation]
        try:
            #           for r in self._matrix: print(r)
            for r in range(len(piece)):
                for c in range(len(piece[0])):
                    if piece[r][c] > 0 and self._stationary_matrix[r + row][c + col] > 0:
                        return 2 if can_end else 1
            return 0
        except IndexError:
            print("fit index error in gameField fit()")
            return 2

    def update_current(self, row, col):
        self._cur_row = row
        self._cur_col = col

        new_matrix = copy(self._stationary_matrix)
        r = row
        c = col
        try:
            for r in range(row, row + self._cur_height):
                for c in range(col, col + self._cur_width):
                    if self._current_piece.rotated[r - row][c - col] == 0: continue
                    new_matrix[r][c] = self._current_piece.code
        except IndexError as e:
            e.args = *e.args, r, c, row, col
            raise e
        self._matrix = copy(new_matrix)

    def next_current(self):
        self._current_piece = self._piece_manager.get_next()
        self._cur_width = len(self._current_piece.rotated[0])
        self._cur_height = len(self._current_piece.rotated)
        self._cur_col = self._columns // 2 - 1
        self._cur_row = self._rows - self._cur_height
        self.update_current(self._cur_row, self._cur_col)

    def log(self):
        for p in self._current_piece.rotated: print(p)
        print()
