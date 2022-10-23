from piece_point import *
from piece import *


class RuleMgr:
    _center_pos = PiecePoint(0, 0)
    _current_player = ""
    _length_of_one_grid = 0
    _piece_list = None

    def __init__(self):
        _currentPlayer = "RED"
        _lengthOfOneGrid = 0
        _pieceList = []

    def set_length_of_one_grid(self, length):
        self._length_of_one_grid = length

    def get_length_of_one_grid(self):
        return self._length_of_one_grid
    
    def get_possible_pos(self, type_name, index):
        pass

    def set_pieces_list(self, piece_list):
        self._piece_list = piece_list

    def get_center_pos(self):
        return self._center_pos

    def set_center_pos(self, pt):
        self._center_pos = pt

    def start_match(self):
        self._current_player = "RED"

    def switch_player(self):
        if self._current_player == "RED":
            self._current_player = "BLACK"
        else:
            self._current_player = "RED"

    def get_current_player(self):
        return self._current_player

    def rook_move_rule(self, current_piece, new_pos):
        ret_val = False
        if current_piece.position.pos_x == new_pos.pos_x:
            find_count= 0
            for pc in self._piece_list:
                less_than_current_pos = pc.position.pos_y < current_piece.position.pos_y
                greater_than_new_pos = pc.position.pos_y > new_pos.pos_y
                exist_up = less_than_current_pos and greater_than_new_pos
                greater_than_current_pos = pc.position.pos_y > current_piece.position.pos_y
                less_than_new_pos = pc.position.pos_y < new_pos.pos_y
                exist_down = greater_than_current_pos and less_than_new_pos
                if (pc.position.pos_x == new_pos.pos_x) and (exist_up or exist_down):
                    find_count = find_count + 1
                    break
            if find_count == 1:
                ret_val = False
            else:
                ret_val = True

        elif current_piece.position.pos_y == new_pos.pos_y:
            find_count = 0
            for pc in self._piece_list:
                less_than_current_pos = pc.position.pos_x < current_piece.position.pos_x
                greater_than_new_pos = pc.position.pos_x > new_pos.pos_x
                exist_left = less_than_current_pos and greater_than_new_pos
                greater_than_current_pos = pc.position.pos_x > current_piece.position.pos_x
                less_than_new_pos = pc.position.pos_x < new_pos.pos_x
                exist_right = greater_than_current_pos and less_than_new_pos
                if pc.position.pos_y == new_pos.pos_y and (exist_left or exist_right):
                    find_count = find_count + 1
                    break
            if find_count == 1:
                ret_val = False
            else:
                ret_val = True

        return ret_val

    def knight_move_rule(self, current_piece, new_pos):
        ret_val = False
        #  one grid in x axis, two grid in y axis
        if current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x \
                        and pc.position.pos_y == current_piece.position.pos_y - self._length_of_one_grid:
                    ret_val = False
                    break

        elif current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x \
                        and pc.position.pos_y == current_piece.position.pos_y - self._length_of_one_grid:
                    ret_val = False
                    break
        elif current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_y == current_piece.position.pos_y \
                        and pc.position.pos_x == current_piece.position.pos_x + self._length_of_one_grid:
                    ret_val = False
                    break
        elif current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_y == current_piece.position.pos_y \
                        and pc.position.pos_x == current_piece.position.pos_x + self._length_of_one_grid:
                    ret_val = False
                    break

        elif current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x \
                        and pc.position.pos_y == current_piece.position.pos_y + self._length_of_one_grid:
                    ret_val = False
                    break

        elif current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x \
                        and pc.position.pos_y == current_piece.position.pos_y + self._length_of_one_grid:
                    ret_val = False
                    break

        elif current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_y == current_piece.position.pos_y \
                        and pc.position.pos_x == current_piece.position.pos_x - self._length_of_one_grid:
                    ret_val = False
                    break

        elif current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_y == current_piece.position.pos_y \
                        and pc.position.pos_x == current_piece.position.pos_x - self._length_of_one_grid:
                    ret_val = False
                    break

        return ret_val

    def minister_move_rule(self, current_piece, new_pos):
        ret_val = False
        original_pos = current_piece.get_original_position()
        if (new_pos.pos_y < original_pos.pos_y - self._length_of_one_grid * 4) \
                or (new_pos.pos_y > original_pos.pos_y + self._length_of_one_grid * 4):
            return ret_val
        if current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x - self._length_of_one_grid \
                        and pc.position.pos_y == current_piece.position.pos_y - self._length_of_one_grid:
                    ret_val = False
                    break
        elif current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x + self._length_of_one_grid \
                        and pc.position.pos_y == current_piece.position.pos_y - self._length_of_one_grid:
                    ret_val = False
                    break
        elif current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x + self._length_of_one_grid \
                        and pc.position.pos_y == current_piece.position.pos_y + self._length_of_one_grid:
                    ret_val = False
                    break

        elif current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid * 2 \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid * 2:
            ret_val = True
            for pc in self._piece_list:
                if pc.position.pos_x == current_piece.position.pos_x - self._length_of_one_grid \
                        and pc.position.pos_y == current_piece.position.pos_y + self._length_of_one_grid:
                    ret_val = False
                    break

        return ret_val

    def soldier_move_rule(self, current_piece, new_pos):
        ret_val = False
        ori_pos_x = self._center_pos.pos_x
        ori_pos_y = current_piece.get_original_position().pos_y
        if (new_pos.pos_x < ori_pos_x - self._length_of_one_grid) or (
                new_pos.pos_x > ori_pos_x + self._length_of_one_grid) or (
                new_pos.pos_y < ori_pos_y - self._length_of_one_grid * 2) or (
                new_pos.pos_y > ori_pos_y + self._length_of_one_grid * 2):
            return ret_val
        if current_piece.position.pos_x + self._length_of_one_grid == new_pos.pos_x \
                and current_piece.position.pos_y - self._length_of_one_grid == new_pos.pos_y:
            ret_val = True
        elif current_piece.position.pos_x - self._length_of_one_grid == new_pos.pos_x \
                and current_piece.position.pos_y - self._length_of_one_grid == new_pos.pos_y:
            ret_val = True
        elif current_piece.position.pos_y + self._length_of_one_grid == new_pos.pos_y \
                and current_piece.position.pos_x - self._length_of_one_grid == new_pos.pos_x:
            ret_val = True
        elif current_piece.position.pos_y + self._length_of_one_grid == new_pos.pos_y \
                and current_piece.position.pos_x + self._length_of_one_grid == new_pos.pos_x:
            ret_val = True

        return ret_val

    def marshal_move_rule(self, current_piece, new_pos):
        ret_val = False
        ori_pos = current_piece.get_original_position()
        if (new_pos.pos_x < ori_pos.pos_x - self._length_of_one_grid) \
                or (new_pos.pos_x > ori_pos.pos_x + self._length_of_one_grid) \
                or (new_pos.pos_y < ori_pos.pos_y - self._length_of_one_grid * 2) \
                or (new_pos.pos_y > ori_pos.pos_y + self._length_of_one_grid * 2):
            return ret_val
        if current_piece.position.pos_x == new_pos.pos_x \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid:
            ret_val = True
        elif current_piece.position.pos_x == new_pos.pos_x \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid:
            ret_val = True
        elif current_piece.position.pos_y == new_pos.pos_y \
                and current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid:
            ret_val = True
        elif current_piece.position.pos_y == new_pos.pos_y \
                and current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid:
            ret_val = True

        return ret_val

    def guard_move_rule(self, current_piece, new_pos):
        ret_val = False
        type_of_current_piece = current_piece.get_type()
        move_steps = current_piece.get_move_steps()
        if type_of_current_piece == "RED":
            if current_piece.position.pos_x == new_pos.pos_x \
                    and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid:
                ret_val = True
            # cross the river
            if move_steps > 1:
                if current_piece.position.pos_y == new_pos.pos_y and (
                        current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid
                        or current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid):
                    ret_val = True
        elif type_of_current_piece == "BLACK":
            if current_piece.position.pos_x == new_pos.pos_x \
                    and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid:
                ret_val = True
            # cross the river
            if move_steps > 1:
                if current_piece.position.pos_y == new_pos.pos_y and (
                        current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid
                        or current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid):
                    ret_val = True

        return ret_val

    def cannon_move_rule(self, current_piece, new_pos):
        ret_val = False
        if current_piece.position.pos_x == new_pos.pos_x:
            piece_count = 0
            for pc in self._piece_list:
                if pc.position.pos_x == new_pos.pos_x and (
                        (pc.position.pos_y < current_piece.position.pos_y and pc.position.pos_y > new_pos.pos_y) or (
                        pc.position.pos_y > current_piece.position.pos_y and pc.position.pos_y < new_pos.pos_y)):
                    piece_count = piece_count + 1
                    break
            if piece_count == 1:
                ret_val = False
            else:
                ret_val = True

        elif current_piece.position.pos_y == new_pos.pos_y:
            piece_count = 0
            for pc in self._piece_list:
                less_than_piece_a = pc.position.pos_x < current_piece.position.pos_x
                greater_than_piece_b = pc.position.pos_x > new_pos.pos_x
                greater_than_piece_a = pc.position.pos_x > current_piece.position.pos_x
                less_than_piece_b = pc.position.pos_x < new_pos.pos_x
                if pc.position.pos_y == new_pos.pos_y and (
                        (less_than_piece_a and greater_than_piece_b) or (
                        greater_than_piece_a and less_than_piece_b)):
                    piece_count = piece_count + 1
                    break
            if piece_count == 1:
                ret_val = False
            else:
                ret_val = True

        return ret_val

    def general_move_rule(self, current_piece, new_pos):
        ret_val = False
        ori_pos = current_piece.get_original_position()
        if (new_pos.pos_x < ori_pos.pos_x - self._length_of_one_grid) or (
                new_pos.pos_x > ori_pos.pos_x + self._length_of_one_grid) or (
                new_pos.pos_y < ori_pos.pos_y - self._length_of_one_grid * 2) or (
                new_pos.pos_y > ori_pos.pos_y + self._length_of_one_grid * 2):
            return ret_val
        if current_piece.position.pos_x == new_pos.pos_x \
                and current_piece.position.pos_y == new_pos.pos_y - self._length_of_one_grid:
            ret_val = True
        elif current_piece.position.pos_x == new_pos.pos_x \
                and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid:
            ret_val = True
        elif current_piece.position.pos_y == new_pos.pos_y \
                and current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid:
            ret_val = True
        elif current_piece.position.pos_y == new_pos.pos_y \
                and current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid:
            ret_val = True

        return ret_val

    _switcher = {
            "Rook": rook_move_rule,
            "Knight": knight_move_rule,
            "Minister": minister_move_rule,
            "Soldier": soldier_move_rule,
            "Marshal": marshal_move_rule,
            "Guard": guard_move_rule,
            "Cannon": cannon_move_rule,
            "General": general_move_rule
        }

    def check_move(self, current_piece, new_pos):
        # get current piece type
        piece_name = current_piece.get_name()
        rule_function = self._switcher.get(piece_name)
        ret_val = False
        if rule_function:
            ret_val = rule_function(self, current_piece, new_pos)

        return ret_val

    def rook_knock_over_rule(self, piece1, piece2):
        return self.rook_move_rule(piece1, piece2.position)

    def knight_knock_over_rule(self, piece1, piece2):
        return self.knight_move_rule(piece1, piece2.position)

    def minister_knock_over_rule(self, piece1, piece2):
        return self.minister_move_rule(piece1, piece2.position)

    def soldier_knock_over_rule(self, piece1, piece2):
        return self.soldier_move_rule(piece1, piece2.position)

    def marshal_knock_over_rule(self, piece1, piece2):
        return self.marshal_move_rule(piece1, piece2.position)

    def guard_knock_over_rule(self, piece1, piece2):
        return self.guard_move_rule(piece1, piece2.position)

    def cannon_knock_over_rule(self, piece1, piece2):
        ret_val = False
        if piece1.position.pos_x == piece2.position.pos_x:
            found_piece_count = 0
            for pc in self._piece_list:
                less_than_piece_a = pc.position.pos_y < piece1.position.pos_y
                greater_than_piece_b = pc.position.pos_y > piece2.position.pos_y
                exist_up = less_than_piece_a and greater_than_piece_b
                greater_than_piece_a = pc.position.pos_y > piece1.position.pos_y
                less_than_piece_b = pc.position.pos_y < piece2.position.pos_y
                exist_down = greater_than_piece_a and less_than_piece_b
                if pc.position.pos_x == piece2.position.pos_x and (exist_up or exist_down):
                    found_piece_count = found_piece_count + 1
                    continue
            if found_piece_count == 1:
                ret_val = True

        elif piece1.position.pos_y == piece2.position.pos_y:
            found_piece_count = 0
            for pc in self._piece_list:
                if pc.position.pos_y == piece2.position.pos_y and ((pc.position.pos_x < piece1.position.pos_x and pc.position.pos_x > piece2.position.pos_x) or (pc.position.pos_x > piece1.position.pos_x and pc.position.pos_x < piece2.position.pos_x)):
                    found_piece_count = found_piece_count + 1
                    continue
            if found_piece_count == 1:
                ret_val = True

        return ret_val

    def general_knock_over_rule(self, piece1, piece2):
        return self.general_move_rule(piece1, piece2.position)

    _switcherEat = {
        "Rook": rook_knock_over_rule,
        "Knight": knight_knock_over_rule,
        "Minister": minister_knock_over_rule,
        "Soldier": soldier_knock_over_rule,
        "Marshal": marshal_knock_over_rule,
        "Guard": guard_knock_over_rule,
        "Cannon": cannon_knock_over_rule,
        "General": general_knock_over_rule
    }

    def check_knock_over(self, p1, p2):
        # get current piece type
        piece_name = p1.get_name()
        rule_function = self._switcherEat.get(piece_name)
        ret_val = False
        if rule_function:
            ret_val = rule_function(self, p1, p2)

        return ret_val
