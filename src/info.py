import dataclasses

from enums import Direction, Terrain


@dataclasses.dataclass
class Info:
    player: str


@dataclasses.dataclass
class LeastTerrainInfo(Info):
    terrain: Terrain


@dataclasses.dataclass
class RangeInfo(Info):
    terrain: Terrain
    start: Direction
    end: Direction
    amount: int
