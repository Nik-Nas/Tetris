import math

from point import Point


class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def length(self): return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def normalized(self):
        magnitude = self.length
        return self.x / magnitude, self.y / magnitude

    @property
    def inverted(self): return -self.x, -self.y

    @property
    def mirrored_x(self): return -self.x, self.y

    @property
    def mirrored_y(self): return self.x, -self.y

    def invert(self):
        self.x = -self.x
        self.y = -self.y

    def mirror_x(self): self.x = -self.x

    def mirror_y(self): self.y = -self.y

    def normalize(self):
        magnitude = self.length
        self.x /= magnitude
        self.y /= magnitude

    def __add__(self, vec:"Vector2"):
        return Vector2(self.x + vec.x, self.y + vec.y)

    def __radd__(self, vec: "Vector2"): return self.__add__(vec)

    def __sub__(self, vec:"Vector2"):
        return Vector2(self.x - vec.x, self.y - vec.y)

    def __rsub__(self, vec: "Vector2"): return self.__sub__(vec)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float): return self.__mul__(scalar)

    def __truediv__(self, scalar: float):
        return Vector2(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: int):
        return Vector2(self.x // scalar, self.y // scalar)

    def __str__(self): return f"({self.x}, {self.y})"

    def __len__(self): return math.sqrt(self.x ** 2 + self.y ** 2)

def lerp(vec_1: Vector2, vec_2: Vector2, alpha: float) -> Vector2:
    return (1 - alpha) * vec_1 + alpha * vec_2

def from_points(start: Point, end: Point):
    return Vector2(end.x - start.x, end.y - start.y)


DEFAULT = Vector2(0, 0)
UP = Vector2(0, 1)
DOWN = Vector2(0, -1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
