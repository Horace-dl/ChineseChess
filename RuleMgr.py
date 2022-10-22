from PiecePoint import *
from Piece import *

class RuleMgr:
    _centerPos = PiecePoint(0, 0)
    _currentPlayer = ""
    _lengthOfOneGrid = 0
    _pieceList = None


    def __init__(self):
        _currentPlayer = "RED"
        _lengthOfOneGrid = 0
        _pieceList = []

    def SetLengthOfOneGrid(self, length):
        self._lengthOfOneGrid = length

    def GetLengthOfOneGrid(self):
        return self._lengthOfOneGrid
    
    def GetPossiblePos(self, type, index):
        pass

    def SetPiecesList(self, pieceList):
        self._pieceList = pieceList

    def GetCenterPos(self):
        return self._centerPos

    def SetCenterPos(self, pt):
        self._centerPos = pt

    def StartMatch(self):
        self._currentPlayer = "RED"

    def SwitchPlayer(self):
        if self._currentPlayer == "RED":
            self._currentPlayer = "BLACK"
        else:
            self._currentPlayer = "RED"

    def GetCurrentPlayer(self):
        return self._currentPlayer

    def RookMoveLine(self, thisPiece, newPoint):
        returnVal = False
        if thisPiece.Position.PosX == newPoint.PosX:
            thereIsOne = 0
            for pc in self._pieceList:
                if pc.Position.PosX == newPoint.PosX and (
                        (pc.Position.PosY < thisPiece.Position.PosY and pc.Position.PosY > newPoint.PosY) or (
                        pc.Position.PosY > thisPiece.Position.PosY and pc.Position.PosY < newPoint.PosY)):
                    thereIsOne = thereIsOne + 1
                    break
            if thereIsOne == 1:
                returnVal = False
            else:
                returnVal = True

        elif thisPiece.Position.PosY == newPoint.PosY:
            thereIsOne = 0
            for pc in self._pieceList:
                if pc.Position.PosY == newPoint.PosY and (
                        (pc.Position.PosX < thisPiece.Position.PosX and pc.Position.PosX > newPoint.PosX) or (
                        pc.Position.PosX > thisPiece.Position.PosX and pc.Position.PosX < newPoint.PosX)):
                    thereIsOne = thereIsOne + 1
                    break
            if thereIsOne == 1:
                returnVal = False
            else:
                returnVal = True

        return returnVal

    def KnightMoveGrid(self, thisPiece, newPoint):
        returnVal = False
        #one grid in x axis, two grid in y axis
        if thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX and pc.Position.PosY == thisPiece.Position.PosY - self._lengthOfOneGrid:
                    returnVal = False
                    break

        elif thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX and pc.Position.PosY == thisPiece.Position.PosY - self._lengthOfOneGrid:
                    returnVal = False
                    break
        elif thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosY == thisPiece.Position.PosY and pc.Position.PosX == thisPiece.Position.PosX + self._lengthOfOneGrid:
                    returnVal = False
                    break
        elif thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosY == thisPiece.Position.PosY and pc.Position.PosX == thisPiece.Position.PosX + self._lengthOfOneGrid:
                    returnVal = False
                    break

        elif thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX and pc.Position.PosY == thisPiece.Position.PosY + self._lengthOfOneGrid:
                    returnVal = False
                    break

        elif thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX and pc.Position.PosY == thisPiece.Position.PosY + self._lengthOfOneGrid:
                    returnVal = False
                    break

        elif thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosY == thisPiece.Position.PosY and pc.Position.PosX == thisPiece.Position.PosX - self._lengthOfOneGrid:
                    returnVal = False
                    break

        elif thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosY == thisPiece.Position.PosY and pc.Position.PosX == thisPiece.Position.PosX - self._lengthOfOneGrid:
                    returnVal = False
                    break

        return returnVal

    def MinisterMoveField(self, thisPiece, newPoint):
        returnVal = False
        if (newPoint.PosY < thisPiece.GetOriginalPosition().PosY - self._lengthOfOneGrid * 4) or (newPoint.PosY > thisPiece.GetOriginalPosition().PosY + self._lengthOfOneGrid * 4):
            return returnVal
        if thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX - self._lengthOfOneGrid and pc.Position.PosY == thisPiece.Position.PosY - self._lengthOfOneGrid:
                    returnVal = False
                    break
        elif thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX + self._lengthOfOneGrid and pc.Position.PosY == thisPiece.Position.PosY - self._lengthOfOneGrid:
                    returnVal = False
                    break
        elif thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX + self._lengthOfOneGrid and pc.Position.PosY == thisPiece.Position.PosY + self._lengthOfOneGrid:
                    returnVal = False
                    break

        elif thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid * 2 and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid * 2:
            returnVal = True
            for pc in self._pieceList:
                if pc.Position.PosX == thisPiece.Position.PosX - self._lengthOfOneGrid and pc.Position.PosY == thisPiece.Position.PosY + self._lengthOfOneGrid:
                    returnVal = False
                    break

        return returnVal

    def SoldierMoveDia(self, thisPiece, newPoint):
        returnVal = False
        oriPosX = self._centerPos.PosX
        oriPosY = thisPiece.GetOriginalPosition().PosY
        if (newPoint.PosX < oriPosX - self._lengthOfOneGrid) or (
                newPoint.PosX > oriPosX + self._lengthOfOneGrid) or (
                newPoint.PosY < oriPosY - self._lengthOfOneGrid * 2) or (
                newPoint.PosY > oriPosY + self._lengthOfOneGrid * 2):
            return returnVal
        if thisPiece.Position.PosX + self._lengthOfOneGrid == newPoint.PosX and thisPiece.Position.PosY - self._lengthOfOneGrid == newPoint.PosY:
            returnVal = True
        elif thisPiece.Position.PosX - self._lengthOfOneGrid == newPoint.PosX and thisPiece.Position.PosY - self._lengthOfOneGrid == newPoint.PosY:
            returnVal = True
        elif thisPiece.Position.PosY + self._lengthOfOneGrid == newPoint.PosY and thisPiece.Position.PosX - self._lengthOfOneGrid == newPoint.PosX:
            returnVal = True
        elif thisPiece.Position.PosY + self._lengthOfOneGrid == newPoint.PosY and thisPiece.Position.PosX + self._lengthOfOneGrid == newPoint.PosX:
            returnVal = True

        return returnVal

    def MarshalMoveInPalace(self, thisPiece, newPoint):
        returnVal = False
        oriPos = thisPiece.GetOriginalPosition()
        if (newPoint.PosX < oriPos.PosX - self._lengthOfOneGrid) or (newPoint.PosX > oriPos.PosX + self._lengthOfOneGrid) or (newPoint.PosY < oriPos.PosY - self._lengthOfOneGrid * 2) or (newPoint.PosY > oriPos.PosY + self._lengthOfOneGrid * 2):
            return returnVal
        if thisPiece.Position.PosX == newPoint.PosX and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid:
            returnVal = True
        elif thisPiece.Position.PosX == newPoint.PosX and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid:
            returnVal = True
        elif thisPiece.Position.PosY == newPoint.PosY and thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid:
            returnVal = True
        elif thisPiece.Position.PosY == newPoint.PosY and thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid:
            returnVal = True

        return returnVal

    def GuardMoveOneStep(self, thisPiece, newPoint):
        returnVal = False
        theType = thisPiece.GetType()
        if theType == "RED":
            if thisPiece.Position.PosX == newPoint.PosX and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid:
                returnVal = True
            # cross the river
            moveSteps = thisPiece.GetMoveSteps()
            if moveSteps > 1:
                if thisPiece.Position.PosY == newPoint.PosY and (
                        thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid or thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid):
                    returnVal = True
        elif theType == "BLACK":
            if thisPiece.Position.PosX == newPoint.PosX and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid:
                returnVal = True
            # cross the river
            if thisPiece.GetMoveSteps() > 1:
                if thisPiece.Position.PosY == newPoint.PosY and (
                        thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid or thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid):
                    returnVal = True

        return returnVal

    def CannonMoveSkipOnePiece(self, thisPiece, newPoint):
        returnVal = False
        if thisPiece.Position.PosX == newPoint.PosX:
            thereIsOne = 0
            for pc in self._pieceList:
                if pc.Position.PosX == newPoint.PosX and (
                        (pc.Position.PosY < thisPiece.Position.PosY and pc.Position.PosY > newPoint.PosY) or (
                        pc.Position.PosY > thisPiece.Position.PosY and pc.Position.PosY < newPoint.PosY)):
                    thereIsOne = thereIsOne + 1
                    break
            if thereIsOne == 1:
                returnVal = False
            else:
                returnVal = True

        elif thisPiece.Position.PosY == newPoint.PosY:
            thereIsOne = 0
            for pc in self._pieceList:
                if pc.Position.PosY == newPoint.PosY and (
                        (pc.Position.PosX < thisPiece.Position.PosX and pc.Position.PosX > newPoint.PosX) or (
                        pc.Position.PosX > thisPiece.Position.PosX and pc.Position.PosX < newPoint.PosX)):
                    thereIsOne = thereIsOne + 1
                    break
            if thereIsOne == 1:
                returnVal = False
            else:
                returnVal = True

        return returnVal

    def GeneralMoveInPalace(self, thisPiece, newPoint):
        returnVal = False
        oriPos = thisPiece.GetOriginalPosition()
        if (newPoint.PosX < oriPos.PosX - self._lengthOfOneGrid) or (
                newPoint.PosX > oriPos.PosX + self._lengthOfOneGrid) or (
                newPoint.PosY < oriPos.PosY - self._lengthOfOneGrid * 2) or (
                newPoint.PosY > oriPos.PosY + self._lengthOfOneGrid * 2):
            return returnVal
        if thisPiece.Position.PosX == newPoint.PosX and thisPiece.Position.PosY == newPoint.PosY - self._lengthOfOneGrid:
            returnVal = True
        elif thisPiece.Position.PosX == newPoint.PosX and thisPiece.Position.PosY == newPoint.PosY + self._lengthOfOneGrid:
            returnVal = True
        elif thisPiece.Position.PosY == newPoint.PosY and thisPiece.Position.PosX == newPoint.PosX - self._lengthOfOneGrid:
            returnVal = True
        elif thisPiece.Position.PosY == newPoint.PosY and thisPiece.Position.PosX == newPoint.PosX + self._lengthOfOneGrid:
            returnVal = True

        return returnVal

    _switcher = {
            "Rook": RookMoveLine,
            "Knight": KnightMoveGrid,
            "Minister": MinisterMoveField,
            "Soldier": SoldierMoveDia,
            "Marshal": MarshalMoveInPalace,
            "Guard": GuardMoveOneStep,
            "Cannon": CannonMoveSkipOnePiece,
            "General": GeneralMoveInPalace
        }

    def CheckMove(self, currentPiece, ptNew):
        # get current piece type
        theName = currentPiece.GetName()
        funcRule = self._switcher.get(theName)
        returnVal = False
        if funcRule:
            returnVal = funcRule(self, currentPiece, ptNew)

        return returnVal

    def RookEatLine(self, piece1, piece2):
        return self.RookMoveLine(piece1, piece2.Position)

    def KnightEatGrid(self, piece1, piece2):
        return self.KnightMoveGrid(piece1, piece2.Position)

    def MinisterEatField(self, piece1, piece2):
        return self.MinisterMoveField(piece1, piece2.Position)

    def SoldierEatDia(self, piece1, piece2):
        return self.SoldierMoveDia(piece1, piece2.Position)

    def MarshalEatInPalace(self, piece1, piece2):
        return self.MarshalMoveInPalace(piece1, piece2.Position)

    def GuardEatOneStep(self, piece1, piece2):
        return self.GuardMoveOneStep(piece1, piece2.Position)

    def CannonEatSkipOnePiece(self, piece1, piece2):
        returnVal = False
        if piece1.Position.PosX == piece2.Position.PosX:
            thereIsOne = 0
            for pc in self._pieceList:
                if pc.Position.PosX == piece2.Position.PosX and ((pc.Position.PosY < piece1.Position.PosY and pc.Position.PosY > piece2.Position.PosY) or (pc.Position.PosY > piece1.Position.PosY and pc.Position.PosY < piece2.Position.PosY)):
                    thereIsOne = thereIsOne + 1
                    continue
            if thereIsOne == 1:
                returnVal = True

        elif piece1.Position.PosY == piece2.Position.PosY:
            thereIsOne = 0
            for pc in self._pieceList:
                if pc.Position.PosY == piece2.Position.PosY and ((pc.Position.PosX < piece1.Position.PosX and pc.Position.PosX > piece2.Position.PosX) or (pc.Position.PosX > piece1.Position.PosX and pc.Position.PosX < piece2.Position.PosX)):
                    thereIsOne = thereIsOne + 1
                    continue
            if thereIsOne == 1:
                returnVal = True

        return returnVal

    def GeneralEatInPalace(self, piece1, piece2):
        return self.GeneralMoveInPalace(piece1, piece2.Position)

    _switcherEat = {
        "Rook": RookEatLine,
        "Knight": KnightEatGrid,
        "Minister": MinisterEatField,
        "Soldier": SoldierEatDia,
        "Marshal": MarshalEatInPalace,
        "Guard": GuardEatOneStep,
        "Cannon": CannonEatSkipOnePiece,
        "General": GeneralEatInPalace
    }

    def CheckEat(self, p1, p2):
        # get current piece type
        theName = p1.GetName()
        funcRule = self._switcherEat.get(theName)
        returnVal = False
        if funcRule:
            returnVal = funcRule(self, p1, p2)

        return returnVal