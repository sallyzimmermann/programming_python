#  x | x | x
#  0 | 0 | 0
#  x | 0 | x
import math
from dataclasses import dataclass

class Board:
    board_mapping = {7: 0, 8: 1, 9: 2,
                     4: 3, 5: 4, 6: 5,
                     1: 6, 2: 7, 3: 8}

    def __init__(self, max_cell_width):
        self.status = [None]*9
        self.width = max_cell_width

    def display(self):
        display = ""
        for count, value in enumerate(self.status):
            if value is None:
                value = " "
            if (count + 1) % 3 == 0:
                display += f"{value}\n"
            else:
                display += f"{value}|"
        print(display)

class TicTacToe:
    possible_wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                     [0, 3, 6], [1, 4, 7], [2, 5, 8],
                     [0, 4, 8], [2, 4, 6]]
    scores = {"X":1,
              "O":-1,
              "tie":0}
    def __init__(self, play_against_computer=True):
        self.play_against_computer = play_against_computer
        self.player_one = Player("X", *self.gather_player_information())
        self.player_two = Player("O", *self.gather_player_information())
        max_cell_width = max(len(self.player_one.sign), len(self.player_two.sign))
        self.board = Board(max_cell_width)
        self.player = self.player_one

    def gather_player_information(self):
        ai = False
        if self.play_against_computer:
            play_against_ai = input("If you want to play against a Computer (will have sign 'X'), answer with 'yes': ")
            if play_against_ai == "yes":
                ai = True
                name = "Computer"
            else:
                name = input(
                    "You are playing against another human (will have the sign 'X'). Please give the first humans name:")
        else:
            name = input("Please give the (second) humans name:")
        return name, ai

    def player_input(self):
        while True:
            print("current board:")
            self.board.display()
            input_value = input("{} choose an unoccupied field:".format(self.player.name))
            try:
                input_value = int(input_value)
                board_index = self.board.board_mapping[input_value]
                if self.board.status[board_index] is None:
                    self.board.status[board_index] = self.player.sign
                    return
            except ValueError:
                print("Input has to be a number.")
            except KeyError:
                print("Input has to be a number betwenn 1 and 9.")

    def check_for_win(self):
        for win in self.possible_wins:
            signs = set(self.board.status[i] for i in win)
            if len(signs) == 1:
                if None in signs:
                    continue
                return signs.pop()
        return False

    def game_over(self):
        return None not in self.board.status

    def minimax(self, is_maximizing):
        winner_sign = self.check_for_win()
        if winner_sign: # Nicht leere Strings evaluieren zu True
            return self.scores[winner_sign]
        elif self.game_over():
            return self.scores["tie"]
        # "X" is maximising, "O" is minimizing
        if is_maximizing:
            max_eval = -math.inf
            for pos in range(0, 9):
                if self.board.status[pos] is None:
                    self.board.status[pos] = "X"
                    eval = self.minimax(False)
                    max_eval = max(max_eval, eval)
                    self.board.status[pos] = None
            return max_eval
        else:
            min_eval = math.inf
            for pos in range(0,9):
                if self.board.status[pos] is None:
                    self.board.status[pos] = "O"
                    eval = self.minimax(True)
                    min_eval = min(min_eval, eval)
                    self.board.status[pos] = None
            return min_eval

    def do_best_move(self, sign):
        best_score = -math.inf if sign == "X" else math.inf
        for pos in range(0, 9):
            if self.board.status[pos] is None:
                self.board.status[pos] = self.player.sign
                score = self.minimax(sign != "X")
                self.board.status[pos] = None
                if (sign == "X" and score > best_score
                    or sign == "O" and score < best_score):
                    best_score = score
                    move_pos = pos
        self.board.status[move_pos] = self.player.sign

    def play(self):
        print("Tic Tac Toe - {} begins.".format(self.player.name))
        print("Choose a field corresponding to the following numbers:")
        print("""
            7 | 8 | 9
            4 | 5 | 6
            1 | 2 | 3
            """)
        while True:
            print("{}'s turn".format(self.player.name))
            if self.player.ai:
                self.do_best_move(self.player.sign)
            else:
                self.player_input()
            if self.check_for_win():
                print("{} has won. Congratulations!".format(self.player.name))
                self.board.display()
                return
            if self.game_over():
                print("Draw. Noone won.")
                self.board.display()
                return

            if self.player == self.player_one:
                self.player = self.player_two
            elif self.player == self.player_two:
                self.player = self.player_one
            else:
                print("something went wrong with assigning players")
                return


@dataclass
class Player:
    sign: str
    name: str
    ai: bool


if __name__ == "__main__":

    Game = TicTacToe()
    Game.play()
