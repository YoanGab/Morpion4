import playerClass as player
import numpy as np

EMPTY = " "
AI = "X"
HUMAN = "O"

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

    def action_IA(self, profondeur):
        beta = np.inf
        alpha = -np.inf
        best_score = - np.inf
        best_move = []
        for move in self.available_moves():
            column, line = move[0], move[1]
            self.board[line][column] = AI
            score = self.minimax(profondeur - 1, False, alpha, beta, column, line)
            self.board[line][column] = EMPTY
            
            if(score > best_score):
                best_score = score
                best_move = [column, line]
        return best_move
    
    # TODO Calculer le score du plateau
    def evaluate_board(self):
        letters_3 = 10
        letters_2 = 3
        score = 0
        for i in range(self.size):
            same_letter = 0
            for j in range(self.size):
                if same_letter == 0:
                    if self.board[i][j] != EMPTY:
                        same_letter = 1
                else:
                    if self.board[i][j] != EMPTY:
                        if self.board[i][j] == self.board[i][j - 1]:
                            same_letter += 1
                        else:
                            if same_letter == 3:
                                if self.board[i][j-1] == AI:
                                    score += letters_3
                                else:
                                    score -= letters_3
                            elif same_letter == 2:
                                if self.board[i][j - 1] == AI:
                                    score += letters_2
                                else:
                                    score -= letters_2
                            same_letter = 1
                    else:
                        if same_letter == 3:
                            if self.board[i][j - 1] == AI:
                                score += letters_3
                            else:
                                score -= letters_3
                        elif same_letter == 2:
                            if self.board[i][j - 1] == AI:
                                score += letters_2
                            else:
                                score -= letters_2
                        same_letter = 0
                    if j == self.size - 1:
                        if same_letter == 3:
                            if self.board[i][j - 1] == AI:
                                score += letters_3
                            else:
                                score -= letters_3
                        elif same_letter == 2:
                            if self.board[i][j - 1] == AI:
                                score += letters_2
                            else:
                                score -= letters_2                             
        return score       
    
    def minimax(self, profondeur, maximize, alpha, beta, column, line):
        player = HUMAN if maximize else AI # Dernier coup joué par l'humain s'il faut maximiser
        is_end = self.winner(line, column, player)
        if(is_end):
            return 9999999 if player == AI else -9999999  # Score de 9999999 si l'IA gagne

        if profondeur == 0:
            return self.evaluate_board()
        
        if(maximize):
            best_score = - np.inf
            score = None
            for move in self.available_moves():
                column, line = move[0], move[1]
                self.board[line][column] = AI
                score = self.minimax(profondeur - 1, False, alpha, beta, column, line)
                self.board[line][column] = EMPTY
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if(beta <= alpha):
                    break
            return best_score
        else:
            best_score = np.inf
            score = None
            for move in self.available_moves():
                column, line = move[0], move[1]
                self.board[line][column] = HUMAN
                score = self.minimax(profondeur - 1, True, alpha, beta, column, line)
                self.board[line][column] = EMPTY
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if(beta <= alpha):
                    break
            return best_score


def play(game, ai_player, human_player, start_player):
    game.print_board()

    letter = start_player
    while game.empty_squares():
        nb_empty_cells = game.num_empty_squares()
        #TODO Calculer la profondeur en fonction du nombre de cases restantes
        profondeur = np.ceil((game.size**2 - nb_empty_cells) / 35)
        
        if letter == HUMAN:
            square = human_player.get_move(game)
        else:
            square = ai_player.get_move(game, profondeur)

        if game.make_move(square, letter):
            print(f"{letter} makes a move to square {square[0] + 1}, {square[1] + 1}")
            game.print_board()
            print('')

            if game.current_winner:
                print(letter + " wins!")
                return letter
            letter = HUMAN if letter == AI else AI

    print('It\'s a tie!')

if __name__ == '__main__':
    ai_player = player.AI(AI)
    human_player = player.HumanPlayer(HUMAN)
    game = TicTacToe()
    play(game=game, ai_player=ai_player, human_player=human_player, start_player=AI)
