import time
import math
from player import *

EMPTY = " "

class TicTacToe():
    def __init__(self, size=12):
        self.size = size
        self.board = self.make_board()
        self.current_winner = None

    def make_board(self):
        return [[EMPTY for i in range(self.size)]for j in  range(self.size)]

    def print_board(self):
        # * Column Number
        print("     | " +
        "  | ".join(f"{i+1:02d}" for i in range(self.size)) + "  |")
        for i in range(self.size):
            for j in range(self.size - 1):
                print("-------", end="")
            print("-")
            for j in range(self.size):
                if j == 0:  # Line Number
                    print(f"{i+1:02d}", end="   | ") 
                print(" " + self.board[i][j], end="  | ")
            print()
        
    def make_move(self, cell, letter):
        if len(cell) != 2:
            return False
        column, line = cell[0], cell[1]
        if self.board[line][column] == EMPTY:
            self.board[line][column] = letter
            if self.winner(column, line, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, column, line, letter):
        # ? Row win
        sameLetter = 0
        start_row = line - 3 if line >= 3 else 0
        end_row = line + 3 if line < self.size - 3 else self.size - 1
        for row in range(start_row, end_row + 1):
            if self.board[row][column] == letter:
                sameLetter += 1
                if sameLetter == 4:
                    return True
            else:
                sameLetter = 0
        
        # ? Column win
        sameLetter = 0
        start_col = column - 3 if column >= 3 else 0
        end_col = column + 3 if column < self.size - 3 else self.size - 1
        for col in range(start_col, end_col + 1):
            if self.board[line][col] == letter:                
                sameLetter += 1
                if sameLetter == 4:
                    return True
            else:
                sameLetter = 0
            
        # ? Lower Diagonal win
        sameLetter = 0
        lower_bound = min(column, line)
        if lower_bound > 4:
            lower_bound = 4
        upper_bound = self.size - max(column, line)
        if upper_bound > 4:
            upper_bound = 4
        
        for i in range(-lower_bound, upper_bound):
            if self.board[line+i][column+i] == letter:
                sameLetter += 1
                if sameLetter == 4:
                    return True
            else:
                sameLetter = 0 
            
        # ? Upper Diagonal win 
        # Col + row -
        sameLetter = 0
        lower_bound = min(column, self.size-1 - line)
        if lower_bound > 3:
            lower_bound = 3
        upper_bound = min(self.size - 1 - column, line) + 1
        if upper_bound > 4:
            upper_bound = 4
        for i in range(-lower_bound, upper_bound):
            if self.board[line-i][column+i] == letter:
                sameLetter += 1
                if sameLetter == 4:
                    return True
            else:
                sameLetter = 0
                
        return False

    def empty_squares(self):
        for col in self.board:
            for cell in col:
                if cell == EMPTY:
                    return True
        return False

    def num_empty_squares(self):
        count_empty_squares = 0
        for col in self.board:
            for cell in col:
                if cell == EMPTY:
                    count_empty_squares += 1
        return count_empty_squares

    def available_moves(self):
        available_moves = []
        for index_col, column in enumerate(self.board):
            for index_line, line in enumerate(column):
                if line == EMPTY:
                    available_moves.append([index_line, index_col])
        return available_moves
        #return [i for i, x in enumerate(self.board) if x == " "]
        
    def evaluate(self):
        pass
    
    def minimax(self, alpha, beta, maximizing, depth):
        pass

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + " makes a move to square {}, {}".format(square[0] + 1, square[1] + 1))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + " wins!")
                return letter
            letter = 'O' if letter == 'X' else 'X'

        #time.sleep(.8)
    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    o_player = HumanPlayer('O')
    x_player = HumanPlayer('X')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
