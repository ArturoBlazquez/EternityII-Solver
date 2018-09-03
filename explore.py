from typing import List

from Board import *

UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1

max_len = 70


# def horizontal_tree(board, starting_position, remaining_pieces):
#     left_trees = horizontal_half_tree(board, [], starting_position, RIGHT, UP, remaining_pieces)
#     right_trees = horizontal_half_tree(board, [], [len(board) - starting_position[1] - 1, starting_position[0]], LEFT,
#                                        UP, remaining_pieces)
#
#     print("\n" * 5)
#     for t in left_trees:
#         print_line(t)
#
#     print("\n" * 5)
#     for t in right_trees:
#         print_line(t[::-1])
#
#     return join_trees(left_trees, right_trees)


# def horizontal_half_tree(board, path, position, move_to, border_position, remaining_pieces):
#     if len(path) == len(board) / 2 - position[1]:
#         return path
#
#     else:
#         pieces_that_fit = horizontal_explore(board, position, move_to, border_position, remaining_pieces)
#         trees = []
#         for piece in pieces_that_fit:
#             board.place(piece, piece.position)
#             remaining_now = remove(remaining_pieces, piece)
#             new_position = [position[0] + move_to, position[1]]
#
#             tree = horizontal_half_tree(board, path + [piece], new_position, move_to, border_position, remaining_now)
#             if tree:
#                 trees.append(tree)
#
#         if trees and isinstance(trees[0][0], list):
#             return [item for sublist in trees for item in sublist]
#         else:
#             return trees
def get_trees(board: Board, starting_position, remaining_pieces: List[Piece], direction) -> List[List[Piece]]:
    if direction == HORIZONTAL:
        starting_position_second = [len(board) - starting_position[0] - 1, starting_position[1]]
        max_len = len(board) / 2 - starting_position[0]
    else:
        starting_position_second = [starting_position[0], len(board) - starting_position[1] - 1]
        max_len = len(board) / 2 - starting_position[1]

    first_trees = half_tree(board, [], starting_position, remaining_pieces, direction, max_len)
    second_trees = half_tree(board, [], starting_position_second, remaining_pieces, direction, max_len)

    return join_trees(first_trees, second_trees, direction)


def half_tree(board: Board, path: List[Piece], position, remaining_pieces: List[Piece], direction, max_len) -> \
        List[List[Piece]]:
    if len(path) == max_len:
        return path

    else:
        next_position, pieces_that_fit = explore(board, position, remaining_pieces, direction)
        trees = []
        for piece in pieces_that_fit:
            board.place(piece, piece.position)
            remaining_now = remove(remaining_pieces, piece)

            tree = half_tree(board, path + [piece], next_position, remaining_now, direction, max_len)
            board.free(position)
            if tree:
                trees.append(tree)

        if trees and isinstance(trees[0][0], list):
            return [item for sublist in trees for item in sublist]
        else:
            return trees


def horizontal_explore(board, position, move_to, border_position, remaining_pieces):
    if move_to == LEFT and border_position == UP:
        tile1 = board.right_piece_tile(position)
        tile2 = board.top_piece_tile(position)
        position_of_first_tile = Piece.RIGHT
    elif move_to == RIGHT and border_position == UP:
        tile1 = board.top_piece_tile(position)
        tile2 = board.left_piece_tile(position)
        position_of_first_tile = Piece.UP
    elif move_to == RIGHT and border_position == DOWN:
        tile1 = board.left_piece_tile(position)
        tile2 = board.bottom_piece_tile(position)
        position_of_first_tile = Piece.LEFT
    elif move_to == LEFT and border_position == DOWN:
        tile1 = board.bottom_piece_tile(position)
        tile2 = board.right_piece_tile(position)
        position_of_first_tile = Piece.DOWN
    else:
        return []

    pieces_that_fit = []
    for piece in remaining_pieces:
        if piece.has_tiles(tile1, tile2):
            for orientation in piece.orientations_of_tiles(tile1, tile2, position_of_first_tile):
                pieces_that_fit.append(Piece(piece.id, piece.tiles, orientation, position))

    return pieces_that_fit


def join_trees(left_trees: List[List[Piece]], right_trees: List[List[Piece]], direction) -> List[List[Piece]]:
    trees = []
    for left_tree in left_trees:
        for right_tree in right_trees:
            if direction == HORIZONTAL:
                first_tile = left_tree[-1].right_tile()
                second_tile = right_tree[-1].left_tile()
            else:
                first_tile = left_tree[-1].bottom_tile()
                second_tile = right_tree[-1].top_tile()

            if first_tile == second_tile:
                tree = left_tree + right_tree[::-1]
                if len(set(tree)) == len(tree):
                    trees.append(left_tree + right_tree[::-1])

    return trees


def remove(array, element):
    ret = list(array)
    ret.remove(element)
    return ret


def explore(board: Board, position: List[int], remaining_pieces: List[Piece], direction=None) -> \
        (List[int], List[Piece]):
    next_position, tiles, position_of_first_tile = board.get_borders_at(position, direction)

    pieces_that_fit = []
    for piece in remaining_pieces:
        if piece.has_tiles(tiles):
            for orientation in piece.orientations_of_tiles(tiles, position_of_first_tile):
                pieces_that_fit.append(Piece(piece.piece_id, piece.tiles, orientation, position))

    return next_position, pieces_that_fit


def explore_tree(board: Board, path: List[Piece], position, remaining_pieces: List[Piece]):
    global max_len
    if len(path) > max_len:
        board.print()
        print()
        board.print_numbers()
        print(len(path))
        print("\n" * 5)
        max_len = len(path)

    next_position, pieces_that_fit = explore(board, position, remaining_pieces)
    for piece in pieces_that_fit:
        board.place(piece, piece.position)
        remaining_now = remove(remaining_pieces, piece)

        explore_tree(board, path + [piece], next_position, remaining_now)
        board.free(position)
