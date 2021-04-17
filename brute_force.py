import argparse
import pickle

import numpy as np

from models import Board, Node


def brute_force(n: int):
    root_board = Board(np.zeros((n, n)), 0)
    root = Node(player=1, board=root_board)

    def construct_tree(node: Node):
        if node.is_terminal:
            return
        node.add_children()
        for child in node.children:
            construct_tree(child)

    construct_tree(root)
    return root


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='Size of tic-tac-toe board')
    parser.add_argument('-f', help='Filename to write to.')

    args = parser.parse_args()

    tree = brute_force(args.n)

    with open(args.f, 'wb') as file_handle:
        pickle.dump(tree, file_handle)
