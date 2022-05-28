from src.board import Board


def test_board_init():
    board = Board()
    assert board.players == ("a", "b", "c", "d", "e", "public", "loot")
