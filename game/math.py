import enum
from math import sqrt


class Direction(enum.Enum):
    left = 0
    right = 1


def points_dis(a, b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


def direction_to_point(a, b):
    dis_x = a[0] - b[0]
    if dis_x > 0:
        return Direction.left
    else:
        return Direction.right

def is_in_range(x, a, b) -> bool:
    return a <= x <= b
