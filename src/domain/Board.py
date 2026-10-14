import copy
from enum import Enum

from src.domain.Player import PlayerColors

class BoardPieces(Enum):
    NoPiece = "n"
    BlackPiece = "b"
    WhitePiece = "w"

    def __str__(self):
        return self.value

class Board:
    """Base board class."""
    def __init__(self):
        """Initialization of the board class."""
        self.__board = [[BoardPieces.NoPiece.value for _ in range(8)] for _ in range(8)]
        self.__board[3][3] = BoardPieces.WhitePiece.value
        self.__board[3][4] = BoardPieces.BlackPiece.value
        self.__board[4][3] = BoardPieces.BlackPiece.value
        self.__board[4][4] = BoardPieces.WhitePiece.value

        self.__directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def clone_board(self):
        """
        Clones the current board.
        :return: Returns a clone of the board.
        """
        new_board = Board()
        new_board.__board = copy.deepcopy(self.__board)
        return new_board

    def search_valid_moves_for_player(self, color: PlayerColors) -> list:
        """
        Searches for all possible moves of a certain color.
        :param color: The color to search possible moves for.
        :return: Returns a list of tuples which contain the coordinates of each possible move.
        """
        possible_moves = []
        if color is PlayerColors.Black:
            search_piece = BoardPieces.BlackPiece.value
            other_piece = BoardPieces.WhitePiece.value
        else:
            search_piece = BoardPieces.WhitePiece.value
            other_piece = BoardPieces.BlackPiece.value

        for i in range(8):
            for j in range(8):
                if self.__board[i][j] == search_piece:
                    #region Searching for all possible moves
                    #Takes all the possible directions and searches them
                    for dir in self.__directions:
                        exists = False
                        for k in range(1, 8):
                            if 0 > i + k * dir[0] or i + k * dir[0] > 7 or 0 > j + k * dir[1] or j + k * dir[1] > 7:
                                break

                            if self.__board[i + k * dir[0]][j + k * dir[1]] == other_piece:
                                exists = True
                                continue
                            elif self.__board[i + k * dir[0]][j + k * dir[1]] == BoardPieces.NoPiece.value:
                                if exists and (i + k * dir[0], j + k * dir[1]) not in possible_moves:
                                    possible_moves.append((i + k * dir[0], j + k * dir[1]))
                                break
                            else:
                                break
                    #endregion
        return possible_moves

    def check_valid_move(self, color: PlayerColors, row: int, column: int) -> bool:
        """
        Checks if a move is valid for a player is valid.
        :param color: The color of the player you want to check the color for.
        :param row: The row of the place you want to make the move.
        :param column: The column of the place you want to make th move.
        :return: Returns True if the move is valid, False if it is not.
        """
        if row < 0 or row > 8:
            return False

        if column < 0 or column > 8:
            return False

        if self.__board[row][column] != BoardPieces.NoPiece.value:
            return False

        if color is PlayerColors.Black:
            player_piece = BoardPieces.BlackPiece.value
            enemy_piece = BoardPieces.WhitePiece.value
        else:
            player_piece = BoardPieces.WhitePiece.value
            enemy_piece = BoardPieces.BlackPiece.value

        #region Verifying all possible directions
        for dir in self.__directions:
            exists = False
            for k in range(1, 8):
                if 0 > row + k * dir[0] or row + k * dir[0] > 7 or 0 > column + k * dir[1] or column + k * dir[1] > 7:
                    break

                if self.__board[row + k * dir[0]][column + k * dir[1]] == player_piece:
                    if exists:
                        return True
                    break
                elif self.__board[row + k * dir[0]][column + k * dir[1]] == enemy_piece:
                    exists = True
                    continue

        return False

    def make_move(self, color: PlayerColors, row: int, column: int) -> None:
        if color is PlayerColors.Black:
            piece = BoardPieces.BlackPiece.value
            enemy_piece = BoardPieces.WhitePiece.value
        else:
            piece = BoardPieces.WhitePiece.value
            enemy_piece = BoardPieces.BlackPiece.value

        #region Find the pieces to be modified
        to_replace = []

        self.__board[row][column] = piece
        for dir in self.__directions:
            temp = []
            for k in range(1, 8):
                if 0 > row + k * dir[0] or row + k * dir[0] > 7 or 0 > column + k * dir[1] or column + k * dir[1] > 7:
                    break

                if self.__board[row + k * dir[0]][column + k * dir[1]] == enemy_piece:
                    if (row + k * dir[0], column + k * dir[1]) not in to_replace:
                        temp.append((row + k * dir[0], column + k * dir[1]))
                elif self.__board[row + k * dir[0]][column + k * dir[1]] == piece:
                    to_replace += temp
                elif self.__board[row + k * dir[0]][column + k * dir[1]] == BoardPieces.NoPiece.value:
                    break
        #endregion

        for coord in to_replace:
            self.__board[coord[0]][coord[1]] = piece

    def count_pieces(self, color: PlayerColors) -> int:
        """
        Counts the pieces of a given color.
        :param color: The color of the pieces to count.
        :return: Returns the number of pieces.
        """
        if color == PlayerColors.Black:
            piece = BoardPieces.BlackPiece
        else:
            piece = BoardPieces.WhitePiece

        count = 0
        for i in range(8):
            for j in range(8):
                if self.__board[i][j] == piece.value:
                    count += 1
        return count

    def get_printable_board(self) -> list[list]:
        return self.__board