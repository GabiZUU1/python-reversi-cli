from abc import ABC, abstractmethod

from src.domain.Player import PlayerColors, PlayerType, Player
from src.services.BoardService import BoardService
from src.services.PlayerService import PlayerService
#from src.services.services import BoardService


class Command(ABC):
    """Base class for all commands."""
    @abstractmethod
    def execute(self):
        pass

class CreatePlayerCommand(Command):
    """Command to create a player and add it to the game."""
    def __init__(self, player_service: PlayerService, player_name: str, player_color: PlayerColors, player_type: PlayerType):
        self.__service = player_service
        self.__name = player_name
        self.__color = player_color
        self.__type = player_type

    def execute(self):
        self.__service.create_player(self.__name, self.__color, self.__type)

class MakeMoveCommand(Command):
    def __init__(self, service: BoardService, player: Player, row: int, column: int):
        self.__service = service
        self.__player = player
        self.__row = row
        self.__column = column

    def execute(self):
        self.__service.make_move(self.__player, self.__row, self.__column)