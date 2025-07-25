from typing import Iterable


class Panel:
    def __init__(self, x: int = 0, y: int = 0, width: int = 100, height: int = 100):
        self._children = []
        self.relative: list[bool] = []
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self): return self._x

    @x.setter
    def x(self, value: int):
        if -400 <= value <= 2000:
            self._x = value
            self.__update_positions((value, self._y))

    @property
    def y(self): return self._y

    @y.setter
    def y(self, value: int):
        if -400 <= value <= 1100:
            self._y = value
            self.__update_positions((self._x, value))

    @property
    def children(self):
        return self._children

    def add(self, *children, relative_position=True | Iterable[bool]):
        if type(relative_position) is bool:
            relative_position = [relative_position] * len(children)
        for child, relative in zip(children, relative_position):
            try:
                child.x = child.x
                if relative:
                    try:
                        child.x2 += self.x
                        child.y2 += self._y
                    except:
                        pass
                    child.x += self.x
                    child.y += self._y
            except AttributeError:
                raise ValueError(
                    f"object of {type(child)} cannot be added as child. Only objects with x, y coordinates can be")
            self._children.append(child)
            self.relative += relative_position

    def remove(self, *children):
        for child in children:
            if child not in self._children: raise ValueError(f"Object {child} is not in list of children!")
            self._children.remove(child)

    def __update_positions(self, new_pos:tuple[int, int]):
        for child, relative in zip(self._children, self.relative):
            if relative:
                try:
                    child.x2 += self.x
                    child.y2 += self._y
                except:
                    pass
                child.x += new_pos[0] - self._x
                child.y += new_pos[1] - self._y
