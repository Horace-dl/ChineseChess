from tkinter import *
from piece_point import *
from piece import *
from board import *
from PIL import ImageTk, Image
from rule_mgr import *
from action_mgr import *
from playsound import playsound

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 660


class CanvasBoard:
    _master = None
    _board_canvas = None
    _board_model = None
    _rule = None
    _action_mgr = None
    _all_pieces_positions = []
    _all_piece_list = []
    _board_inner_width = 0
    _board_inner_height = 0
    _radius = 0

    def __init__(self, root):
        self._master = root

    def init_members(self):
        # init members
        self._all_pieces_positions = []
        self._all_piece_list = []
        self._board_inner_width = 0
        self._board_inner_height = 0
        self._radius = 0

    def init_canvas(self):
        #  init canvas
        self._board_canvas = Canvas(self._master,
                                    width=CANVAS_WIDTH,
                                    height=CANVAS_HEIGHT, bg="#D2BE9A")
        self._board_canvas.pack()

        self.init_members()
        self.draw_board()
        self.generate_piece_info()

        for pc in self._all_piece_list:
            self.refine_image(self._radius, self._radius, pc)

        self.bling_one_piece()
        self._board_canvas.bind('<Button-1>', self.click_on_canvas)

    def draw_board(self):

        interval_y = int(CANVAS_HEIGHT / 11)
        interval_x = int(CANVAS_WIDTH / 10)
        single_grid_width = interval_x - 5
        single_grid_height = interval_y - 5
        self._board_inner_width = interval_x
        self._board_inner_height = interval_y

        # create chess piece
        self._radius = interval_x * 2 / 5

        self._board_model = Board()

        self._rule = RuleMgr()
        self._rule.set_length_of_one_grid(interval_x)
        self._rule.set_pieces_list(self._all_piece_list)

        self._board_canvas.create_line(interval_x, interval_y, CANVAS_WIDTH - interval_x, interval_y, fill="#476042", width=2)
        self._board_canvas.create_line(interval_x, interval_y, interval_x, CANVAS_HEIGHT - interval_y, fill="#476042", width=2)

        self._board_canvas.create_line(CANVAS_WIDTH - interval_x, interval_y, CANVAS_WIDTH - interval_x, CANVAS_HEIGHT - interval_y,
                                       fill="#476042", width=2)
        self._board_canvas.create_line(interval_x, CANVAS_HEIGHT - interval_y, CANVAS_WIDTH - interval_x, CANVAS_HEIGHT - interval_y,
                                       fill="#476042", width=2)

        self._board_canvas.create_line(single_grid_width, single_grid_height, CANVAS_WIDTH - single_grid_width,
                                       single_grid_height, fill="#476042", width=4)
        self._board_canvas.create_line(single_grid_width, single_grid_height, single_grid_width,
                                       CANVAS_HEIGHT - single_grid_height, fill="#476042", width=4)

        self._board_canvas.create_line(CANVAS_WIDTH - single_grid_width, single_grid_height,
                                       CANVAS_WIDTH - single_grid_width, CANVAS_HEIGHT - single_grid_height,
                                       fill="#476042", width=4)
        self._board_canvas.create_line(single_grid_width, CANVAS_HEIGHT - single_grid_height,
                                       CANVAS_WIDTH - single_grid_width, CANVAS_HEIGHT - single_grid_height,
                                       fill="#476042", width=4)

        for i in range(8):
            self._board_canvas.create_line(interval_x + i * interval_x, interval_y, interval_x + i * interval_x, 4 * interval_y + interval_y,
                                           fill="#476042", width=2)
            self._board_canvas.create_line(interval_x + i * interval_x, 5 * interval_y + interval_y, interval_x + i * interval_x,
                                           CANVAS_HEIGHT - interval_y, fill="#476042", width=2)

        for i in range(9):
            self._board_canvas.create_line(interval_x, interval_y + i * interval_y, CANVAS_WIDTH - interval_x, interval_y + i * interval_y,
                                           fill="#476042", width=2)

        for i in range(9):
            for j in range(8):
                if (i == 1 or i == 7) and (j == 2 or j == 7):
                    # cannon pos
                    self._board_canvas.create_line(interval_x + i * interval_x - 12, interval_y + j * interval_y - 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y - 4, fill="#476042", width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y - 12, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y - 4, fill="#476042", width=2)

                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y - 12, interval_x + i * interval_x + 4,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y - 4, interval_x + i * interval_x + 12,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)

                    self._board_canvas.create_line(interval_x + i * interval_x - 12, interval_y + j * interval_y + 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y + 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y + 4, interval_x + i * interval_x + 4,
                                                   interval_y + j * interval_y + 12, fill="#476042",
                                                   width=2)

                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y + 4, interval_x + i * interval_x + 12,
                                                   interval_y + j * interval_y + 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y + 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y + 12, fill="#476042",
                                                   width=2)

                    # guard pos
                if (i == 2 or i == 4 or i == 6) and (j == 3 or j == 6):
                    self._board_canvas.create_line(interval_x + i * interval_x - 12, interval_y + j * interval_y - 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y - 12, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)

                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y - 12, interval_x + i * interval_x + 4,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y - 4, interval_x + i * interval_x + 12,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)

                    self._board_canvas.create_line(interval_x + i * interval_x - 12, interval_y + j * interval_y + 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y + 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y + 4, interval_x + i * interval_x + 4,
                                                   interval_y + j * interval_y + 12, fill="#476042",
                                                   width=2)

                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y + 4, interval_x + i * interval_x + 12,
                                                   interval_y + j * interval_y + 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y + 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y + 12, fill="#476042",
                                                   width=2)
                if i == 0 and (j == 3 or j == 6):
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y - 12, interval_x + i * interval_x + 4,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y - 4, interval_x + i * interval_x + 12,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y + 4, interval_x + i * interval_x + 4,
                                                   interval_y + j * interval_y + 12, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x + 4, interval_y + j * interval_y + 4, interval_x + i * interval_x + 12,
                                                   interval_y + j * interval_y + 4, fill="#476042",
                                                   width=2)

                if i == 8 and (j == 3 or j == 6):
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y - 12, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y - 4, interval_x + i * interval_x - 12,
                                                   interval_y + j * interval_y - 4, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y + 4, interval_x + i * interval_x - 4,
                                                   interval_y + j * interval_y + 12, fill="#476042",
                                                   width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x - 4, interval_y + j * interval_y + 4, interval_x + i * interval_x - 12,
                                                   interval_y + j * interval_y + 4, fill="#476042",
                                                   width=2)

                if i == 3 and j == 2:
                    self._board_canvas.create_line(interval_x + i * interval_x, interval_y + j * interval_y, interval_x + 5 * interval_x, interval_y,
                                                   fill="#476042", width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x, interval_y, interval_x + 5 * interval_x, interval_y + interval_y * j,
                                                   fill="#476042", width=2)
                if i == 3 and j == 7:
                    self._board_canvas.create_line(interval_x + i * interval_x, interval_y + j * interval_y, interval_x + 5 * interval_x,
                                                   interval_y + 9 * interval_y, fill="#476042", width=2)
                    self._board_canvas.create_line(interval_x + i * interval_x, CANVAS_HEIGHT - interval_y, interval_x + 5 * interval_x,
                                                   interval_y + interval_y * j, fill="#476042", width=2)

        filename0 = PhotoImage(file="Res\\ch.png")
        image0 = self._board_canvas.create_image(200, CANVAS_HEIGHT / 2, image=filename0)

        filename1 = PhotoImage(file="Res\\hj.png")
        image1 = self._board_canvas.create_image(400, CANVAS_HEIGHT / 2, image=filename1)

    def generate_piece_info(self):

        #  store the points of chess piece
        pos = PiecePoint(0, 0)
        for i in range(9):
            for j in range(10):
                pos = PiecePoint(self._board_inner_width * (1 + i), self._board_inner_height * (1 + j))
                self._all_pieces_positions.append(pos)
        '''
        def Showpiece():
            rookBPic0 = Image.open(rookBPiece0.ImagePath)
            # The (450, 350) is (height, width)
            rookBPic0 = rookBPic0.resize((int(radiusX * 2), int(radiusY * 2)), Image.ANTIALIAS)
            rookBPic0_r = ImageTk.PhotoImage(rookBPic0)
            w.create_image(rookBPiece0.Position.PosX, rookBPiece0.Position.PosY, image=rookBPic0_r)
        '''
        #  Rook - Black
        rook_b_piece0 = Piece("BLACK", "Rook", 0, PiecePoint(self._all_pieces_positions[0].pos_x,
                                                           self._all_pieces_positions[0].pos_y), "Res\\Rook-b.png")
        self._all_piece_list.append(rook_b_piece0)

        rook_b_piece1 = Piece("BLACK", "Rook", 1, PiecePoint(self._all_pieces_positions[80].pos_x,
                                                           self._all_pieces_positions[80].pos_y), "Res\\Rook-b.png")
        self._all_piece_list.append(rook_b_piece1)

        # Rook - Red
        rook_r_piece0 = Piece("RED", "Rook", 0, PiecePoint(self._all_pieces_positions[9].pos_x,
                                                         self._all_pieces_positions[9].pos_y), "Res\\Rook-r.png")
        self._all_piece_list.append(rook_r_piece0)

        rook_r_piece1 = Piece("RED", "Rook", 1, PiecePoint(self._all_pieces_positions[89].pos_x,
                                                         self._all_pieces_positions[89].pos_y), "Res\\Rook-r.png")
        self._all_piece_list.append(rook_r_piece1)

        # Knight - Black
        knight_b_piece0 = Piece("BLACK", "Knight", 0, PiecePoint(self._all_pieces_positions[10].pos_x,
                                                               self._all_pieces_positions[10].pos_y),
                              "Res\\Knight-b.png")
        self._all_piece_list.append(knight_b_piece0)

        knight_b_piece1 = Piece("BLACK", "Knight", 1, PiecePoint(self._all_pieces_positions[70].pos_x,
                                                               self._all_pieces_positions[70].pos_y),
                              "Res\\Knight-b.png")
        self._all_piece_list.append(knight_b_piece1)
        # Knight - Red
        knight_r_piece0 = Piece("RED", "Knight", 0, PiecePoint(self._all_pieces_positions[19].pos_x,
                                                             self._all_pieces_positions[19].pos_y), "Res\\Knight-r.png")
        self._all_piece_list.append(knight_r_piece0)

        knight_r_piece1 = Piece("RED", "Knight", 1, PiecePoint(self._all_pieces_positions[79].pos_x,
                                                             self._all_pieces_positions[79].pos_y), "Res\\Knight-r.png")
        self._all_piece_list.append(knight_r_piece1)

        # Ministor - Black
        minister_b_piece0 = Piece("BLACK", "Minister", 0, PiecePoint(self._all_pieces_positions[20].pos_x,
                                                                   self._all_pieces_positions[20].pos_y),
                                "Res\\Minister-b.png")
        self._all_piece_list.append(minister_b_piece0)

        minister_b_piece1 = Piece("BLACK", "Minister", 1, PiecePoint(self._all_pieces_positions[60].pos_x,
                                                                   self._all_pieces_positions[60].pos_y),
                                "Res\\Minister-b.png")
        self._all_piece_list.append(minister_b_piece1)
        # Ministor - Red
        minister_r_piece0 = Piece("RED", "Minister", 0, PiecePoint(self._all_pieces_positions[29].pos_x,
                                                                 self._all_pieces_positions[29].pos_y),
                                "Res\\Minister-r.png")
        self._all_piece_list.append(minister_r_piece0)

        minister_r_piece1 = Piece("RED", "Minister", 1, PiecePoint(self._all_pieces_positions[69].pos_x,
                                                                 self._all_pieces_positions[69].pos_y),
                                "Res\\Minister-r.png")
        self._all_piece_list.append(minister_r_piece1)

        # Soldier - Black
        soldier_b_piece0 = Piece("BLACK", "Soldier", 0, PiecePoint(self._all_pieces_positions[30].pos_x,
                                                                 self._all_pieces_positions[30].pos_y),
                               "Res\\Soldier-b.png")
        self._all_piece_list.append(soldier_b_piece0)

        soldier_b_piece1 = Piece("BLACK", "Soldier", 1, PiecePoint(self._all_pieces_positions[50].pos_x,
                                                                 self._all_pieces_positions[50].pos_y),
                               "Res\\Soldier-b.png")
        self._all_piece_list.append(soldier_b_piece1)
        # Soldier - Red
        soldier_r_piece0 = Piece("RED", "Soldier", 0, PiecePoint(self._all_pieces_positions[39].pos_x,
                                                               self._all_pieces_positions[39].pos_y),
                               "Res\\Soldier-r.png")
        self._all_piece_list.append(soldier_r_piece0)

        soldier_r_piece1 = Piece("RED", "Soldier", 1, PiecePoint(self._all_pieces_positions[59].pos_x,
                                                               self._all_pieces_positions[59].pos_y),
                               "Res\\Soldier-r.png")
        self._all_piece_list.append(soldier_r_piece1)

        # General - Black
        general_b_piece0 = Piece("BLACK", "General", 0, PiecePoint(self._all_pieces_positions[40].pos_x,
                                                                 self._all_pieces_positions[40].pos_y),
                               "Res\\General.png")
        self._all_piece_list.append(general_b_piece0)

        # Marshal - Red
        marshal_r_piece0 = Piece("RED", "Marshal", 0, PiecePoint(self._all_pieces_positions[49].pos_x,
                                                               self._all_pieces_positions[49].pos_y),
                               "Res\\Marshal.png")
        self._all_piece_list.append(marshal_r_piece0)
        self._rule.set_center_pos(PiecePoint(self._all_pieces_positions[49].pos_x,
                                             self._all_pieces_positions[49].pos_y))

        # Cannon - Black
        cannon_b_piece0 = Piece("BLACK", "Cannon", 0, PiecePoint(self._all_pieces_positions[12].pos_x,
                                                               self._all_pieces_positions[12].pos_y),
                              "Res\\Cannon-b.png")
        self._all_piece_list.append(cannon_b_piece0)

        cannon_b_piece1 = Piece("BLACK", "Cannon", 1, PiecePoint(self._all_pieces_positions[72].pos_x,
                                                               self._all_pieces_positions[72].pos_y),
                              "Res\\Cannon-b.png")
        self._all_piece_list.append(cannon_b_piece1)
        # Cannon - Red
        cannon_r_piece0 = Piece("RED", "Cannon", 0, PiecePoint(self._all_pieces_positions[17].pos_x,
                                                             self._all_pieces_positions[17].pos_y), "Res\\Cannon-r.png")
        self._all_piece_list.append(cannon_r_piece0)

        cannon_r_piece1 = Piece("RED", "Cannon", 1, PiecePoint(self._all_pieces_positions[77].pos_x,
                                                             self._all_pieces_positions[77].pos_y), "Res\\Cannon-r.png")
        self._all_piece_list.append(cannon_r_piece1)

        # Guard - Black
        guard_b_piece0 = Piece("BLACK", "Guard", 0, PiecePoint(self._all_pieces_positions[3].pos_x,
                                                             self._all_pieces_positions[3].pos_y), "Res\\Guard-b.png")
        self._all_piece_list.append(guard_b_piece0)

        guard_b_piece1 = Piece("BLACK", "Guard", 1, PiecePoint(self._all_pieces_positions[23].pos_x,
                                                             self._all_pieces_positions[23].pos_y), "Res\\Guard-b.png")
        self._all_piece_list.append(guard_b_piece1)

        guard_b_piece2 = Piece("BLACK", "Guard", 2, PiecePoint(self._all_pieces_positions[43].pos_x,
                                                             self._all_pieces_positions[43].pos_y), "Res\\Guard-b.png")
        self._all_piece_list.append(guard_b_piece2)

        guard_b_piece3 = Piece("BLACK", "Guard", 3, PiecePoint(self._all_pieces_positions[63].pos_x,
                                                             self._all_pieces_positions[63].pos_y), "Res\\Guard-b.png")
        self._all_piece_list.append(guard_b_piece3)

        guard_b_piece4 = Piece("BLACK", "Guard", 4, PiecePoint(self._all_pieces_positions[83].pos_x,
                                                             self._all_pieces_positions[83].pos_y), "Res\\Guard-b.png")
        self._all_piece_list.append(guard_b_piece4)

        # Guard - Red
        guard_r_piece0 = Piece("RED", "Guard", 0, PiecePoint(self._all_pieces_positions[6].pos_x,
                                                           self._all_pieces_positions[6].pos_y), "Res\\Guard-r.png")
        self._all_piece_list.append(guard_r_piece0)

        guard_r_piece1 = Piece("RED", "Guard", 1, PiecePoint(self._all_pieces_positions[26].pos_x,
                                                           self._all_pieces_positions[26].pos_y), "Res\\Guard-r.png")
        self._all_piece_list.append(guard_r_piece1)

        guard_r_piece2 = Piece("RED", "Guard", 2, PiecePoint(self._all_pieces_positions[46].pos_x,
                                                           self._all_pieces_positions[46].pos_y), "Res\\Guard-r.png")
        self._all_piece_list.append(guard_r_piece2)

        guard_r_piece3 = Piece("RED", "Guard", 3, PiecePoint(self._all_pieces_positions[66].pos_x,
                                                           self._all_pieces_positions[66].pos_y), "Res\\Guard-r.png")
        self._all_piece_list.append(guard_r_piece3)

        guard_r_piece4 = Piece("RED", "Guard", 4, PiecePoint(self._all_pieces_positions[86].pos_x,
                                                           self._all_pieces_positions[86].pos_y), "Res\\Guard-r.png")
        self._all_piece_list.append(guard_r_piece4)

        #   cannonBPiece0.refine()

        self._board_model.set_pieces(self._all_piece_list)

        self._rule.start_match()

    def refine_image(self, radius_x, radius_y, piece_object):
        piece_object.image_in_canvas = Image.open(piece_object.image_path)
        # The (450, 350) is (height, width)
        piece_object.image_in_canvas = piece_object.image_in_canvas.resize((int(radius_x * 2), int(radius_y * 2)),
                                                                           Image.Resampling.LANCZOS)
        piece_object.resized_image_in_canvas = ImageTk.PhotoImage(piece_object.image_in_canvas)
        piece_object.image_id = self._board_canvas.create_image(piece_object.position.pos_x,
                                                                piece_object.position.pos_y,
                                                                image=piece_object.resized_image_in_canvas)

    def bling_one_piece(self):
        for p in self._all_piece_list:
            # bling
            if p.get_status() == 2:
                if p.ui_state == "Show":
                    self._board_canvas.itemconfig(p.image_id, state='hidden')
                    p.ui_state = "Hide"
                else:
                    self._board_canvas.itemconfig(p.image_id, state='normal')
                    p.ui_state = "Show"
            else:
                self._board_canvas.itemconfig(p.image_id, state='normal')
        self._master.after(400, self.bling_one_piece)

    def try_move_piece(self, original_piece, x_pos, y_pos, undo):
        new_pt = PiecePoint(x_pos, y_pos)
        original_pt = PiecePoint(original_piece.position.pos_x, original_piece.position.pos_y)
        if not undo:
            #  check if we could move to the position
            successful = self._rule.check_move(original_piece, new_pt)
            if not successful:
                return False
        self._board_canvas.itemconfig(original_piece.image_id, state='normal')
        original_piece.ui_state = "Show"

        self._board_canvas.move(original_piece.image_id, x_pos - original_pt.pos_x,
                                y_pos - original_pt.pos_y)
        original_piece.move(x_pos, y_pos)
        original_piece.deselect()
        original_piece.set_status(0)
        if not undo:
            #  add one action to action list
            self._action_mgr.execute_action("Move", original_piece, original_pt, new_pt)
        else:
            self._rule.switch_player()
        return True

    def try_knock_over_piece(self, p1, p2):
        # check if we could move to the position
        successful = self._rule.check_knock_over(p1, p2)
        if not successful:
            return False
        self._board_canvas.move(p1.image_id, p2.position.pos_x - p1.position.pos_x,
                                p2.position.pos_y - p1.position.pos_y)
        p1.set_position(p2.position)
        # dead status
        p2.set_status(1)
        p2.set_position(PiecePoint(0, 0))
        self._board_canvas.itemconfig(p2.image_id, state='hidden')
        self._board_canvas.move(p2.image_id, -1 * CANVAS_WIDTH, - 1 * CANVAS_HEIGHT)
        #  add one action to action list
        self._action_mgr.execute_action("Eat", p1, p2)
        return True

    def handle_current_piece(self, x, y):
        original_piece = None
        target_piece = None
        x_pos = 0
        y_pos = 0
        for p in self._all_piece_list:
            if p.is_selected():
                original_piece = p
                break

        for targetPos in self._all_pieces_positions:
            x_pos = targetPos.pos_x
            y_pos = targetPos.pos_y
            target_greater_x = x_pos + self._radius > x
            target_less_x = x_pos - self._radius < x
            search_pos_x = target_greater_x and target_less_x
            target_greater_y = y_pos + self._radius > y
            target_less_y = y_pos - self._radius < y
            search_pos_y = target_greater_y and target_less_y
            if search_pos_x and search_pos_y:
                for p in self._all_piece_list:
                    if p.position.pos_x == x_pos and p.position.pos_y == y_pos:
                        target_piece = p
                        break
                break

        if original_piece is not None:
            res = False
            if target_piece is None:
                res = self.try_move_piece(original_piece, x_pos, y_pos, False)
                
            else:
                res = self.try_knock_over_piece(original_piece, target_piece)
                #play sound
                #playsound("D:\\Python\\Projects\\Chess\\Res\\eat.WAV")
                #why the play sound is not working??? the driver is not recognized, and searching the answer
                
            if res:
                self._rule.switch_player()

        for p in self._all_piece_list:
            p.deselect()

    def click_on_canvas(self, event):
        click_in_piece = False
        x = event.x
        y = event.y
        pre_selected_piece = None
        #  find according piece
        for p in self._all_piece_list:
            if p.get_status() == 2:  # bling
                p.set_status(0)
                pre_selected_piece = p
        #  bling the piece
        for p in self._all_piece_list:
            player_now = self._rule.get_current_player()
            if p.get_type() != player_now:
                continue
            x_in_range_a = p.position.pos_x + self._radius > x
            x_in_range_b = p.position.pos_x - self._radius < x
            y_in_range_a = p.position.pos_y + self._radius > y
            y_in_range_b = p.position.pos_y - self._radius < y
            x_in_range = x_in_range_a and x_in_range_b
            y_in_range = y_in_range_a and y_in_range_b
            if x_in_range and y_in_range:
                if p.is_selected():
                    p.deselect()                    

                else:
                    p.select()
                    p.set_status(2)  # bling it
                    if pre_selected_piece is not None:
                        pre_selected_piece.deselect()

                click_in_piece = True

        #  move the piece
        if not click_in_piece:
            self.handle_current_piece(x, y)

    def set_action_manager(self, action_manager):
        self._action_mgr = action_manager

