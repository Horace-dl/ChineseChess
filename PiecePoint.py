class PiecePoint:
    PosX = 0
    PosY = 0

    def __init__(self, x, y):
        self.PosX = x
        self.PosY = y

    def SetXPos(self, x):
        self.PosX = x

    def SetYPos(self, y):
        self.PosY = y

    def GetXPos(self):
        return self.PosX

    def GetYPos(self):
        return self.PosY

    def __add__(self, o):
        
        self.PosX = self.PosX + o.PosX
        self.PosY = self.PosY + o.PosY
        return self

