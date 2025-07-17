from matrixTools import rotate_matrix


class Piece:
    def __init__(self, matrix: list, spinning_point: int, code: int):
        self.__base_matrix = matrix
        self._spinning_point = spinning_point
        self.__code = code
        self._rotation_index = 0
        self.rotations = [rotate_matrix(self.__base_matrix)]
        for i in range(1, 4):
            self.rotations.append(rotate_matrix(self.rotations[i - 1]))
        del matrix

        row_correction = 0
        col_correction = 0

        if spinning_point < 15:
            lines_above = spinning_point // 5
            lines_left = spinning_point - lines_above * 5

            row_change = -2 + lines_left - lines_above
            column_change = lines_left - 2 + lines_above

            row_correction = 2 - lines_above
            col_correction = lines_left - 2

    @property
    def code(self):
        return self.__code

    def rotate(self, is_clockwise=True):
        self._rotation_index = self.next_rotation if is_clockwise else self.prev_rotation

    @property
    def rotation(self):
        return self._rotation_index

    @property
    def width(self):
        return len(self.rotated[0])

    @property
    def height(self):
        return len(self.rotated)

    @property
    def next_rotation(self):
        return (self._rotation_index + 1) % 4

    @property
    def prev_rotation(self):
        return (self._rotation_index + 3) % 4

    @property
    def base(self):
        return self.__base_matrix

    @property
    def rotated(self):
        return self.rotations[self._rotation_index]
