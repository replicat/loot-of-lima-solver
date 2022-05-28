from src.board import LootOfLimaBoard


def test_board_init():
    board = LootOfLimaBoard()
    assert board.players == ("a", "b", "c", "d", "e", "public", "loot")
