# -*- coding: utf-8 -*-
"""
Created on Fri May 14 14:10:43 2021

@author: kintr
"""

import numpy as np
import time

EMPTY = " "
AI = "X"
HUMAN = "O"


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            column = input(
                f"{self.letter}'s turn. Column move (1-{game.size}): \nType cancel to cancel last move ")
            if column.lower() == "cancel":
                return column
            line = input(f"{self.letter}'s turn. Line move (1-{game.size}): ")
            try:
                column = int(column) - 1
                line = int(line) - 1
                val = [column, line]
                if val not in available_moves(game.board):
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class AIPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game, profondeur):
        if game.num_empty_squares() == game.size**2:
            return [int(game.size/2), int(game.size/2)]
        return game.action_IA(profondeur)


class TicTacToe():
    def __init__(self, size=12):
        self.size = size
        self.board = self.make_board()
        self.current_winner = None

    def make_board(self):
        return [[EMPTY for i in range(self.size)]for j in range(self.size)]

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
            if winner(self.board, column, line, letter):
                self.current_winner = letter
            return True
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

    def action_IA(self, profondeur):
        start_time = time.time()
        beta = np.inf
        alpha = -np.inf
        best_score = - np.inf
        best_move = []
        smallest_board, min_index = get_smallest_board(self.board)
        for move in available_moves(smallest_board):
            column, line = move[0], move[1]
            smallest_board[line][column] = AI
            score = self.minimax(profondeur - 1, False,
                                 alpha, beta, column, line, smallest_board)
            smallest_board[line][column] = EMPTY

            if(score > best_score):
                best_score = score
                best_move = [column + min_index, line + min_index]
        end_time = time.time()
        print(f"Temps IA : {end_time - start_time}")
        return best_move

    def minimax(self, profondeur, maximize, alpha, beta, column, line, smallest_board):
        # Dernier coup joué par l'humain s'il faut maximiser
        player = HUMAN if maximize else AI
        is_end = winner(smallest_board, column, line, player)

        if(is_end):
            return 9999999 if player == AI else -9999999  # Score de 9999999 si l'IA gagne

        if profondeur == 0:
            return evaluate_board(smallest_board)

        if(maximize):
            best_score = - np.inf
            score = None
            for move in available_moves(smallest_board):
                column, line = move[0], move[1]
                smallest_board[line][column] = AI
                score = self.minimax(profondeur - 1, False,
                                     alpha, beta, column, line, smallest_board)
                smallest_board[line][column] = EMPTY
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if(beta <= alpha):
                    break
            return best_score
        else:
            best_score = np.inf
            score = None
            for move in available_moves(smallest_board):
                column, line = move[0], move[1]
                smallest_board[line][column] = HUMAN
                score = self.minimax(profondeur - 1, True,
                                     alpha, beta, column, line, smallest_board)
                smallest_board[line][column] = EMPTY
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if(beta <= alpha):
                    break
            return best_score

def winner(board, column, line, letter):
    # ? Row win
    size = len(board)
    sameLetter = 0
    start_row = line - 3 if line >= 3 else 0
    end_row = line + 3 if line < size - 3 else size - 1
    for row in range(start_row, end_row + 1):
        if board[row][column] == letter:
            sameLetter += 1
            if sameLetter == 4:
                return True
        else:
            sameLetter = 0

    # ? Column win
    sameLetter = 0
    start_col = column - 3 if column >= 3 else 0
    end_col = column + 3 if column < size - 3 else size - 1
    for col in range(start_col, end_col + 1):
        if board[line][col] == letter:
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
    upper_bound = size - max(column, line)
    if upper_bound > 4:
        upper_bound = 4

    for i in range(-lower_bound, upper_bound):
        if board[line+i][column+i] == letter:
            sameLetter += 1
            if sameLetter == 4:
                return True
        else:
            sameLetter = 0

    # ? Upper Diagonal win
    # Col + row -
    sameLetter = 0
    lower_bound = min(column, size-1 - line)
    if lower_bound > 3:
        lower_bound = 3
    upper_bound = min(size - 1 - column, line) + 1
    if upper_bound > 4:
        upper_bound = 4
    for i in range(-lower_bound, upper_bound):
        if board[line-i][column+i] == letter:
            sameLetter += 1
            if sameLetter == 4:
                return True
        else:
            sameLetter = 0

    return False

def get_smallest_board(board):
    size = len(board)
    min_index_line = size
    max_index_line = 0
    min_index_column = size
    max_index_column = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] != EMPTY:
                min_index_line = min(i, min_index_line)
                max_index_line = max(i, max_index_line)
                min_index_column = min(j, min_index_column)
                max_index_column = max(j, max_index_column)

    min_index_line -= 2
    max_index_line += 2
    min_index_column -= 2
    max_index_column += 2

    if min_index_line < 0:
        min_index_line = 0
    if max_index_line > size:
        max_index_line = size
    if min_index_column < 0:
        min_index_column = 0
    if max_index_column > size:
        max_index_column = size
    min_index = min(min_index_column, min_index_line)
    max_index = max(max_index_column, max_index_line)

    return [[board[i][j] for j in range(int(min_index), int(max_index))] for i in range(int(min_index), int(max_index))], min_index

def available_moves(board):
    available_moves = []
    for index_col, column in enumerate(board):
        for index_line, line in enumerate(column):
            if line == EMPTY:
                available_moves.append([index_line, index_col])
    return available_moves

def evaluate_board(board):
    letters_3_boards_2 = 100
    letters_3_boards_1 = 15
    letters_2_boards_2 = 5
    score = 0
    is_case_precedente_ligne_empty = False
    is_case_precedente_colonne_empty = False
    is_case_precedente_diag_empty_mont_g = False
    is_case_precedente_diag_empty_mont_d = False
    same_letter_ligne = 0
    same_letter_colonne = 0
    same_letter_diag_mont_g = 0
    same_letter_diag_mont_d = 0
    size = len(board)
    # Line and Column Score
    for i in range(size):
        for j in range(size):
            case_ligne = board[i][j]
            case_precedente_ligne = board[i][j - 1]
            case_colonne = board[j][i]
            case_precedente_colonne = board[j - 1][i]

            if j == 0:
                if case_ligne == EMPTY:
                    is_case_precedente_ligne_empty = True
                else:
                    is_case_precedente_ligne_empty = False
                    same_letter_ligne = 1

                if case_colonne == EMPTY:
                    is_case_precedente_colonne_empty = True
                else:
                    is_case_precedente_colonne_empty = False
                    same_letter_colonne = 1
            else:
                if case_ligne == EMPTY:
                    if same_letter_ligne == 3:
                        if is_case_precedente_ligne_empty:
                            score += letters_3_boards_2 if case_precedente_ligne == AI else -letters_3_boards_2
                        else:
                            score += letters_3_boards_1 if case_precedente_ligne == AI else -letters_3_boards_1
                    elif same_letter_ligne == 2 and is_case_precedente_ligne_empty:
                        score += letters_2_boards_2 if case_precedente_ligne == AI else -letters_2_boards_2
                    same_letter_ligne = 0
                    is_case_precedente_ligne_empty = True
                else:
                    if case_ligne == case_precedente_ligne:
                        same_letter_ligne += 1
                        if j == size - 1:
                            if same_letter_ligne == 3 and is_case_precedente_ligne_empty:
                                score += letters_3_boards_1 if case_ligne == AI else -letters_3_boards_1
                    else:
                        if same_letter_ligne == 3 and is_case_precedente_ligne_empty:
                            score += letters_3_boards_1 if case_precedente_ligne == AI else -letters_3_boards_1
                        if case_precedente_ligne != EMPTY:
                            is_case_precedente_ligne_empty = False
                        same_letter_ligne = 1

                # Column
                if case_colonne == EMPTY:
                    if same_letter_colonne == 3:
                        if is_case_precedente_colonne_empty:
                            score += letters_3_boards_2 if case_precedente_colonne == AI else -letters_3_boards_2
                        else:
                            score += letters_3_boards_1 if case_precedente_colonne == AI else -letters_3_boards_1
                    elif same_letter_colonne == 2 and is_case_precedente_colonne_empty:
                        score += letters_2_boards_2 if case_precedente_colonne == AI else -letters_2_boards_2
                    same_letter_colonne = 0
                    is_case_precedente_colonne_empty = True
                else:
                    if case_colonne == case_precedente_colonne:
                        same_letter_colonne += 1
                        if j == size - 1:
                            if same_letter_colonne == 3 and is_case_precedente_colonne_empty:
                                score += letters_3_boards_1 if case_colonne == AI else -letters_3_boards_1
                    else:
                        if same_letter_colonne == 3 and is_case_precedente_colonne_empty:
                            score += letters_3_boards_1 if case_precedente_colonne == AI else -letters_3_boards_1
                        if case_precedente_colonne != EMPTY:
                            is_case_precedente_colonne_empty = False
                        same_letter_colonne = 1   
                        
    for i in range(size):
        for j in range(size):
            for k in range(3):
                
                case_diag_mont_g = board[i][j]
                case_diag_mont_d = board[j][i]
                #case_precedente_diag_empty_desc_g = board[i + k][j - k]
                #case_precedente_diag_empty_desc_d = board[i + k][j + k]
    
                if j == 0:                    
                    if case_diag_mont_g == EMPTY:
                        is_case_precedente_diag_empty_mont_g = True
                    else:
                        is_case_precedente_diag_empty_mont_g = False
                        same_letter_diag_mont_g = 1
    
                    if case_diag_mont_d == EMPTY:
                        is_case_precedente_diag_empty_mont_d = True
                    else:
                        is_case_precedente_diag_empty_mont_d = False
                        same_letter_diag_mont_d = 1                
                else:
                    case_precedente_diag_mont_g = board[i - k][j - k]
                    #case_precedente_diag_mont_d = board[(size-1)-j][i + k]
                    case_precedente_diag_mont_d = board[j - k][i + k]
                    if case_diag_mont_g == EMPTY:
                        if same_letter_diag_mont_g == 3:
                            if is_case_precedente_diag_empty_mont_g:
                                score += letters_3_boards_2 if case_precedente_diag_mont_g == AI else -letters_3_boards_2
                            else:
                                score += letters_3_boards_1 if case_precedente_diag_mont_g == AI else -letters_3_boards_1
                        elif same_letter_diag_mont_g == 2 and is_case_precedente_diag_empty_mont_g:
                            score += letters_2_boards_2 if case_precedente_diag_mont_g == AI else -letters_2_boards_2
                        same_letter_diag_mont_g = 0
                        is_case_precedente_diag_empty_mont_g = True
                    else:
                        if case_diag_mont_g == case_precedente_diag_mont_g:
                            same_letter_diag_mont_g += 1
                            if j == size - 1:
                                if same_letter_diag_mont_g == 3 and is_case_precedente_diag_empty_mont_g:
                                    score += letters_3_boards_1 if case_diag_mont_g == AI else -letters_3_boards_1
                        else:
                            if same_letter_diag_mont_g == 3 and is_case_precedente_diag_empty_mont_g:
                                score += letters_3_boards_1 if case_precedente_diag_mont_g == AI else -letters_3_boards_1
                            if case_precedente_diag_mont_g != EMPTY:
                                is_case_precedente_diag_empty_mont_g = False
                            same_letter_diag_mont_g = 1
                            
                            
                    if case_diag_mont_d == EMPTY:
                        if same_letter_diag_mont_d == 3:
                            if is_case_precedente_diag_empty_mont_d:
                                score += letters_3_boards_2 if case_precedente_diag_mont_d == AI else -letters_3_boards_2
                            else:
                                score += letters_3_boards_1 if case_precedente_diag_mont_d == AI else -letters_3_boards_1
                        elif same_letter_diag_mont_d == 2 and is_case_precedente_diag_empty_mont_d:
                            score += letters_2_boards_2 if case_precedente_diag_mont_d == AI else -letters_2_boards_2
                        same_letter_diag_mont_d = 0
                        is_case_precedente_diag_empty_mont_d = True
                    else:
                        if case_diag_mont_d == case_precedente_diag_mont_d:
                            same_letter_diag_mont_d += 1
                            if j == size - 1:
                                if same_letter_diag_mont_d == 3 and is_case_precedente_diag_empty_mont_d:
                                    score += letters_3_boards_1 if case_diag_mont_d == AI else -letters_3_boards_1
                        else:
                            if same_letter_diag_mont_d == 3 and is_case_precedente_diag_empty_mont_d:
                                score += letters_3_boards_1 if case_precedente_diag_mont_d == AI else -letters_3_boards_1
                            if case_precedente_diag_mont_d != EMPTY:
                                is_case_precedente_diag_empty_mont_d = False
                            same_letter_diag_mont_d = 1              
                
        #double boucle pour les diags
    #technique +- k, attention limites du tableau !!!
    return score

def play(game, ai_player, human_player, start_player):
    game.print_board()
    letter = start_player
    last_moves = []
    while game.empty_squares():
        nb_empty_cells = game.num_empty_squares()

        profondeur = 4
        if letter == HUMAN:
            square = human_player.get_move(game)
            if square == "cancel":
                last_move = last_moves.pop()
                game.board[last_move[1]][last_move[0]] = EMPTY
                print(last_move)
                last_move = last_moves.pop()
                game.board[last_move[1]][last_move[0]] = EMPTY
                game.print_board()
        else:
            square = ai_player.get_move(game, profondeur)

        if game.make_move(square, letter):
            last_moves.append(square)
            print(last_moves)
            print(
                f"{letter} makes a move to square {square[0] + 1}, {square[1] + 1}")
            game.print_board()
            print('')

            if game.current_winner:
                print(letter + " wins!")
                return letter
            letter = HUMAN if letter == AI else AI

    print('It\'s a tie!')

if __name__ == '__main__':
    ai_player = AIPlayer(AI)
    human_player = HumanPlayer(HUMAN)
    game = TicTacToe()
    play(game=game, ai_player=ai_player,
         human_player=human_player, start_player=AI)
