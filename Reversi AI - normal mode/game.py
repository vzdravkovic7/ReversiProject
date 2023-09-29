import copy
import time
import tabela
from heuristika import *
import pygame
import sys

hand_cursor = pygame.image.load("hand_cursor.png")

cursor_size = (20, 20)  # Set the desired size
hand_cursor = pygame.transform.scale(hand_cursor, cursor_size)

TIME_LIMIT = 2.9

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
WIDTH, HEIGHT = 400, 500

# Game board parameters
ROWS = 8
COLUMNS = 8
CELL_SIZE = 60

stanje_tabele = tabela.Tabela(8, 8)


def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        for x in value.keys():
            if x == target_value:
                return key
    return None


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col


def is_mouse_over_valid_move(mouse_pos, valid_moves):
    for move in valid_moves.values():
        for x in move.keys():
            row, col = x
            if row * CELL_SIZE <= mouse_pos[1] <= (row + 1) * CELL_SIZE and col * CELL_SIZE <= mouse_pos[0] <= (col + 1) * CELL_SIZE:
                if stanje_tabele.get_table_value(row, col) == "W" or stanje_tabele.get_table_value(row, col) == "B":
                    return False
                return True
    return False


def count_time():
    global start_time
    start_time = time.time()


class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((COLUMNS * CELL_SIZE, ROWS * CELL_SIZE + 100))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Player Black's turn", True, WHITE)
        self.text_rect = self.text.get_rect(center=(COLUMNS * CELL_SIZE // 2, 510))
        self.screen.blit(self.text, self.text_rect)
        self.font2 = pygame.font.Font(None, 24)
        self.text2 = self.font2.render(" ", True, WHITE)
        self.text2_rect = self.text2.get_rect(center=(COLUMNS * CELL_SIZE // 2 - 170, 550))
        self.screen.blit(self.text2, self.text2_rect)
        pygame.display.set_caption("Reversi - Player vs AI - normal mode")
        self.clock = pygame.time.Clock()
        self._current_player = ""
        self._opponent = ""
        self._winner = ""
        self.valid_options = {}
        self.without_option = 0
        self.original_table = {}
        self._game_is_over = False
        self.running = True
        self.game_start()

    def update(self):
        if not self._game_is_over:
            self.draw_board()
            if self._current_player == "Black":
                self.draw_valid_moves(self.valid_options)
        else:
            self.screen.fill(DARK_GREEN)
            font = pygame.font.Font(None, 36)
            end_text = font.render("Game Over", True, WHITE)
            end_rect = end_text.get_rect(center=(WIDTH // 2 + 35, HEIGHT // 2 - 40))
            self.screen.blit(end_text, end_rect)

            play_again_text = font.render("Play Again", True, WHITE)
            play_again_rect = play_again_text.get_rect(center=(WIDTH // 2 + 35, HEIGHT // 2 + 30))
            pygame.draw.rect(self.screen, BLUE, play_again_rect)
            self.screen.blit(play_again_text, play_again_rect)
            pygame.display.flip()
        pygame.display.update()

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                color = GREEN if (row + col) % 2 == 0 else DARK_GREEN
                pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                piece = stanje_tabele.get_table_value(row, col)
                if piece != 0:
                    if piece == "W":
                        color = WHITE
                    elif piece == "B":
                        color = BLACK
                    pygame.draw.circle(self.screen, color, (col * CELL_SIZE + CELL_SIZE // 2,
                                                            row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    def draw_valid_moves(self, moves):
        for move in moves.values():
            for x in move.keys():
                row, col = x
                if stanje_tabele.get_table_value(row, col) == "W" or stanje_tabele.get_table_value(row, col) == "B":
                    continue
                else:
                    pygame.draw.circle(self.screen, BLUE,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 10)

    def handle_events(self, moves):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if stanje_tabele.if_is_in_valid_moves(moves, row, col):
                    option = (list(moves.values())).index((row, col))
                    new_table = stanje_tabele.make_a_move(moves, option)
                    self.passturn(new_table)
                else:
                    if self.without_option == 1:
                        print("Passing turn")
                    if self._game_is_over:
                        exit()
                    print("Invalid option")

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

    def print_score(self, black_discs, white_discs):
        print("Current score")
        print("_______________")
        self.text2 = self.font2.render(
            "Current score - Player black: " + str(black_discs) + " Player white: " + str(
                white_discs), True, WHITE)
        self.screen.blit(self.text2, self.text2_rect)
        print("Player black: " + str(black_discs))
        print("Player white: " + str(white_discs))
        print("_______________")

    def print_pass_turn(self, black_discs, white_discs):
        print("Passing turn")
        self.screen.fill(BLACK)
        self.text = self.font.render("Passing turn", True, WHITE)
        self.screen.blit(self.text, self.text_rect)
        self.text2 = self.font2.render(
            "Current score - Player black: " + str(black_discs) + " Player white: " + str(
                white_discs), True, WHITE)
        self.screen.blit(self.text2, self.text2_rect)
        pygame.time.delay(1000)

    def print_invalid_option(self, black_discs, white_discs):
        print("Invalid option")
        self.screen.fill(BLACK)
        self.text = self.font.render("Invalid option", True, WHITE)
        self.screen.blit(self.text, self.text_rect)
        self.text2 = self.font2.render(
            "Current score - Player black: " + str(black_discs) + " Player white: " + str(
                white_discs), True, WHITE)
        self.screen.blit(self.text2, self.text2_rect)

    def print_final_score(self, black_discs, white_discs, end_table):
        print("The end")
        print("Final score")
        print("_______________")
        self.text2 = self.font2.render("The end. Final score - Player black: " + str(
            black_discs) + " Player white: " + str(white_discs), True, WHITE)
        self.screen.blit(self.text2, self.text2_rect)
        print("Player black: " + str(black_discs))
        print("Player white: " + str(white_discs))
        print("_______________")
        stanje_tabele.print_state(end_table)
        pygame.time.delay(1000)
        self.game_over(black_discs, white_discs)
        self._game_is_over = True

    def passturn(self, tabela_za_prebacivanje):
        print("Welcome!")
        print()
        print("Player Black's turn")
        discs = stanje_tabele.count_discs()
        black_discs = discs[0]
        white_discs = discs[1]
        if self.is_game_over(tabela_za_prebacivanje):
            end_table = stanje_tabele.update_table(tabela_za_prebacivanje)
            self.print_final_score(black_discs, white_discs, end_table)
        else:
            self.print_score(black_discs, white_discs)
        stanje_tabele.print_state(tabela_za_prebacivanje)

        while self.running:
            pygame.display.flip()
            self.clock.tick(30)

            # Get the current mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculate the position to draw the custom cursor image
            cursor_x = mouse_x - hand_cursor.get_width() // 2
            cursor_y = mouse_y - hand_cursor.get_height() // 2

            options = {}
            if self._current_player == "Black":
                moves = stanje_tabele.moves(tabela_za_prebacivanje)
                options = moves[1]
            # else:
            #     moves = stanje_tabele.AI_moves(tabela_za_prebacivanje)
            # options = moves[1]
            if not bool(options):
                self.without_option += 1
                self.print_pass_turn(black_discs, white_discs)
                # if self._game_is_over:
                #     exit()
            elif self.without_option == 1:
                self.without_option -= 1
            self.valid_options = options
            self.update()
            if self.without_option == 2:
                # self.running = False
                discs = stanje_tabele.count_discs()
                black_discs = discs[0]
                white_discs = discs[1]
                end_table = stanje_tabele.update_table(tabela_za_prebacivanje)
                self.print_final_score(black_discs, white_discs, end_table)
                pygame.time.delay(3000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self._game_is_over:
                        if play_again_rect.collidepoint(event.pos):
                            self.text_rect = self.text.get_rect(center=(COLUMNS * CELL_SIZE // 2 - 25, 510))
                            self.screen.fill(BLACK)
                            self.text = self.font.render("Player Black's turn", True, WHITE)
                            self.screen.blit(self.text, self.text_rect)
                            # self.screen.blit(self.text2, self.text2_rect)
                            # Reset the game state

                            self._game_is_over = False
                            self._current_player = ""
                            self._opponent = ""
                            self._winner = ""
                            self.valid_options = {}
                            self.without_option = 0
                            self.game_start()

                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)

                    if self._current_player == "Black":  # Player Black's turn
                        self.screen.fill(BLACK)
                        self.text = self.font.render("Player White's turn", True, WHITE)
                        self.screen.blit(self.text, self.text_rect)
                        print("Player White's turn:")
                        if stanje_tabele.if_is_in_valid_moves(self.valid_options, row,
                                                              col) and stanje_tabele.get_table_value(row,
                                                                                                     col) != "W" and stanje_tabele.get_table_value(
                            row, col) != "B":
                            option = find_key_by_value(self.valid_options, (row, col))
                            new_table = stanje_tabele.make_a_move(self.valid_options, option)
                            stanje_tabele.update_table(new_table)
                            self.valid_options = {}
                            self._current_player = "White"
                            self._opponent = "Black"
                            discs = stanje_tabele.count_discs()
                            black_discs = discs[0]
                            white_discs = discs[1]
                            if self.is_game_over(tabela_za_prebacivanje):
                                end_table = stanje_tabele.update_table(tabela_za_prebacivanje)
                                self.print_final_score(black_discs, white_discs, end_table)
                                # pygame.time.delay(3000)
                            else:
                                self.print_score(black_discs, white_discs)
                            stanje_tabele.print_state(new_table)
                            self.update()
                        else:
                            if self.without_option == 1:
                                self.print_pass_turn(black_discs, white_discs)
                            # if self._game_is_over:
                            #     exit()
                            self.print_invalid_option(black_discs, white_discs)

                            continue

                    pygame.time.delay(250)
                    # AI's turn
                    self.screen.fill(BLACK)
                    self.text = self.font.render("Player Black's turn", True, WHITE)
                    self.screen.blit(self.text, self.text_rect)
                    print("Player Black's turn:")

                    options = stanje_tabele.AI_moves_copy(tabela_za_prebacivanje)
                    if bool(options):
                        tabela_copy = copy.deepcopy(tabela_za_prebacivanje)
                        self.original_table = tabela_copy
                        options = stanje_tabele.AI_moves(tabela_za_prebacivanje)
                        stanje_tabele.print_state(tabela_za_prebacivanje)
                        broj_opcija = []
                        for option in options.keys():
                            broj_opcija.append(option)
                        if len(broj_opcija) > 10:
                            depth = 2
                        elif len(broj_opcija) > 4:
                            depth = 3
                        else:
                            depth = 5
                        count_time()
                        best_option = self.minimax(tabela_copy, depth, float('-inf'), float('inf'), True)[1]
                        new_table = stanje_tabele.make_a_move(options, best_option)
                        end_time = time.time()
                        time_taken = end_time - start_time
                        print("Time taken to make a move for AI: " + str(time_taken))
                        # self.passturn(new_table)
                        # new_table = stanje_tabele.make_a_move_AI(options)
                        stanje_tabele.update_table(new_table)
                        self.valid_options = {}
                        self._current_player = "Black"
                        self._opponent = "White"
                        discs = stanje_tabele.count_discs()
                        black_discs = discs[0]
                        white_discs = discs[1]
                        if self.is_game_over(tabela_za_prebacivanje):
                            end_table = stanje_tabele.update_table(tabela_za_prebacivanje)
                            self.print_final_score(black_discs, white_discs, end_table)
                            # pygame.time.delay(3000)
                        else:
                            self.print_score(black_discs, white_discs)
                        stanje_tabele.print_state(new_table)
                        # self.update()
                    else:
                        if self.without_option == 1:
                            self.print_pass_turn(black_discs, white_discs)
                        # if self._game_is_over:
                        #     exit()
                        self.print_invalid_option(black_discs, white_discs)

            if not self._game_is_over:

                self.update()

                if is_mouse_over_valid_move(pygame.mouse.get_pos(), self.valid_options):
                    pygame.mouse.set_visible(False)
                    self.screen.blit(hand_cursor, (cursor_x, cursor_y))
                    # pygame.mouse.set_cursor(*pygame.cursors.diamond)  # Change to a hand cursor
                else:
                    pygame.mouse.set_visible(True)
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)  # Change to the default arrow cursor

            else:
                self.screen.fill(DARK_GREEN)
                font = pygame.font.Font(None, 36)
                end_text = font.render("Game Over", True, WHITE)
                end_rect = end_text.get_rect(center=(WIDTH // 2 + 35, HEIGHT // 2 - 40))
                self.screen.blit(end_text, end_rect)

                play_again_text = font.render("Play Again", True, WHITE)
                play_again_rect = play_again_text.get_rect(center=(WIDTH // 2 + 35, HEIGHT // 2 + 30))
                pygame.draw.rect(self.screen, BLUE, play_again_rect)
                self.screen.blit(play_again_text, play_again_rect)
                pygame.display.flip()
                continue

        pygame.quit()
        sys.exit()

    def game_over(self, blacks, whites):
        self.text_rect = self.text.get_rect(center=(COLUMNS * CELL_SIZE // 2 - 100, 525))
        if blacks > whites:
            self._winner = "Black"
            self.screen.fill(BLACK)
            self.text = self.font.render(self._winner + " is the winner with " + str(blacks) + "pts", True, WHITE)
            self.screen.blit(self.text, self.text_rect)
            print(self._winner + " is the winner with " + str(blacks) + "pts")
        elif whites > blacks:
            self._winner = "White"
            self.screen.fill(BLACK)
            self.text = self.font.render(self._winner + " is the winner with " + str(whites) + "pts", True, WHITE)
            self.screen.blit(self.text, self.text_rect)
            print(self._winner + " is the winner with " + str(whites) + "pts")
        else:
            self.screen.fill(BLACK)
            self.text = self.font.render("Its a tie! Both players have " + str(blacks) + "pts", True, WHITE)
            self.screen.blit(self.text, self.text_rect)
            print("Its a tie! Both players have " + str(blacks) + "pts")
        self.update()
        pygame.time.delay(3000)
        # exit()

    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        tabela_copy = copy.deepcopy(node)
        current_time = time.time()
        if current_time - start_time >= TIME_LIMIT:
            return [dynamic_heuristic_evaluation_function(dict_to_list_of_lists(tabela_copy)), 0]
        if depth == 0 or self.is_game_over(tabela_copy):
            board_value = dynamic_heuristic_evaluation_function(dict_to_list_of_lists(tabela_copy))
            stanje_tabele.update_table(self.original_table)
            return [board_value, 0]
        if maximizingPlayer:  # AI
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
        else:  # Minimizing player - Human
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
