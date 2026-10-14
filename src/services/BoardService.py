from src.domain.Board import Board
from src.domain.Player import Player
from src.repository.BaseRepo import BaseRepo
from src.services.BaseService import BaseService


class BoardService(BaseService):
    """Class for the service that manages the board."""
    def __init__(self, repository: BaseRepo):
        """
        Initialization of the BoardService class.
        :param repository: The repository the service will use.
        """
        super().__init__(repository)

    def get_printable_board(self) -> list[list]:
        """Gets the board in an easy to print way."""
        return self._repo.get_printable_board()

    def get_board(self) -> Board:
        """Gets the board."""
        return self._repo.get_board()

    def set_board(self, new_board: Board) -> None:
        """Sets the board to a given board."""
        self._repo.set_board(new_board)

    def search_valid_moves_for_players(self, player: Player) -> list:
        """
        Searches for all the valid moves for a given player.
        :param player: The player to search the moves for.
        :return: Returns the list of moves.
        """
        return self._repo.search_valid_moves_for_player(player.color)

    def make_move(self, player: Player, row: int, column: int) -> None:
        """
        Performs a move for a player.
        :param player: The player that makes the move.
        :param row: The row of the move.
        :param column: The column of the move.
        :return: None
        """
        self._repo.make_move(player.color, row - 1, column - 1)