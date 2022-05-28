import pytest

from src.board import Board
from src.enums import StandardDirection, StandardTerrain


@pytest.fixture(scope="function")
def board():
    return Board(
        players=("A", "B", "C", "D", "E", "Public", "Loot"),
        terrains=StandardTerrain,
        directions=StandardDirection,
    )


def test_board_init(board: Board):
    assert board.players == ("A", "B", "C", "D", "E", "Public", "Loot")


@pytest.mark.parametrize(
    "player, name, expected",
    [
        ("A", "1B", "Locations_('A',_<StandardTerrain.BEACH:_'B'_,_<StandardDirection.NORTH:_1_)"),
        ("B", "7M", "Locations_('B',_<StandardTerrain.MOUNTAIN:_'M'_,_<StandardDirection.WEST:_7_)"),
    ],
)
def test_board_get_location_success(
    board: Board,
    player: str,
    name: str,
    expected: str,
):
    location = board.get_location(player, name)
    assert location.name == expected


@pytest.mark.parametrize(
    "player, terrain, start, end, expected",
    [
        (
            "A",
            StandardTerrain.MOUNTAIN.value,
            StandardDirection.NORTH.value,
            StandardDirection.SOUTH.value,
            ["1M", "2M", "3M", "4M"],
        ),
        (
            "B",
            StandardTerrain.BEACH.value,
            StandardDirection.SOUTH.value,
            StandardDirection.NORTH.value,
            ["5B", "6B", "7B", "8B"],
        ),
        (
            "C",
            StandardTerrain.FOREST.value,
            StandardDirection.SOUTH.value,
            StandardDirection.SOUTHWEST.value,
            ["5F"],
        ),
        (
            "D",
            StandardTerrain.FOREST.value,
            StandardDirection.SOUTHWEST.value,
            StandardDirection.SOUTH.value,
            ["1F", "2F", "3F", "4F", "6F", "7F", "8F"],
        ),
        (
            "E",
            StandardTerrain.BEACH.value,
            StandardDirection.NORTH.value,
            StandardDirection.NORTH.value,
            ["1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B"],
        ),
    ],
)
def test_board_get_locations(
    board: Board,
    player: str,
    terrain: str,
    start: int,
    end: int,
    expected: int,
):
    locations = board.get_locations(player, terrain, start, end)
    assert set(locations) == set(board.get_location(player, loc) for loc in expected)
