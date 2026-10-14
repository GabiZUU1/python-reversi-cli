import pytest
import pytest_mock as pytm

from src.domain.Board import Board
from src.domain.Player import Player, PlayerColors, PlayerType
from src.exceptions.Exceptions import ValidationError
from src.repository.BaseRepo import BaseRepo


class TestBaseRepo:
    @pytest.fixture
    def repo(self):
        return BaseRepo(Board(), Player("1", PlayerColors.Black, PlayerType.Real), Player("2", PlayerColors.White, PlayerType.Computer))

    def test_initialization(self):
        b = Board()
        repo = BaseRepo(b)

        assert repo.board is b
        assert repo.player1 is None
        assert repo.player2 is None

    def test_getters_and_setters(self, repo):
        brd = Board()
        brd.make_move(PlayerColors.Black, 2, 3)

        repo.board = brd
        assert repo.board == brd
        assert repo.get_printable_board() == brd.get_printable_board()
        with pytest.raises(ValidationError):
            repo.board = 1

        p = Player("wow", PlayerColors.Black, PlayerType.Computer)
        repo.player1 = p
        assert repo.player1 == p
        with pytest.raises(ValidationError):
            repo.player1 = 1

        p = Player("wow", PlayerColors.White, PlayerType.Computer)
        repo.player2 = p
        assert repo.player2 == p
        with pytest.raises(ValidationError):
            repo.player2 = 1

    @pytest.mark.parametrize(
        "player_color, expected",
        [
            (
                PlayerColors.Black,
                {(2, 3), (4, 5), (5, 4), (3, 2)},
            ),
            (
                PlayerColors.White,
                {(2, 4), (4, 2), (5, 3), (3, 5)},
            ),
        ]
    )
    def test_search_valid_moves_for_player(self, repo, player_color, expected):
        assert set(repo.search_valid_moves_for_player(player_color)) == expected

    def test_get_player_by_color(self, repo):
        assert repo.get_player_by_color(PlayerColors.Black) is repo.player1
        assert repo.get_player_by_color(PlayerColors.White) is repo.player2

    def test_make_move(self, repo):
        repo.make_move(PlayerColors.Black, 2, 3)
        brd = Board()
        brd.make_move(PlayerColors.Black, 2, 3)

        assert repo.get_printable_board() == brd.get_printable_board()

        with pytest.raises(ValidationError):
            repo.make_move(PlayerColors.Black, -1, -1)

    def test_get_score(self, repo):
        assert repo.get_score(PlayerColors.Black) == 2

        repo.make_move(PlayerColors.Black, 2, 3)
        assert repo.get_score(PlayerColors.Black) == 4
        assert repo.get_score(PlayerColors.White) == 1

    def test_set_player(self, repo):
        p = Player("tiktok", PlayerColors.Black, PlayerType.Real)
        with pytest.raises(ValidationError):
            repo.set_player(p)

        repo = BaseRepo(Board())
        repo.set_player(p)
        assert repo.player1 is p

        p.color = PlayerColors.White
        repo.set_player(p)
        assert repo.player2 is p

    def test_set_board(self, repo):
        new_board = Board()
        repo.set_board(new_board)
        assert repo.get_board() is new_board

    def test_get_player_by_type(self, repo):
        new_repo = BaseRepo(Board())
        new_repo.set_player(Player("tesdt", PlayerColors.Black, PlayerType.Real))
        assert new_repo.get_player_by_type(PlayerType.Computer) is None

        assert repo.get_player_by_type(PlayerType.Real) is repo.player1
        assert repo.get_player_by_type(PlayerType.Computer) is repo.player2