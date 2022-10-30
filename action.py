from piece import *


class Action:
    #  "Move", "Eat"
    _actionName = ""
    #  first piece
    _pieceItemA = None

    _originalPos = None

    _newPos = None
    #  second piece
    _pieceItemB = None

    def __init__(self, actionName):
        self._actionName = actionName

    def get_action_name(self):
        return self._actionName

    def set_piece_a(self, pieceA):
        self._pieceItemA = pieceA

    def set_piece_b(self, pieceB):
        self._pieceItemB = pieceB

    def set_original_pos(self, pos):
        self._originalPos = pos

    def set_new_pos(self, pos):
        self._newPos = pos

    def get_piece_a(self):
        return self._pieceItemA

    def get_piece_b(self):
        return self._pieceItemB

    def get_original_pos(self):
        return self._originalPos

    def get_new_pos(self):
        return self._newPos
