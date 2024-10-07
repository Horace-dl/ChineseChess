from action import *
from canvasboard import *


class ActionManager:
    _action_list = None
    _canvas_object = None

    def __init__(self):
        self._action_list = []

    def set_canvas_object(self, canvas_para):
        self._canvas_object = canvas_para

    def __add_action(self, action):
        self._action_list.append(action)

    def __remove_action(self, action):
        self._action_list.remove(action)

    def clear_actions(self):
        self._action_list.clear()

    def execute_action(self, action_name, *para):
        act = Action(action_name)
        if action_name == "Move":
            act.set_piece_a(para[0])
            act.set_original_pos(para[1])
            act.set_new_pos(para[2])
        elif action_name == "Eat":
            act.set_piece_a(para[0])
            act.set_piece_b(para[1])
        else:
            raise Exception("ActionManager - execute - Not supported action")
        self.__add_action(act)

    def undo_action(self):
        act = self._action_list[-1]
        act_name = act.get_action_name()
        if act_name == "Move":
            current_piece = act.get_piece_a()
            target_pos = act.get_original_pos()
            self._canvas_object.try_move_piece(current_piece, target_pos.get_x_pos(), target_pos.get_y_pos(), True)
        elif act_name == "Eat":
            piece_first = act.get_piece_a()
            piece_second = act.get_piece_b()
            pos_original = act.get_original_pos()
            pos_new = act.get_new_pos()
            self._canvas_object.try_move_piece(piece_first, pos_original.get_x_pos(), pos_original.get_y_pos(), True)
            self._canvas_object.try_move_piece(piece_second, pos_new.get_x_pos(), pos_new.get_y_pos(), True)
        else:
            raise Exception("ActionManager - undo - Not supported action")
        self._action_list.pop()


