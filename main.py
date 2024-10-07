from tkinter import *
from canvasboard import *
from action_mgr import *


def init_menu(master):
    #  init menu
    global menu_main
    menu_main = Menu(master)
    master.config(menu=menu_main)
    match_menu = Menu(menu_main)
    match_menu.add_command(label="Restart", command=restart_command)
    match_menu.add_command(label="Rollback", command=rollback_command)
    menu_main.add_cascade(label="Match", menu=match_menu)

    view_menu = Menu(menu_main)
    view_menu.add_command(label="Switch Side", command=switch_side_command)
    menu_main.add_cascade(label="View", menu=view_menu)
    return menu_main


def switch_side_command():
    global canvas_main
    canvas_main.switch_side()


def restart_command():
    global canvas_main
    canvas_main.reset_canvas_data()
    global action_manager
    action_manager.clear_actions()


def rollback_command():
    action_manager.undo_action()


def init_canvas(master):
    global canvas_main
    canvas_main = CanvasBoard(master)
    canvas_main.init_canvas()

    return canvas_main
    # act_mgr.set_canvas_object(canvas_main)


def main() -> int:
    #  init tkinter object
    master = Tk()
    master.resizable(False, False)  # disable max
    menu_main = init_menu(master)
    canvas_main = init_canvas(master)
    global action_manager
    action_manager = ActionManager()
    canvas_main.set_action_manager(action_manager)
    action_manager.set_canvas_object(canvas_main)

    mainloop()

    return 0


if __name__ == '__main__':
    main()
