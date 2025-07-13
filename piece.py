from matrixTools import rotate_matrix

class Piece:
    def __init__(self, matrix: list, spinpoint: int, code: int):
        self.__base_matrix = matrix
        self._spinpoint = spinpoint
        self.__code = code
        self._rotated_matrix = matrix

        row_correction = 0
        col_correсtion = 0
        
        if spinpoint < 15:
            lines_above = spinpoint // 5
            lines_left = spinpoint - lines_above * 5

            row_change = -2 + lines_left - lines_above
            column_change = lines_left - 2 + lines_above
            
            row_correction = 2 - lines_above
            col_correction = lines_left - 2

    @property
    def code(self): return self.__code

    def rotate(self, is_clockwise=True):
        self._rotated_matrix = rotate_matrix(self._rotated_matrix, is_clockwise)
    
        
