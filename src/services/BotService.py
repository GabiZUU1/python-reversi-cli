from src.commands.Commands import MakeMoveCommand
from src.domain.Board import Board
from src.domain.Player import PlayerType, PlayerColors
from src.repository.BaseRepo import BaseRepo
from src.repository.MemoryRepo import MemoryRepo
from src.services.BaseService import BaseService
from src.services.BoardService import BoardService
from src.services.GameService import GameService
from src.services.PlayerService import PlayerService


class BotService(BaseService):
    """Class for the service that manages the bot/AI."""
    def __init__(self, repository: BaseRepo, player_service: PlayerService):
        """
        Initialization of the class.
        :param repository: The repository the service will use.
        :param player_service: Player service class for functions related to the players.
        """
        super().__init__(repository)
        self._player_service = player_service
        self._human = self._player_service.get_player_by_type(PlayerType.Real)
        self._bot = self._player_service.get_player_by_type(PlayerType.Computer)

    def minimax(self, alpha: int, beta: int, depth: int, bot_turn: bool, board: Board) -> int:
        """
        Minimax algorithm implementation.
        :param alpha: The best value the maximizer(bot) can guarantee at said level.
        :param beta: The best value the minimizer(player) can guarantee at said level.
        :param depth: Tracks how deep the recursion is. Can be used to limit the search.
        :param bot_turn: Indicates if it's the bot's turn or the player's turn.
        :param board: The current board. Used for finding all possible moves.
        :return: The score of the scenario. 1 if the bot wins, -1 if the human wins, 0 if it ends up in a tie.
        """
        repo = MemoryRepo(board, self._human, self._bot)
        temp_board_service = BoardService(repo)
        temp_game_service = GameService(repo)

        if depth == 5:
            bot_score = temp_game_service.get_score(self._bot)
            human_score = temp_game_service.get_score(self._human)

            if human_score == bot_score:
                return 0
            if human_score > bot_score:
                return -1
            if bot_score > human_score:
                return 1

        if temp_game_service.is_game_over():
            winner = temp_game_service.get_winner()
            if winner is None:
                return 0
            if winner.type == PlayerType.Computer:
                return 1
            if winner.type == PlayerType.Real:
                return -1

        if bot_turn:
            best_score = -99999
            moves = temp_board_service.search_valid_moves_for_players(self._bot)
            for move in moves:
                # Make the move
                row = move[0] + 1
                col = move[1] + 1

                saved_board = temp_board_service.get_board().clone_board()

                # cmd = MakeMoveCommand(temp_board_service, self.__bot, row, col)
                # cmd.execute()
                #
                temp_board_service.make_move(self._bot, row, col)

                # Calculate the score of the move and the upcoming moves with recursivity
                score = self.minimax(alpha, beta, depth + 1, False, temp_board_service.get_board())

                # Reload the board
                temp_board_service.set_board(saved_board)

                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = 99999
            moves = temp_board_service.search_valid_moves_for_players(self._human)
            for move in moves:
                # Make the move
                row = move[0] + 1
                col = move[1] + 1

                saved_board = temp_board_service.get_board().clone_board()

                # cmd = MakeMoveCommand(temp_board_service, self.__human, row, col)
                # cmd.execute()
                #
                temp_board_service.make_move(self._human, row, col)

                # Calculate the score of the move and the upcoming moves with recursivity
                score = self.minimax(alpha, beta, depth + 1, True, temp_board_service.get_board())

                # Reload the board
                temp_board_service.set_board(saved_board)

                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    def find_best_move(self, board: Board) -> (int, int):
        """
        Find the best move for the bot using minimax.
        :param board: The board to find the move on.
        :return: The tuple of the move, with the first item being the row, and the second item being the column.
        """
        best_score = -99999
        best_move = None

        temp_board_service = BoardService(MemoryRepo(board))

        moves = temp_board_service.search_valid_moves_for_players(self._bot)
        for move in moves:
            # Make the move
            row = move[0] + 1
            col = move[1] + 1

            saved_board = temp_board_service.get_board().clone_board()

            # cmd = MakeMoveCommand(temp_board_service, self.__bot, row, col)
            # cmd.execute()
            #
            temp_board_service.make_move(self._bot, row, col)

            # Find the score of the move
            score = self.minimax(-10, 10, 0, False, temp_board_service.get_board())

            # Reload the board
            temp_board_service.set_board(saved_board)

            # Check if the move is the best move
            if score > best_score:
                best_score = score
                best_move = move
        return best_move