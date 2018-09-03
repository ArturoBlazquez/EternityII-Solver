from Board import Board, HORIZONTAL, VERTICAL
from Piece import Piece, get_piece_by_id
from explore import get_trees, explore_tree

with open('cornerPieces.txt') as f:
    piecesString = [x.strip().split() for x in f.readlines()]
    cornerPieces = [Piece(int(x[0]), list(x[1])) for x in piecesString]

with open('borderPieces.txt') as f:
    piecesString = [x.strip().split() for x in f.readlines()]
    borderPieces = [Piece(int(x[0]), list(x[1])) for x in piecesString]

with open('innerPieces.txt') as f:
    piecesString = [x.strip().split() for x in f.readlines()]
    innerPieces = [Piece(int(x[0]), list(x[1])) for x in piecesString]

centerPiece = get_piece_by_id(139, innerPieces)
centerPiece.orientation = Piece.DOWN

board = Board()

board.place(centerPiece, [7, 8], innerPieces)

print(centerPiece)

for p in cornerPieces:
    print(p)

print(cornerPieces[0].has_tiles(['X', 'X']))
print(cornerPieces[0].has_tiles(['X', 'A']))
print(cornerPieces[0].has_tiles(['X', 'S']))
print(cornerPieces[0].has_tiles(['X', 's']))
print(cornerPieces[0].has_tiles(['R', 'X']))
print(cornerPieces[0].has_tiles(['R', 'S']))
print(cornerPieces[0].has_tiles(['S', 'R']))
print(cornerPieces[0].has_tiles(['S', 'X']))

pieces = [3, 43, 47, 53, 55, 58, 23, 51, 17, 19, 20, 33, 9, 42, 21, 4, 16, 11, 37, 12, 57, 18, 6, 25, 59, 13, 7, 15, 40,
          48, 2, 24, 31, 27, 29, 44, 36, 56, 35, 60, 38, 46, 14, 22, 26, 1, 52, 8, 5, 45, 54, 39, 10, 50, 49, 30, 28,
          32, 41, 34]

for i in range(len(board)):
    board.auto_place(pieces[i], [i, 0], cornerPieces + borderPieces)

for i in range(len(board) - 1):
    board.auto_place(pieces[i + len(board)], [len(board) - 1, i + 1], cornerPieces + borderPieces)

for i in range(len(board) - 1):
    board.auto_place(pieces[i + 2 * len(board) - 1], [len(board) - i - 2, len(board) - 1], cornerPieces + borderPieces)

for i in range(len(board) - 2):
    board.auto_place(pieces[i + 3 * len(board) - 1 - 1], [0, len(board) - 2 - i], cornerPieces + borderPieces)

board.print()

# first_row = horizontal_tree(board, [1, 1], innerPieces)
#
# print(len(first_row))

explore_tree(board, [], [1, 1], innerPieces[2::3]+innerPieces[::3]+innerPieces[1::3]) # 123
# explore_tree(board, [], [1, 1], innerPieces[-3::-3]+innerPieces[::-3]+innerPieces[-2::-3])

# first_rows = get_trees(board, [1, 1], innerPieces, HORIZONTAL)
# last_rows = get_trees(board, [1, 14], innerPieces, HORIZONTAL)
# left_rows = get_trees(board, [1, 1], innerPieces, VERTICAL)
# right_rows = get_trees(board, [14, 1], innerPieces, VERTICAL)
#
# print(len(first_rows))
# print(len(last_rows))
# print(len(left_rows))
# print(len(right_rows))
#
# count = 0
# for first_row in first_rows:
#     for left_row in left_rows:
#         if first_row[0] == left_row[0]:
#             for last_row in last_rows:
#                 if left_row[-1] == last_rows[0]:
#                     for right_row in right_rows:
#                         if last_row[-1] == right_row[-1] and right_row[0] == first_row[-1]:
#                             row = first_row + right_row[1:] + last_row[1:] + left_row[1:]
#                             if len(set(row)) == 52:
#                                 print(row)
#     count += 1
#     print(count)
