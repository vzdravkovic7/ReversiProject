import copy
import time
TIME_LIMIT = 2.9
import tabela
from heuristika import *

stanje_tabele = tabela.Tabela(8, 8)


def count_time():
    global start_time
    start_time = time.time()


class Game(object):
    def __init__(self):
        self._current_player = ""
        self._opponent = ""
        self._winner = ""
        self.without_option = 0
        self.original_table = {}
        self._game_is_over = False
        self.game_start()

    def game_start(self):
        self._current_player = "Black"
        self._opponent = "White"
        self.passturn(stanje_tabele.create_table_start())

    def is_game_over(self, tabela_za_prebacivanje):
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
        if self._current_player == "Black":  # Player's turn
            self._current_player = "White"
            self._opponent = "Black"
            moves = stanje_tabele.moves(tabela_za_prebacivanje)
            options_list = moves[0]
            options = moves[1]
            if not bool(options):
                self.without_option += 1
                print("Passing turn")
                if self._game_is_over:
                    exit()
                self.passturn(tabela_za_prebacivanje)
            elif self.without_option == 1:
                self.without_option -= 1
            stanje_tabele.print_state(tabela_za_prebacivanje)
            print("Options:")
            for x in options_list:
                for key, value in x.items():
                    print(key + " " + value)
            while True:
                try:
                    option = int(input("Enter option: "))
                    if option in options.keys():
                        new_table = stanje_tabele.make_a_move(options, option)
                        self.passturn(new_table)
                    else:
                        if self.without_option == 1:
                            print("Passing turn")
                        if self._game_is_over:
                            exit()
                        print("Invalid option")
                except:
                    if self.without_option == 1:
                        print("Passing turn")
                    if self._game_is_over:
                        exit()
                    print("Invalid option")

        if self._current_player == "White":  # AI's turn
            self._current_player = "Black"
            self._opponent = "White"
            options = stanje_tabele.AI_moves_copy(tabela_za_prebacivanje)
            if not bool(options):
                self.without_option += 1
                print("Passing turn")
                if self._game_is_over:
                    exit()
                self.passturn(tabela_za_prebacivanje)
            elif self.without_option == 1:
                self.without_option -= 1
            tabela_copy = copy.deepcopy(tabela_za_prebacivanje)
            self.original_table = tabela_copy
            options = stanje_tabele.AI_moves(tabela_za_prebacivanje)
            stanje_tabele.print_state(tabela_za_prebacivanje)
            broj_opcija = []
            for option in options.keys():
                broj_opcija.append(option)
            count_time()
            best_option = self.minimax(tabela_copy, 6, float('-inf'), float('inf'), True)[1]
            new_table = stanje_tabele.make_a_move(options, best_option)
            end_time = time.time()
            time_taken = end_time - start_time
            print("Time taken to make a move for AI: " + str(time_taken))
            self.passturn(new_table)

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
        tabela_copy = copy.deepcopy(node)
        current_time = time.time()
        if current_time - start_time >= TIME_LIMIT:
            return [dynamic_heuristic_evaluation_function(dict_to_list_of_lists(tabela_copy)), 0]
        if depth == 0 or self.is_game_over(tabela_copy):
            board_value = dynamic_heuristic_evaluation_function(dict_to_list_of_lists(tabela_copy))
            stanje_tabele.update_table(self.original_table)
            return [board_value, 0]
        if maximizingPlayer:    # AI
            value = float('-inf')
            options = stanje_tabele.AI_moves_copy(tabela_copy)
            best_option = 0
            for option in options.keys():
                copied_dict = tabela_copy
                copied_dict = stanje_tabele.make_a_move_copy(options, option)
                unpack = self.minimax(copied_dict, depth - 1, alpha, beta, False)
                if unpack[0] > value:
                    value = unpack[0]
                    best_option = option
                alpha = max(alpha, value)
                if value >= beta:
                    break  # β cutoff
            return value, best_option
        else:   # Minimizing player - Human
            value = float('inf')
            options = stanje_tabele.moves_copy(tabela_copy)[1]
            best_option = 0
            for option in options.keys():
                copied_dict = tabela_copy
                copied_dict = stanje_tabele.make_a_move_copy(options, option)
                unpack = self.minimax(copied_dict, depth - 1, alpha, beta, True)
                if unpack[0] < value:
                    value = unpack[0]
                    best_option = option
                beta = min(beta, value)
                if value <= alpha:
                    break  # α cutoff
            return value, best_option
