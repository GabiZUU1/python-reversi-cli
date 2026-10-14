from enum import Enum

from src.exceptions.Exceptions import ValidationError


class PlayerColors(Enum):
    """Enum class that specifies the color of a player."""
    Black = 1
    White = 2

    def __str__(self):
        return self.name

class PlayerType(Enum):
    """Enum class that specifies that the player is either real or the computer."""
    Real = 1
    Computer = 2

    def __str__(self):
        return self.name

class Player:
    """Base player class."""
    def __init__(self, player_name: str, player_color: PlayerColors, player_type: PlayerType) -> None:
        """
        Initialization of the player class.
        :param player_name: The name of the player.
        :param player_color: The color of the players pieces.
        :param player_type: The type of the player.
        """
        if not isinstance(player_name, str):
            raise ValidationError("The name must be a string!")
        if player_name.strip() == "" or len(player_name) == 0:
            raise ValidationError("Please provide a name!")
        self.__name = player_name

        if not isinstance(player_color, PlayerColors):
            raise ValidationError("The color of the player must be a PlayerColor value!")
        self.__color = player_color

        if not isinstance(player_type, PlayerType):
            raise ValidationError("The type of the player must be a PlayerType value!")
        self.__type = player_type

    def __str__(self) -> str:
        return "Name: " + self.__name + "; Color: " + str(self.__color) + "; Type: " + str(self.__type)

    #region Getters and setters
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        if not isinstance(new_name, str):
            raise ValidationError("The name must be a string!")
        if new_name.strip() == "" or len(new_name) == 0:
            raise ValidationError("Please provide a name!")
        self.__name = new_name

    @property
    def color(self) -> PlayerColors:
        return self.__color

    @color.setter
    def color(self, new_color: PlayerColors) -> None:
        if not isinstance(new_color, PlayerColors):
            raise ValidationError("The color of the player must be a PlayerColor value!")
        self.__color = new_color

    @property
    def type(self) -> PlayerType:
        return self.__type

    @type.setter
    def type(self, new_type: PlayerType) -> None:
        if not isinstance(new_type, PlayerType):
            raise ValidationError("The type of the player must be a PlayerType value!")
        self.__type = new_type
    #endregion