import argparse
import pickle
from typing import Tuple

from brute_force import brute_force
from models import Node
import numpy as np


def get_int(prompt: int, n: int):
    while True:
        try:
            coord = int(input(prompt))
            if coord >= n or coord < 0:
                continue
            break
        except ValueError:
            print('Integers only please')
    return coord

def get_move(node: Node, is_human: bool) -> Tuple[int, int]:
    n = node._board._n
    if is_human:
        while True:
            i = get_int('Enter x coord of move: ', n)
            j = get_int('Enter y coord of move: ', n)
            if node._board._board[i][j] != 0:
                continue
            break
        board = node._board.move(node._player, i, j, copy_board=True)
        for child in node._children:
            if np.allclose(child._board._board, board._board):
                return child
    else:
        return node._children[node._optmove]

    return

def play(tree: Node, starting: bool):
    node = tree
    is_human = starting
    print(tree._board._board)
    while not node.is_terminal:
        node = get_move(node, is_human)
        is_human = not is_human
        print(node._board._board)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='Size of tic-tac-toe board.')
    parser.add_argument('-f', help='Name of tic-tac-toe game tree file.')
    parser.add_argument('--starting', action='store_true', help='Whether you start the game.')

    args = parser.parse_args()

    if args.f:
        with open(args.f, 'rb') as f:
            tree = pickle.load(f)
    elif args.n:
        tree = brute_force(args.n)

    play(tree, args.starting)

