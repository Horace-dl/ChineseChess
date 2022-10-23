class PiecePoint:
    pos_x = 0
    pos_y = 0

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def set_x_pos(self, x):
        self.pos_x = x

    def set_y_pos(self, y):
        self.pos_y = y

    def get_x_pos(self):
        return self.pos_x

    def get_y_pos(self):
        return self.pos_y

    def __add__(self, o):
        
        self.pos_x = self.pos_x + o.pos_x
        self.pos_y = self.pos_y + o.pos_y
        return self

