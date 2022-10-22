from Piece import *

class Board:
    PieceList = []
    Direction = 0
    _CenterPos = PiecePoint(0, 0)

    def __init__(self):
        pass

    def SetPieces(self, pieces):
        self.PieceList = pieces

    def AddPiece(self, pc):
        self.PieceList.append(pc)

    def SetCenterPos(self, x, y):
        self._CenterPos = PiecePoint(x, y)

    def GetCenterPos(self):
        return self._CenterPos

    def SwitchDirection(self):
        self.Direction = (self.Direction + 1) % 2
        #resort pieces
        #TODO

    def Revert(self):
        #TODO
        pass

