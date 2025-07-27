from typing import Iterable

from tools import vector2
from tools.matrixTools import copy
from tools.pieceManager import PieceManager
from tools.vector2 import Vector2


def log(arr: Iterable, message="", step=1):
    if message: print(message)
    for p in arr[::step]: print(p)
    print()


class GameField:

    def __init__(self, rows, columns):
        ##dimensions of field (in cells)
        self._rows = rows
        self._columns = columns

        #matrix containing stationary data and current piece
        self._matrix: list[list[int]] = []
        for i in range(rows):
            self._matrix.append([0] * columns)

        #matrix with stationary blocks only
        self._stationary_matrix = copy(self._matrix)

        #current and hold pieces
        self._current_piece = None
        self._hold_piece = None
        self._next_piece = None

        #piece manager to get next
        self._piece_manager = PieceManager()

        self._current_piece = self._piece_manager.get_next()
        self._cur_col = columns // 2 - (self._current_piece.width // 2)
        self._cur_row = rows - self._current_piece.height
        self.update_field(self._cur_row, self._cur_col)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    def tick_current(self):
        self.move_current(vector2.DOWN)

    def rotate_current(self, is_clockwise=False):
        if self._current_piece is None: return False
        matrix = self._current_piece.next_rotation if is_clockwise else self._current_piece.prev_rotation
        if self.fit(matrix, self._cur_row, self._cur_col, vector2.DEFAULT) != 0:
            print("STOP")
            return False
        #print("raw", self._cur_row, self._cur_col, self._current_piece.width)

        #print("corrected", self._cur_row, self._cur_col)
        correctors = self._current_piece.position_correctors
        self._cur_row += correctors[0]
        self._cur_col += correctors[1]
        self._current_piece.rotate(is_clockwise)
        self.update_field(self._cur_row, self._cur_col)
        return True

    def move_current(self, direction:Vector2) -> bool:
        old_pos = (self._cur_row, self._cur_col)
        row, col = old_pos
        match direction:
            case vector2.DOWN:
                row -= 1
            case vector2.LEFT:
                col -= 1
            case vector2.RIGHT:
                col += 1
            case _:
                raise ValueError(f"wtf is going on? Direction {direction} is not supported")
        fit_status = self.fit(self._current_piece.rotated, row, col, direction)
        if fit_status != 0: row, col = old_pos

        self.update_field(row, col)
        if fit_status == 2:
            self.delete_full_rows(row)
            self._stationary_matrix = copy(self._matrix)
            self.next_current()
        return fit_status != 1

    def update_field(self, row, col):
        self._cur_row = row
        self._cur_col = col

        new_matrix = copy(self._stationary_matrix)
        r = row
        c = col
        try:
            for r in range(row, row + self._current_piece.height):
                for c in range(col, col + self._current_piece.width):
                    if self._current_piece[r - row, c - col] == 0: continue
                    new_matrix[r][c] = self._current_piece.code
        except IndexError as e:
            e.args = (*e.args, r - row, c - col, row, col, self._current_piece.width,
                      self._current_piece.height)
            raise e
        self._matrix = copy(new_matrix)

    def next_current(self):
        self._current_piece = self._piece_manager.get_next()
        self._cur_col = self._columns // 2 - 1
        self._cur_row = self._rows - self._current_piece.height
        self.update_field(self._cur_row, self._cur_col)


    def delete_full_rows(self, start_row: int) -> int:

        """delete full rows and returns their amount"""

        full_rows_indexes: list[int] = []
        for row in range(start_row, min(start_row + self._current_piece.height, self._rows - 1)):
            if all(num != 0 for num in self._matrix[row]):
                full_rows_indexes.append(row)
        if len(full_rows_indexes) > 0:
            new_matrix = []
            for i in range(1, len(full_rows_indexes)):
                new_matrix += self._matrix[full_rows_indexes[i - 1] + 1:full_rows_indexes[i]]
            new_matrix += self._matrix[full_rows_indexes[-1] + 1:self._rows]
            for i in range(len(full_rows_indexes)): new_matrix.append([0] * self._columns)
            self._matrix = new_matrix
        return len(full_rows_indexes)


    def fit(self, matrix: list[list[int]], row: int, col: int, direction: Vector2) -> int:
        """checks if matrix fits in game field at given position"""
        width = len(matrix[0])
        height = len(matrix)
        if direction == vector2.DEFAULT:
            correctors = self._current_piece.position_correctors
            row += correctors[0]
            col += correctors[1]
        if col < 0 or col > self._columns - width:
            return 1
        if row < 0:
            return 2
        if row > self._rows - height: return 1
        try:
            for r in range(height):
                for c in range(width):
                    if matrix[r][c] > 0 and self._stationary_matrix[r + row][c + col] > 0:
                        return 2 if direction == vector2.DOWN else 1
            return 0
        except IndexError:
            print("fit index error in gameField fit()")
            return 2
