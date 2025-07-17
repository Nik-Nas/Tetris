import struct
import random
from piece import Piece
from matrixTools import *


class PieceManager:

    def __init__(self):
        self._shapes = []
        with open("shapes.bin", "r+b") as stream:
            content = stream.read()
            if len(content) > 0:
                for i in range(0, len(content), 2):
                    stuff = struct.unpack("=BB", content[i:i + 2])
                    self._shapes.append(Piece(int_to_bin_matrix(stuff[0], 4),
                                              stuff[1], len(self._shapes) + 1))
        self.__repeat_spacer = 2
        self.__used_indexes = {i: -1 for i in range(1, self.__repeat_spacer + 1)}

    def get_next(self) -> Piece:
        used = self.__used_indexes.values()
        unused_shapes = [self._shapes[i] for i in range(len(self._shapes)) if i not in used]
        index = random.randint(0, len(unused_shapes) - 1)
        source_index = self._shapes.index(unused_shapes[index])

        for i in range(1, self.__repeat_spacer):
            self.__used_indexes[i] = self.__used_indexes[i + 1]
        self.__used_indexes[self.__repeat_spacer] = source_index
        return unused_shapes[index]
