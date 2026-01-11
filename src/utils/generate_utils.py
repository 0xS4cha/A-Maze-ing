from typing import List
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Bit_position(Enum):
    VISITED = 0b10000
    NORTH = 0b00001
    EAST = 0b00010
    SOUTH = 0b00100
    WEST = 0b01000


def remove_wall(maze: List[List[int]], x1: int,
                y1: int, x2: int, y2: int) -> None:
    """Carve connection between two adjacent cells."""
    if x1 == x2:
        if y1 > y2:  # Neighbor is North
            maze[y1][x1] |= Bit_position.NORTH.value
            maze[y2][x2] |= Bit_position.SOUTH.value
        else:        # Neighbor is South
            maze[y1][x1] |= Bit_position.SOUTH.value
            maze[y2][x2] |= Bit_position.NORTH.value
    elif y1 == y2:
        if x1 > x2:  # Neighbor is West
            maze[y1][x1] |= Bit_position.WEST.value
            maze[y2][x2] |= Bit_position.EAST.value
        else:        # Neighbor is East
            maze[y1][x1] |= Bit_position.EAST.value
            maze[y2][x2] |= Bit_position.WEST.value
