import dataclasses


@dataclasses.dataclass
class Info:
    player: str


@dataclasses.dataclass
class SingleInfo(Info):
    name: str
    present: bool


@dataclasses.dataclass
class RangeInfo(Info):
    terrain: str
    start: int
    end: int
    amount: int


@dataclasses.dataclass
class LeastTerrainInfo(Info):
    terrain: str
