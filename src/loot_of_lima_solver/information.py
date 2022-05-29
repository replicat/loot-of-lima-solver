import dataclasses


@dataclasses.dataclass
class Info:
    pass


@dataclasses.dataclass
class UniqueLocationInfo(Info):
    pass


@dataclasses.dataclass
class SingleInfo(Info):
    player: str
    name: str
    present: bool


@dataclasses.dataclass
class RangeInfo(Info):
    player: str
    terrain: str
    start: int
    end: int
    amount: int


@dataclasses.dataclass
class LeastTerrainInfo(Info):
    player: str
    terrain: str
