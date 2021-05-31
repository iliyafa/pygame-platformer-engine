from enum import Enum, auto

# Colors:
Color = {
    "Blue"  : [0, 5, 141],
    "Green" : [40, 255, 0],
    "Red"   : [255, 15, 0],
    "Cyan"  : [174, 196, 255],
}

class Sides(Enum):
    TOP = auto(),
    BOTTOM = auto(),
    LEFT = auto(),
    RIGHT = auto(),
    UNKNOWN = auto()


class Direction(Enum):
    LEFT = -1
    RIGHT = 1