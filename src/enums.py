import enum


class Terrain(enum.Enum):
    BEACH = enum.auto()
    FOREST = enum.auto()
    MOUNTAIN = enum.auto()
    ALL = enum.auto()


class Direction(enum.Enum):
    NORTH = enum.auto()
    NORTHEAST = enum.auto()
    EAST = enum.auto()
    SOUTHEAST = enum.auto()
    SOUTH = enum.auto()
    SOUTHWEST = enum.auto()
    WEST = enum.auto()
    NORTHWEST = enum.auto()
