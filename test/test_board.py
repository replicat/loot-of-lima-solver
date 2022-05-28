import pytest

from src.board import Board
from src.enums import StandardDirection, StandardTerrain


def test_board_init():
    board = Board(
        players=("A", "B", "C", "D", "E", "Public", "Loot"),
        terrains=StandardTerrain,
        directions=StandardDirection,
    )
    assert board.players == ("A", "B", "C", "D", "E", "Public", "Loot")


@pytest.fixture(scope="function")
def board():
    return Board(
        players=("A", "B", "C", "D", "E", "Public", "Loot"),
        terrains=StandardTerrain,
        directions=StandardDirection,
    )


@pytest.mark.parametrize(
    "player, terrain, start, end, expected",
    [
        ("A", StandardTerrain.MOUNTAIN.value, StandardDirection.NORTH.value, StandardDirection.SOUTH.value, 4),
        ("B", StandardTerrain.BEACH.value, StandardDirection.NORTH.value, StandardDirection.SOUTH.value, 4),
        ("C", StandardTerrain.FOREST.value, StandardDirection.SOUTH.value, StandardDirection.SOUTHWEST.value, 1),
        ("D", StandardTerrain.FOREST.value, StandardDirection.SOUTHWEST.value, StandardDirection.SOUTH.value, 7),
        ("E", StandardTerrain.BEACH.value, StandardDirection.NORTH.value, StandardDirection.NORTH.value, 8),
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
    assert len(locations) == expected
