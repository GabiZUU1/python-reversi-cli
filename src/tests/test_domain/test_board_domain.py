import pytest

from src.domain.Board import Board, BoardPieces
from src.domain.Player import PlayerColors


class TestBoardDomain:
    @pytest.fixture
    def board(self):
        """Creates a new board for each test."""
        return Board()

    def test_board_pieces_str(self):
        assert str(BoardPieces.NoPiece) == "n"
        assert str(BoardPieces.BlackPiece) == "b"
        assert str(BoardPieces.WhitePiece) == "w"

    def test_clone_board(self, board):
        assert board.get_printable_board() == board.clone_board().get_printable_board()

    @pytest.mark.parametrize(
        "color, expected_moves",
        [
            (
                PlayerColors.Black,
                {(2, 3), (4, 5), (5, 4), (3, 2)},
            ),
            (
                PlayerColors.White,
                {(2, 4), (4, 2), (5, 3), (3, 5)},
            ),
        ],
    )
    def test_search_valid_moves_for_player(self, board, color, expected_moves):
        moves = board.search_valid_moves_for_player(color)
        assert set(moves) == expected_moves

    @pytest.mark.parametrize(
        "color, row, column, expected",
        [
            (PlayerColors.Black, 2, 3, True),
            (PlayerColors.Black, 1, 1, False),
            (PlayerColors.White, 2, 4, True),
            (PlayerColors.White, 1, 1, False),
            (PlayerColors.Black, 0, 0, False),
            (PlayerColors.White, 0, 0, False),
            (PlayerColors.Black, 9, 1, False),
            (PlayerColors.White, 1, 9, False),
            (PlayerColors.Black, 3, 4, False)
        ]
    )
    def test_check_valid_move(self, board, color, row, column, expected):
        assert board.check_valid_move(color, row, column) == expected

    def test_make_move(self, board):
        board.make_move(PlayerColors.Black, 2, 3)
        b = Board()
        b.make_move(PlayerColors.Black, 2, 3)

        assert board.get_printable_board() == b.get_printable_board()

    def test_count_pieces(self, board):
        assert board.count_pieces(PlayerColors.Black) == 2
        assert board.count_pieces(PlayerColors.White) == 2

        board.make_move(PlayerColors.Black, 2, 3)
        assert board.count_pieces(PlayerColors.Black) == 4
        assert board.count_pieces(PlayerColors.White) == 1