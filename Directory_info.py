import os
import time as tm
import json
import datetime
from tkinter import *
import tkinter.filedialog as fd
from tkinter import filedialog, messagebox

WIN_WIDTH, WIN_HEIGHT = 0, 0
APP_WIDTH, APP_HEIGHT = 400, 600

MEDIA_FILES = ["jpg", "jpeg", "png", "bmp", "dcm", "gif", "ico", "webp", "raw", "svg", "img"]
VIDEO_FILES = ["mp4", "mov", "avi", "mpeg", "webm", "vob"]
AUDIO_FILES = ["mp3", "mp2", "wav", "mpc", "wma"]
DOC_FILES = ["pdf", "wps", "wpd", "txt", "log", "json"]
FORMAT_FILES = ["doc", "docx", "ppt", "pptx", "xls", "slsx", "odt", "xpc", "xml"]
DATABASE_FILES = ["pdb", "dbf", "db", "mdb", "sql", "dat"]
ARCHIVE_FILES = ["zip", "zipx", "rar", "7z", "arj", "tar", "apk"]
WEBSITE_FILES = ["html", "htm", "xhtml", "php", "js", "apk", "css", "kml"]
EXECUTABLE_FILES = ["exe", "com", "bat"]


def get_size_monitor() -> None:
    """ Sets the screen size value """
    global WIN_WIDTH, WIN_HEIGHT
    root_info = Tk()
    root_info.attributes('-fullscreen', True)
    WIN_WIDTH = root_info.winfo_screenwidth()
    WIN_HEIGHT = root_info.winfo_screenheight()
    root_info.destroy()
    # print(f"Size of monitor: {WIN_WIDTH}x{WIN_HEIGHT}")


class App:
    def __init__(self):
        self.cb_options = []
        self.selected_op = None
        self.btn_folder = None
        self.lb_valid = None
        self.entry_path = None
        self.RIGHT_PATH = False

        self.root = Tk()
        self.frame_options = LabelFrame(self.root, text="Options")
        self.set_options_window()

    def set_options_window(self) -> None:
        self.set_sizes_and_position()
        self.set_configure()
        self.add_objects()

    def set_sizes_and_position(self) -> None:
        self.root.resizable(False, False)
        offset_width, offset_height = WIN_WIDTH // 2 - APP_WIDTH // 2, WIN_HEIGHT // 2 - APP_HEIGHT // 2
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{offset_width}+{offset_height}")

    def set_configure(self) -> None:
        self.root.title("Directory Info")
        # self.root.configure(background="grey")
        # root.wm_attributes('-transparentcolor', root['bg'])  # Прозрачное приложение!

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add event for close window

    def is_valid(self, new_val: str) -> bool:
        global RIGHT_PATH
        if not new_val:
            self.lb_valid['text'] = ''
            RIGHT_PATH = False
        elif os.path.exists(new_val):
            self.lb_valid['text'] = 'Ok, the path exists!'
            self.lb_valid['fg'] = 'green'
            RIGHT_PATH = True
        else:
            self.lb_valid['text'] = 'The path not exists!'
            self.lb_valid['fg'] = 'red'
            RIGHT_PATH = False
        self.root.update()
        return True

    def get_initial_path(self) -> None:
        # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        initial_path = fd.askdirectory(title="Select a folder", initialdir="/")
        if os.path.exists(initial_path):
            self.entry_path.delete(0, END)
            self.entry_path.insert(0, initial_path)

    def create_frame_options(self) -> None:
        # var = BooleanVar()
        # var.set(False)
        options_name = ['Media files', 'Audio files', 'Video files',
                        'Document files', 'Microsoft filse', 'Database files',
                        'Archive files', 'Website files', 'Executable files']
        key_pos = 0
        for row in range(1, 4):
            for col in range(1, 4):
                selected_cb = IntVar()
                cb = Checkbutton(
                    self.frame_options, text=options_name[key_pos], variable=selected_cb,
                    onvalue=1, offvalue=0, command=lambda: self.check_checkbuttons())  # , variable=var
                cb.grid(row=row, column=col, ipadx=2, ipady=2, padx=2, pady=2, sticky='nw')  # i = item
                self.cb_options.append((cb, selected_cb, options_name[key_pos]))
                key_pos += 1
                # print(cb.keys())
                print(cb.winfo_name())

    def display_options(self) -> None:
        # print(self.selected_op, self.selected_op.get())
        self.frame_options.place(relx=0.07, rely=0.3, anchor=NW)
        self.root.update()

    def destroy_options(self) -> None:
        # for widgets in self.frame_options.winfo_children():
        #     widgets.destroy()
        self.frame_options.place_forget()
        self.root.update()

    def check_checkbuttons(self):
        for item in self.cb_options:
            print(item[0], item[1], item[1].get())

    def add_objects(self) -> None:
        root = self.root
        # TITLE
        lb_title = Label(text='DIR_INFO', font=('Times', 20, 'italic', 'bold'), fg='magenta')
        # lb_title.place(relx=0.5, rely=0.01, anchor=N)
        lb_title.pack(anchor=N, pady=7)

        # ENTRY PATH
        check = (root.register(self.is_valid), "%P")
        self.entry_path = Entry(validate="key", validatecommand=check, width=34, bg='lightgrey',
                                font=('Times', 13,), fg='darkorange', cursor='pencil')
        self.entry_path.place(relx=0.05, rely=0.1, anchor=NW)
        self.lb_valid = Label(text='', font=('Times', 8))
        self.lb_valid.place(relx=0.1, rely=0.136, anchor=NW)

        # BUTTON FOR PATH
        photo_folder = PhotoImage(file=r"data\folder.png")  # icon button
        photo_folder = photo_folder.subsample(16, 16)  # photo size reduction (less)
        self.btn_folder = Button(root, command=self.get_initial_path, image=photo_folder, activebackground="pink",
                                 borderwidth=0)
        self.btn_folder.image = photo_folder
        self.btn_folder.place(relx=0.865, rely=0.088, anchor=NW)

        # LABEL PARAMETERS
        options_label = Label(text='Data collection parameters', font=('Arial', 14, 'italic', 'bold'), fg='maroon1')
        options_label.place(relx=0.5, rely=0.18, anchor=N)

        # RADIOBUTTON FOR OPTIONS
        self.selected_op = IntVar()
        self.selected_op.set(0)
        rad_1 = Radiobutton(root, text='All', value=1, variable=self.selected_op,
                            font=2, activeforeground='yellow', command=self.destroy_options)
        rad_2 = Radiobutton(root, text='Selectively', value=2, variable=self.selected_op,
                            font=2, activeforeground='yellow', command=self.display_options)
        rad_1.place(relx=0.3, rely=0.23, anchor=N)
        rad_2.place(relx=0.7, rely=0.23, anchor=N)

        # CHECKBUTTON FOR OPTIONS
        self.create_frame_options()

        # lb_delimiter = Label(text=f"{'-' * 80}", font=('Times', 20), fg='cyan')
        # lb_delimiter.place(relx=0.5, rely=0.06, anchor=N)
        # lb_cw = Label(master=root, text="Control window:", font=('Comic Sans MC', 15))
        # lb_cb = Label(text="Control button:", font=('Comic Sans MC', 15))
        # lb_ew = Label(text="Exit window:", font=('Comic Sans MC', 15))
        # lb_eb = Label(text="Exit button:", font=('Comic Sans MC', 15))
        # lb_cw.place(x=10, y=100, anchor=W)
        # lb_cb.place(x=10, y=190, anchor=W)
        # lb_ew.place(x=10, y=280, anchor=W)
        # lb_eb.place(x=10, y=370, anchor=W)
        #
        # btn_cb = Button(root, text="Выбрать", command=lambda: choose_img_file(1), activeforeground="blue",
        #                 activebackground="pink")
        # btn_ew = Button(root, text="Выбрать", command=lambda: choose_img_file(2), activeforeground="blue",
        #                 activebackground="pink")
        # btn_eb = Button(root, text="Выбрать", command=lambda: choose_img_file(3), activeforeground="blue",
        #                 activebackground="pink")
        # btn_cw.place(x=200, y=100, anchor=CENTER)
        # btn_cb.place(x=190, y=190, anchor=CENTER)
        # btn_ew.place(x=180, y=280, anchor=CENTER)
        # btn_eb.place(x=170, y=370, anchor=CENTER)
        # btn_all = [btn_cw, btn_cb, btn_ew, btn_eb]
        # btn_start = Button(root, text="Старт", font=('Arial', 16, 'italic', 'bold'), command=start_stop_app,
        #                    activeforeground="blue",
        #                    activebackground="pink", bg='red', bd=5, width=12, height=2)
        # btn_start.place(relx=0.5, rely=0.8, anchor=N)

    def display(self):
        # self.root.update()
        self.root.mainloop()

    def on_closing(self) -> None:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            tm.sleep(1)
            exit()


def main() -> None:
    get_size_monitor()
    a = App()
    a.display()


if __name__ == '__main__':
    main()
