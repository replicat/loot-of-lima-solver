import pytest

from src.board import Board
from src.enums import Direction, Terrain


def test_board_init():
    board = Board()
    assert board.players == ("a", "b", "c", "d", "e", "public", "loot")


@pytest.mark.parametrize(
    "player, terrain, start, end, expected",
    [
        ("a", Terrain.MOUNTAIN, Direction.NORTH, Direction.SOUTH, 4),
    ],
)
def test_board_get_slots(player, terrain, start, end, expected):
    board = Board()
    slots = board._get_slots(player, terrain, start, end)
    assert len(slots) == expected
