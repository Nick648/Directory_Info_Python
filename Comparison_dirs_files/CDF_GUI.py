import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from Backend_functions import Total_info_files_dir, Search_type_files, Search_type_files_FTP
from Backend_functions.Work_with_ftp import ConnectionToFtp

# CONSTs
APP_WIDTH, APP_HEIGHT = 400, 600
ROW_OPTIONS_COUNT = 4
COL_OPTIONS_COUNT = 3
OPTIONS_NAME = []


def get_size_monitor() -> tuple[int, int]:
    """
    Get the screen size value

    Returns:
        tuple[int, int]: The value of the width and height of the PC screen
    """
    root_info = Tk()
    root_info.attributes('-fullscreen', True)
    win_width = root_info.winfo_screenwidth()
    win_height = root_info.winfo_screenheight()
    root_info.destroy()
    # print(f"Size of monitor: {win_width}x{win_height}")
    return win_width, win_height


def create_frame_options(master_frame: LabelFrame, cb_options: list) -> None:
    key_pos = 0
    for row in range(1, ROW_OPTIONS_COUNT + 1):
        for col in range(1, COL_OPTIONS_COUNT + 1):
            if key_pos == len(OPTIONS_NAME):
                return
            cb = MyCheckButton(master=master_frame, title=OPTIONS_NAME[key_pos], row=row, col=col)
            cb_options.append(cb)
            key_pos += 1


def get_frame_list_gif(file: str) -> list:
    frame_index = 0
    frame_list = []
    while True:
        try:
            part = "gif -index {}".format(frame_index)
            frame = PhotoImage(file=file, format=part).subsample(4, 4)
        except TclError:
            break
        frame_list.append(frame)
        frame_index += 1
    return frame_list


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


class App:

    def __init__(self):
        # Main window
        self.root = Tk()
        # FTP
        self.ftp_service = ConnectionToFtp()
        # Tabs/Pages
        tab_control = ttk.Notebook(self.root)
        self.tab_1 = ttk.Frame(tab_control)
        self.tab_2 = ttk.Frame(tab_control)
        tab_control.add(self.tab_1, text='Check repetitions')
        tab_control.add(self.tab_2, text='Check similarity')
        tab_control.pack(expand=1, fill='both')
        # Elements Page №1
        self.entry_path_parse = Entry(master=self.tab_1)
        self.btn_folder_parse = Button(master=self.tab_1)
        self.lb_valid_parse = Label(master=self.tab_1)
        self.correct_path_parse = False
        self.entry_path_save = Entry(master=self.tab_1)
        self.btn_folder_save = Button(master=self.tab_1)
        self.lb_valid_save = Label(master=self.tab_1)
        self.correct_path_save = False
        self.selected_op_rad = IntVar()
        self.rad_options = []
        self.frame_options = LabelFrame(master=self.tab_1, text="Options")
        self.cb_options = []
        self.btn_start = Button(master=self.tab_1)
        # Elements Page №2
        self.style_tk = ttk.Style()
        self.btn_reset_tab_2 = Button(master=self.tab_2)
        self.entry_host_parse = ttk.Entry(master=self.tab_2)
        self.lb_valid_host = ttk.Label(master=self.tab_2)
        self.correct_host = False
        self.entry_port_parse = ttk.Entry(master=self.tab_2)
        self.lb_valid_port = ttk.Label(master=self.tab_2)
        self.correct_port = False
        self.connect_to_ftp = False
        self.btn_check_connect = Button(master=self.tab_2)
        self.entry_password_ftp = Entry(master=self.tab_2)
        self.lb_gif_host = Label(master=self.tab_2)
        self.lb_gif_port = Label(master=self.tab_2)
        self.selected_anon = BooleanVar()
        self.selected_anon.set(False)
        self.btn_check_login = Button(master=self.tab_2)
        self.lb_gif_login = Label(master=self.tab_2)
        self.lbl_initial_path_ftp = Label(master=self.tab_2)
        self.lb_password_ftp = Label(master=self.tab_2)
        self.entry_login_ftp = Entry(master=self.tab_2)
        self.lb_gif_password = Label(master=self.tab_2)
        self.lb_login_ftp = Label(master=self.tab_2)
        self.check_btn_anon = Checkbutton(master=self.tab_2)
        self.cmbx_path = ttk.Combobox(master=self.tab_2)
        self.selected_op_rad_ftp = IntVar()
        self.selected_op_rad_ftp.set(0)
        self.rad_options_ftp = []
        self.cb_options_ftp = []
        self.options_label_ftp = Label(master=self.tab_2)
        self.frame_options_ftp = LabelFrame(master=self.tab_2, text="Options")
        self.lb_path_saving_ftp = Label(master=self.tab_2)
        self.entry_path_save_ftp = Entry(master=self.tab_2)
        self.btn_folder_save_ftp = Button(master=self.tab_2)
        self.lb_valid_save_ftp = Label(master=self.tab_2)
        self.correct_path_save_ftp = False
        self.btn_start_ftp = Button(master=self.tab_2)
        # Storage
        self.tree_paths = []
        self.btn_prompts = []
        # Creating another configurations
        self.set_options_window()

    def set_options_window(self) -> None:
        self.set_sizes_and_position()
        self.set_configures()
        self.add_objects()

    def set_styles(self) -> None:
        print(self.style_tk.element_names(), self.style_tk.theme_names(), self.style_tk.theme_use(), sep='\n')
        # style_tk.configure('My.TFrame', background='green')
        # style_tk.configure('TButton', background='red')

    def set_sizes_and_position(self) -> None:
        self.root.resizable(width=False, height=False)
        win_width, win_height = get_size_monitor()
        offset_width, offset_height = win_width // 2 - APP_WIDTH // 2, win_height // 2 - APP_HEIGHT // 2
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{offset_width}+{offset_height}")

    def set_configures(self) -> None:
        self.root.title("Directory Info")
        # self.root.configure(background="grey")
        # self.root.wm_attributes('-transparentcolor', self.root['bg'])  # Прозрачное приложение!
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add event for close window

    def is_valid_path_parse(self, new_val: str) -> bool:
        if not new_val:
            self.lb_valid_parse['text'] = ''
            self.correct_path_parse = False
        elif os.path.exists(new_val):
            if os.path.isdir(new_val):
                self.lb_valid_parse['text'] = 'Ok, the path is correct!'
                self.lb_valid_parse['fg'] = 'green'
                self.correct_path_parse = True
            else:
                self.lb_valid_parse['text'] = "The path exists, but it's not a folder!"
                self.lb_valid_parse['fg'] = 'darkorange'
                self.correct_path_parse = False
        else:
            self.lb_valid_parse['text'] = 'The path not exists!'
            self.lb_valid_parse['fg'] = 'red'
            self.correct_path_parse = False
        return True

    def is_valid_path_save(self, new_val: str) -> bool:
        if not new_val:
            self.lb_valid_save['text'] = ''
            self.correct_path_save = False
        elif os.path.exists(new_val):
            if os.path.isdir(new_val):
                self.lb_valid_save['text'] = 'Ok, the path is correct!'
                self.lb_valid_save['fg'] = 'green'
                self.correct_path_save = True
            else:
                self.lb_valid_save['text'] = "The path exists, but it's not a folder!"
                self.lb_valid_save['fg'] = 'darkorange'
                self.correct_path_save = False
        else:
            self.lb_valid_save['text'] = 'The path not exists!'
            self.lb_valid_save['fg'] = 'red'
            self.correct_path_save = False
        return True

    def get_paths_cmbx(self) -> None:
        try:
            self.tree_paths = self.ftp_service.gen_ftp_walk()
        except Exception as ex:
            messagebox.showerror(title="Error", message=f'{ex} \n Try to connect again...')

    def display_login_entry(self) -> None:
        self.lb_login_ftp.place(relx=0.05, rely=0.2, anchor=NW)
        self.entry_login_ftp.place(relx=0.25, rely=0.2, anchor=NW)
        self.lb_password_ftp.place(relx=0.05, rely=0.25, anchor=NW)
        self.entry_password_ftp.place(relx=0.25, rely=0.25, anchor=NW)
        self.check_btn_anon.place(relx=0.6, rely=0.2, anchor=NW)
        self.btn_check_login.place(relx=0.6, rely=0.25, anchor=NW)

    def place_parameters_for_parse_ftp(self) -> None:
        self.options_label_ftp.place(relx=0.5, rely=0.47, anchor=N)
        self.rad_options_ftp[0].place(relx=0.3, rely=0.51, anchor=N)
        self.rad_options_ftp[1].place(relx=0.7, rely=0.51, anchor=N)
        self.place_lbl_save_and_btn_start_ftp()

    def place_lbl_save_and_btn_start_ftp(self) -> None:
        self.lb_path_saving_ftp.place(relx=0.06, rely=0.37, anchor=NW)
        self.entry_path_save_ftp.place(relx=0.05, rely=0.4, anchor=NW)
        self.btn_folder_save_ftp.place(relx=0.865, rely=0.385, anchor=NW)
        self.lb_valid_save_ftp.place(relx=0.1, rely=0.44, anchor=NW)
        self.btn_start_ftp.place(relx=0.5, rely=0.89, relheight=0.1, anchor=N)

    def get_initial_path(self, mode: str) -> None:
        # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        title = mode
        initial_dir = "/"
        if mode == 'parse':
            title = 'Select a folder for parsing'
        elif mode == 'save':
            title = 'Select a folder for saving'
            initial_dir = os.getcwd()
        options = {
            "initialdir": initial_dir,
            "title": title,
            "mustexist": False,
        }

        initial_path = filedialog.askdirectory(**options)
        if os.path.exists(initial_path):
            if mode == 'parse':
                self.entry_path_parse.delete(0, END)
                self.entry_path_parse.insert(0, initial_path)
            elif mode == 'save':
                self.entry_path_save.delete(0, END)
                self.entry_path_save.insert(0, initial_path)
            elif mode == 'save_ftp':
                self.entry_path_save_ftp.delete(0, END)
                self.entry_path_save_ftp.insert(0, initial_path)

    def reset_tab_2(self) -> None:
        self.entry_host_parse['state'] = 'normal'
        self.entry_host_parse.delete(0, END)
        self.entry_port_parse['state'] = 'normal'
        self.entry_port_parse.delete(0, END)
        self.btn_check_connect['state'] = 'normal'
        self.correct_host = False
        self.correct_port = False

        if self.connect_to_ftp:
            self.ftp_service.close()
            self.connect_to_ftp = False

        self.lb_gif_host.place_forget()
        self.lb_gif_port.place_forget()
        self.lb_gif_login.place_forget()
        self.lb_gif_password.place_forget()

        self.connect_to_ftp = False
        self.entry_login_ftp['state'] = 'normal'
        self.entry_login_ftp.delete(0, END)
        self.entry_password_ftp['state'] = 'normal'
        self.entry_password_ftp.delete(0, END)
        self.lb_login_ftp.place_forget()
        self.entry_login_ftp.place_forget()
        self.lb_password_ftp.place_forget()
        self.entry_password_ftp.place_forget()
        self.check_btn_anon['state'] = 'normal'
        self.selected_anon.set(False)
        self.check_btn_anon.place_forget()
        self.btn_check_login['state'] = 'normal'
        self.btn_check_login.place_forget()

        self.lbl_initial_path_ftp.place_forget()
        self.cmbx_path['state'] = 'normal'
        self.cmbx_path.place_forget()

        self.lb_path_saving_ftp.place_forget()
        self.entry_path_save_ftp['state'] = 'normal'
        self.entry_path_save_ftp.delete(0, END)
        self.entry_path_save_ftp.place_forget()
        self.btn_folder_save_ftp['state'] = 'normal'
        self.btn_folder_save_ftp.place_forget()
        self.lb_valid_save_ftp['text'] = ''
        self.correct_path_save_ftp = False
        self.lb_valid_save_ftp.place_forget()

        self.options_label_ftp.place_forget()
        self.rad_options_ftp[0].place_forget()
        self.rad_options_ftp[1].place_forget()
        self.selected_op_rad_ftp.set(0)
        self.frame_options_ftp.place_forget()
        for item_rad in self.rad_options_ftp:
            item_rad['state'] = 'normal'
            item_rad.deselect()
        for item_cb in self.cb_options_ftp:
            item_cb.cb['state'] = 'normal'
            item_cb.cb.deselect()

        self.btn_start_ftp['bg'] = 'green'
        self.btn_start_ftp['state'] = 'normal'
        self.btn_start_ftp.place_forget()
        self.tab_2.update()

    def disable_objects_tab_2(self) -> None:
        self.entry_host_parse['state'] = 'disabled'
        self.entry_port_parse['state'] = 'disabled'
        self.btn_check_connect['state'] = 'disabled'

        self.entry_login_ftp['state'] = 'disabled'
        self.entry_password_ftp['state'] = 'disabled'
        self.entry_login_ftp['state'] = 'disabled'
        self.check_btn_anon['state'] = 'disabled'
        self.btn_check_login['state'] = 'disabled'

        self.cmbx_path['state'] = 'disabled'

        self.entry_path_save_ftp['state'] = 'disabled'
        self.btn_folder_save_ftp['state'] = 'disabled'

        for item_rad in self.rad_options_ftp:
            item_rad['state'] = 'normal'
        for item_cb in self.cb_options_ftp:
            item_cb.cb['state'] = 'normal'

        self.btn_start_ftp['bg'] = 'dark red'
        self.btn_start_ftp['state'] = 'disabled'
        self.tab_2.update()

    def disable_objects_tab_1(self) -> None:
        self.entry_path_parse['state'] = 'disabled'
        self.btn_folder_parse['state'] = 'disabled'
        self.entry_path_save['state'] = 'disabled'
        self.btn_folder_save['state'] = 'disabled'
        for item_rad in self.rad_options:
            item_rad['state'] = 'disabled'
        for item_cb in self.cb_options:
            item_cb.cb['state'] = 'disabled'
        self.btn_start['bg'] = 'dark red'
        self.btn_start['state'] = 'disabled'
        self.tab_1.update()

    def activate_object_tab_1(self) -> None:
        self.lb_valid_parse['text'] = ''
        self.lb_valid_save['text'] = ''
        self.entry_path_parse['state'] = 'normal'
        self.entry_path_parse.delete(0, END)
        self.entry_path_save['state'] = 'normal'
        self.entry_path_save.delete(0, END)
        self.btn_folder_parse['state'] = 'normal'
        self.btn_folder_save['state'] = 'normal'
        self.selected_op_rad.set(0)
        for item_rad in self.rad_options:
            item_rad['state'] = 'normal'
            item_rad.deselect()
        for item_cb in self.cb_options:
            item_cb.cb['state'] = 'normal'
            item_cb.cb.deselect()
        self.frame_options.place_forget()
        self.btn_start['bg'] = 'green'
        self.btn_start['state'] = 'normal'
        self.correct_path_parse = False
        self.correct_path_save = False
        self.tab_1.update()

    def start_app_path(self) -> None:
        if not self.correct_path_parse:
            messagebox.showerror(title="Error", message="Enter the correct path to the parse folder!")
            return
        if not self.correct_path_save:
            messagebox.showerror(title="Error", message="Enter the correct path to the save result folder!")
            return
        if self.selected_op_rad.get() != 1 and self.selected_op_rad.get() != 2:
            messagebox.showwarning(title="Warning", message="You need to select the search parameter!")
            return

        path_for_save = self.entry_path_save.get()

        if self.selected_op_rad.get() == 1:  # Total search
            self.disable_objects_tab_1()
            progress_bar = ttk.Progressbar(master=self.tab_1, orient="horizontal", length=170, value=0)
            progress_bar.place(relx=0.5, rely=0.78, anchor=N)
            lb_step = Label(master=self.tab_1, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
            lb_step.place(relx=0.5, rely=0.72, anchor=N)
            report = Total_info_files_dir.run_total_search(initial_path=self.entry_path_parse.get(),
                                                           progress_bar=progress_bar, lb_step=lb_step,
                                                           path_for_save=path_for_save)
            messagebox.showinfo(title="Feedback report", message=report)
            progress_bar.destroy()
            lb_step.destroy()
            self.activate_object_tab_1()

        if self.selected_op_rad.get() == 2:  # Search type files
            types_search_files = []
            for cb_item in self.cb_options:
                if cb_item.var_select.get():
                    name_cb = cb_item.title.replace(' ', '_').upper()
                    for type_file in globals()[name_cb]:  # accessing a variable via a string
                        types_search_files.append('.' + type_file.lower())
            if types_search_files:
                self.disable_objects_tab_1()
                progress_bar = ttk.Progressbar(master=self.tab_1, orient="horizontal", length=170, value=0)
                progress_bar.place(relx=0.5, rely=0.78, anchor=N)
                lb_step = Label(master=self.tab_1, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
                lb_step.place(relx=0.5, rely=0.73, anchor=N)
                report = Search_type_files.run_search_types(initial_path=self.entry_path_parse.get(),
                                                            search_type_files=types_search_files,
                                                            progress_bar=progress_bar, lb_step=lb_step,
                                                            path_for_save=path_for_save)
                messagebox.showinfo(title="Feedback report", message=report)
                progress_bar.destroy()
                lb_step.destroy()
                self.activate_object_tab_1()
            else:
                messagebox.showwarning(title="Warning", message="You need to select the search parameters!")
                return

    def start_app_ftp(self) -> None:
        if not self.correct_path_save_ftp:
            messagebox.showerror(title="Error", message="Enter the correct path to the save result folder!")
            return
        if self.selected_op_rad_ftp.get() != 1 and self.selected_op_rad_ftp.get() != 2:
            messagebox.showwarning(title="Warning", message="You need to select the search parameter!")
            return

        path_for_save = self.entry_path_save_ftp.get()

        if self.selected_op_rad_ftp.get() == 1:  # Total search
            messagebox.showinfo(title="Info", message="In development...")

        if self.selected_op_rad_ftp.get() == 2:  # Search type files
            types_search_files = []
            for cb_item in self.cb_options_ftp:
                if cb_item.var_select.get():
                    name_cb = cb_item.title.replace(' ', '_').upper()
                    for type_file in globals()[name_cb]:  # accessing a variable via a string
                        types_search_files.append('.' + type_file.lower())
            if types_search_files:
                self.disable_objects_tab_2()
                progress_bar = ttk.Progressbar(master=self.tab_2, orient="horizontal", length=170, value=0)
                progress_bar.place(relx=0.5, rely=0.85, anchor=N)
                lb_step = Label(master=self.tab_2, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
                lb_step.place(relx=0.5, rely=0.8, anchor=N)
                report = Search_type_files_FTP.run_search_types(initial_path=self.cmbx_path.get(),
                                                                search_type_files=types_search_files,
                                                                progress_bar=progress_bar, lb_step=lb_step,
                                                                tree_paths=self.tree_paths,
                                                                path_for_save=path_for_save)
                messagebox.showinfo(title="Feedback report", message=report)
                progress_bar.destroy()
                lb_step.destroy()
                self.reset_tab_2()
            else:
                messagebox.showwarning(title="Warning", message="You need to select the search parameters!")
                return

    def add_objects(self) -> None:
        # -> PAGE №1
        # TITLE PC
        lb_title = Label(master=self.tab_1, text=' DIR_INFO_PC ', font=('Cooper Black', 18, 'italic'), fg='magenta')
        lb_title.place(relx=0.5, rely=0.01, anchor=N)

        # LABEL PATH FOR PARSING
        lb_path_parsing = Label(master=self.tab_1, text='Path for parsing', font=('Arial', 10, 'italic'), fg='black')
        lb_path_parsing.place(relx=0.06, rely=0.06, anchor=NW)

        # ENTRY PATH PARSING
        check_path_parse = (self.root.register(self.is_valid_path_parse), "%P")
        self.entry_path_parse = Entry(master=self.tab_1, validate="key", validatecommand=check_path_parse, width=34,
                                      bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil')
        self.entry_path_parse.place(relx=0.05, rely=0.1, anchor=NW)

        # BUTTON FOR PATH PARSING
        photo_folder_load = PhotoImage(file=r"data/folder_load.png")  # icon button
        photo_folder_load = photo_folder_load.subsample(15, 15)  # photo size reduction (less)
        self.btn_folder_parse = Button(master=self.tab_1, command=lambda: self.get_initial_path('parse'),
                                       image=photo_folder_load, activebackground="pink", borderwidth=0)
        self.btn_folder_parse.image = photo_folder_load
        self.btn_folder_parse.place(relx=0.865, rely=0.09, anchor=NW)

        # LABEL VALID PATH PARSING
        self.lb_valid_parse = Label(master=self.tab_1, text='', font=('Times', 9))
        self.lb_valid_parse.place(relx=0.1, rely=0.14, anchor=NW)

        # LABEL PATH TO SAVE
        lb_path_saving = Label(master=self.tab_1, text='Path to save the result',
                               font=('Arial', 10, 'italic'), fg='black')
        lb_path_saving.place(relx=0.06, rely=0.18, anchor=NW)

        # ENTRY PATH SAVE
        check_path_save = (self.root.register(self.is_valid_path_save), "%P")
        self.entry_path_save = Entry(master=self.tab_1, validate="key", validatecommand=check_path_save, width=34,
                                     bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil')
        self.entry_path_save.place(relx=0.05, rely=0.22, anchor=NW)

        # BUTTON FOR PATH SAVING
        photo_folder_save = PhotoImage(file=r"data/folder_save.png")
        photo_folder_save = photo_folder_save.subsample(16, 16)
        self.btn_folder_save = Button(master=self.tab_1, command=lambda: self.get_initial_path('save'),
                                      image=photo_folder_save, activebackground="pink", borderwidth=0)
        self.btn_folder_save.image = photo_folder_save
        self.btn_folder_save.place(relx=0.865, rely=0.205, anchor=NW)

        # LABEL VALID PATH SAVING
        self.lb_valid_save = Label(master=self.tab_1, text='', font=('Times', 9))
        self.lb_valid_save.place(relx=0.1, rely=0.26, anchor=NW)

        # LABEL PARAMETERS
        options_label = Label(master=self.tab_1, text='Data collection parameters',
                              font=('Arial', 14, 'italic', 'bold'), fg='chocolate2')
        options_label.place(relx=0.5, rely=0.3, anchor=N)

        # RADIOBUTTON FOR OPTIONS
        self.selected_op_rad = IntVar()
        self.selected_op_rad.set(0)
        rad_1 = Radiobutton(master=self.tab_1, text='All', value=1, variable=self.selected_op_rad,
                            font=2, activeforeground='yellow', command=lambda: self.frame_options.place_forget())
        rad_2 = Radiobutton(master=self.tab_1, text='Selectively', value=2, variable=self.selected_op_rad, font=2,
                            activeforeground='yellow',
                            command=lambda: self.frame_options.place(relx=0.07, rely=0.4, anchor=NW))
        self.rad_options.append(rad_1)
        self.rad_options.append(rad_2)
        rad_1.place(relx=0.3, rely=0.345, anchor=N)
        rad_2.place(relx=0.7, rely=0.345, anchor=N)

        # CHECKBUTTON FOR OPTIONS
        create_frame_options(master_frame=self.frame_options, cb_options=self.cb_options)

        # BUTTON FOR START APP
        self.btn_start = Button(master=self.tab_1, text="Start parsing", font=('Comic Sans MC', 16, 'italic', 'bold'),
                                command=self.start_app_path,
                                activeforeground="blue", activebackground="pink", relief='groove',
                                fg='coral', bg='green', bd=2, width=14, height=2)
        # some_relief = ['flat', 'raised', 'sunken', 'ridge', 'solid', 'groove']
        self.btn_start.place(relx=0.5, rely=0.85, anchor=N)

        # -> PAGE №2
        # TITLE FTP
        lb_title_ftp = Label(master=self.tab_2, text=' DIR_INFO_FTP ', font=('Cooper Black', 18, 'italic'),
                             fg='magenta')
        lb_title_ftp.place(relx=0.5, rely=0.01, anchor=N)

        # BUTTON RESET PAGE 2
        self.btn_reset_tab_2 = Button(master=self.tab_2, text='Reset', font=('Times', 12),
                                      fg='#A5260A', bg='#B5B8B1', bd=0, command=self.reset_tab_2)
        self.btn_reset_tab_2.place(relx=0.83, rely=0.02, anchor=NW)

        # LABEL HOST PARSING
        lb_host_parsing = Label(master=self.tab_2, text='Host', font=('Arial', 10, 'italic'), fg='black')
        lb_host_parsing.place(relx=0.06, rely=0.06, anchor=NW)

        # ENTRY HOST PARSING
        check_host = (self.root.register(self.is_valid_host), "%P")
        self.entry_host_parse = Entry(master=self.tab_2, validate="key", validatecommand=check_host, width=14,
                                      bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil', takefocus=0)
        self.entry_host_parse.place(relx=0.05, rely=0.1, anchor=NW)
        self.entry_host_parse.bind("<FocusIn>", lambda e: self.focus_in_for_prompt(e, 'host', self.entry_host_parse))
        self.entry_host_parse.bind("<KeyRelease>", lambda e: self.focus_in_for_prompt(e, 'host', self.entry_host_parse))
        self.entry_host_parse.bind("<FocusOut>", self.focus_out_for_prompt)

        # LABEL VALID HOST PARSING
        self.lb_valid_host = Label(master=self.tab_2, text='', font=('Times', 9))
        self.lb_valid_host.place(relx=0.08, rely=0.14, anchor=NW)

        # LABEL PORT PARSING
        lb_port_parsing = Label(master=self.tab_2, text='Port', font=('Arial', 10, 'italic'), fg='black')
        lb_port_parsing.place(relx=0.48, rely=0.06, anchor=NW)

        # ENTRY PORT PARSING
        check_port = (self.root.register(self.is_valid_port), "%P")
        self.entry_port_parse = Entry(master=self.tab_2, validate="key", validatecommand=check_port, width=10,
                                      bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil', takefocus=0)
        self.entry_port_parse.place(relx=0.47, rely=0.1, anchor=NW)
        self.entry_port_parse.bind("<FocusIn>", lambda e: self.focus_in_for_prompt(e, 'port', self.entry_port_parse))
        self.entry_port_parse.bind("<KeyRelease>", lambda e: self.focus_in_for_prompt(e, 'port', self.entry_port_parse))
        self.entry_port_parse.bind("<FocusOut>", self.focus_out_for_prompt)

        # LABEL VALID PORT PARSING
        self.lb_valid_port = Label(master=self.tab_2, text='', font=('Times', 9))
        self.lb_valid_port.place(relx=0.48, rely=0.14, anchor=NW)

        # BUTTON CHECK CONNECT
        self.btn_check_connect = Button(master=self.tab_2, text='Connect', font=('Comic Sans MC', 8, 'italic'),
                                        fg='black', bg='orange', activeforeground="blue", activebackground="pink",
                                        width=8, command=self.check_connect_ftp)
        self.btn_check_connect.place(relx=0.8, rely=0.095, anchor=NW)

        # LABEL LOGIN SERVER
        self.lb_login_ftp = Label(master=self.tab_2, text='Login:', font=('Arial', 10, 'italic'), fg='black')

        # ENTRY LOGIN SERVER
        self.entry_login_ftp = Entry(master=self.tab_2, width=10, bg='light grey', font=('Times', 13,), fg='purple')
        self.entry_login_ftp.bind("<FocusIn>", lambda e: self.focus_in_for_prompt(e, 'login', self.entry_login_ftp))
        self.entry_login_ftp.bind("<KeyRelease>", lambda e: self.focus_in_for_prompt(e, 'login', self.entry_login_ftp))
        self.entry_login_ftp.bind("<FocusOut>", self.focus_out_for_prompt)

        # LABEL PASSWORD SERVER
        self.lb_password_ftp = Label(master=self.tab_2, text='Password:', font=('Arial', 10, 'italic'), fg='black')

        # ENTRY PASSWORD SERVER
        self.entry_password_ftp = Entry(master=self.tab_2, width=10, bg='light grey', font=('Times', 13,), fg='purple',
                                        show='*')

        # RADIOBUTTON FOR ANONYMOUS LOGIN
        self.check_btn_anon = Checkbutton(master=self.tab_2, text='Anonymous', onvalue=True, offvalue=False,
                                          variable=self.selected_anon, font=2, activeforeground='yellow',
                                          command=lambda: self.disable_login())

        # BUTTON CHECK LOGIN
        self.btn_check_login = Button(master=self.tab_2, text='Login', font=('Comic Sans MC', 8, 'italic'),
                                      fg='black', bg='orange', activeforeground="blue", activebackground="pink",
                                      width=8, command=self.check_login_ftp)

        # LABEL PARAMETERS
        self.options_label_ftp = Label(master=self.tab_2, text='Data collection parameters',
                                       font=('Arial', 13, 'italic', 'bold'), fg='chocolate2')

        # RADIOBUTTON FOR OPTIONS
        rad_1 = Radiobutton(master=self.tab_2, text='All', value=1, variable=self.selected_op_rad_ftp,
                            font=2, activeforeground='yellow', command=lambda: self.frame_options_ftp.place_forget())
        rad_2 = Radiobutton(master=self.tab_2, text='Selectively', value=2, variable=self.selected_op_rad_ftp, font=2,
                            activeforeground='yellow',
                            command=lambda: self.frame_options_ftp.place(relx=0.07, rely=0.55, anchor=NW))
        self.rad_options_ftp.append(rad_1)
        self.rad_options_ftp.append(rad_2)

        # LABEL PATH TO SAVE
        self.lb_path_saving_ftp = Label(master=self.tab_2, text='Path to save the result',
                                        font=('Arial', 10, 'italic'), fg='black')

        # ENTRY PATH SAVE
        check_path_save_ftp = (self.root.register(self.is_valid_path_save_ftp), "%P")
        self.entry_path_save_ftp = Entry(master=self.tab_2, validate="key", validatecommand=check_path_save_ftp,
                                         width=34,
                                         bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil')

        # BUTTON FOR PATH SAVING
        photo_folder_save = PhotoImage(file=r"data/folder_save.png")
        photo_folder_save = photo_folder_save.subsample(16, 16)
        self.btn_folder_save_ftp = Button(master=self.tab_2, command=lambda: self.get_initial_path('save_ftp'),
                                          image=photo_folder_save, activebackground="pink", borderwidth=0)
        self.btn_folder_save_ftp.image = photo_folder_save

        # LABEL VALID PATH SAVING
        self.lb_valid_save_ftp = Label(master=self.tab_2, text='', font=('Times', 8))

        # CHECKBUTTON FOR OPTIONS
        create_frame_options(master_frame=self.frame_options_ftp, cb_options=self.cb_options_ftp)

        # BUTTON FOR START APP
        self.btn_start_ftp = Button(master=self.tab_2, text="Start parsing",
                                    font=('Comic Sans MC', 16, 'italic', 'bold'),
                                    command=self.start_app_ftp,
                                    activeforeground="blue", activebackground="pink", relief='groove',
                                    fg='coral', bg='green', bd=2, width=14)
        # some_relief = ['flat', 'raised', 'sunken', 'ridge', 'solid', 'groove']

    def display(self) -> None:
        self.root.update()
        self.root.mainloop()

    def on_closing(self) -> None:
        if messagebox.askokcancel("Exit", "Do you want to quit?"):
            self.ftp_service.close()
            self.root.destroy()
            exit()


if __name__ == '__main__':
    a = App()
    a.display()
