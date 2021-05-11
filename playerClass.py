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
            column = input(f"{self.letter}'s turn. Column move (1-{game.size}): ")
            line = input(f"{self.letter}'s turn. Line move (1-{game.size}): ")
            try:
                column = int(column) - 1
                line = int(line) - 1
                val = [column, line]
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val
    
    
class AI(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game, profondeur):
        return game.action_IA(profondeur)