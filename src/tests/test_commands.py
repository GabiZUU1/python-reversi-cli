import pytest
import pytest_mock

from src.commands.Commands import CreatePlayerCommand, MakeMoveCommand, Command
from src.domain.Player import PlayerColors, PlayerType, Player
from src.exceptions.Exceptions import ValidationError


class TestCommands:
    def test_create_player_command(self, mocker):
        service = mocker.Mock()

        cmd = CreatePlayerCommand(
            service,
            "marcel",
            PlayerColors.Black,
            PlayerType.Real
        )
        cmd.execute()

        service.create_player.assert_called_once_with("marcel", PlayerColors.Black, PlayerType.Real)

    def test_make_move_command(self, mocker):
        service = mocker.Mock()
        p = Player("test", PlayerColors.Black, PlayerType.Real)

        cmd = MakeMoveCommand(
            service,
            p,
            1, 1
        )
        cmd.execute()

        service.make_move.assert_called_once_with(p, 1, 1)