from piece_point import *
from piece import *


class RuleMgr:
    _center_pos = PiecePoint(0, 0)
    _current_player = ""
    _length_of_one_grid = 0
    _piece_list = None
    _direction = 0

    def __init__(self):
        _currentPlayer = "RED"
        _length_of_one_grid = 0
        _pieceList = []
        _direction = 0
        _center_pos = PiecePoint(0, 0)

    def set_length_of_one_grid(self, length):
        self._length_of_one_grid = length

    def get_length_of_one_grid(self):
        return self._length_of_one_grid
    
    def get_possible_pos(self, type_name, index):
        # return a list of PiecePoint that the piece (type_name, index) can move to
        possible = []
        if self._piece_list is None:
            return possible

        # find the piece object by type and id
        current_piece = None
        for pc in self._piece_list:
            try:
                pc_id = pc._id
            except Exception:
                pc_id = None
            if pc.get_type() == type_name and pc_id == index:
                current_piece = pc
                break

        if current_piece is None:
            return possible

        # board grid: 9 columns (i=0..8), 10 rows (j=0..9)
        for i in range(9):
            for j in range(10):
                new_x = self._length_of_one_grid * (1 + i)
                new_y = self._length_of_one_grid * (1 + j)
                new_pos = PiecePoint(new_x, new_y)

                # check if a same-color piece occupies the target
                occupied_same = False
                occupied_piece = None
                for pc in self._piece_list:
                    if pc.position.pos_x == new_x and pc.position.pos_y == new_y and pc.get_status() == 0:
                        occupied_piece = pc
                        if pc.get_type() == current_piece.get_type():
                            occupied_same = True
                        break

                if occupied_same:
                    continue

                # if occupied by opponent, use knock_over rule
                if occupied_piece is not None and occupied_piece.get_type() != current_piece.get_type():
                    can_eat, _ = self.check_knock_over(current_piece, occupied_piece)
                    if can_eat:
                        possible.append(new_pos)
                    continue

                # empty square: check normal move
                if self.check_move(current_piece, new_pos):
                    possible.append(new_pos)

        return possible

    def set_pieces_list(self, piece_list):
        self._piece_list = piece_list

    def get_center_pos(self):
        return self._center_pos

    def set_center_pos(self, pt):
        self._center_pos = pt

    def get_direction(self):
        return self._direction

    def set_direction(self, value):
        self._direction = value

    def start_match(self):
        self._current_player = "RED"

    def reset_data(self):
        self._current_player = "RED"
        self._direction = 0

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
        ori_x_pos = original_pos.pos_x
        ori_y_pos = original_pos.pos_y
        if self._direction == 1:
            ori_x_pos = self._length_of_one_grid * 9 - ori_x_pos
            ori_y_pos = self._length_of_one_grid * 11 - ori_y_pos

        if (new_pos.pos_y < ori_y_pos - self._length_of_one_grid * 4) \
                or (new_pos.pos_y > ori_y_pos + self._length_of_one_grid * 4):
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
        if self._direction == 1:
            ori_pos_y = self._length_of_one_grid * 11 - ori_pos_y
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
        ori_pos_x = ori_pos.pos_x
        ori_pos_y = ori_pos.pos_y
        if self._direction == 1:
            ori_pos_x = self._length_of_one_grid * 10 - ori_pos_x
            ori_pos_y = self._length_of_one_grid * 11 - ori_pos_y

        if (new_pos.pos_x < ori_pos_x - self._length_of_one_grid) \
                or (new_pos.pos_x > ori_pos_x + self._length_of_one_grid) \
                or (new_pos.pos_y < ori_pos_y - self._length_of_one_grid * 2) \
                or (new_pos.pos_y > ori_pos_y + self._length_of_one_grid * 2):
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
        if (type_of_current_piece == "RED" and self._direction == 0) or \
                (type_of_current_piece == "BLACK" and self._direction == 1):
            if current_piece.position.pos_x == new_pos.pos_x \
                    and current_piece.position.pos_y == new_pos.pos_y + self._length_of_one_grid:
                ret_val = True
            # cross the river
            if move_steps > 1:
                if current_piece.position.pos_y == new_pos.pos_y and (
                        current_piece.position.pos_x == new_pos.pos_x - self._length_of_one_grid
                        or current_piece.position.pos_x == new_pos.pos_x + self._length_of_one_grid):
                    ret_val = True
        elif (type_of_current_piece == "BLACK" and self._direction == 0) or \
                (type_of_current_piece == "RED" and self._direction == 1):
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
                        (current_piece.position.pos_y > pc.position.pos_y > new_pos.pos_y) or (
                        current_piece.position.pos_y < pc.position.pos_y < new_pos.pos_y)):
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
        ori_pos_x = ori_pos.pos_x
        ori_pos_y = ori_pos.pos_y
        if self._direction == 1:
            ori_pos_x = self._length_of_one_grid * 10 - ori_pos_x
            ori_pos_y = self._length_of_one_grid * 11 - ori_pos_y
        if (new_pos.pos_x < ori_pos_x - self._length_of_one_grid) or (
                new_pos.pos_x > ori_pos_x + self._length_of_one_grid) or (
                new_pos.pos_y < ori_pos_y - self._length_of_one_grid * 2) or (
                new_pos.pos_y > ori_pos_y + self._length_of_one_grid * 2):
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

        # If the basic movement rule passes, ensure the move does not leave own general in check
        if ret_val:
            try:
                if self._move_leaves_king_in_check(current_piece, new_pos):
                    return False
            except Exception:
                # on any error do not allow the move for safety
                return False

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
                if pc.position.pos_y == piece2.position.pos_y \
                        and ((piece1.position.pos_x > pc.position.pos_x > piece2.position.pos_x)
                             or (piece1.position.pos_x < pc.position.pos_x < piece2.position.pos_x)):
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
        ret_msg = ""
        if rule_function:
            ret_val = rule_function(self, p1, p2)
            if p2.get_name() == "General" or p2.get_name() == "Marshal":
                ret_msg = "Game over"

        # ensure capture does not leave own king in check (illegal)
        if ret_val:
            try:
                if self._capture_leaves_king_in_check(p1, p2):
                    return False, ""
            except Exception:
                return False, ""

        return ret_val, ret_msg

    # --- Helpers for check/validation and game-over detection ---
    def _get_king_name(self, player_type):
        return 'Marshal' if player_type == 'RED' else 'General'

    def _find_king(self, player_type):
        king_name = self._get_king_name(player_type)
        for pc in self._piece_list:
            if pc.get_type() == player_type and pc.get_name() == king_name and pc.get_status() == 0:
                return pc
        return None

    def _no_pieces_between(self, pos_a, pos_b):
        # Only meaningful for same column (x). Check if any alive piece between y coords
        if pos_a.pos_x != pos_b.pos_x:
            return False
        low = min(pos_a.pos_y, pos_b.pos_y)
        high = max(pos_a.pos_y, pos_b.pos_y)
        for pc in self._piece_list:
            if pc.get_status() != 0:
                continue
            if pc.position.pos_x == pos_a.pos_x and low < pc.position.pos_y < high:
                return False
        return True

    def _is_attacked(self, piece):
        # check if any opponent piece can legally capture `piece`
        if piece is None:
            return False
        opponent = 'RED' if piece.get_type() == 'BLACK' else 'BLACK'
        # face-to-face general rule: opponent's king sees this king with no pieces between
        opp_king = self._find_king(opponent)
        if opp_king is not None:
            if opp_king.position.pos_x == piece.position.pos_x and self._no_pieces_between(opp_king.position, piece.position):
                return True

        for pc in self._piece_list:
            if pc.get_status() != 0:
                continue
            if pc.get_type() != opponent:
                continue
            ok, _ = self.check_knock_over(pc, piece)
            if ok:
                return True
        return False

    def _move_leaves_king_in_check(self, piece, dest_pos):
        # simulate moving `piece` to dest_pos (without capture) and check if own king is attacked
        orig_pos = PiecePoint(piece.position.pos_x, piece.position.pos_y)
        piece.set_position(dest_pos)
        injured = self._is_attacked(self._find_king(piece.get_type()))
        piece.set_position(orig_pos)
        return injured

    def _capture_leaves_king_in_check(self, piece, target):
        # simulate capture: remove target temporarily, move piece to target.position
        orig_pos_piece = PiecePoint(piece.position.pos_x, piece.position.pos_y)
        orig_status_target = target.get_status()
        orig_pos_target = PiecePoint(target.position.pos_x, target.position.pos_y)

        # perform simulated capture
        target.set_status(1)
        target.set_position(PiecePoint(0, 0))
        piece.set_position(orig_pos_target)

        injured = self._is_attacked(self._find_king(piece.get_type()))

        # restore
        piece.set_position(orig_pos_piece)
        target.set_status(orig_status_target)
        target.set_position(orig_pos_target)

        return injured

    def is_in_check(self, player_type):
        king = self._find_king(player_type)
        return self._is_attacked(king)

    def has_no_legal_moves(self, player_type):
        # if any piece of player has any legal move (including captures) then False
        for pc in self._piece_list:
            if pc.get_status() != 0 or pc.get_type() != player_type:
                continue
            try:
                pid = getattr(pc, '_id', None)
                poss = self.get_possible_pos(pc.get_type(), pid)
                if poss:
                    return False
            except Exception:
                continue
        return True

    def is_game_over(self):
        # game over if any king (General/Marshal) is captured
        for pc in self._piece_list:
            if pc.get_name() == 'Marshal' and pc.get_status() == 1:
                return True, 'BLACK'
            if pc.get_name() == 'General' and pc.get_status() == 1:
                return True, 'RED'

        # checkmate: side to move has no legal moves and is in check
        opponent = 'BLACK' if self._current_player == 'RED' else 'RED'
        if self.is_in_check(opponent) and self.has_no_legal_moves(opponent):
            winner = self._current_player
            return True, winner

        return False, None
