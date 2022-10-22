from Piece import *
class Action:

    _actionName = ""

    _pieceItemA = None

    _originalPos = None

    _newPos = None

    _pieceItemB = None

    def __init__(self, actionName):
        _actionName = actionName

    def GetActionName(self):
        return self._actionName

    def SetPieceA(self, pieceA):
        self._pieceItemA = pieceA

    def SetPieceB(self, pieceB):
        self._pieceItemB = pieceB

    def SetOriginalPos(self, pos):
        self._originalPos = pos

    def SetNewPos(self, pos):
        self._newPos = pos

    def GetPieceA(self):
        return self._pieceItemA

    def GetPieceB(self):
        return self._pieceItemB

    def GetOriginalPos(self):
        return self._originalPos

    def GetNewPos(self):
        return self._newPos
