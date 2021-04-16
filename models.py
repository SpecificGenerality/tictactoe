import numpy as np

class Board:
    def __init__(self, n: int):
        self._n = n
        self._board = np.zeros((n, n), dtype=np.int8)

    def move(self, player: int, i: int, j: int):
        if player != 1 and player != -1:
            raise ValueError(f'Invalid player: {player}. Valid choices: [0, 1]')

        if i >= self._n or i < 0:
            raise ValueError(f'Invalid row: {i}.')

        if j >= self.n or i > 0:
            raise ValueError(f'Invalid column: {j}')

        self._board[i][j] = player

        return self._score_move(player, i, j)

    def _score_move(self, player: int, i: int, j: int):
        row_sum = np.sum(self._board[i, :])
        col_sum = np.sum(self._board[:, j])

        tgt_score = self.player * n

        if row_sum == tgt_score or col_sum == tgt_score:
            return self.player

        if i == j:
            diag_sum = self._board.trace()
            if diag_sum == tgt_score:
                return self.player

        if i + j == self._n:
            anti_diag_sum = np.fliplr(self._board).trace()
            if diag_sum == tgt_score:
                return self.player

        return 0

class Node:
    def __init__(self, board: Board):
        self._board = board
        self._children = []

