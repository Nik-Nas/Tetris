from tools.matrixTools import rotate_matrix, recalc_spin_point, get_vertex_spin_point, get_cell_spin_point


class Piece:
    def __init__(self, matrix: list, spinpoint: int, code: int):
        self._base_matrix = matrix
        self._base_spinpoint = spinpoint
        self.__code = code
        self._width = len(matrix[0])
        self._height = len(matrix)
        self._spinpoint = recalc_spin_point(spinpoint, 4, 2, self._width, self._height, True)
        self._rotations = [rotate_matrix(rotate_matrix(self._base_matrix[:]))]
        for i in range(1, 4):
            self._rotations.append(rotate_matrix(self._rotations[i - 1], clockwise=False))
        del matrix

        self._rotation_index = 0

        self._row_correction = 0
        self._col_correction = 0
        self.__update_correctors(1, True)

    @property
    def code(self):
        return self.__code

    @property
    def matrix(self):
        return self._rotations[self._rotation_index]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def rotated_clockwise(self):
        return self._rotations[(self._rotation_index + 1) % 4]

    @property
    def rotated_counterclockwise(self):
        return self._rotations[(self._rotation_index + 3) % 4]

    @property
    def base(self):
        return self._base_matrix

    @property
    def base_spinpoint(self): return self._base_spinpoint

    def get_rotation(self, index: int):
        return self._rotations[index]

    def rotate(self, clockwise=True):
        # basically cycles rotation index (next index if clockwise otherwise previous index)
        self._rotation_index = (self._rotation_index + (1 if clockwise else 3)) % 4
        self._width += self._height
        self._height = self._width - self._height
        self._width -= self._height
        # swap corrections
        self.__update_correctors((self._rotation_index + (1 if clockwise else 3)) % 4, clockwise)
            #print("aft", self._spinpoint, "ind", self._rotation_index, self.position_correctors, "ab/lft", (lines_above, lines_left), "hor_mrr", horiz_mirror, "vrt_mrr", vert_mirror)
        #print("new corrections", self._row_correction, self._col_correction)

    def __update_correctors(self, index: int, clockwise: bool):
        vertices_in_row = self._width + 1
        vertices_in_col = self._height + 1
        if self._spinpoint < vertices_in_row * vertices_in_col:

            lines_above = self._spinpoint // vertices_in_row
            lines_below = self._height - lines_above
            lines_left = self._spinpoint - lines_above * vertices_in_row
            lines_right = self._width - lines_left

            del vertices_in_row, vertices_in_col

            if clockwise:
                self._row_correction = lines_below - lines_right
                self._col_correction = lines_left - lines_below
                arg_1 = lines_left
                arg_2 = lines_below
            else:
                self._row_correction = lines_below - lines_left
                self._col_correction = lines_left - lines_above
                arg_1 = lines_right
                arg_2 = lines_above
            # print("bef", self._spinpoint, end=" ")
            self._spinpoint = get_vertex_spin_point(self._height, self._width, arg_1, arg_2, horiz_indexation=True)

            del lines_above, lines_left, lines_below, lines_right
        else:
            block_spin = self._spinpoint - vertices_in_row * vertices_in_col
            rows_above = block_spin // self._width
            columns_left = block_spin - rows_above * self._width
            columns_right = self._width - columns_left - 1
            rows_below = self._height - rows_above - 1
            if clockwise:
                self._row_correction = rows_below - columns_right
                self._col_correction = columns_left - rows_below
                arg_1 = columns_left
                arg_2 = rows_below
            else:
                self._row_correction = rows_below - columns_left
                self._col_correction = columns_left - rows_above
                arg_1 = columns_right
                arg_2 = rows_above
            self._spinpoint = get_cell_spin_point(self._height, self._width, arg_1, arg_2, horiz_indexation=True,
                                                  pre_inex_vertices=True)

    @property
    def position_correctors(self):
        return self._row_correction, self._col_correction

    def __getitem__(self, position):
        # returning number from  a rotation
        return self._rotations[self._rotation_index][position[0]][position[1]]
