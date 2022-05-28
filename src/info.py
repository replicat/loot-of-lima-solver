import dataclasses

from .enums import Direction, Terrain


@dataclasses.dataclass
class Info:
    player: str


class LeastTerrainInfo(Info):
    terrain: Terrain


class RangeInfo(Info):
    terrain: Terrain
    start: Direction
    end: Direction
    amount: int


class SingleInfo(Info):
    terrain: Terrain
    direction: Direction
    exist: bool
