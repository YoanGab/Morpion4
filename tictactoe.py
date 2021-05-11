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
            self.board[move[0]][move[1]] == AI
            score = self.minimax(profondeur, False, alpha, beta, move[0], move[1])
            self.board[move[0]][move[1]] == EMPTY
            if(score > best_score):
                best_score = score
                best_move = [move[0], move[1]]
        return best_move


        """
        Calcule le score du plateau (score en fonction du nombre de X à la suite et du nombre de O à la suite)
        """
    def score_tableau(self):
        return 1
    
    def minimax(self, profondeur, maximize, alpha, beta, line, column):
        letter = HUMAN if maximize else AI
        Fin = self.winner(column, line, letter)
        if(Fin):
            return np.inf if letter == AI else -np.inf

        if profondeur == 0:
            return self.score_tableau()
        
        if(maximize):
            Bscore = - np.inf
            score = None
            for i in range(self.size):
                for j in range(self.size):
                    if (self.board[i][j] == EMPTY):
                        self.board[i][j] = AI
                        score = self.minimax(profondeur - 1, False, alpha, beta, i, j)
                        self.board[i][j] = EMPTY
                        Bscore = max(score, Bscore)
                        alpha = max(alpha, Bscore)
                        if(beta <= alpha):
                            break
            return Bscore
        else:
            Bscore = np.inf
            score = None
            for i in range(self.size):
                for j in range(self.size):
                    if (self.board[i][j] == EMPTY):
                        self.board[i][j] = HUMAN
                        score = self.minimax(profondeur - 1, True, alpha, beta, i, j)
                        self.board[i][j] = EMPTY
                        Bscore = min(score, Bscore)
                        beta = min(beta, Bscore)
                        if(beta <= alpha):
                            break
            return Bscore


def play(game, ai_player, human_player, profondeur):
    game.print_board()

    letter = AI
    while game.empty_squares():
        if letter == HUMAN:
            square = human_player.get_move(game)
        else:
            square = ai_player.get_move(game, profondeur)

        if game.make_move(square, letter):
            print(f"{letter} makes a move to square {square[0] + 1}, {square[1] + 1}")
            #print(letter + " makes a move to square {}, {}".format(square[0] + 1, square[1] + 1))
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
    t = TicTacToe()
    play(t, ai_player, human_player, profondeur=1)
