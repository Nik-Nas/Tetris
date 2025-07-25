import math


class RadiansAngle:
    def __init__(self, value: float):
        self.value = value

    def __add__(self, other: 'RadiansAngle'):
        self.value += other.value

    def __sub__(self, other: 'RadiansAngle'):
        self.value -= other.value


RIGHT_ANGLE = RadiansAngle(math.pi / 2)
STRAIGHT_ANGLE = RadiansAngle(math.pi)
COMPLETE_ANGLE = RadiansAngle(2 * math.pi)