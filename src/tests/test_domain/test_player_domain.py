import pytest

from src.domain.Player import Player, PlayerColors, PlayerType
from src.exceptions.Exceptions import ValidationError


class TestPlayerDomain:
    @pytest.fixture
    def player(self):
        return Player("test", PlayerColors.Black, PlayerType.Real)

    @pytest.mark.parametrize(
        "name, color, type, expected",
        [
            (1, PlayerColors.White, PlayerType.Real, ValidationError),
            ("", PlayerColors.Black, PlayerType.Real, ValidationError),
            ("  ", PlayerColors.Black, PlayerType.Real, ValidationError),
            ("gigi", "black", PlayerType.Real, ValidationError),
            ("gigi", PlayerColors.Black, "real", ValidationError)
        ]
    )
    def test_player_init(self, name, color, type, expected):
        with pytest.raises(expected):
            assert Player(name, color, type)

    def test_player_str(self, player):
        assert str(player) == "Name: test; Color: Black; Type: Real"
        assert str(player) != "ok"

    def test_assert_player_properties(self, player):
        player.name = "miau"
        assert player.name == "miau"
        with pytest.raises(ValidationError):
            player.name = " "
        with pytest.raises(ValidationError):
            player.name = 1

        player.color = PlayerColors.White
        assert player.color == PlayerColors.White
        with pytest.raises(ValidationError):
            player.color = 1

        player.type = PlayerType.Computer
        assert player.type == PlayerType.Computer
        with pytest.raises(ValidationError):
            player.type = 1