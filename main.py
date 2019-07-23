from board import *
import uct


if __name__ == '__main__':
    b = Board()
    while b.get_result(b.playerJustMoved) is None:
        if b.playerJustMoved == PLAYER_O:
            available_moves = b.get_moves()
            move = int(input(f'Enter move (available: {available_moves})>'))
            assert move in available_moves, 'Move not in available moves'
            b.make_move(move)
            print(b)
        else:
            print('Engine thinking')
            move = uct.uct_multi(b, itermax=10000)
            b.make_move(move)
            print(f'Engine makes move {move}')
            print(b)

    result = b.get_result(PLAYER_O)
    if result == DRAW:
        print('Draw')
    elif result == WIN:
        print('O wins')
    elif result == LOSS:
        print('X wins')

