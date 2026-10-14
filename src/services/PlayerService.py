from src.domain.Player import PlayerColors, PlayerType, Player
from src.exceptions.Exceptions import ValidationError
from src.repository.BaseRepo import BaseRepo
from src.services.BaseService import BaseService


class PlayerService(BaseService):
    """Class for the service that manages the players."""
    def __init__(self, repository: BaseRepo):
        """
        Initialization of the PlayerService class.
        :param repository: The repository the service will use.
        """
        super().__init__(repository)

    def create_player(self, player_name: str, player_color: PlayerColors, player_type: PlayerType) -> None:
        """
        Function that creates a player and adds him to the game.
        If there already exist two players, raises ValidationError.
        :param player_name: The name of the player you want to create.
        :param player_color: The color of the players pieces.
        :param player_type: The type of the player.
        :return: None
        """
        if not isinstance(player_name, str):
            raise ValidationError("The name of the player must be a str!")
        if not isinstance(player_color, PlayerColors):
            raise ValidationError("The color of the player must be of type PlayerColors!")
        if not isinstance(player_type, PlayerType):
            raise ValidationError("The type of the player must be of the type PlayerType!")

        if self._repo.player1 is not None and self._repo.player1.color == player_color:
            raise ValidationError("A player already has this color!")

        p = Player(player_name, player_color, player_type)
        self._repo.set_player(p)

    def get_player_by_color(self, color: PlayerColors) -> Player:
        """
        Gets a player by its color.
        :param color: The color of the player you want to get.
        :return: The player.
        """
        return self._repo.get_player_by_color(color)

    def get_player_by_type(self, type: PlayerType) -> Player:
        """
        Gets a player by its type.
        :param type: The type of the player you want to get.
        :return: The player.
        """
        return self._repo.get_player_by_type(type)