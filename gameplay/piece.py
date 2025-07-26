from tools.matrixTools import rotate_matrix


class Piece:
    def __init__(self, matrix: list, spinning_point: int, code: int):
        self.__base_matrix = matrix
        self._spinning_point = spinning_point
        self.__code = code
        self._width = len(matrix[0])
        self._height = len(matrix)
        self._rotations = [self.__base_matrix[:]]
        for i in range(1, 4):
            self._rotations.append(rotate_matrix(self._rotations[i - 1]))
        del matrix

        self._rotation_index = 0

        self.row_correction = 0
        self.col_correction = 0

        if spinning_point < 15:
            lines_above = spinning_point // 5
            lines_left = spinning_point - lines_above * 5

            row_change = -2 + lines_left - lines_above
            column_change = lines_left - lines_above

            self.row_correction = 2 - lines_above
            self.col_correction = lines_left - 2

    @property
    def code(self):
        return self.__code

    @property
    def rotation_index(self):
        return self._rotation_index

    @property
    def rotated(self):
        return self._rotations[self._rotation_index]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def next_rotation(self) -> list[list[int]]:
        return self._rotations[(self._rotation_index + 1) % 4]

    @property
    def prev_rotation(self) -> list[list[int]]:
        return self._rotations[(self._rotation_index + 3) % 4]

    @property
    def base(self):
        return self.__base_matrix

    def get_rotation(self, index: int):
        return self._rotations[index]

    def rotate(self, is_clockwise=True):
        # basically cycles rotation index (next index if clockwise otherwise previous index)
        self._rotation_index = (self._rotation_index + (1 if is_clockwise else 3)) % 4
        #swaps width and height through pure math
        self._width += self._height
        self._height = self._width - self._height
        self._width -= self._height

    @property
    def position_correctors(self):
        return self.row_correction, self.col_correction




    def __getitem__(self, position):
        # returning number from  a rotation
        return self._rotations[self._rotation_index][position[0]][position[1]]