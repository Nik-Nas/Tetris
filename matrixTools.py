def int_to_bin_matrix(num, row_length, fillmode=0, strip_empty=True):
    ##fillmode: 0 - place zeros at the start, 1 - place zeros at the end, 2 - no filling
    binary_view = bin(num)[2:]
    signs = len(binary_view)
    if fillmode == 2 and signs % row_length != 0:
        raise ValueError(f"number ({num}) doesn't unpack evenly into matrix of specified row length ({row_length}) without filling")
    matrix = []
    match fillmode:
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

def reverse_rows(matrix):
    return matrix[::-1]

def reverse_columns(matrix):
    return [row[::-1] for row in matrix]









                
