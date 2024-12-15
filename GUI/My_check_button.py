from tkinter import *


def get_frame_options(master_frame: LabelFrame, row_options_count: int, col_options_count: int,
                      option_names: list) -> list:
    cb_options = []
    key_pos, len_options_name = 0, len(option_names)
    for row in range(1, row_options_count + 1):
        for col in range(1, col_options_count + 1):
            if key_pos == len_options_name:
                return cb_options
            cb = MyCheckButton(master=master_frame, title=option_names[key_pos], row=row, col=col)
            cb_options.append(cb)
            key_pos += 1
    return cb_options


class MyCheckButton:
    """The Checkbutton class is made specifically for the operation of the program.

    Args:
        master (LabelFrame): The elements will be located in the LabelFrame.
        title (str): Text of Checkbutton.
        row (int): A row for the location in the LabelFrame according to the grid layout.
        col (int): A column for the location in the LabelFrame according to the grid layout.

    Attributes:
        var_select (BooleanVar): Element Activity.
        num_button (int): Sequence number.
    """
    num_button = 0

    def __init__(self, master: LabelFrame, title: str, row: int = -1, col: int = -1):
        self.var_select = BooleanVar()
        self.var_select.set(False)
        self.title = title
        MyCheckButton.num_button += 1
        self.num_button = MyCheckButton.num_button
        self.cb = Checkbutton(
            master=master, text=title, variable=self.var_select,
            onvalue=1, offvalue=0)
        if row == -1 and col == -1:
            self.cb.pack(side=LEFT)
        else:
            self.cb.grid(row=row, column=col, ipadx=2, ipady=2, padx=2, pady=2, sticky='nw')  # i = item
