import tabela
from heuristika import *

stanje_tabele = tabela.Tabela(8, 8)


class Game(object):
    def __init__(self):
        self._current_player = ""
        self._opponent = ""
        self._winner = ""
        self.without_option = 0
        self._game_is_over = False
        self.game_start()

    def game_start(self):
        self._current_player = "Black"
        self._opponent = "White"
        self.passturn(stanje_tabele.make_a_move_player(stanje_tabele.create_table_start()))

    def is_game_over(self, tabela_za_prebacivanje):
        if stanje_tabele.lost_options(tabela_za_prebacivanje):
            self.without_option += 1
            print("Passing turn")
        elif self.without_option == 1:
            self.without_option -= 1
        stanje_tabele.update_table(tabela_za_prebacivanje)
        discs = stanje_tabele.count_discs()
        black_discs = discs[0]
        white_discs = discs[1]
        if black_discs == 0 or white_discs == 0 or (black_discs + white_discs) == 64 or self.without_option == 2:
            return True
        else:
            return False

    def passturn(self, tabela_za_prebacivanje):
        discs = stanje_tabele.count_discs()
        black_discs = discs[0]
        white_discs = discs[1]
        if self.is_game_over(tabela_za_prebacivanje):
            end_table = stanje_tabele.update_table(tabela_za_prebacivanje)
            print("The end")
            print("Final score")
            print("_______________")
            print("Player black: " + str(black_discs))
            print("Player white: " + str(white_discs))
            print("_______________")
            stanje_tabele.print_state(end_table)
            self._game_is_over = True
            self.game_over(black_discs, white_discs)
        else:
            print("Current score")
            print("_______________")
            print("Player black: " + str(black_discs))
            print("Player white: " + str(white_discs))
            print("_______________")
        if self._current_player == "Black":
            self._current_player = "White"
            self._opponent = "Black"
            self.passturn(stanje_tabele.make_a_move_AI(tabela_za_prebacivanje))

        if self._current_player == "White":
            self._current_player = "Black"
            self._opponent = "White"
            self.passturn(stanje_tabele.make_a_move_player(tabela_za_prebacivanje))

    def game_over(self, blacks, whites):
        if blacks > whites:
            self._winner = "Black"
            print(self._winner + " is the winner with " + str(blacks) + "pts")
        elif whites > blacks:
            self._winner = "White"
            print(self._winner + " is the winner with " + str(whites) + "pts")
        else:
            print("Its a tie! Both players have " + str(blacks) + "pts")
        exit()

    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.is_game_over(node):
            return dynamic_heuristic_evaluation_function(node)
        if maximizingPlayer:
            value = float('-inf')
            for child in node.children:
                value = max(value, self.minimax(child, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if value >= beta:
                    break  # β cutoff
            return value
        else:
            value = float('inf')
            for child in node.children:
                value = min(value, self.minimax(child, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if value <= alpha:
                    break  # α cutoff
            return value
