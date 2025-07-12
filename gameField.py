import pyglet
from physicsEngine import *
from matrixTools import *
from vector2D import *
from pieceManager import *

class GameField:

    
    def copy(self, l):
        res = []
        for i in l:
            res.append([item for item in i])
        return res

    
    def __init__(self, rows, columns):
        ##dimensions of field (in cells)
        self._rows = rows
        self._columns = columns
        self._matrix = []        
        for i in range(rows):
            self._matrix.append([0] * columns)
        self._stationary_matrix = self.copy(self._matrix)
        self.__current_piece = None
        self.__hold_piece = None
        self.__piece_manager = PieceManager()
        
        self.__current_piece = self.__piece_manager.GetNext()
        self.__cur_width = len(self.__current_piece._rotated_matrix[0])
        self.__cur_height = len(self.__current_piece._rotated_matrix)
        self.__cur_col = columns // 2 - 1
        self.__cur_row = rows - self.__cur_height
        self.update_current(self.__cur_row, self.__cur_col)


    def tick_current(self):
        self.move_current(Vector2D_Presets.DOWN)


    def rotate_current(self, is_clockwise=True):
        if self.__current_piece is not None:
            self.__current_piece.rotate(is_clockwise)
            self.__cur_width = len(self.__current_piece._rotated_matrix[0])
            self.__cur_height = len(self.__current_piece._rotated_matrix)


    def move_current(self, direction):
        if not direction: raise ValueError("direction is not specified")
        old_pos = (self.__cur_row,  self.__cur_col)
        row, col = old_pos
        match direction:
            case Vector2D_Presets.DOWN:
                row -= 1
            case Vector2D_Presets.LEFT:
                col -= 1
            case Vector2D_Presets.UP:
                row += 1
            case Vector2D_Presets.RIGHT:
                col += 1
            case _: raise ValueError(f"wtf is going on? Direction {direction} is not supported")

        is_stopped = not(self.fit(row, col))
        if is_stopped: row, col = old_pos

        self.update_current(row, col)
        if is_stopped: 
            self._stationary_matrix = self.copy(self._matrix)
            self.next_current()


    def fit(self, row, col):
        if self.__current_piece is None: return True
        if row < 0 or col < 0 or col > self._columns - self.__cur_width:
            return False
        piece = self.__current_piece._rotated_matrix
        try:
##            for r in self._matrix: print(r)
            for r in range(len(piece)):
                for c in range(len(piece[0])):
                    if piece[r][c] > 0 and self._stationary_matrix[r + row][c + col] > 0:
                        return False
            return True
        except IndexError:
            print("fit index error in gameField fit()")
            return False

    def update_current(self, row, col):
        self.__cur_row = row
        self.__cur_col = col
        
        new_matrix = self.copy(self._stationary_matrix)
        for r in range(row, row + self.__cur_height):
            for c in range(col, col + self.__cur_width):
                if self.__current_piece._rotated_matrix[r - row][c - col] == 0: continue
                new_matrix[r][c] = self.__current_piece._code
        
        self._matrix = self.copy(new_matrix)


    def next_current(self):
        self.__current_piece = self.__piece_manager.GetNext()
        self.__cur_width = len(self.__current_piece._rotated_matrix[0])
        self.__cur_height = len(self.__current_piece._rotated_matrix)
        self.__cur_col = self._columns // 2 - 1
        self.__cur_row = self._rows - self.__cur_height
        self.update_current(self.__cur_row, self.__cur_col)

    def log(self):
        for p in self._matrix[::-1]: print(p)
        print()
                

        

