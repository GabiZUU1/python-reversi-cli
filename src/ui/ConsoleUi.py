import os
from time import sleep

from src.commands.Commands import CreatePlayerCommand, MakeMoveCommand
from src.domain.Player import PlayerColors, PlayerType
from src.exceptions.Exceptions import ValidationError
from src.services.BotService import BotService
from src.ui.BaseUi import BaseUI, PrintablePieces


class ConsoleUI(BaseUI):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        os.system('cls')
        try:
            while True:
                print("Do you want to play against a bot or a local player?")
                print("1. Against bot")
                print("2. Against local player")
                c = int(input("Enter your choice: "))
                match c:
                    case 1:
                        self.against_bot_ui()
                        break
                    case 2:
                        self.against_player_ui()
                        break
                    case _:
                        os.system('cls')
                        print("Not a valid option, try again!")
                        continue

            os.system('cls')

            self.game_ui()

        except (ValueError, ValidationError) as e:
            print(e)

    def game_ui(self):
        try:
            while True:
                print("□ = black            ■ = white")
                print("X = possible move    O = free piece")

                p1 = self._player_service.get_player_by_color(PlayerColors.Black)
                scores = self._game_service.get_score()
                p2 = self._player_service.get_player_by_color(PlayerColors.White)
                print(f"Score: {p1.name} - {str(scores[0])}; {p2.name} - {str(scores[1])}")
                print("---------------------------------")

                current_player = self._game_service.get_current_player()



                if current_player.type is PlayerType.Real:
                    print(f"It's {current_player.name}'s turn ({current_player.color})!!!!!!!!!!!!")
                    self.print_board(self._board_service.search_valid_moves_for_players(current_player))

                    while True:
                        try:
                            inp = input("Enter the move you want to want to make (row and column separated by a space): ").strip()
                            row = int(inp.split(" ")[0])
                            column = str(inp.split(" ")[1])[0].upper()

                            if column > 'H':
                                raise ValueError
                            elif column.isnumeric():
                                raise ValueError
                            else:
                                column = int(ord(column) - ord('A') + 1)

                            break
                        except ValueError:
                            print("Incorrect input, try again!")
                            continue
                else:
                    print(f"It's {current_player.name}'s turn ({current_player.color})!!!!!!!!!!!!")
                    self.print_board()

                    print("Finding the best move...")
                    clone_board = self._board_service.get_board().clone_board()
                    move = self._bot_service.find_best_move(clone_board)
                    row = move[0] + 1
                    column = move[1] + 1
                    sleep(1)
                    print("Found best move, executing it!")

                try:
                    cmd = MakeMoveCommand(self._board_service, current_player, row, column)
                    cmd.execute()

                    os.system('cls')
                except ValidationError as e:
                    os.system('cls')
                    print(e)
                    continue

                if self._game_service.next_turn():
                    print(f"{self._game_service.get_current_player().name} had no moves. Skipping his turn!")

                if self._game_service.is_game_over():
                    print("!-----------------------------!")
                    print("Game is over!")
                    winner = self._game_service.get_winner()
                    print(f"{winner.name} has won with the score of {self._game_service.get_score(winner)}!")
                    print("!-----------------------------!")
        except ValueError as e:
            os.system('cls')
            print(e)

    def against_bot_ui(self) -> None:
        os.system('cls')
        print("You chose to play against a bot.")

        name = str(input("Enter your name: "))

        cmd = CreatePlayerCommand(self._player_service, name, PlayerColors.Black, PlayerType.Real)
        cmd.execute()

        cmd = CreatePlayerCommand(self._player_service, "Gigel (Bot)", PlayerColors.White, PlayerType.Computer)
        cmd.execute()

        self._bot_service = BotService(self._repo, self._player_service)

    def against_player_ui(self) -> None:
        os.system('cls')
        print("You chose to play against a local player.")

        name = str(input("Enter the name of the first player: "))
        cmd = CreatePlayerCommand(self._player_service, name, PlayerColors.Black, PlayerType.Real)
        cmd.execute()

        name = str(input("Enter the name of the second player: "))
        cmd = CreatePlayerCommand(self._player_service, name, PlayerColors.White, PlayerType.Real)
        cmd.execute()

    def print_board(self, highlighted_pieces: list = None) -> None:
        if highlighted_pieces is None:
            highlighted_pieces = []

        b = self._board_service.get_printable_board()

        print(" ", end = " ")
        for i in range(8):
            print(chr(ord('A') + i), end=" ")
            #print(i + 1, end = " ")
        print()

        for i in range(8):
            print(i + 1, end = " ")
            for j in range(8):
                if (i, j) in highlighted_pieces:
                    print(PrintablePieces.MovePiece.value, end = " ")
                    continue

                match b[i][j]:
                    case "n":
                        print(PrintablePieces.NoPiece.value, end = " ")
                    case "b":
                        print(PrintablePieces.BlackPiece.value, end = " ")
                    case "w":
                        print(PrintablePieces.WhitePiece.value, end = " ")
            print(i + 1)

        print(" ", end=" ")
        for i in range(8):
            print(chr(ord('A') + i), end=" ")
            #print(i + 1, end=" ")
        print()