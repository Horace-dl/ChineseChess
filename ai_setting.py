import tkinter as tk

# Simple AI configuration module
# Module-level settings accessible by other modules
MACHINE_SIDE = None  # 'RED', 'BLACK', or None for no AI
DEPTH = 3


def open_settings_window(master=None):
	"""Open a small window to choose which side the machine plays and search depth."""
	win = tk.Toplevel(master) if master is not None else tk.Tk()
	win.title('AI Settings')
	win.resizable(False, False)

	side_var = tk.StringVar(value=MACHINE_SIDE if MACHINE_SIDE is not None else 'None')
	depth_var = tk.IntVar(value=DEPTH)

	tk.Label(win, text='Machine Side:').grid(row=0, column=0, sticky='w', padx=8, pady=4)
	tk.Radiobutton(win, text='None', variable=side_var, value='None').grid(row=0, column=1)
	tk.Radiobutton(win, text='RED', variable=side_var, value='RED').grid(row=0, column=2)
	tk.Radiobutton(win, text='BLACK', variable=side_var, value='BLACK').grid(row=0, column=3)

	tk.Label(win, text='Search Depth (ply):').grid(row=1, column=0, sticky='w', padx=8, pady=4)
	tk.Spinbox(win, from_=1, to=6, textvariable=depth_var, width=5).grid(row=1, column=1)


	def on_ok():
		global MACHINE_SIDE, DEPTH
		val = side_var.get()
		MACHINE_SIDE = None if val == 'None' else val
		DEPTH = int(depth_var.get())
		win.destroy()

	def on_cancel():
		win.destroy()

	tk.Button(win, text='OK', command=on_ok).grid(row=2, column=1, pady=8)
	tk.Button(win, text='Cancel', command=on_cancel).grid(row=2, column=2, pady=8)

	return win


def get_machine_side():
	return MACHINE_SIDE


def get_depth():
	return DEPTH