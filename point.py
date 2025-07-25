from vector2 import Vector2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_position(self): return Vector2(self.x, self.y)

def from_vector(start: Point, vector: Vector2):
    return Point(start.x + vector.x, start.y + vector.y)