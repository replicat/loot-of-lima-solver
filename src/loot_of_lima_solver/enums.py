import enum


class CustomEnumMeta(enum.EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class CustomEnum(enum.Enum, metaclass=CustomEnumMeta):
    def __str__(self):
        return str(self.value)


class StandardTerrain(CustomEnum):
    BEACH = "B"
    FOREST = "F"
    MOUNTAIN = "M"


class StandardDirection(CustomEnum):
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8
