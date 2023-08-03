import copy
# black i white dot promeniti zavisno od themea
WHITE_DOT = u"\u25CF"
BLACK_DOT = u"\u25CB"
ROWS = 8
COLS = 8


class Tabela(object):
    def __init__(self, rows, cols):
        self._tabela = {}
        self._rows = rows
        self._cols = cols

        self._tabela = self.create_table_start()

    def create_table_start(self):
        for i in range(self._rows):
            for j in range(self._cols):
                self._tabela.update({(i, j): "O"})
                if (i == 3 and j == 3) or (i == 4 and j == 4):
                    self._tabela[(i, j)] = "B"
                if (i == 4 and j == 3) or (i == 3 and j == 4):
                    self._tabela[(i, j)] = "W"
        return self._tabela

    def update_table(self, izmena_tabele):
        for x in izmena_tabele.keys():
            for y in self._tabela.keys():
                if y == x:
                    self._tabela[y] = izmena_tabele[x]
        return self._tabela

    def update_copy(self, izmena_tabele):
        copied_dict = copy.deepcopy(self._tabela)
        for x in izmena_tabele.keys():
            for y in copied_dict.keys():
                if y == x:
                    copied_dict[y] = izmena_tabele[x]
        return copied_dict

    def print_state(self, new_table):
        self._tabela = self.update_table(new_table)
        print("_________________________________________________________________")
        red = ""
        for polje in self._tabela.items():
            if polje[1] == "B":
                red += " [  " + BLACK_DOT + "  ]"
            elif polje[1] == "W":
                red += " [  " + WHITE_DOT + "  ]"
            elif polje[1] == "O":
                red += " [  " + " " + "  ]"
            else:
                red += " [  " + polje[1] + "  ]"
            if polje[0][1] >= 7:
                print(red)
                print("_________________________________________________________________")
                red = ""

    def count_discs(self):
        blacks = 0
        whites = 0
        for x in self._tabela.keys():
            if self._tabela[x] == "B":
                blacks += 1
            if self._tabela[x] == "W":
                whites += 1
        return [blacks, whites]

    def moves(self, tabela_diskovi):
        self._tabela = self.update_table(tabela_diskovi)
        protivnicki_diskovi_za_obrtanje_up = {}
        protivnicki_diskovi_za_obrtanje_left = {}
        protivnicki_diskovi_za_obrtanje_down = {}
        protivnicki_diskovi_za_obrtanje_right = {}
        protivnicki_diskovi_za_obrtanje_up_left = {}
        protivnicki_diskovi_za_obrtanje_down_right = {}
        protivnicki_diskovi_za_obrtanje_up_right = {}
        protivnicki_diskovi_za_obrtanje_down_left = {}
        option_list = []
        options = {}
        i = 0
        for x in self._tabela.keys():
            if self._tabela[x][0] == "B":
                disc_counter_black = 0
                while (x[0] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0] - disc_counter_black, x[1])
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_up.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up.update({y: "B"})
                            option_list.append({str(i): "Up"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up = {}
                disc_counter_black = 0
                while (x[1] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0], x[1] - disc_counter_black)
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_left.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_left):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_left.update({y: "B"})
                            option_list.append({str(i): "Left"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_left = {}
                disc_counter_black = 0
                while (x[0] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0] + disc_counter_black, x[1])
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_down.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down.update({y: "B"})
                            option_list.append({str(i): "Down"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down = {}
                disc_counter_black = 0
                while (x[1] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0], x[1] + disc_counter_black)
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_right.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_right):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_right.update({y: "B"})
                            option_list.append({str(i): "Right"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_right = {}
                disc_counter_black = 0
                while (x[0] - disc_counter_black) > 0 and (x[1] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0] - disc_counter_black, x[1] - disc_counter_black)
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_up_left.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_left):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_left.update({y: "B"})
                            option_list.append({str(i): "Up-Left"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_left = {}
                disc_counter_black = 0
                while (x[0] + disc_counter_black) < 7 and (x[1] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0] + disc_counter_black, x[1] + disc_counter_black)
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_down_right.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_right):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_right.update({y: "B"})
                            option_list.append({str(i): "Down-right"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_right = {}
                disc_counter_black = 0
                while (x[0] - disc_counter_black) > 0 and (x[1] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0] - disc_counter_black, x[1] + disc_counter_black)
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_up_right.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_right):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_right.update({y: "B"})
                            option_list.append({str(i): "Up-right"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_right = {}
                disc_counter_black = 0
                while (x[0] + disc_counter_black) < 7 and (x[1] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0] + disc_counter_black, x[1] - disc_counter_black)
                    if self._tabela[y] == "B":
                        break
                    if self._tabela[y] == "W":
                        protivnicki_diskovi_za_obrtanje_down_left.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_left):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_left.update({y: "B"})
                            option_list.append({str(i): "Down-left"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_left = {}
        return [option_list, options]

    def moves_copy(self, tabela_diskovi):
        copied_dict = copy.deepcopy(self._tabela)
        copied_dict = self.update_copy(tabela_diskovi)
        protivnicki_diskovi_za_obrtanje_up = {}
        protivnicki_diskovi_za_obrtanje_left = {}
        protivnicki_diskovi_za_obrtanje_down = {}
        protivnicki_diskovi_za_obrtanje_right = {}
        protivnicki_diskovi_za_obrtanje_up_left = {}
        protivnicki_diskovi_za_obrtanje_down_right = {}
        protivnicki_diskovi_za_obrtanje_up_right = {}
        protivnicki_diskovi_za_obrtanje_down_left = {}
        option_list = []
        options = {}
        i = 0
        for x in copied_dict.keys():
            if copied_dict[x][0] == "B":
                disc_counter_black = 0
                while (x[0] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0] - disc_counter_black, x[1])
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_up.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up.update({y: "B"})
                            option_list.append({str(i): "Up"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up = {}
                disc_counter_black = 0
                while (x[1] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0], x[1] - disc_counter_black)
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_left.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_left):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_left.update({y: "B"})
                            option_list.append({str(i): "Left"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_left = {}
                disc_counter_black = 0
                while (x[0] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0] + disc_counter_black, x[1])
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_down.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down.update({y: "B"})
                            option_list.append({str(i): "Down"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down = {}
                disc_counter_black = 0
                while (x[1] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0], x[1] + disc_counter_black)
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_right.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_right):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_right.update({y: "B"})
                            option_list.append({str(i): "Right"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_right = {}
                disc_counter_black = 0
                while (x[0] - disc_counter_black) > 0 and (x[1] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0] - disc_counter_black, x[1] - disc_counter_black)
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_up_left.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_left):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_left.update({y: "B"})
                            option_list.append({str(i): "Up-Left"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_left = {}
                disc_counter_black = 0
                while (x[0] + disc_counter_black) < 7 and (x[1] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0] + disc_counter_black, x[1] + disc_counter_black)
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_down_right.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_right):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_right.update({y: "B"})
                            option_list.append({str(i): "Down-right"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_right = {}
                disc_counter_black = 0
                while (x[0] - disc_counter_black) > 0 and (x[1] + disc_counter_black) < 7:
                    disc_counter_black += 1
                    y = (x[0] - disc_counter_black, x[1] + disc_counter_black)
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_up_right.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_right):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_right.update({y: "B"})
                            option_list.append({str(i): "Up-right"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_right = {}
                disc_counter_black = 0
                while (x[0] + disc_counter_black) < 7 and (x[1] - disc_counter_black) > 0:
                    disc_counter_black += 1
                    y = (x[0] + disc_counter_black, x[1] - disc_counter_black)
                    if copied_dict[y] == "B":
                        break
                    if copied_dict[y] == "W":
                        protivnicki_diskovi_za_obrtanje_down_left.update({y: "B"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_left):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_left.update({y: "B"})
                            option_list.append({str(i): "Down-left"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_left = {}
        return [option_list, options]

    def make_a_move(self, options, option):
        self._tabela = self.update_table(options[option])
        for x in self._tabela.keys():
            if self._tabela[x][0] != "W" and self._tabela[x][0] != "B" and self._tabela[x][0] != "O":
                self._tabela[x] = "O"
        return self._tabela

    def make_a_move_copy(self, options, option):
        copied_dict = self.update_copy(options[option])
        for x in copied_dict.keys():
            if copied_dict[x] != "W" and copied_dict[x] != "B" and copied_dict[x] != "O":
                copied_dict[x] = "O"
        return copied_dict

    def AI_moves(self, tabela_diskovi):
        self._tabela = self.update_table(tabela_diskovi)
        protivnicki_diskovi_za_obrtanje_up = {}
        protivnicki_diskovi_za_obrtanje_left = {}
        protivnicki_diskovi_za_obrtanje_down = {}
        protivnicki_diskovi_za_obrtanje_right = {}
        protivnicki_diskovi_za_obrtanje_up_left = {}
        protivnicki_diskovi_za_obrtanje_down_right = {}
        protivnicki_diskovi_za_obrtanje_up_right = {}
        protivnicki_diskovi_za_obrtanje_down_left = {}
        options = {}
        i = 0
        for x in self._tabela.keys():
            if self._tabela[x][0] == "W":
                disc_counter_white = 0
                while (x[0] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0] - disc_counter_white, x[1])
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_up.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up = {}
                disc_counter_white = 0
                while (x[1] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0], x[1] - disc_counter_white)
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_left.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_left):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_left.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_left = {}
                disc_counter_white = 0
                while (x[0] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0] + disc_counter_white, x[1])
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_down.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down = {}
                disc_counter_white = 0
                while (x[1] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0], x[1] + disc_counter_white)
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_right.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_right):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_right.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_right = {}
                disc_counter_white = 0
                while (x[0] - disc_counter_white) > 0 and (x[1] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0] - disc_counter_white, x[1] - disc_counter_white)
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_up_left.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_left):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_left.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_left = {}
                disc_counter_white = 0
                while (x[0] + disc_counter_white) < 7 and (x[1] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0] + disc_counter_white, x[1] + disc_counter_white)
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_down_right.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_right):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_right.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_right = {}
                disc_counter_white = 0
                while (x[0] - disc_counter_white) > 0 and (x[1] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0] - disc_counter_white, x[1] + disc_counter_white)
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_up_right.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_right):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_right.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_right = {}
                disc_counter_white = 0
                while (x[0] + disc_counter_white) < 7 and (x[1] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0] + disc_counter_white, x[1] - disc_counter_white)
                    if self._tabela[y] == "W":
                        break
                    if self._tabela[y] == "B":
                        protivnicki_diskovi_za_obrtanje_down_left.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_left):
                        if self._tabela[y] == "O":
                            i += 1
                            self._tabela[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_left.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_left = {}
        return options

    def AI_moves_copy(self, tabela_diskovi):
        copied_dict = self.update_copy(tabela_diskovi)
        protivnicki_diskovi_za_obrtanje_up = {}
        protivnicki_diskovi_za_obrtanje_left = {}
        protivnicki_diskovi_za_obrtanje_down = {}
        protivnicki_diskovi_za_obrtanje_right = {}
        protivnicki_diskovi_za_obrtanje_up_left = {}
        protivnicki_diskovi_za_obrtanje_down_right = {}
        protivnicki_diskovi_za_obrtanje_up_right = {}
        protivnicki_diskovi_za_obrtanje_down_left = {}
        options = {}
        i = 0
        for x in copied_dict.keys():
            if copied_dict[x][0] == "W":
                disc_counter_white = 0
                while (x[0] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0] - disc_counter_white, x[1])
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_up.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up = {}
                disc_counter_white = 0
                while (x[1] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0], x[1] - disc_counter_white)
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_left.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_left):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_left.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_left = {}
                disc_counter_white = 0
                while (x[0] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0] + disc_counter_white, x[1])
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_down.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down = {}
                disc_counter_white = 0
                while (x[1] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0], x[1] + disc_counter_white)
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_right.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_right):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_right.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_right = {}
                disc_counter_white = 0
                while (x[0] - disc_counter_white) > 0 and (x[1] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0] - disc_counter_white, x[1] - disc_counter_white)
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_up_left.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_left):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_left.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_left = {}
                disc_counter_white = 0
                while (x[0] + disc_counter_white) < 7 and (x[1] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0] + disc_counter_white, x[1] + disc_counter_white)
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_down_right.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_right):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_right.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_right = {}
                disc_counter_white = 0
                while (x[0] - disc_counter_white) > 0 and (x[1] + disc_counter_white) < 7:
                    disc_counter_white += 1
                    y = (x[0] - disc_counter_white, x[1] + disc_counter_white)
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_up_right.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_up_right):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_up_right.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_up_right})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_up_right)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_up_right = {}
                disc_counter_white = 0
                while (x[0] + disc_counter_white) < 7 and (x[1] - disc_counter_white) > 0:
                    disc_counter_white += 1
                    y = (x[0] + disc_counter_white, x[1] - disc_counter_white)
                    if copied_dict[y] == "W":
                        break
                    if copied_dict[y] == "B":
                        protivnicki_diskovi_za_obrtanje_down_left.update({y: "W"})
                    elif bool(protivnicki_diskovi_za_obrtanje_down_left):
                        if copied_dict[y] == "O":
                            i += 1
                            copied_dict[y] = str(i)
                            protivnicki_diskovi_za_obrtanje_down_left.update({y: "W"})
                            options.update({i: protivnicki_diskovi_za_obrtanje_down_left})
                            break
                        else:
                            found = False
                            for option in options.items():
                                for coordinate in option[1].keys():
                                    if coordinate == y:
                                        found = True
                                        options[option[0]].update(protivnicki_diskovi_za_obrtanje_down_left)
                                        break
                                if found:
                                    break
                            break
                    else:
                        break
                protivnicki_diskovi_za_obrtanje_down_left = {}
        return options
