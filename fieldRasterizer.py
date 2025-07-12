from pixelMathTools import *
from graphicsTools import *
from gameField import *

class FieldRasterizer:

    def __init__(self, field, cell_width, cell_height, \
                 auto_margin=True, margin=None):
        if not auto_margin and margin is None: raise TypeError("margin is not defined and auto-margin is disabled")
        self._margin_coefficient = 10
        self.__cell_width = cell_width
        self.__cell_height = cell_height
        self.auto_margin = auto_margin
        self.__observers = []
        if auto_margin: self.__margin = self.calc_margin(cell_width, cell_height)
        else: self.__margin = margin
        self.__field = field
        self.__gridSize = getGridSize(self.__field._rows, self.__field._columns, \
                     self.__cell_width, self.__cell_height, self.__margin)
        self.data_color_match = {
            0: (0, 0, 0),
            1: (0, 255, 0),
            2: (255, 255, 0),
            3: (0, 0, 255),
            }
        self.__lastCell = None


    def calc_margin(self, cell_width: int, cell_height: int) -> int:
        return calcMarginOnAverage(cell_width, cell_height, self._margin_coefficient)

    def margin_coefficient(self, num: int) -> None:
        self._margin_coefficient = num
        self.update_grid_size()

    @property
    def cell_width(self): return self.__cell_width

    @cell_width.setter
    def cell_width(self, width: int):
        self.__cell_width = width
        self.update_grid_size()


    @property
    def cell_height(self): return self.__cell_height

    @cell_height.setter
    def cell_height(self, height: int):
        self.__cell_height = height
        self.update_grid_size()


    def update_grid_size(self):
        if self.auto_margin: self.__margin = self.calc_margin(self.__cell_width, self.__cell_height)
        self.__gridSize = getGridSize(self.__field._rows, self.__field._columns, \
                     self.__cell_width, self.__cell_height, self.__margin)


    @property
    def cell_size(self): return (self.__cell_width, self.__cell_height)

    @cell_height.setter
    def cell_size(self, width: int, height: int) -> None:
        self.__cell_width = width
        self.__cell_height = height
        self.update_grid_size()
    

    def toImage(self) -> []:
        return drawMatrix(self.__field._matrix, self.data_color_match, \
                          self.__gridSize[0], self.__gridSize[1], self.__margin, (0, 0, 0), \
                          opacityType=OpacityType.DEFINE_TRANSPARENT, opacityData={0:0})

    def getCell(self, x, y):
        offset = 2 if self.__margin >= 4 else 0
        cell = getCellByCoordinates(x, y, 0, 0, self.__gridSize[0], \
                                   self.__gridSize[1], self.__field._rows, \
                                   self.__field._columns, self.__margin, offset)
        if cell:
            self.__field._matrix[cell[0]][cell[1]] = 1
            if self.__lastCell: self.__field._matrix[self.__lastCell[0]][self.__lastCell[1]] = 0
            self.__lastCell = cell
        return cell
        

    
