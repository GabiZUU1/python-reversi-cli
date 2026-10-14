from src.domain.Player import Player
from src.domain.Board import Board
from src.repository.BaseRepo import BaseRepo


class MemoryRepo(BaseRepo):
    """Class for the memory based repository."""
    def __init__(self, board: Board, player1: Player = None, player2: Player = None):
        """
        Initialization of the MemoryRepo class.
        :param board: The board the game will play on.
        """
        super().__init__(board, player1, player2)