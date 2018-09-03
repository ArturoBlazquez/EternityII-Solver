from Piece import Piece, shift, get_piece_by_id
from typing import List

VERTICAL = "vertical"
HORIZONTAL = "horizontal"


class Board:
    def __init__(self, length=16):
        self.board = [[None for _ in range(length + 2)] for _ in range(length + 2)]
        for i in range(length + 2):
            self.board[0][i] = Piece(0, ['X'] * 4, Piece.DOWN, [-1, i - 1])
            self.board[length + 1][i] = Piece(0, ['X'] * 4, Piece.DOWN, [length, i - 1])

        for i in range(length):
            self.board[1 + i][0] = Piece(0, ['X'] * 4, Piece.DOWN, [i, -1])
            self.board[1 + i][length + 1] = Piece(0, ['X'] * 4, Piece.DOWN, [i, length])

    def __len__(self):
        return len(self.board) - 2

    def place(self, piece, position, remaining_tiles=[]):
        piece.position = position
        self.board[position[0] + 1][position[1] + 1] = piece

        if remaining_tiles:
            remaining_tiles.remove(piece)

    def free(self, position):
        self.board[position[0] + 1][position[1] + 1] = None

    def auto_place(self, piece_id, position, remaining_tiles):
        piece = get_piece_by_id(piece_id, remaining_tiles)

        bottom_tile = self.bottom_piece_tile(position)
        right_tile = self.right_piece_tile(position)
        top_tile = self.top_piece_tile(position)
        left_tile = self.left_piece_tile(position)

        if top_tile is not None and left_tile is not None:
            if piece.has_tiles([top_tile, left_tile]):
                piece.orientation = piece.orientations_of_tiles([top_tile, left_tile], Piece.UP)[0]
        if right_tile is not None and top_tile is not None:
            if piece.has_tiles([right_tile, top_tile]):
                piece.orientation = piece.orientations_of_tiles([right_tile, top_tile], Piece.RIGHT)[0]
        if bottom_tile is not None and right_tile is not None:
            if piece.has_tiles([bottom_tile, right_tile]):
                piece.orientation = piece.orientations_of_tiles([bottom_tile, right_tile], Piece.DOWN)[0]
        if left_tile is not None and bottom_tile is not None:
            if piece.has_tiles([left_tile, bottom_tile]):
                piece.orientation = piece.orientations_of_tiles([left_tile, bottom_tile], Piece.LEFT)[0]

        self.place(piece, position, remaining_tiles)

    def piece_at(self, position) -> Piece:
        return self.board[position[0] + 1][position[1] + 1]

    def bottom_piece(self, position) -> Piece:
        return self.board[position[0] + 1][position[1] + 2]

    def right_piece(self, position) -> Piece:
        return self.board[position[0] + 2][position[1] + 1]

    def top_piece(self, position) -> Piece:
        return self.board[position[0] + 1][position[1]]

    def left_piece(self, position) -> Piece:
        return self.board[position[0]][position[1] + 1]

    def get_bottom_tile(self, position):
        return self.piece_at(position).bottom_tile()

    def get_top_tile(self, position):
        return self.piece_at(position).top_tile()

    def get_left_tile(self, position):
        return self.piece_at(position).left_tile()

    def get_right_tile(self, position):
        return self.piece_at(position).right_tile()

    def bottom_piece_tile(self, position):
        if self.bottom_piece(position):
            return self.bottom_piece(position).top_tile()

    def right_piece_tile(self, position):
        if self.right_piece(position):
            return self.right_piece(position).left_tile()

    def top_piece_tile(self, position):
        if self.top_piece(position):
            return self.top_piece(position).bottom_tile()

    def left_piece_tile(self, position):
        if self.left_piece(position):
            return self.left_piece(position).right_tile()

    def get_borders_at(self, position, direction=None) -> (List[int], List[Piece]):
        bottom_tile = self.bottom_piece_tile(position)
        right_tile = self.right_piece_tile(position)
        top_tile = self.top_piece_tile(position)
        left_tile = self.left_piece_tile(position)

        bottom_position = [position[0], position[1] + 1]
        right_position = [position[0] + 1, position[1]]
        top_position = [position[0], position[1] - 1]
        left_position = [position[0] - 1, position[1]]

        tiles = [bottom_tile, right_tile, top_tile, left_tile]

        if tiles.count(None) < 2:
            if bottom_tile is None:
                tiles = shift(tiles, 1)
                position_of_first_tile = Piece.RIGHT
                next_position = bottom_position
            elif right_tile is None:
                tiles = shift(tiles, 2)
                position_of_first_tile = Piece.UP
                next_position = right_position
            elif top_tile is None:
                tiles = shift(tiles, 3)
                position_of_first_tile = Piece.LEFT
                next_position = top_position
            elif left_tile is None:
                position_of_first_tile = Piece.DOWN
                next_position = left_position
        else:
            if left_tile is None and bottom_tile is None:
                tiles = shift(tiles, 1)
                position_of_first_tile = Piece.RIGHT
                next_position = bottom_position
            elif bottom_tile is None and right_tile is None:
                tiles = shift(tiles, 2)
                position_of_first_tile = Piece.UP
                next_position = right_position
            elif right_tile is None and top_tile is None:
                tiles = shift(tiles, 3)
                position_of_first_tile = Piece.LEFT
                next_position = top_position
            elif top_tile is None and left_tile is None:
                position_of_first_tile = Piece.DOWN
                next_position = left_position

        tiles = [x for x in tiles if x is not None]

        if direction == HORIZONTAL:
            if left_tile is None:
                next_position = left_position
            else:
                next_position = right_position
        elif direction == VERTICAL:
            if top_tile is None:
                next_position = top_position
            else:
                next_position = bottom_position

        return next_position, tiles, position_of_first_tile

    def print(self):
        for x in range(len(self.board)):
            row = []
            for y in range(len(self.board)):
                row.append(self.board[y][x])
            print_line(row)

    def print_numbers(self):
        for x in range(len(self.board)):
            row = []
            for y in range(len(self.board)):
                if self.board[y][x]:
                    piece_id = self.board[y][x].piece_id
                    if len(str(piece_id)) == 1:
                        print(" ", piece_id, "", end='')
                    elif len(str(piece_id)) == 2:
                        print("", piece_id, "", end='')
                    else:
                        print(piece_id, "", end='')
                else:
                    print(" -- ", end='')
            print()


def print_line(row):
    for place in row:
        if place is None:
            print(" | ", end='')
        else:
            print(" " + place.top_tile() + " ", end='')
    print()
    for place in row:
        if place is None:
            print("- -", end='')
        else:
            print(place.left_tile() + " " + place.right_tile(), end='')
    print()
    for place in row:
        if place is None:
            print(" | ", end='')
        else:
            print(" " + place.bottom_tile() + " ", end='')
    print()
