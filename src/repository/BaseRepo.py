from src.domain.Board import Board
from src.domain.Player import Player, PlayerColors, PlayerType
from src.exceptions.Exceptions import ValidationError


class BaseRepo:
    """Base class for the repositories."""
    def __init__(self, board: Board, player1: Player = None, player2: Player = None):
        """
        Initialization of the base repository.
        :param board: The board the game will play on.
        """
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2

    @property
    def board(self):
        return self.__board
    @board.setter
    def board(self, new_board: Board):
        if not isinstance(new_board, Board):
            raise ValidationError("The new board must be of type Board!")
        self.__board = new_board

    @property
    def player1(self):
        return self.__player1
    @player1.setter
    def player1(self, new_player: Player):
        if not isinstance(new_player, Player):
            raise ValidationError("The new player must be of type Player!")
        self.__player1 = new_player

    @property
    def player2(self):
        return self.__player2
    @player2.setter
    def player2(self, new_player: Player):
        if not isinstance(new_player, Player):
            raise ValidationError("The new player must be of type Player!")
        self.__player2 = new_player

    def get_printable_board(self) -> list[list]:
        """
        Gets the board in an easy to print way.
        :return: Returns the board as a list[list]
        """
        return self.board.get_printable_board()

    def get_board(self) -> Board:
        """
        Gets the board.
        :return: Returns the board as a Board class.
        """
        return self.board

    def set_board(self, new_board: Board) -> None:
        """
        Sets the board to a given board.
        :param new_board: The new board.
        :return: None
        """
        self.board = new_board

    def search_valid_moves_for_player(self, color: PlayerColors) -> list:
        """
        Searches for all the valid moves of a given player by its color.
        :param color: The color of the player you want to search moves for.
        :return: Returns the list of moves.
        """
        return self.board.search_valid_moves_for_player(color)

    def get_player_by_color(self, color: PlayerColors) -> Player:
        """
        Gets a player by a given color.
        :param color: The color of the player you want to get.
        :return: Returns the player.
        """
        if self.__player1.color is color:
            return self.__player1
        else:
            return self.__player2

    def get_player_by_type(self, type: PlayerType) -> Player | None:
        """
        Gets a player by its type.
        :param type: The type of the player you want to get.
        :return: The player.
        """
        if self.player1 is not None and self.player1.type is type:
            return self.player1
        elif self.player2 is not None and self.player2.type is type:
            return self.player2
        else:
            return None

    def make_move(self, color: PlayerColors, row: int, column: int) -> None:
        """
        Performs a move for a color.
        :param color: The color that makes the move.
        :param row: The row of the move.
        :param column: The column of the move.
        :return: None
        """
        if self.__board.check_valid_move(color, row, column):
            self.__board.make_move(color, row, column)
        else:
            raise ValidationError(f"Not a valid move!")

    def get_score(self, color: PlayerColors) -> int:
        """
        Gets the score of a player by its color.
        :return: Returns the players score.
        """
        return self.__board.count_pieces(color)

    def set_player(self, player: Player) -> None:
        """
        Sets a player on an available spot.
        :param player: The player to be set.
        :return: None
        """
        if self.__player1 is None:
            self.__player1 = player
        elif self.__player2 is None:
            self.__player2 = player
        else:
            raise ValidationError("Both players are occupied!")