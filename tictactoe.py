from itertools import cycle
import game_functions as fn

game_is_running = True
players = ('X', 'O')
player = cycle(players)
logo = fn.open_logo('logo.txt')
fn.display(logo)
statistics, players_names = fn.loading_statistics()
player_name = cycle(players_names)

while game_is_running:
    win = False
    tie = False
    fn.display(logo)

    gameboard_size = input('Size of the gameboard? (e.g. 3 => 3x3): ')
    while True:
        try:
            gameboard_size = int(gameboard_size)
            if gameboard_size >= 3:
                gameboard = fn.gameboard_maker(gameboard_size)
                break
            else:
                gameboard_size = input('This is too small, try again: ')

        except Exception:
            gameboard_size = input('It is not a number, try again: ')

    piece_to_win = input('Pieces to win the game? ')
    while True:
        try:
            piece_to_win = int(piece_to_win)
            if piece_to_win <= gameboard_size and piece_to_win >= 3:
                break
            else:
                piece_to_win = input('It is impossible, try again: ')

        except Exception:
            piece_to_win = input('It is not a number, try again: ')

    fn.display(logo, statistics, gameboard, gameboard_size, players_names)

    while not win and not tie:
        current_player = next(player)
        current_players_name = next(player_name)

        while True:
            row = int(input(f'{current_players_name} row? '))
            col = int(input(f'{current_players_name} column? '))
            try:
                if gameboard[row][col] == ' ':
                    gameboard[row][col] = current_player
                    break
                else:
                    print('You can not put there, try again!')

            except Exception:
                print('That is incorrect, try again!')

        fn.display(logo, statistics, gameboard, gameboard_size, players_names)
        win, checkable_tuple = fn.check_win(
            gameboard, current_player, piece_to_win)
        tie = fn.check_tie(checkable_tuple, piece_to_win)

        if win:
            statistics[current_player] += 1
            fn.display(logo, statistics, gameboard,
                       gameboard_size, players_names)
            print(f'{current_players_name} has been won!\n')

        elif tie:
            print('Its a tie!\n')

    game_is_running = fn.quit_game(statistics, players_names)
