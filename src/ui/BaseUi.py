from abc import ABC, abstractmethod
from enum import Enum

from src.domain.Board import Board
from src.repository.MemoryRepo import MemoryRepo
from src.services.BoardService import BoardService
from src.services.GameService import GameService
from src.services.PlayerService import PlayerService


class PrintablePieces(Enum):
    NoPiece = "o"
    BlackPiece = "□"
    WhitePiece = "■"
    MovePiece = "X"

class BaseUI(ABC):
    def __init__(self):
        self._repo = MemoryRepo(Board())
        self._game_service = GameService(self._repo)
        self._player_service = PlayerService(self._repo)
        self._board_service = BoardService(self._repo)
        self._bot_service = None

    @abstractmethod
    def start(self) -> None:
        pass