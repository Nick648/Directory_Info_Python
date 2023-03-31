import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from Search_type_files import run_search_types
from Total_info_files_dir import run_total_search

# CONSTs
WIN_WIDTH, WIN_HEIGHT = 0, 0
APP_WIDTH, APP_HEIGHT = 400, 600
ROW_OPTIONS_COUNT = 3
COL_OPTIONS_COUNT = 3

# FILE TYPES
MEDIA_FILES = ["jpg", "jpeg", "png", "bmp", "dcm", "gif", "ico", "webp", "raw", "svg", "img"]
VIDEO_FILES = ["mp4", "mov", "avi", "mpeg", "webm", "vob"]
AUDIO_FILES = ["mp3", "mp2", "wav", "mpc", "wma"]
DOCUMENT_FILES = ["pdf", "wps", "wpd", "txt", "log", "json", "xml"]
MICROSOFT_FILES = ["doc", "docx", "ppt", "pptx", "xls", "slsx", "odt", "xpc"]
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


class MyCheckButton:
    num_button = 0

    def __init__(self, master, title: str, row: int = -1, col: int = -1):
        self.var_select = BooleanVar()
        self.var_select.set(False)
        self.title = title
        MyCheckButton.num_button += 1
        self.num_button = MyCheckButton.num_button
        self.cb = Checkbutton(
            master, text=title, variable=self.var_select,
            onvalue=1, offvalue=0)  # command=lambda: print(self.title)
        if row == -1 and col == -1:
            self.cb.pack(side=LEFT)
        else:
            self.cb.grid(row=row, column=col, ipadx=2, ipady=2, padx=2, pady=2, sticky='nw')  # i = item


class App:
    def __init__(self):
        # Main window
        self.root = Tk()
        # Elements
        self.btn_start = Button(master=self.root)
        self.cb_options = []
        self.rad_options = []
        self.selected_op = IntVar()
        self.btn_folder = Button(master=self.root)
        self.lb_valid = Label(master=self.root)
        self.entry_path = Entry(master=self.root)
        self.correct_path = False
        self.frame_options = LabelFrame(master=self.root, text="Options")
        # Creating another configurations
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
        # self.root.wm_attributes('-transparentcolor', self.root['bg'])  # Прозрачное приложение!

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add event for close window

    def is_valid(self, new_val: str) -> bool:
        if not new_val:
            self.lb_valid['text'] = ''
            self.correct_path = False
        elif os.path.exists(new_val):
            self.lb_valid['text'] = 'Ok, the path exists!'
            self.lb_valid['fg'] = 'green'
            self.correct_path = True
        else:
            self.lb_valid['text'] = 'The path not exists!'
            self.lb_valid['fg'] = 'red'
            self.correct_path = False
        self.root.update()
        return True

    def get_initial_path(self) -> None:
        # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        initial_path = filedialog.askdirectory(title="Select a folder", initialdir="/")
        if os.path.exists(initial_path):
            self.entry_path.delete(0, END)
            self.entry_path.insert(0, initial_path)

    def create_frame_options(self) -> None:
        options_name = ['Media files', 'Audio files', 'Video files',
                        'Document files', 'Microsoft files', 'Database files',
                        'Archive files', 'Website files', 'Executable files']
        key_pos = 0
        for row in range(1, ROW_OPTIONS_COUNT + 1):
            for col in range(1, COL_OPTIONS_COUNT + 1):
                cb = MyCheckButton(master=self.frame_options, title=options_name[key_pos], row=row, col=col)
                self.cb_options.append(cb)
                key_pos += 1

    def display_options(self) -> None:
        self.frame_options.place(relx=0.07, rely=0.3, anchor=NW)
        self.root.update()

    def hide_options(self) -> None:
        # Do not uncomment, otherwise delete. (Created once)!
        # for widgets in self.frame_options.winfo_children():
        #     widgets.destroy()
        self.frame_options.place_forget()
        self.root.update()

    def disable_objects(self) -> None:
        self.entry_path['state'] = 'disabled'
        self.btn_folder['state'] = 'disabled'
        for item_rad in self.rad_options:
            item_rad['state'] = 'disabled'
        for item_cb in self.cb_options:
            item_cb.cb['state'] = 'disabled'
        self.btn_start['bg'] = 'dark red'
        self.btn_start['state'] = 'disabled'
        self.root.update()

    def activate_object(self) -> None:
        self.lb_valid['text'] = ''
        self.entry_path['state'] = 'normal'
        self.entry_path.delete(0, END)
        self.btn_folder['state'] = 'normal'
        self.selected_op.set(0)
        for item_rad in self.rad_options:
            item_rad['state'] = 'normal'
            item_rad.deselect()
        for item_cb in self.cb_options:
            item_cb.cb['state'] = 'normal'
            item_cb.cb.deselect()
        self.hide_options()
        self.btn_start['bg'] = 'green'
        self.btn_start['state'] = 'normal'
        self.correct_path = False
        self.root.update()

    def start_app(self) -> None:  # FIXME: ADD THREAD
        if not self.correct_path:
            messagebox.showerror(title="Error", message="Enter the correct path to the folder!")
            return
        if self.selected_op.get() != 1 and self.selected_op.get() != 2:
            messagebox.showwarning(title="Warning", message="You need to select the search parameter!")
            return

        if self.selected_op.get() == 1:
            self.disable_objects()
            progress_bar = ttk.Progressbar(master=self.root, orient="horizontal", length=170, value=0)
            progress_bar.place(relx=0.5, rely=0.78, anchor=N)
            # FIXME: ADD iridescent color
            lb_step = Label(master=self.root, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
            lb_step.place(relx=0.5, rely=0.73, anchor=N)
            report = run_total_search(initial_path=self.entry_path.get(),
                                      progress_bar=progress_bar, lb_step=lb_step)
            messagebox.showinfo(title="Feedback report", message=report)
            progress_bar.destroy()
            lb_step.destroy()
            self.activate_object()

        if self.selected_op.get() == 2:
            types_search_files = []
            for cb_item in self.cb_options:
                # print(f'{cb_item.num_button=}; {cb_item.title=}; {cb_item.var_select.get()=}; {name_cb=}')
                if cb_item.var_select.get():
                    name_cb = cb_item.title.replace(' ', '_').upper()
                    for type_file in globals()[name_cb]:  # accessing a variable via a string
                        types_search_files.append('.' + type_file)
            # print(f'{types_search_files=}')
            if types_search_files:
                self.disable_objects()
                progress_bar = ttk.Progressbar(master=self.root, orient="horizontal", length=170, value=0)
                progress_bar.place(relx=0.5, rely=0.78, anchor=N)
                # FIXME: ADD iridescent color
                lb_step = Label(master=self.root, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
                lb_step.place(relx=0.5, rely=0.73, anchor=N)
                report = run_search_types(initial_path=self.entry_path.get(),
                                          search_type_files=types_search_files,
                                          progress_bar=progress_bar, lb_step=lb_step)
                messagebox.showinfo(title="Feedback report", message=report)
                progress_bar.destroy()
                lb_step.destroy()
                self.activate_object()
            else:
                messagebox.showwarning(title="Warning", message="You need to select the search parameters!")
                return

    def add_objects(self) -> None:
        root = self.root
        # TITLE
        lb_title = Label(text='DIR_INFO', font=('Times', 20, 'italic', 'bold'), fg='magenta')
        lb_title.place(relx=0.5, rely=0.015, anchor=N)

        # ENTRY PATH
        check = (root.register(self.is_valid), "%P")
        self.entry_path = Entry(validate="key", validatecommand=check, width=34, bg='light grey',
                                font=('Times', 13,), fg='purple', cursor='pencil')
        self.entry_path.place(relx=0.05, rely=0.1, anchor=NW)
        self.lb_valid = Label(text='', font=('Times', 8))
        self.lb_valid.place(relx=0.1, rely=0.136, anchor=NW)

        # BUTTON FOR PATH
        photo_folder = PhotoImage(file=r"data\folder.png")  # icon button
        photo_folder = photo_folder.subsample(16, 16)  # photo size reduction (less)
        self.btn_folder = Button(master=root, command=self.get_initial_path, image=photo_folder,
                                 activebackground="pink", borderwidth=0)
        self.btn_folder.image = photo_folder
        self.btn_folder.place(relx=0.865, rely=0.088, anchor=NW)

        # LABEL PARAMETERS
        options_label = Label(text='Data collection parameters', font=('Arial', 14, 'italic', 'bold'), fg='maroon1')
        options_label.place(relx=0.5, rely=0.17, anchor=N)

        # RADIOBUTTON FOR OPTIONS
        self.selected_op = IntVar()
        self.selected_op.set(0)
        rad_1 = Radiobutton(root, text='All', value=1, variable=self.selected_op,
                            font=2, activeforeground='yellow', command=self.hide_options)
        rad_2 = Radiobutton(root, text='Selectively', value=2, variable=self.selected_op,
                            font=2, activeforeground='yellow', command=self.display_options)
        self.rad_options.append(rad_1)
        self.rad_options.append(rad_2)
        rad_1.place(relx=0.3, rely=0.23, anchor=N)
        rad_2.place(relx=0.7, rely=0.23, anchor=N)

        # CHECKBUTTON FOR OPTIONS
        self.create_frame_options()

        # BUTTON FOR START APP
        self.btn_start = Button(root, text="Start parsing", font=('Comic Sans MC', 16, 'italic', 'bold'),
                                command=self.start_app,
                                activeforeground="blue", activebackground="pink", relief='groove',
                                fg='coral', bg='green', bd=2, width=14, height=2)
        # some_relief = ['flat', 'raised', 'sunken', 'ridge', 'solid', 'groove']
        self.btn_start.place(relx=0.5, rely=0.85, anchor=N)

    def display(self) -> None:
        self.root.update()
        self.root.mainloop()

    def on_closing(self) -> None:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit()


def main() -> None:
    get_size_monitor()
    a = App()
    a.display()


if __name__ == '__main__':
    main()
