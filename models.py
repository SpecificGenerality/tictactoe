import numpy as np
from typing import Tuple, List

class Board:
    def __init__(self, board, score=0):
        n, m = board.shape
        if n != m:
            raise ValueError('Non-square, rectangular boards not yet supported.')

        self._n = n
        self._board = board
        self._score = score
        self._terminal = score != 0

    @property
    def is_terminal(self):
        return self._terminal

    def get_next_moves(self) -> Tuple[List, List]:
        if self.is_terminal:
            return None, None
        return np.where(self._board == 0)

    @classmethod
    def score_move(cls, board: np.array, player: int, i: int, j: int):
        n = len(board)
        row_sum = np.sum(board[i, :])
        col_sum = np.sum(board[:, j])

        tgt_score = player * n

        if row_sum == tgt_score or col_sum == tgt_score:
            return player

        if i == j:
            diag_sum = board.trace()
            if diag_sum == tgt_score:
                return player

        if i + j == n:
            anti_diag_sum = np.fliplr(board).trace()
            if anti_diag_sum == tgt_score:
                return player

        return 0

    def move(self, player: int, i: int, j: int, copy_board=True):
        if player != 1 and player != -1:
            raise ValueError(f'Invalid player: {player}. Valid choices: [0, 1]')

        if i >= self._n or i < 0:
            raise ValueError(f'Invalid row: {i}.')

        if j >= self._n or j < 0:
            raise ValueError(f'Invalid column: {j}')

        if copy_board:
            board = self._board.copy()
        else:
            board = self._board

        board[i][j] = player
        score = Board.score_move(board, player, i, j)

        if score != 0 and not copy_board:
            self._terminal = True

        return Board(board, score)

class Node:
    def __init__(self, player: int, board: Board):
        self._player = player
        self._board = board
        self._children = []

    @classmethod
    def size(cls, node):
        def size_helper(node, acc: int):
            if node.is_terminal:
                return acc + 1
            else:
                for child in node.children:
                    acc += size_helper(child, acc)
                return acc
        return size_helper(node, 0)

    @property
    def is_terminal(self):
        return self._board.is_terminal

    @property
    def children(self):
        return self._children

    def add_children(self) -> bool:
        if self._board.is_terminal:
            return False

        if isinstance(self._children, tuple):
            return False

        child_player = self._player * -1
        x, y = self._board.get_next_moves()
        for i in range(len(x)):
            child_board = self._board.move(child_player, x[i], y[i], copy_board=True)
            child_node = Node(child_player, child_board)
            self._children.append(child_node)

        self._children = tuple(self._children)

        return True
