import tabela
from heuristika import *
import pygame
import sys

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
        pygame.display.set_caption("Reversi - Player vs Player")
        self.clock = pygame.time.Clock()
        self._current_player = ""
        self._opponent = ""
        self._winner = ""
        self.valid_options = {}
        self.without_option = 0
        self._game_is_over = False
        self.running = True
        self.game_start()

    def update(self):
        if not self._game_is_over:
            self.draw_board()
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
                    pygame.draw.circle(self.screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 10)

    def handle_events(self, moves):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if stanje_tabele.if_is_in_valid_moves(moves, row, col):
                    option = (list(moves.values())).index((row, col))
                    new_table = stanje_tabele.make_a_move_player(moves, option)
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
            options = {}
            if self._current_player == "Black":
                moves = stanje_tabele.moves(tabela_za_prebacivanje)
            else:
                moves = stanje_tabele.AI_moves(tabela_za_prebacivanje)
            options = moves[1]
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
                            self.text_rect = self.text.get_rect(center=(COLUMNS * CELL_SIZE // 2 - 40, 510))
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
                        if stanje_tabele.if_is_in_valid_moves(self.valid_options, row, col) and stanje_tabele.get_table_value(row, col) != "W" and stanje_tabele.get_table_value(row, col) != "B":
                            option = find_key_by_value(self.valid_options, (row, col))
                            new_table = stanje_tabele.make_a_move_player(self.valid_options, option)
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
                        else:
                            if self.without_option == 1:
                                self.print_pass_turn(black_discs, white_discs)
                            # if self._game_is_over:
                            #     exit()
                            self.print_invalid_option(black_discs, white_discs)

                    elif self._current_player == "White":  # Player White's turn
                        self.screen.fill(BLACK)
                        self.text = self.font.render("Player Black's turn", True, WHITE)
                        self.screen.blit(self.text, self.text_rect)
                        print("Player Black's turn:")

                        if stanje_tabele.if_is_in_valid_moves(self.valid_options, row, col) and stanje_tabele.get_table_value(row, col) != "W" and stanje_tabele.get_table_value(row, col) != "B":
                            option = find_key_by_value(self.valid_options, (row, col))
                            new_table = stanje_tabele.make_a_move_player(self.valid_options, option)
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
                        else:
                            if self.without_option == 1:
                                self.print_pass_turn(black_discs, white_discs)
                            # if self._game_is_over:
                            #     exit()
                            self.print_invalid_option(black_discs, white_discs)

            if not self._game_is_over:

                self.update()

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

