
from PiecePoint import *
# Importing ImageDraw for
# using floodfill function
from PIL import Image, ImageDraw

class Piece:
    _Type = "" #""RED", "BLACK"
    Position = PiecePoint(0, 0)
    ImagePath = ""
    ImageInCanvas = object
    ResizedImageInCanvas = object
    UIState = ""
    ImageID = 0
    _Name = ""
    _ID = 0
    _Status = 0 # 0: live, 1: dead, 2:bling, 3: moving
    _IsSelected = False
    _MoveSteps = 0
    _OriginalPosition = PiecePoint(0, 0)

    def __init__(self, type, name, id, pt, image):
        self._Type = type
        self._Name = name
        self.ID = id
        self.Position = pt
        self.ImagePath = image
        self.UIState = "Show"
        self._Status = 0
        self._OriginalPosition = PiecePoint(pt.PosX, pt.PosY)

    def SetPosition(self, pt):
        self.Position = pt

    def SetImage(self, fileName):
        self.ImagePath = fileName

    def SetStatus(self, status):
        self._Status = status

    def GetStatus(self):
        return self._Status

    def GetName(self):
        return self._Name

    def GetMoveSteps(self):
        return self._MoveSteps

    def GetOriginalPosition(self):
        return self._OriginalPosition

    def Select(self):
        self._IsSelected = True

    def DeSelect(self):
        self._IsSelected = False

    def IsSelected(self):
        return self._IsSelected

    def Refine(self):

        # Opening the image and
        # converting its type to RGBA
        img = Image.open(self.ImagePath).convert('RGBA')

        # Location of seed
        seed = (0, 0)

        # Pixel Value which would
        # be used for replacement
        rep_value = (0, 0, 0, 0)

        # Calling the floodfill() function and
        # passing it image, seed, value and
        # thresh as arguments
        ImageDraw.floodfill(img, seed, rep_value, thresh=100)

        img.save(self.ImagePath + "-0.png")
        #self.canvas.create_image(60, 60, image=img)

    def GetType(self):
        return self._Type

    def Move(self, x, y):
        self.Position.PosX = x
        self.Position.PosY = y
        self._MoveSteps = self._MoveSteps + 1
        pass


