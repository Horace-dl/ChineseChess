from tkinter import *
from canvasboard import *

def init_menu(master):
    #  init menu
    menu_main = Menu(master)
    master.config(menu=menu_main)
    match_menu = Menu(menu_main)
    match_menu.add_command(label="Restart")
    match_menu.add_command(label="Revert 1 step")
    menu_main.add_cascade(label="Match", menu=match_menu)

    view_menu = Menu(menu_main)
    view_menu.add_command(label="Switch Side")
    menu_main.add_cascade(label="View", menu=view_menu)


def init_canvas(master):
    canvas_main = CanvasBoard(master)
    canvas_main.init_canvas()


def main() -> int:
    #  init tkinter object
    master = Tk()
    master.resizable(False, False)  # disable max
    init_menu(master)
    init_canvas(master)

    mainloop()

    return 0


if __name__ == '__main__':
    main()