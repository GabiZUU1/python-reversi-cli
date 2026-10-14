import pytest

from src.domain.Board import Board
from src.domain.Player import PlayerColors, PlayerType, Player
from src.repository.BaseRepo import BaseRepo
from src.services.BoardService import BoardService


class TestBoardService:
    @pytest.fixture
    def service(self):
        repo = BaseRepo(Board())
        service = BoardService(repo)
        return service

    def test_initialization(self):
        repo = BaseRepo(Board())
        service = BoardService(repo)
        assert service._repo is repo

    def test_get_board(self, service):
        assert service.get_board() is service._repo.get_board()

    def test_search_valid_moves_for_player(self, service):
        p = Player("gigi", PlayerColors.Black, PlayerType.Real)

        assert set(service.search_valid_moves_for_players(p)) == {(2, 3), (4, 5), (5, 4), (3, 2)}

    def test_make_move(self, service):
        p = Player("gigi", PlayerColors.Black, PlayerType.Real)

        brd = Board()
        brd.make_move(PlayerColors.Black, 2, 3)

        service.make_move(p, 3, 4)
        assert service.get_printable_board() == brd.get_printable_board()

    def test_set_board(self, service):
        new_board = Board()
        service.set_board(new_board)
        assert service.get_board() is new_board