def can_move(self, opp, string):
    if string[0] != opp:
        return False
    for ctr in range(1, 8):
        if string[ctr] == '-':
            return False
        if string[ctr] == self:
            return True
    return False


def is_legal_move(self, opp, grid, start_x, start_y):
    if grid[start_x][start_y] != '-':
        return False
    string = [''] * 10
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
                  (1, 1), (1, 0), (1, -1), (0, -1)]
    for dx, dy in directions:
        string[0] = ''
        for ctr in range(1, 8):
            x = start_x + ctr * dx
            y = start_y + ctr * dy
            if 0 <= x < 8 and 0 <= y < 8:
                string[ctr - 1] = grid[x][y]
            else:
                string[ctr - 1] = '0'
        if can_move(self, opp, string):
            return True
    return False


def num_valid_moves(self, opp, grid):
    count = 0
    for i in range(8):
        for j in range(8):
            if is_legal_move(self, opp, grid, i, j):
                count += 1
    return count


def dynamic_heuristic_evaluation_function(grid):
    my_color = 'b'  # Assuming my_color stores your color
    opp_color = 'w'  # and opp_color stores the opponent's color

    my_tiles = 0
    opp_tiles = 0
    my_front_tiles = 0
    opp_front_tiles = 0
    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
    V = [[20, -3, 11, 8, 8, 11, -3, 20],
         [-3, -7, -4, 1, 1, -4, -7, -3],
         [11, -4, 2, 2, 2, 2, -4, 11],
         [8, 1, 2, -3, -3, 2, 1, 8],
         [8, 1, 2, -3, -3, 2, 1, 8],
         [11, -4, 2, 2, 2, 2, -4, 11],
         [-3, -7, -4, 1, 1, -4, -7, -3],
         [20, -3, 11, 8, 8, 11, -3, 20]]

    # Piece difference, frontier disks, and disk squares
    for i in range(8):
        for j in range(8):
            if grid[i][j] == my_color:
                d += V[i][j]
                my_tiles += 1
            elif grid[i][j] == opp_color:
                d -= V[i][j]
                opp_tiles += 1
            if grid[i][j] != '-':
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if 0 <= x < 8 and 0 <= y < 8 and grid[x][y] == '-':
                        if grid[i][j] == my_color:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles += 1
                        break

    if my_tiles > opp_tiles:
        p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
        p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
    else:
        p = 0

    if my_front_tiles > opp_front_tiles:
        f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
    elif my_front_tiles < opp_front_tiles:
        f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
    else:
        f = 0

    # Corner occupancy
    my_tiles = opp_tiles = 0
    if grid[0][0] == my_color:
        my_tiles += 1
    elif grid[0][0] == opp_color:
        opp_tiles += 1
    if grid[0][7] == my_color:
        my_tiles += 1
    elif grid[0][7] == opp_color:
        opp_tiles += 1
    if grid[7][0] == my_color:
        my_tiles += 1
    elif grid[7][0] == opp_color:
        opp_tiles += 1
    if grid[7][7] == my_color:
        my_tiles += 1
    elif grid[7][7] == opp_color:
        opp_tiles += 1
    c = 25 * (my_tiles - opp_tiles)

    # Corner closeness
    my_tiles = opp_tiles = 0
    if grid[0][0] == '-':
        if grid[0][1] == my_color:
            my_tiles += 1
        elif grid[0][1] == opp_color:
            opp_tiles += 1
        if grid[1][1] == my_color:
            my_tiles += 1
        elif grid[1][1] == opp_color:
            opp_tiles += 1
        if grid[1][0] == my_color:
            my_tiles += 1
        elif grid[1][0] == opp_color:
            opp_tiles += 1
    if grid[0][7] == '-':
        if grid[0][6] == my_color:
            my_tiles += 1
        elif grid[0][6] == opp_color:
            opp_tiles += 1
        if grid[1][6] == my_color:
            my_tiles += 1
        elif grid[1][6] == opp_color:
            opp_tiles += 1
        if grid[1][7] == my_color:
            my_tiles += 1
        elif grid[1][7] == opp_color:
            opp_tiles += 1
    if grid[7][0] == '-':
        if grid[7][1] == my_color:
            my_tiles += 1
        elif grid[7][1] == opp_color:
            opp_tiles += 1
        if grid[6][1] == my_color:
            my_tiles += 1
        elif grid[6][1] == opp_color:
            opp_tiles += 1
        if grid[6][0] == my_color:
            my_tiles += 1
        elif grid[6][0] == opp_color:
            opp_tiles += 1
    if grid[7][7] == '-':
        if grid[6][7] == my_color:
            my_tiles += 1
        elif grid[6][7] == opp_color:
            opp_tiles += 1
        if grid[6][6] == my_color:
            my_tiles += 1
        elif grid[6][6] == opp_color:
            opp_tiles += 1
        if grid[7][6] == my_color:
            my_tiles += 1
        elif grid[7][6] == opp_color:
            opp_tiles += 1
    l = -12.5 * (my_tiles - opp_tiles)

    # Mobility
    my_tiles = num_valid_moves(my_color, opp_color, grid)
    opp_tiles = num_valid_moves(opp_color, my_color, grid)
    if my_tiles > opp_tiles:
        m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
        m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
    else:
        m = 0

    # final weighted score
    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score
