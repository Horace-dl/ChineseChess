from tkinter import *
from PiecePoint import *
from Piece import *
from Board import *
from PIL import ImageTk, Image
from RuleMgr import *

master = Tk()
master.resizable(False, False) #disable max
#init menu
menuMain = Menu(master)
master.config(menu=menuMain)
matchMenu = Menu(menuMain)
matchMenu.add_command(label="Restart")
matchMenu.add_command(label="Revert 1 step")
menuMain.add_cascade(label="Match", menu=matchMenu)

viewMenu = Menu(menuMain)
viewMenu.add_command(label="Switch Side")
menuMain.add_cascade(label="View", menu=viewMenu)


#init canvas
canvas_width = 600
canvas_height = 660
w = Canvas(master,
           width=canvas_width,
           height=canvas_height, bg="#D2BE9A")
w.pack()

y = int(canvas_height / 11)
x = int(canvas_width / 10)
boardx = x - 5
boardy = y - 5
boardxInner = x
boardyInner = y

invx = x
invy = y

#create chess piece
radiusX = invx * 2 / 5
radiusY = invy * 2 / 5
mainBoard = Board()
#init members
totalPiecesPosition = []
pieceList = []
rule = RuleMgr()
rule.SetLengthOfOneGrid(invx)
rule.SetPiecesList(pieceList)

w.create_line(x, y, canvas_width - x, y, fill="#476042", width=2)
w.create_line(x, y, x, canvas_height - y, fill="#476042", width=2)

w.create_line(canvas_width - x, y, canvas_width - x, canvas_height - y, fill="#476042", width=2)
w.create_line(x, canvas_height - y, canvas_width - x, canvas_height - y, fill="#476042", width=2)

w.create_line(boardx, boardy, canvas_width - boardx, boardy, fill="#476042", width=4)
w.create_line(boardx, boardy, boardx, canvas_height - boardy, fill="#476042", width=4)

w.create_line(canvas_width - boardx, boardy, canvas_width - boardx, canvas_height - boardy, fill="#476042", width=4)
w.create_line(boardx, canvas_height - boardy, canvas_width - boardx, canvas_height - boardy, fill="#476042", width=4)

for i in range(8):
    w.create_line(x + i * invx, y, x + i * invx, 4 * invy + y, fill="#476042", width=2)
    w.create_line(x + i * invx, 5 * invy + y, x + i * invx, canvas_height - y, fill="#476042", width=2)

for i in range(9):
    w.create_line(x, y + i * invy, canvas_width - x, y + i * invy, fill="#476042", width=2)

for i in range(9):
    for j in range(8):
        if (i == 1 or i == 7) and (j == 2 or j == 7):
            #cannon pos
            w.create_line(x + i * invx - 12, y + j * invy - 4, x + i * invx - 4, y + j * invy - 4, fill="#476042", width=2)
            w.create_line(x + i * invx - 4, y + j * invy - 12, x + i * invx - 4, y + j * invy - 4, fill="#476042", width=2)

            w.create_line(x + i * invx + 4, y + j * invy - 12, x + i * invx + 4, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy - 4, x + i * invx +12, y + j * invy - 4, fill="#476042",
                          width=2)

            w.create_line(x + i * invx - 12, y + j * invy + 4, x + i * invx - 4, y + j * invy + 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy + 4, x + i * invx + 4, y + j * invy + 12, fill="#476042",
                          width=2)

            w.create_line(x + i * invx + 4, y + j * invy + 4, x + i * invx + 12, y + j * invy + 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx - 4, y + j * invy + 4, x + i * invx - 4, y + j * invy + 12, fill="#476042",
                          width=2)

            #guard pos
        if (i == 2 or i == 4 or i == 6) and (j == 3 or j == 6):
            w.create_line(x + i * invx - 12, y + j * invy - 4, x + i * invx - 4, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx - 4, y + j * invy - 12, x + i * invx - 4, y + j * invy - 4, fill="#476042",
                          width=2)

            w.create_line(x + i * invx + 4, y + j * invy - 12, x + i * invx + 4, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy - 4, x + i * invx + 12, y + j * invy - 4, fill="#476042",
                          width=2)

            w.create_line(x + i * invx - 12, y + j * invy + 4, x + i * invx - 4, y + j * invy + 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy + 4, x + i * invx + 4, y + j * invy + 12, fill="#476042",
                          width=2)

            w.create_line(x + i * invx + 4, y + j * invy + 4, x + i * invx + 12, y + j * invy + 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx - 4, y + j * invy + 4, x + i * invx - 4, y + j * invy + 12, fill="#476042",
                          width=2)
        if i == 0 and (j == 3 or j == 6):
            w.create_line(x + i * invx + 4, y + j * invy - 12, x + i * invx + 4, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy - 4, x + i * invx + 12, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy + 4, x + i * invx + 4, y + j * invy + 12, fill="#476042",
                          width=2)
            w.create_line(x + i * invx + 4, y + j * invy + 4, x + i * invx + 12, y + j * invy + 4, fill="#476042",
                          width=2)

        if i == 8 and (j == 3 or j == 6):
            w.create_line(x + i * invx - 4, y + j * invy - 12, x + i * invx - 4, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx - 4, y + j * invy - 4, x + i * invx - 12, y + j * invy - 4, fill="#476042",
                          width=2)
            w.create_line(x + i * invx - 4, y + j * invy + 4, x + i * invx - 4, y + j * invy + 12, fill="#476042",
                          width=2)
            w.create_line(x + i * invx - 4, y + j * invy + 4, x + i * invx - 12, y + j * invy + 4, fill="#476042",
                          width=2)

        if i == 3 and j == 2:
            w.create_line(x + i * invx, y + j * invy, x + 5 * invx, y, fill="#476042",width=2)
            w.create_line(x + i * invx, y, x + 5 * invx, y + invy * j, fill="#476042",width=2)
        if i == 3 and j == 7:
            w.create_line(x + i * invx, y + j * invy, x + 5 * invx, y + 9 * invy, fill="#476042",width=2)
            w.create_line(x + i * invx, canvas_height - y, x + 5 * invx, y + invy * j, fill="#476042",width=2)


filename0 = PhotoImage(file = "Res\\ch.png")
image0 = w.create_image(200, canvas_height / 2, image=filename0)

filename1 = PhotoImage(file = "Res\\hj.png")
image1 = w.create_image(400, canvas_height / 2, image=filename1)


#store the points of chess piece
pos = PiecePoint(0,0)
for i in range(9):
    for j in range(10):
        pos = PiecePoint(boardxInner + invx * i, boardyInner + invy * j)
        totalPiecesPosition.append(pos)
'''
def Showpiece():
    rookBPic0 = Image.open(rookBPiece0.ImagePath)
    # The (450, 350) is (height, width)
    rookBPic0 = rookBPic0.resize((int(radiusX * 2), int(radiusY * 2)), Image.ANTIALIAS)
    rookBPic0_r = ImageTk.PhotoImage(rookBPic0)
    w.create_image(rookBPiece0.Position.PosX, rookBPiece0.Position.PosY, image=rookBPic0_r)
'''


#Rook - Black
rookBPiece0 = Piece("BLACK", "Rook", 0, PiecePoint(totalPiecesPosition[0].PosX, totalPiecesPosition[0].PosY), "Res\\Rook-b.png")
pieceList.append(rookBPiece0)

rookBPiece1 = Piece("BLACK", "Rook", 1, PiecePoint(totalPiecesPosition[80].PosX, totalPiecesPosition[80].PosY), "Res\\Rook-b.png")
pieceList.append(rookBPiece1)

# Rook - Red
rookRPiece0 = Piece("RED", "Rook", 0, PiecePoint(totalPiecesPosition[9].PosX, totalPiecesPosition[9].PosY), "Res\\Rook-r.png")
pieceList.append(rookRPiece0)

rookRPiece1 = Piece("RED", "Rook", 1, PiecePoint(totalPiecesPosition[89].PosX, totalPiecesPosition[89].PosY), "Res\\Rook-r.png")
pieceList.append(rookRPiece1)

#Knight - Black
knightBPiece0 = Piece("BLACK", "Knight", 0, PiecePoint(totalPiecesPosition[10].PosX, totalPiecesPosition[10].PosY), "Res\\Knight-b.png")
pieceList.append(knightBPiece0)

knightBPiece1 = Piece("BLACK", "Knight", 1, PiecePoint(totalPiecesPosition[70].PosX, totalPiecesPosition[70].PosY), "Res\\Knight-b.png")
pieceList.append(knightBPiece1)
#Knight - Red
knightRPiece0 = Piece("RED", "Knight", 0, PiecePoint(totalPiecesPosition[19].PosX, totalPiecesPosition[19].PosY), "Res\\Knight-r.png")
pieceList.append(knightRPiece0)

knightRPiece1 = Piece("RED", "Knight", 1, PiecePoint(totalPiecesPosition[79].PosX, totalPiecesPosition[79].PosY), "Res\\Knight-r.png")
pieceList.append(knightRPiece1)

#Ministor - Black
ministorBPiece0 = Piece("BLACK", "Minister", 0, PiecePoint(totalPiecesPosition[20].PosX, totalPiecesPosition[20].PosY), "Res\\Minister-b.png")
pieceList.append(ministorBPiece0)

ministorBPiece1 = Piece("BLACK", "Minister", 1, PiecePoint(totalPiecesPosition[60].PosX, totalPiecesPosition[60].PosY), "Res\\Minister-b.png")
pieceList.append(ministorBPiece1)
#Ministor - Red
ministorRPiece0 = Piece("RED", "Minister", 0, PiecePoint(totalPiecesPosition[29].PosX, totalPiecesPosition[29].PosY), "Res\\Minister-r.png")
pieceList.append(ministorRPiece0)

ministorRPiece1 = Piece("RED", "Minister", 1, PiecePoint(totalPiecesPosition[69].PosX, totalPiecesPosition[69].PosY), "Res\\Minister-r.png")
pieceList.append(ministorRPiece1)


#Soldier - Black
soldierBPiece0 = Piece("BLACK", "Soldier", 0, PiecePoint(totalPiecesPosition[30].PosX, totalPiecesPosition[30].PosY), "Res\\Soldier-b.png")
pieceList.append(soldierBPiece0)

soldierBPiece1 = Piece("BLACK", "Soldier", 1, PiecePoint(totalPiecesPosition[50].PosX, totalPiecesPosition[50].PosY), "Res\\Soldier-b.png")
pieceList.append(soldierBPiece1)
#Soldier - Red
soldierRPiece0 = Piece("RED", "Soldier", 0, PiecePoint(totalPiecesPosition[39].PosX, totalPiecesPosition[39].PosY), "Res\\Soldier-r.png")
pieceList.append(soldierRPiece0)

soldierRPiece1 = Piece("RED", "Soldier", 1, PiecePoint(totalPiecesPosition[59].PosX, totalPiecesPosition[59].PosY), "Res\\Soldier-r.png")
pieceList.append(soldierRPiece1)

#General - Black
generalBPiece0 = Piece("BLACK", "General", 0, PiecePoint(totalPiecesPosition[40].PosX, totalPiecesPosition[40].PosY), "Res\\General.png")
pieceList.append(generalBPiece0)

#Marshal - Red
marshalRPiece0 = Piece("RED", "Marshal", 0, PiecePoint(totalPiecesPosition[49].PosX, totalPiecesPosition[49].PosY), "Res\\Marshal.png")
pieceList.append(marshalRPiece0)
rule.SetCenterPos(PiecePoint(totalPiecesPosition[49].PosX, totalPiecesPosition[49].PosY))

#Cannon - Black
cannonBPiece0 = Piece("BLACK", "Cannon", 0, PiecePoint(totalPiecesPosition[12].PosX, totalPiecesPosition[12].PosY), "Res\\Cannon-b.png")
pieceList.append(cannonBPiece0)

cannonBPiece1 = Piece("BLACK", "Cannon", 1, PiecePoint(totalPiecesPosition[72].PosX, totalPiecesPosition[72].PosY), "Res\\Cannon-b.png")
pieceList.append(cannonBPiece1)
#Cannon - Red
cannonRPiece0 = Piece("RED", "Cannon", 0, PiecePoint(totalPiecesPosition[17].PosX, totalPiecesPosition[17].PosY), "Res\\Cannon-r.png")
pieceList.append(cannonRPiece0)

cannonRPiece1 = Piece("RED", "Cannon", 1, PiecePoint(totalPiecesPosition[77].PosX, totalPiecesPosition[77].PosY), "Res\\Cannon-r.png")
pieceList.append(cannonRPiece1)

#Guard - Black
guardBPiece0 = Piece("BLACK", "Guard", 0, PiecePoint(totalPiecesPosition[3].PosX, totalPiecesPosition[3].PosY), "Res\\Guard-b.png")
pieceList.append(guardBPiece0)

guardBPiece1 = Piece("BLACK", "Guard", 1, PiecePoint(totalPiecesPosition[23].PosX, totalPiecesPosition[23].PosY), "Res\\Guard-b.png")
pieceList.append(guardBPiece1)

guardBPiece2 = Piece("BLACK", "Guard", 2, PiecePoint(totalPiecesPosition[43].PosX, totalPiecesPosition[43].PosY), "Res\\Guard-b.png")
pieceList.append(guardBPiece2)

guardBPiece3 = Piece("BLACK", "Guard", 3, PiecePoint(totalPiecesPosition[63].PosX, totalPiecesPosition[63].PosY), "Res\\Guard-b.png")
pieceList.append(guardBPiece3)

guardBPiece4 = Piece("BLACK", "Guard", 4, PiecePoint(totalPiecesPosition[83].PosX, totalPiecesPosition[83].PosY), "Res\\Guard-b.png")
pieceList.append(guardBPiece4)

#Guard - Red
guardRPiece0 = Piece("RED", "Guard", 0, PiecePoint(totalPiecesPosition[6].PosX, totalPiecesPosition[6].PosY), "Res\\Guard-r.png")
pieceList.append(guardRPiece0)

guardRPiece1 = Piece("RED", "Guard", 1, PiecePoint(totalPiecesPosition[26].PosX, totalPiecesPosition[26].PosY), "Res\\Guard-r.png")
pieceList.append(guardRPiece1)

guardRPiece2 = Piece("RED", "Guard", 2, PiecePoint(totalPiecesPosition[46].PosX, totalPiecesPosition[46].PosY), "Res\\Guard-r.png")
pieceList.append(guardRPiece2)

guardRPiece3 = Piece("RED", "Guard", 3, PiecePoint(totalPiecesPosition[66].PosX, totalPiecesPosition[66].PosY), "Res\\Guard-r.png")
pieceList.append(guardRPiece3)

guardRPiece4 = Piece("RED", "Guard", 4, PiecePoint(totalPiecesPosition[86].PosX, totalPiecesPosition[86].PosY), "Res\\Guard-r.png")
pieceList.append(guardRPiece4)

cannonBPiece0.Refine()

mainBoard.SetPieces(pieceList)

rule.StartMatch()


#draw init pieces


def RefineImage(radiusX, radiusY, paraPiece):
    paraPiece.ImageInCanvas = Image.open(paraPiece.ImagePath)
    # The (450, 350) is (height, width)
    paraPiece.ImageInCanvas = paraPiece.ImageInCanvas.resize((int(radiusX * 2), int(radiusY * 2)), Image.Resampling.LANCZOS)
    paraPiece.ResizedImageInCanvas = ImageTk.PhotoImage(paraPiece.ImageInCanvas)
    paraPiece.ImageID = w.create_image(paraPiece.Position.PosX, paraPiece.Position.PosY, image=paraPiece.ResizedImageInCanvas)

for pc in pieceList:
    RefineImage(radiusX, radiusY, pc)


def BlingOnePiece():
    for p in pieceList:
        if p.GetStatus() == 2:#bling
            if p.UIState == "Show":
                w.itemconfig(p.ImageID, state='hidden')
                p.UIState = "Hide"
            else:
                w.itemconfig(p.ImageID, state='normal')
                p.UIState = "Show"
        else:
            w.itemconfig(p.ImageID, state='normal')
    master.after(400, BlingOnePiece)

BlingOnePiece()

def TryEatPiece(p1, p2): #p1 eat p2
    # check if we could move to the position
    successful = rule.CheckEat(p1, p2)
    if successful == False:
        return False
    w.move(p1.ImageID, p2.Position.PosX - p1.Position.PosX, p2.Position.PosY - p1.Position.PosY)
    p1.SetPosition(p2.Position)
    p2.SetStatus(1)#dead
    p2.SetPosition(PiecePoint(0,0))
    w.itemconfig(p2.ImageID, state='hidden')
    w.move(p2.ImageID, -1 * canvas_width, - 1 * canvas_height)

    return True

def HandleCurrentPiece(x, y):
    originalPiece = None
    targetPiece = None
    xPos = 0
    yPos = 0
    for p in pieceList:
        if p.IsSelected():
            originalPiece = p
            break

    for targetPos in totalPiecesPosition:
        xPos = targetPos.PosX
        yPos = targetPos.PosY
        if (xPos + radiusX > x and xPos - radiusX < x and yPos + radiusY > y and yPos - radiusY < y):
            for p in pieceList:
                if p.Position.PosX == xPos and p.Position.PosY == yPos:
                    targetPiece = p
                    break
            break


    if originalPiece != None:
        res = False
        if targetPiece == None:
            res = TryMovePiece(originalPiece, xPos, yPos)
        else:
            res = TryEatPiece(originalPiece, targetPiece)
        if res == True:
            rule.SwitchPlayer()

    for p in pieceList:
        p.DeSelect()


def TryMovePiece(originalPiece, xPos, yPos):
    #check if we could move to the position
    successful = rule.CheckMove(originalPiece, PiecePoint(xPos, yPos))
    if successful == False:
        return False
    w.itemconfig(originalPiece.ImageID, state='normal')
    originalPiece.UIState = "Show"
    w.move(originalPiece.ImageID, xPos - originalPiece.Position.PosX, yPos - originalPiece.Position.PosY)
    originalPiece.Move(xPos, yPos)
    originalPiece.DeSelect()
    originalPiece.SetStatus(0)
    return True

def ClickOnCanvas(event):
    clickInPiece = False
    x = event.x
    y = event.y
    preSelectedPiece = None
    #find according piece
    for p in pieceList:
        if p.GetStatus() == 2: #bling
            p.SetStatus(0)
            preSelectedPiece = p
    #bling the piece
    for p in pieceList:
        playerNow = rule.GetCurrentPlayer()
        if p.GetType() != playerNow:
            continue
        if p.Position.PosX + radiusX > x and p.Position.PosX - radiusX < x and p.Position.PosY + radiusY > y and p.Position.PosY - radiusY < y:
            if p.IsSelected():
                p.DeSelect()
            else:
                p.Select()
                p.SetStatus(2)  # bling it
                if preSelectedPiece != None:
                    preSelectedPiece.DeSelect()

            clickInPiece = True

    #move the piece
    if clickInPiece == False:
        HandleCurrentPiece(x, y)

w.bind('<Button-1>', ClickOnCanvas)




mainloop()