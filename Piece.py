class Piece:
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    UNKNOWN = 4

    def __init__(self, piece_id, tiles, orientation=UNKNOWN, position=[-1, -1]):
        self.piece_id = piece_id
        self.tiles = tiles
        self.orientation = orientation
        self.position = position

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.piece_id == other.piece_id
        else:
            return self.piece_id == other

    def __hash__(self):
        return hash(self.piece_id)

    def has_tiles(self, tiles):
        positions = [i for i, e in enumerate(self.tiles) if e == tiles[0]]
        for position in positions:
            piece_tiles = shift(self.tiles, position)
            if piece_tiles[:len(tiles)] == tiles:
                return True
        return False

    def orientations_of_tiles(self, tiles, pos1):
        positions = [i for i, e in enumerate(self.tiles) if e == tiles[0]]
        orientations = []
        for position in positions:
            piece_tiles = shift(self.tiles, position)
            if piece_tiles[:len(tiles)] == tiles:
                if position % 2 == 1:
                    pos_aux = position + 2 % 4
                else:
                    pos_aux = position
                orientations.append((pos_aux - pos1) % 4)
        return orientations

    # def has_tiles(self, tile1, tile2):
    #     tiles = self.tiles + [self.tiles[0]]
    #     positions = [i for i, e in enumerate(self.tiles) if e == tile1]
    #     for position in positions:
    #         if tiles[position + 1] == tile2:
    #             return True
    #     return False
    #
    # def orientations_of_tiles(self, tile1, tile2, pos1):
    #     tiles = self.tiles + [self.tiles[0]]
    #     positions = [i for i, e in enumerate(self.tiles) if e == tile1]
    #     orientations = []
    #     for position in positions:
    #         if tiles[position + 1] == tile2:
    #             if position % 2 == 1:
    #                 pos_aux = position + 2 % 4
    #             else:
    #                 pos_aux = position
    #             orientations.append((pos_aux - pos1) % 4)
    #     return orientations

    def __str__(self):
        ret = "(" + str(self.piece_id) + ") " + str(self.tiles) + ", orientation: "
        if self.orientation == self.DOWN:
            ret += "DOWN"
        elif self.orientation == self.LEFT:
            ret += "LEFT"
        elif self.orientation == self.UP:
            ret += "UP"
        elif self.orientation == self.RIGHT:
            ret += "RIGHT"
        else:
            ret += "UNKNOWN"

        return ret + ", position: " + str(self.position)

    def print(self):
        ret = "(" + str(self.piece_id) + ") Position:" + str(self.position) + "\n"
        ret += " " + self.top_tile() + "\n"
        ret += self.left_tile() + " " + self.right_tile() + "\n"
        ret += " " + self.bottom_tile() + " "

        if self.orientation == self.UNKNOWN:
            ret += "???"

        print(ret + "\n")

    def bottom_tile(self):
        return self.tiles[0 - self.orientation]

    def right_tile(self):
        return self.tiles[1 - self.orientation]

    def top_tile(self):
        return self.tiles[2 - self.orientation]

    def left_tile(self):
        return self.tiles[3 - self.orientation]


def shift(list, times):
    return list[times:] + list[:times]


def get_piece_by_id(piece_id, pieces):
    return next((x for x in pieces if x.piece_id == piece_id), None)
