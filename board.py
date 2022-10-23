from piece import *


class Board:
    PieceList = []
    Direction = 0
    _CenterPos = PiecePoint(0, 0)

    def __init__(self):
        pass

    def set_pieces(self, pieces):
        self.PieceList = pieces

    def add_piece(self, pc):
        self.PieceList.append(pc)

    def set_center_pos(self, x, y):
        self._CenterPos = PiecePoint(x, y)

    def get_center_pos(self):
        return self._CenterPos

    def switch_direction(self):
        self.Direction = (self.Direction + 1) % 2
        # resort pieces
        # TODO

    def revert(self):
        # TODO
        pass
