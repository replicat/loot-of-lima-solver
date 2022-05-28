import enum


class Terrain(enum.Enum):
    ALL = enum.auto()
    BEACH = enum.auto()
    FOREST = enum.auto()
    MOUNTAIN = enum.auto()


class Direction(enum.Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
