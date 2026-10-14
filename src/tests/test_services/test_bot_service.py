import pytest

from src.domain.Board import Board
from src.domain.Player import PlayerType, Player, PlayerColors
from src.repository.BaseRepo import BaseRepo
from src.services.BotService import BotService
from src.services.PlayerService import PlayerService


class TestBotService:
    @pytest.fixture
    def service(self):
        repo = BaseRepo(Board())
        player_service = PlayerService(repo)
        player_service.create_player("1", PlayerColors.Black, PlayerType.Real)
        player_service.create_player("2", PlayerColors.White, PlayerType.Computer)

        return BotService(repo, player_service)

    def test_initialization(self):
        repo = BaseRepo(Board())
        player_service = PlayerService(repo)
        player_service.create_player("1", PlayerColors.Black, PlayerType.Real)
        player_service.create_player("2", PlayerColors.White, PlayerType.Computer)

        bot_service = BotService(repo, player_service)

        assert bot_service._player_service is player_service
        assert bot_service._bot.type is PlayerType.Computer
        assert bot_service._human.type is PlayerType.Real

    def test_minimax(self, service):
        board = Board()

        score = service.minimax(-10, 10, 0, True, board)
        assert score in (-1, 0, 1)

        score = service.minimax(-10, 10, 0, False, board)
        assert score in (-1, 0, 1)

    def test_find_best_move(self, service):
        board = Board()

        move = service.find_best_move(board)
        assert move is not None

        valid_moves = board.search_valid_moves_for_player(PlayerColors.Black)
        move = (move[0] - 1, move[1] - 1)
        assert move in valid_moves