from os import system, stat, path
from time import sleep


def open_logo(txt_file):
    file = open(txt_file)
    logo = file.read()
    file.close()
    return logo


def gameboard_maker(gameboard_size):
    gameboard = []
    for x in range(gameboard_size):
        row = []
        for y in range(gameboard_size):
            row.append(' ')
        gameboard.append(row)
    return gameboard


def display(logo=False, statistics=False, board=False, size=False, names=('X', 'O')):
    system('cls')
    if logo:
        print(logo)

    if statistics:
        for index in range(len(statistics)):
            print('Wins of ', names[index], ' (', tuple(statistics.keys())[
                  index], ') : ', tuple(statistics.values())[index], sep='')

    if board and size:
        print('\n    '+'   '.join(str(col_num) for col_num in range(size)))
        for num, row in enumerate(board):
            print('  '+'----'*size)
            print(str(num), ' | ', ' | '.join(
                data for data in row), ' |', sep='')
        print('  '+'----'*size, '\n', sep='')


def check_win(gameboard, current_player, piece_to_win):

    def simple_collect(list2d, tuple_to_con, piece_to_win):
        for l in list2d:
            for i in range(piece_to_win, len(l) + 1):
                tuple_to_con += tuple(l[i - piece_to_win:i])
        return tuple_to_con

    def collect_diagonals(list2d, tuple_to_con, piece_to_win):
        col = 0
        row_changer = 0
        col_count = 0
        while True:
            one_diagonal = tuple()
            for row in range((len(list2d) - 1) - row_changer, (len(list2d) - 1) - row_changer - piece_to_win, -1):
                try:
                    one_diagonal += tuple(list2d[row][col])
                except Exception:
                    break
                col += 1

            if len(one_diagonal) == piece_to_win:
                tuple_to_con += one_diagonal

            if col_count == len(list2d) - 1:
                row_changer += 1
                col_count = -1

            col_count += 1
            col = col_count

            if (len(list2d) - 1) - row_changer < piece_to_win:
                break

        col = 0
        row_changer = 0
        col_count = 0
        while True:
            one_diagonal = tuple()
            for row in range(row_changer, row_changer + piece_to_win):
                try:
                    one_diagonal += tuple(list2d[row][col])
                except Exception:
                    break
                col += 1

            if len(one_diagonal) == piece_to_win:
                tuple_to_con += one_diagonal

            if col_count == len(list2d) - 1:
                row_changer += 1
                col_count = -1

            col_count += 1
            col = col_count

            if (len(list2d) - 1) - row_changer < piece_to_win:
                break
        return tuple_to_con

    tuple_to_check = tuple()
    horizontal = tuple(map(tuple, zip(*gameboard)))
    tuple_to_check = collect_diagonals(gameboard, simple_collect(horizontal, simple_collect(
        gameboard, tuple_to_check, piece_to_win), piece_to_win), piece_to_win)

    for i in range(piece_to_win, len(tuple_to_check) + 1, piece_to_win):
        if tuple_to_check[i - piece_to_win:i].count(current_player) == piece_to_win:
            return True, tuple_to_check
            break
    else:
        return False, tuple_to_check


def check_tie(tuple_to_check, piece_to_win):
    values = tuple()

    for i in range(piece_to_win, len(tuple_to_check) + 1, piece_to_win):
        if 'X' in tuple_to_check[i - piece_to_win:i] and 'O' in tuple_to_check[i - piece_to_win:i]:
            values += (0,)
        else:
            values += (1,)

    if values.count(1) == 1:
        return True
    else:
        return False


def loading_animation(message):
    print(message, end='', flush=True)
    for dot in '...':
        sleep(1)
        print(dot, end='', flush=True)


def loading_statistics():
    try:
        if stat("saved_data.txt").st_size != 0 and path.isfile('saved_data.txt'):
            loading_stat = input(
                'Do you want to load the previously saved statistics? (y/n) ').lower()
            if loading_stat == 'y':
                data_file = open('saved_data.txt', 'r')
                loaded_data = data_file.read().strip().split()
                data_file.close()
                statistics = {
                    'X': int(loaded_data[1]), 'O': int(loaded_data[3])}
                players_names = [loaded_data[0], loaded_data[2]]

            else:
                raise Exception
        else:
            raise Exception

    except Exception:
        player_x = input("Name of the player of 'X'? ")
        player_o = input("Name of the player of 'O'? ")
        players_names = [player_x, player_o]
        statistics = {'X': 0, 'O': 0}

    return statistics, players_names


def quit_game(statistics, players_names):
    qg = input('Quit? (y/n) ').lower()
    display()

    if qg == 'y':
        save_stat = input(
            'Do you want to save the statistics of the game? (y/n) ').lower()
        if save_stat == 'y':
            saved_data = open('saved_data.txt', 'w')
            for index in range(len(statistics)):
                print(players_names[index], tuple(statistics.values())[
                      index], file=saved_data, end=' ')
            saved_data.close()

        display()
        loading_animation('Closing')
        return False
    else:
        loading_animation('Loading')
        return True
