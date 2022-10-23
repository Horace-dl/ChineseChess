
from piece_point import *
# Importing ImageDraw for
# using floodfill function
from PIL import Image, ImageDraw


class Piece:
    _type = ""  # ""RED", "BLACK"
    position = PiecePoint(0, 0)
    image_path = ""
    image_in_canvas = object
    resized_image_in_canvas = object
    ui_state = ""
    image_id = 0
    _name = ""
    _id = 0
    _status = 0  # 0: live, 1: dead, 2:bling, 3: moving
    _is_selected = False
    _move_steps = 0
    _original_position = PiecePoint(0, 0)

    def __init__(self, type_name, name, id_val, pt, image):
        self._type = type_name
        self._name = name
        self._id = id_val
        self.position = pt
        self.image_path = image
        self.ui_state = "Show"
        self._status = 0
        self._original_position = PiecePoint(pt.pos_x, pt.pos_y)

    def set_position(self, pt):
        self.position = pt

    def set_image(self, file_name):
        self.image_path = file_name

    def set_status(self, status):
        self._status = status

    def get_status(self):
        return self._status

    def get_name(self):
        return self._name

    def get_move_steps(self):
        return self._move_steps

    def get_original_position(self):
        return self._original_position

    def select(self):
        self._is_selected = True

    def deselect(self):
        self._is_selected = False

    def is_selected(self):
        return self._is_selected

    # This is an old function to do image refine work.
    def refine(self):

        # Opening the image and
        # converting its type to RGBA
        img = Image.open(self.image_path).convert('RGBA')

        # Location of seed
        seed = (0, 0)

        # Pixel Value which would
        # be used for replacement
        rep_value = (0, 0, 0, 0)

        # Calling the floodfill() function and
        # passing it image, seed, value and
        # thresh as arguments
        ImageDraw.floodfill(img, seed, rep_value, thresh=100)

        img.save(self.image_path + "-0.png")
        #  self.canvas.create_image(60, 60, image=img)

    def get_type(self):
        return self._type

    def move(self, x, y):
        self.position.pos_x = x
        self.position.pos_y = y
        self._move_steps = self._move_steps + 1
        pass


