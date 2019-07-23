from constants import *


class Board:
    """Board implementation for a single NxN board"""

    def __init__(self):
        self.pos = [0] * BOARD_SIZE
        self.playerJustMoved = PLAYER_O
        self.history = []

    def get_row_strings(self):
        lines = []
        for combo in zip(*[self.pos[i::ROWS] for i in range(ROWS)]):
            lines.append(''.join(['{:<5}'.format(STR_MATRIX[elem]) for elem in combo]))
        return lines

    def __str__(self):
        return '\n'.join(self.get_row_strings())

    def __copy__(self):
        _b = Board()
        _b.pos = self.pos[:]  # copy list
        _b.playerJustMoved = self.playerJustMoved
        _b.history = self.history[:]
        return _b

    def make_move(self, move):
        assert move in self.get_moves(), 'Position is already occupied'
        self.playerJustMoved = -self.playerJustMoved

        self.pos[move] = self.playerJustMoved
        self.history.append(move)

    def take_move(self):
        if not self.history:
            print("History is empty")
            return

        last_element = self.history.pop()
        self.pos[last_element] = NO_PLAYER
        self.playerJustMoved = -self.playerJustMoved

    def get_moves(self):
        return [idx for idx, value in enumerate(self.pos) if value == NO_PLAYER]

    def get_result(self, player_jm):
        cols_combo = [self.pos[i::ROWS] for i in range(ROWS)]
        rows_combo = list(zip(*cols_combo))

        for i in range(ROWS):
            # Sum a row and a column
            row_result, col_result = sum(rows_combo[i]), sum(cols_combo[i])

            # Check if sum of values of a row is not equal to number of rows
            # i.e. all 1s or all -1s
            if abs(row_result) == ROWS:
                return WIN if int(row_result / ROWS) == player_jm else LOSS

            if abs(col_result) == ROWS:
                return WIN if int(col_result / ROWS) == player_jm else LOSS

        # Sum values on Right diagonal
        # Look at right Diagonal
        # exclude last element since it is not part of the diagonal
        # i.e. if you have [1, 2, 3,
        #                   4, 5, 6,
        #                   7 ,8 ,9] then right diagonal is [3, 5, 7]
        # i.e. starting from the right corner the diagonal is formed by
        # every second number (3, 5, 7), however this will also result
        # in 9 being included which it should not be therefore we remove it
        result = sum(self.pos[ROWS - 1::ROWS - 1][:-1])
        if abs(result) == ROWS:
            return WIN if int(result / ROWS) == player_jm else LOSS

        # Left diagonal
        result = sum(self.pos[::ROWS + 1])
        if abs(result) == ROWS:
            return WIN if int(result / ROWS) == player_jm else LOSS

        # Lastly check if no available squares are on the board => TIE
        if sum([abs(elem) for elem in self.pos]) == BOARD_SIZE:
            # here 0.5 indicates a DRAW and for ultimate tttoe
            # this means that a drawn board is not taken into account for
            # any player
            return DRAW

        return None


if __name__ == '__main__':
    b = Board()
    print(b)
    b.make_move(0)
    print(b.pos)
    b.make_move(1)
    b.make_move(3)
    b.make_move(4)
    b.make_move(6)
    print(b)
    print(b.get_result(b.playerJustMoved), b.get_result(-b.playerJustMoved))