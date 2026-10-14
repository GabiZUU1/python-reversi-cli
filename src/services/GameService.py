from src.domain.Player import PlayerColors, Player
from src.exceptions.Exceptions import GameNotFinishedError
from src.repository.BaseRepo import BaseRepo
from src.services.BaseService import BaseService


class GameService(BaseService):
    """Class for the service that manages the game."""
    def __init__(self, repository: BaseRepo):
        """
        Initialization of the GameService class.
        :param repository: The repository the class will use.
        """
        super().__init__(repository)
        self.__current_color = PlayerColors.Black

    def get_current_player(self) -> Player:
        """
        Gets the player whose turn it is.
        :return: Returns the player.
        """
        return self._repo.get_player_by_color(self.__current_color)

    def next_turn(self) -> bool:
        """
        Proceeds the game to the next turn. If the next player has no possible moves, it skips him as well.
        :return: Returns True if a skip has happened, False otherwise.
        """
        skip = False
        if self.__current_color is PlayerColors.Black:
            self.__current_color = PlayerColors.White
            if len(self._repo.search_valid_moves_for_player(self.__current_color)) == 0:
                skip = True
                self.__current_color = PlayerColors.Black
        else:
            self.__current_color = PlayerColors.Black
            if len(self._repo.search_valid_moves_for_player(self.__current_color)) == 0:
                skip = True
                self.__current_color = PlayerColors.White
        return skip

    def get_score(self, player: Player = None) -> tuple[int, int] | int:
        """
        Gets the score of both the players, or just the specified player.
        :return: Returns a tuple of both the players, with the first element being the score of the player whose color is black or the score of the specified player.
        """
        if player is not None:
            return self._repo.get_score(player.color)

        black = self._repo.get_score(PlayerColors.Black)
        white = self._repo.get_score(PlayerColors.White)

        return black, white

    def is_game_over(self) -> bool:
        """
        Checks all the end/win conditions.
        :return: Returns True if the game is over, False otherwise.
        """
        if self.check_board_end():
            return True

        if self.check_moves_left():
            return True

        return False

    def check_board_end(self) -> bool:
        """
        Checks if the board is full.
        :return: Returns True if the board is full or False in the other case.
        """
        if self._repo.get_score(PlayerColors.Black) + self._repo.get_score(PlayerColors.White) == 64:
            return True
        return False

    def check_moves_left(self) -> bool:
        """
        Checks if both the players have any possible moves. If both of them don't have any possible moves left, returns True.
        :return: Returns True if both players can't continue, False otherwise.
        """
        if len(self._repo.search_valid_moves_for_player(PlayerColors.Black)) == 0 and len(self._repo.search_valid_moves_for_player(PlayerColors.White)) == 0:
            return True
        return False

    def get_winner(self) -> Player | None:
        """
        If the game has ended, returns the player with the highest score.
        :return: Return the player with the highest score or None in case of a tie.
        """
        if self.is_game_over():
            p1 = self._repo.get_player_by_color(PlayerColors.Black)
            p2 = self._repo.get_player_by_color(PlayerColors.White)

            if self.get_score(p1) > self.get_score(p2):
                return p1
            elif self.get_score(p1) < self.get_score(p2):
                return p2
            else:
                return None
        else:
            raise GameNotFinishedError("The game is not yet finished. Can't get the winner!")