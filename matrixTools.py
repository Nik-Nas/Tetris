def integerToBinaryMatrix(num, rowLength, fillmode=0, stripEmpty=True):
    ##fillmode: 0 - place zeros at the start, 1 - place zeros at the end, 2 - no filling
    binaryView = bin(num)[2:]
    signs = len(binaryView)
    if fillmode == 2 and signs % rowLength != 0:
        raise ValueError(f"number ({num}) doesn't unpack evenly into matrix of specified row length ({rowLength}) without filling")
    matrix = []
    match fillmode:
        case 0:
            binaryView = binaryView.zfill(((signs + rowLength - 1) // rowLength) * rowLength)
        case 1:
            binaryView = binaryView + "0" * (signs % rowLength)
    index = 0
    signs = len(binaryView)
    for i in range(signs // rowLength):
        matrix.append(list(map(int, binaryView[index: index + rowLength])))
        index += rowLength
    empty = [0] * rowLength
    
    while stripEmpty and empty in matrix:
        matrix.remove(empty)
    empty = [0] * len(matrix)
    matrix = transposeMatrix(matrix)
    while stripEmpty and (empty) in matrix:
        matrix.remove(empty)
    matrix = transposeMatrix(matrix)
    return matrix
        
def binaryMatrixToInteger(matrix, minLength=None):
    stringForm = ""
    for row in matrix:
        for num in row:
            stringForm += str(num)
    if minLength and len(stringForm) < minLength:
        stringForm += "0" * (minLength - len(stringForm))
    return int(stringForm)


def transposeMatrix(matrix):
    resultMatrix = []
    for column in range(len(matrix[0])):
        newRow = []
        for row in range(len(matrix)):
            newRow.append(matrix[row][column])
        resultMatrix.append(newRow)
    return resultMatrix

    
def rotateMatrix(matrix, clockwise=True):
    resultMatrix = []
    rowStep = 1 if clockwise else -1
    columnStep = -1 if clockwise else 1
    for column in range(len(matrix[0])):
        newRow = []
        for row in range(len(matrix)):
            newRow.append(matrix[row][column])
        resultMatrix.append(newRow[::columnStep])
    return resultMatrix[::rowStep]

def reverseRows(matrix):
    return matrix[::-1]

def reverseColumns(matrix):
    return [row[::-1] for row in matrix]









                
