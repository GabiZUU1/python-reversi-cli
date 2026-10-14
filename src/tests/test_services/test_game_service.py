import pytest

from src.domain.Board import Board
from src.domain.Player import PlayerColors, Player, PlayerType
from src.exceptions.Exceptions import GameNotFinishedError
from src.repository.BaseRepo import BaseRepo
from src.services.GameService import GameService
from src.services.PlayerService import PlayerService


class TestGameService:
    @pytest.fixture
    def service(self):
        repo = BaseRepo(Board())
        p1 = Player("a", PlayerColors.Black, PlayerType.Real)
        p2 = Player("b", PlayerColors.White, PlayerType.Real)
        repo.set_player(p1)
        repo.set_player(p2)
        service = GameService(repo)
        return service

    def test_initialization(self):
        repo = BaseRepo(Board())
        service = GameService(repo)

        assert service._repo is repo
        assert service._GameService__current_color is PlayerColors.Black

    def test_get_current_player(self, service):
        assert service.get_current_player() is service._repo.get_player_by_color(PlayerColors.Black)

    def test_next_turn(self, mocker):
        board = mocker.Mock()
        board.search_valid_moves_for_player.return_value = [1, 2, 3]
        repo = BaseRepo(board)
        service = GameService(repo)
        assert not service.next_turn()

        board.search_valid_moves_for_player.return_value = []
        assert service.next_turn()

    def test_get_score(self, service):
        assert service.get_score() == (2, 2)
        service._repo.make_move(PlayerColors.Black, 2, 3)
        assert service.get_score() == (4, 1)
        assert service.get_score(service.get_current_player()) == 4
        service.next_turn()
        assert service.get_score(service.get_current_player()) == 1

    def test_is_game_over(self, service):
        assert not service.is_game_over()

    def test_get_winner(self, mocker):
        board = Board()
        repo = mocker.Mock(BaseRepo)
        repo.get_score.return_value = 32

        service = GameService(repo)
        assert not isinstance(service.get_winner(), Player)