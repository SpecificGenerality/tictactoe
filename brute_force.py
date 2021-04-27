import argparse
import pickle
import sys

import numpy as np

from models import Board, Node


def brute_force(n: int):
    root_board = Board(np.zeros((n, n)), 0)
    root = Node(player=1, board=root_board)

    def construct_tree(node: Node):
        if node._board.is_terminal:
            return
        node.add_children()
        for child in node.children:
            construct_tree(child)

    construct_tree(root)
    minimax(root)
    return root


def minimax(root: Node):
    def max_value(node: Node):
        if node.is_terminal:
            node._value = node._board._score
            return node._board._score
        v = -sys.maxsize
        for child in node.children:
            v = max(v, min_value(child))
        node._value = v
        node._optmove = np.argmax([child._value for child in node.children])
        return v

    def min_value(node: Node):
        if node.is_terminal:
            node._value = node._board._score
            return node._value
        v = sys.maxsize
        for child in node.children:
            v = min(v, max_value(child))
        node._value = v
        node._optmove = np.argmin([child._value for child in node.children])
        return v
    return max_value(root) if (root._player == 1) else min_value(root)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='Size of tic-tac-toe board')
    parser.add_argument('-f', help='Filename to write to.')

    args = parser.parse_args()

    tree = brute_force(args.n)

    with open(args.f, 'wb') as file_handle:
        pickle.dump(tree, file_handle)
