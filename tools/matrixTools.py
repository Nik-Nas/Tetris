from typing import Iterable


def int_to_bin_matrix(num, row_length, fill_mode=0, strip_empty=True):
    ##fillmode: 0 - place zeros at the start, 1 - place zeros at the end, 2 - no filling
    binary_view = bin(num)[2:]
    signs = len(binary_view)
    if fill_mode == 2 and signs % row_length != 0:
        raise ValueError(
            f"number ({num}) doesn't unpack evenly into matrix of specified row length ({row_length}) without filling")
    matrix = []
    match fill_mode:
        case 0:
            binary_view = binary_view.zfill(((signs + row_length - 1) // row_length) * row_length)
        case 1:
            binary_view = binary_view + "0" * (signs % row_length)
    index = 0
    signs = len(binary_view)
    for i in range(signs // row_length):
        matrix.append(list(map(int, binary_view[index: index + row_length])))
        index += row_length
    empty = [0] * row_length

    while strip_empty and empty in matrix:
        matrix.remove(empty)
    empty = [0] * len(matrix)
    matrix = transpose_matrix(matrix)
    while strip_empty and empty in matrix:
        matrix.remove(empty)
    matrix = transpose_matrix(matrix)
    return matrix


def bin_matrix_to_int(matrix, min_length=None):
    string_form = ""
    for row in matrix:
        for num in row:
            string_form += str(num)
    if min_length and len(string_form) < min_length:
        string_form += "0" * (min_length - len(string_form))
    return int(string_form)


def transpose_matrix(matrix):
    result_matrix = []
    for column in range(len(matrix[0])):
        new_row = []
        for row in range(len(matrix)):
            new_row.append(matrix[row][column])
        result_matrix.append(new_row)
    return result_matrix


def rotate_matrix(matrix, clockwise=True):
    result_matrix = []
    row_step = 1 if clockwise else -1
    column_step = -1 if clockwise else 1
    for column in range(len(matrix[0])):
        new_row = []
        for row in range(len(matrix)):
            new_row.append(matrix[row][column])
        result_matrix.append(new_row[::column_step])
    return result_matrix[::row_step]


def subtract_matrices(mat_1: list[list], mat_2: list[list]) -> list[list]:
    """returns result of subtracting mat_2 from mat_1"""
    res = []
    if len(mat_1) != len(mat_2) or len(mat_1[0]) != len(mat_2[0]):
        raise ValueError("matrix dimensions aren't equal")
    for row in range(len(mat_1)):
        res.append([mat_1[row][i] - mat_2[row][i] for i in range(len(mat_1[row]))])
    return res


def reverse_rows(matrix):
    return matrix[::-1]


def reverse_columns(matrix):
    return [row[::-1] for row in matrix]


def copy(iterable: Iterable):
    result = []
    for i in iterable:
        result.append([item for item in i])
    return result

def recalc_spin_point(old_spin: int, old_width: int, old_height: int, new_width: int, new_height: int) -> int:
    vertices_row = old_width + 1
    vertices_col = old_height + 1
    if old_spin < vertices_row * vertices_col:
        lines_above = old_spin // vertices_row
        lines_left = old_spin - lines_above * vertices_row
        raw_new_spin = lines_above * (new_width + 1) + lines_left
        lim = (new_width + 1) * (new_height + 1)
        return raw_new_spin if raw_new_spin < lim else lim - 1
    return  old_spin

def get_vertex_spin_point(width, height, lines_above, lines_left, horiz_indexation: bool,
                          mirrored_horiz=False, mirrored_vert=False):
    if mirrored_horiz: lines_above = height - lines_above
    if mirrored_vert: lines_left = width - lines_left
    if horiz_indexation:
        return lines_above * (width + 1) + lines_left
    else:
        return lines_left * (height + 1) + lines_above

"""def change_indexation_direction(old_spin: int, width: int, height: int, from_horizontal: bool):
    vertices_row = width + 1
    vertices_col = height + 1
    if old_spin < vertices_row * vertices_col:
        if from_horizontal:
            lines_above = old_spin // vertices_row
            lines_left = old_spin - vertices_row * lines_above
            return lines_left * vertices_col + lines_above
        else:
            lines_left = old_spin // vertices_row
            lines_above = old_spin - vertices_row * lines_left
            return lines_above * vertices_row + lines_left
    return old_spin"""

"""def mirror_spin_point(old_spin, width, height, horizontal_indexation: bool, mirror_horizontal=True) -> int:
    vertices_row = width + 1
    vertices_col = height + 1
    if old_spin < vertices_row * vertices_col:
        print("before", old_spin, end=" ")
        if not horizontal_indexation:
            old_spin = change_indexation_direction(old_spin, width, height, False)
            print("change to", old_spin)

        lines_above = old_spin // vertices_row
        lines_left = old_spin - lines_above * vertices_row
        if mirror_horizontal:
            print("after", vertices_row * (height - lines_above) + lines_left, "left", lines_left, "above", lines_above, "width", width, "height", height)
            return vertices_row * (height - lines_above) + lines_left
        else:
            print("after", vertices_row * lines_above + (width - lines_left), "left", lines_left, "above", lines_above, "width", width, "height", height)
            return vertices_row * lines_above + (width - lines_left)
    return old_spin"""