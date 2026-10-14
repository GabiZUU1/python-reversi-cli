import pytest

from src.domain.Board import Board
from src.domain.Player import PlayerColors, PlayerType
from src.exceptions.Exceptions import ValidationError
from src.repository.BaseRepo import BaseRepo
from src.services.PlayerService import PlayerService


class TestPlayerService:
    @pytest.fixture
    def service(self):
        repo = BaseRepo(Board())
        service = PlayerService(repo)
        return service

    def test_initialization(self):
        repo = BaseRepo(Board())
        service = PlayerService(repo)
        assert service._repo is repo

    def test_create_player(self, service):
        with pytest.raises(ValidationError):
            service.create_player(1, PlayerColors.Black, PlayerType.Real)
        with pytest.raises(ValidationError):
            service.create_player("ds", 1, PlayerType.Real)
        with pytest.raises(ValidationError):
            service.create_player("sd", PlayerColors.Black, 1)

        service.create_player("g", PlayerColors.Black, PlayerType.Real)
        with pytest.raises(ValidationError):
            service.create_player("s", PlayerColors.Black, PlayerType.Real)

    def test_get_player_by_color(self, service):
        service.create_player("f", PlayerColors.Black, PlayerType.Real)
        service.create_player("s", PlayerColors.White, PlayerType.Real)
        assert service.get_player_by_color(PlayerColors.Black) is service._repo.player1

    def test_get_player_by_type(self, service):
        service.create_player("f", PlayerColors.Black, PlayerType.Real)
        service.create_player("s", PlayerColors.White, PlayerType.Computer)
        assert service.get_player_by_type(PlayerType.Real) is service._repo.player1