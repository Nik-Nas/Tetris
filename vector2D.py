from enum import Enum


class Vector2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def length(self): return (self.x ** 2 + self.y ** 2) ** 0.5

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

    @property
    def vector(self): return self.x, self.y

    def multiply(self, number):
        self.x *= number
        self.y *= number

    def invert(self):
        self.x = -self.x
        self.y = -self.y

    def mirror_x(self): self.x = -self.x

    def mirror_y(self): self.y = -self.y

    def normalize(self):
        magnitude = self.length
        self.x /= magnitude
        self.y /= magnitude


class Vector2dPresets(Enum):
    DEFAULT = Vector2D(0, 0)
    UP = Vector2D(0, 1)
    DOWN = Vector2D(0, -1)
    LEFT = Vector2D(-1, 0)
    RIGHT = Vector2D(1, 0)
