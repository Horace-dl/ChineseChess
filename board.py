from piece import *


class Board:
    PieceList = []
    # red : 0 , black : 1
    direction = 0
    _center_pos = PiecePoint(0, 0)
    _internal_size = 0

    def __init__(self):
        pass

    def set_internal_size(self, value):
        self._internal_size = value

    def get_internal_size(self):
        return self._internal_size

    def set_pieces(self, pieces):
        self.PieceList = pieces

    def add_piece(self, pc):
        self.PieceList.append(pc)

    def set_center_pos(self, x, y):
        self._center_pos = PiecePoint(x, y)

    def get_center_pos(self):
        return self._center_pos

    def switch_direction(self):
        self.direction = (self.direction + 1) % 2
        # resort pieces
        for pc in self.PieceList:
            pt = pc.get_position()
            pos_x = pt.get_x_pos()
            pos_y = pt.get_y_pos()
            pt_new = PiecePoint(self._internal_size * 10 - pos_x, self._internal_size * 11 - pos_y)
            pc.set_position(pt_new)
            pc

    def revert(self):
        # TODO
        pass
