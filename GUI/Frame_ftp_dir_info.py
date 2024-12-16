from tkinter import *
from tkinter import messagebox, ttk
import socket
import time
from threading import Thread
from GUI.My_check_button import get_frame_options
from Backend_functions import Common_functions, Search_type_files_FTP
from GUI.GUI_common_functions import *
from Backend_functions.Work_with_ftp import ConnectionToFtp
from GUI.My_widget_prompts_for_Entry import MyWidgetPrompts
from GUI.My_progressbar import MyProgressBar
from data import Consts


class FrameFTPDirInfo(ttk.Frame):

    def __init__(self, master_frame: ttk.Notebook):
        super().__init__(master=master_frame)
        self.master_frame = master_frame
        # FTP
        self.ftp_service = ConnectionToFtp()
        # Elements Page FTP
        self.btn_reset_tab_2 = Button(master=self)
        self.entry_host_parse = ttk.Entry(master=self)
        self.lb_valid_host = ttk.Label(master=self)
        self.correct_host = False
        self.entry_port_parse = ttk.Entry(master=self)
        self.lb_valid_port = ttk.Label(master=self)
        self.correct_port = False
        self.connect_to_ftp = False
        self.btn_check_connect = Button(master=self)
        self.entry_password_ftp = Entry(master=self)
        self.lb_gif_host = Label(master=self)
        self.lb_gif_port = Label(master=self)
        self.selected_anon = BooleanVar()
        self.selected_anon.set(False)
        self.btn_check_login = Button(master=self)
        self.lb_gif_login = Label(master=self)
        self.lbl_initial_path_ftp = Label(master=self)
        self.lb_password_ftp = Label(master=self)
        self.entry_login_ftp = Entry(master=self)
        self.lb_gif_password = Label(master=self)
        self.lb_login_ftp = Label(master=self)
        self.check_btn_anon = Checkbutton(master=self)
        self.cmbx_path = ttk.Combobox(master=self)
        self.selected_op_rad_ftp = IntVar()
        self.selected_op_rad_ftp.set(0)
        self.rad_options_ftp = []
        self.cb_options_ftp = []
        self.options_label_ftp = Label(master=self)
        self.frame_options_ftp = LabelFrame(master=self, text="Options")
        self.lb_path_saving_ftp = Label(master=self)
        self.entry_path_save_ftp = Entry(master=self)
        self.btn_folder_save_ftp = Button(master=self)
        self.lb_valid_save_ftp = Label(master=self)
        self.correct_path_save_ftp = False
        self.btn_start_ftp = Button(master=self)
        # Storages
        self.tree_paths = []
        self.prompts_for_entry = MyWidgetPrompts(master_frame=self)

        self.add_objects()

    def add_objects(self) -> None:
        # TITLE FTP
        lb_title_ftp = Label(master=self, text=' DIR_INFO_FTP ', font=('Cooper Black', 18, 'italic'),
                             fg='magenta')
        lb_title_ftp.place(relx=0.5, rely=0.01, anchor=N)

        # BUTTON RESET PAGE 2
        self.btn_reset_tab_2 = Button(master=self, text='Reset', font=('Times', 12),
                                      fg='#A5260A', bg='#B5B8B1', bd=0, command=self.reset_frame)
        self.btn_reset_tab_2.place(relx=0.83, rely=0.02, anchor=NW)

        # LABEL HOST PARSING
        lb_host_parsing = Label(master=self, text='Host', font=('Arial', 10, 'italic'), fg='black')
        lb_host_parsing.place(relx=0.06, rely=0.06, anchor=NW)

        # ENTRY HOST PARSING
        check_host = (self.register(self.is_valid_host), "%P")
        self.entry_host_parse = Entry(master=self, validate="key", validatecommand=check_host, width=14,
                                      bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil', takefocus=0)
        self.entry_host_parse.place(relx=0.05, rely=0.1, anchor=NW)
        self.entry_host_parse.bind("<FocusIn>",
                                   lambda _: self.prompts_for_entry.focus_in_widget(key_prompt="host",
                                                                                    widget_entry=self.entry_host_parse
                                                                                    ))
        self.entry_host_parse.bind("<KeyRelease>",
                                   lambda _: self.prompts_for_entry.focus_in_widget(key_prompt="host",
                                                                                    widget_entry=self.entry_host_parse
                                                                                    ))
        self.entry_host_parse.bind("<FocusOut>", self.prompts_for_entry.focus_out_widget)

        # LABEL VALID HOST PARSING
        self.lb_valid_host = Label(master=self, text='', font=('Times', 9))
        self.lb_valid_host.place(relx=0.08, rely=0.14, anchor=NW)

        # LABEL PORT PARSING
        lb_port_parsing = Label(master=self, text='Port', font=('Arial', 10, 'italic'), fg='black')
        lb_port_parsing.place(relx=0.48, rely=0.06, anchor=NW)

        # ENTRY PORT PARSING
        check_port = (self.register(self.is_valid_port), "%P")
        self.entry_port_parse = Entry(master=self, validate="key", validatecommand=check_port, width=10,
                                      bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil', takefocus=0)
        self.entry_port_parse.place(relx=0.47, rely=0.1, anchor=NW)
        self.entry_port_parse.bind("<FocusIn>",
                                   lambda _: self.prompts_for_entry.focus_in_widget(key_prompt="port",
                                                                                    widget_entry=self.entry_port_parse
                                                                                    ))
        self.entry_port_parse.bind("<KeyRelease>",
                                   lambda _: self.prompts_for_entry.focus_in_widget(key_prompt="port",
                                                                                    widget_entry=self.entry_port_parse
                                                                                    ))
        self.entry_port_parse.bind("<FocusOut>", self.prompts_for_entry.focus_out_widget)

        # LABEL VALID PORT PARSING
        self.lb_valid_port = Label(master=self, text='', font=('Times', 9))
        self.lb_valid_port.place(relx=0.48, rely=0.14, anchor=NW)

        # BUTTON CHECK CONNECT
        self.btn_check_connect = Button(master=self, text='Connect', font=('Comic Sans MC', 8, 'italic'),
                                        fg='black', bg='orange', activeforeground="blue", activebackground="pink",
                                        width=8, command=self.check_connect_ftp)
        self.btn_check_connect.place(relx=0.8, rely=0.095, anchor=NW)

        # LABEL LOGIN SERVER
        self.lb_login_ftp = Label(master=self, text='Login:', font=('Arial', 10, 'italic'), fg='black')

        # ENTRY LOGIN SERVER
        self.entry_login_ftp = Entry(master=self, width=10, bg='light grey', font=('Times', 13,), fg='purple')
        self.entry_login_ftp.bind("<FocusIn>",
                                  lambda _: self.prompts_for_entry.focus_in_widget(key_prompt="login",
                                                                                   widget_entry=self.entry_login_ftp
                                                                                   ))
        self.entry_login_ftp.bind("<KeyRelease>",
                                  lambda _: self.prompts_for_entry.focus_in_widget(key_prompt="login",
                                                                                   widget_entry=self.entry_login_ftp
                                                                                   ))
        self.entry_login_ftp.bind("<FocusOut>", self.prompts_for_entry.focus_out_widget)

        # LABEL PASSWORD SERVER
        self.lb_password_ftp = Label(master=self, text='Password:', font=('Arial', 10, 'italic'), fg='black')

        # ENTRY PASSWORD SERVER
        self.entry_password_ftp = Entry(master=self, width=10, bg='light grey', font=('Times', 13,), fg='purple',
                                        show='*')

        # RADIOBUTTON FOR ANONYMOUS LOGIN
        self.check_btn_anon = Checkbutton(master=self, text='Anonymous', onvalue=True, offvalue=False,
                                          variable=self.selected_anon, font=2, activeforeground='yellow',
                                          command=lambda: self.disable_login())

        # BUTTON CHECK LOGIN
        self.btn_check_login = Button(master=self, text='Login', font=('Comic Sans MC', 8, 'italic'),
                                      fg='black', bg='orange', activeforeground="blue", activebackground="pink",
                                      width=8, command=self.check_login_ftp)

        # LABEL PARAMETERS
        self.options_label_ftp = Label(master=self, text='Data collection parameters',
                                       font=('Arial', 13, 'italic', 'bold'), fg='chocolate2')

        # RADIOBUTTON FOR OPTIONS
        rad_1 = Radiobutton(master=self, text='All', value=1, variable=self.selected_op_rad_ftp,
                            font=2, activeforeground='yellow', command=lambda: self.frame_options_ftp.place_forget())
        rad_2 = Radiobutton(master=self, text='Selectively', value=2, variable=self.selected_op_rad_ftp, font=2,
                            activeforeground='yellow',
                            command=lambda: self.frame_options_ftp.place(relx=0.07, rely=0.55, anchor=NW))
        self.rad_options_ftp.append(rad_1)
        self.rad_options_ftp.append(rad_2)

        # LABEL PATH TO SAVE
        self.lb_path_saving_ftp = Label(master=self, text='Path to save the result',
                                        font=('Arial', 10, 'italic'), fg='black')

        # ENTRY PATH SAVE
        check_path_save_ftp = (self.register(self.is_valid_path_save_ftp), "%P")
        self.entry_path_save_ftp = Entry(master=self, validate="key", validatecommand=check_path_save_ftp,
                                         width=34,
                                         bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil')

        # BUTTON FOR PATH SAVING
        photo_folder_save = PhotoImage(file=fr"{Consts.PATH_DATA_DIR}/folder_save.png")
        photo_folder_save = photo_folder_save.subsample(16, 16)
        self.btn_folder_save_ftp = Button(master=self,
                                          command=lambda: get_initial_path(mode='save_ftp',
                                                                           entry_path=self.entry_path_save_ftp),
                                          activebackground="pink", borderwidth=0, image=photo_folder_save)
        self.btn_folder_save_ftp.image = photo_folder_save

        # LABEL VALID PATH SAVING
        self.lb_valid_save_ftp = Label(master=self, text='', font=('Times', 8))

        # CHECKBUTTON FOR OPTIONS
        self.cb_options_ftp = get_frame_options(master_frame=self.frame_options_ftp,
                                                row_options_count=ROW_OPTIONS_COUNT,
                                                col_options_count=COL_OPTIONS_COUNT, option_names=LIST_OPTION_NAMES)

        # BUTTON FOR START APP
        self.btn_start_ftp = Button(master=self, text="Start parsing",
                                    font=('Comic Sans MC', 16, 'italic', 'bold'),
                                    command=self.start_app_ftp,
                                    activeforeground="blue", activebackground="pink", relief='groove',
                                    fg='coral', bg='green', bd=2, width=14)

    def is_valid_path_save_ftp(self, new_val: str) -> bool:
        if not new_val:
            self.lb_valid_save_ftp['text'] = ''
            self.correct_path_save_ftp = False
        elif os.path.exists(new_val):
            if os.path.isdir(new_val):
                self.lb_valid_save_ftp['text'] = 'Ok, the path is correct!'
                self.lb_valid_save_ftp['fg'] = 'green'
                self.correct_path_save_ftp = True
            else:
                self.lb_valid_save_ftp['text'] = "The path exists, but it's not a folder!"
                self.lb_valid_save_ftp['fg'] = 'darkorange'
                self.correct_path_save_ftp = False
        else:
            self.lb_valid_save_ftp['text'] = 'The path not exists!'
            self.lb_valid_save_ftp['fg'] = 'red'
            self.correct_path_save_ftp = False
        return True

    def reset_frame(self) -> None:
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
        self.update()

    def is_valid_host(self, new_val: str) -> bool:
        if not new_val:
            self.lb_valid_host['text'] = ''
            self.correct_host = False
        else:
            try:
                socket.inet_aton(new_val)
                if new_val.count('.') == 3:
                    self.lb_valid_host['text'] = 'Ok, the host is correct!'
                    self.lb_valid_host['fg'] = 'green'
                    self.correct_host = True
                else:
                    self.lb_valid_host['text'] = 'The host is not incorrect!'
                    self.lb_valid_host['fg'] = 'red'
                    self.correct_host = False
            except socket.error:
                self.lb_valid_host['text'] = 'The host is not incorrect!'
                self.lb_valid_host['fg'] = 'red'
                self.correct_host = False
        return True

    def is_valid_port(self, new_val: str) -> bool:
        if not new_val:
            self.lb_valid_port['text'] = ''
            self.correct_port = False
            return True
        elif new_val.isdigit() and len(new_val) < 6:
            self.lb_valid_port['text'] = 'The port is correct!'
            self.lb_valid_port['fg'] = 'green'
            self.correct_port = True
            return True
        else:
            return False

    def check_connect_ftp(self) -> None:
        if not self.correct_host:
            self.connect_to_ftp = False
            messagebox.showerror(title="Error", message="Enter the correct HOST to the parse device!")
            return
        if not self.correct_port:
            self.connect_to_ftp = False
            messagebox.showerror(title="Error", message="Enter the correct PORT to the parse device!")
            return
        host = self.entry_host_parse.get().strip()
        port = int(self.entry_port_parse.get())
        response, report = self.ftp_service.check_connect(host=host, port=port)
        Common_functions.overwrite_input_prompts(host=host, port=port)
        if response:
            messagebox.showinfo(title="Info", message=report)
            self.connect_to_ftp = True
            self.after(50, lambda _: self.display_gif(lb_gif=self.lb_gif_host), 0)
            self.after(400, lambda _: self.display_gif(lb_gif=self.lb_gif_port), 0)
            self.entry_host_parse['state'] = 'disabled'
            self.entry_port_parse['state'] = 'disabled'
            self.display_login_entry()
        else:
            self.connect_to_ftp = False
            messagebox.showerror(title="Error", message=report)

    def check_login_ftp(self) -> None:
        login = self.entry_login_ftp.get().strip()
        password = self.entry_password_ftp.get().strip()
        if not login and not password and not self.selected_anon.get():
            messagebox.showerror(title="Error", message="You must enter your username and password "
                                                        "or choose an anonymous login")
            return
        else:
            if self.selected_anon.get():
                response, report = self.ftp_service.check_login()
            else:
                response, report = self.ftp_service.check_login(user=login, password=password)
                Common_functions.overwrite_input_prompts(login=login, password=password)
            if response:
                messagebox.showinfo(title="Info", message=report)
                self.entry_login_ftp['state'] = 'disabled'
                self.entry_password_ftp['state'] = 'disabled'
                self.after(50, lambda _: self.display_gif(lb_gif=self.lb_gif_login), 0)
                self.after(400, lambda _: self.display_gif(lb_gif=self.lb_gif_password), 0)
                thread_1 = Thread(name='Thread-show_paths', target=self.show_paths_cmbx, daemon=True)
                thread_1.start()
            else:
                messagebox.showerror(title="Error", message=report)

    def display_gif(self, lb_gif: Label) -> None:
        match lb_gif:
            case self.lb_gif_host:
                self.lb_gif_host.place(relx=0.39, rely=0.1, anchor=NW)
            case self.lb_gif_port:
                self.lb_gif_port.place(relx=0.72, rely=0.1, anchor=NW)
            case self.lb_gif_login:
                self.lb_gif_login.place(relx=0.52, rely=0.2, anchor=NW)
            case self.lb_gif_password:
                self.lb_gif_password.place(relx=0.52, rely=0.25, anchor=NW)
            case _:
                print("Error case gif")

        frames = get_frame_list_gif(file=fr"{Consts.PATH_DATA_DIR}/check_mark.gif")
        size_gif = len(frames)
        photo = PhotoImage(file=fr"{Consts.PATH_DATA_DIR}/check_mark.gif").subsample(4, 4)
        count_secs = 3

        def update(index):
            frame = frames[index]
            if index == size_gif - 1:
                lb_gif.configure(image=photo)
                return
            index += 1
            lb_gif.configure(image=frame, bd=0, bg=self['bg'])
            self.after(int(count_secs * 1000 / size_gif), update, index)

        self.after(0, update, 0)

    def get_paths_cmbx(self) -> None:
        try:
            self.tree_paths = self.ftp_service.gen_ftp_walk()
        except Exception as ex:
            messagebox.showerror(title="Error", message=f'{ex} \n Try to connect again...')

    def show_paths_cmbx(self) -> None:
        thread_get_paths = Thread(name='Thread-get-tree', target=self.get_paths_cmbx, daemon=True)
        thread_get_paths.start()
        load_lbl = Label(master=self, text='Parsing ', font=('Arial', 14, 'italic'), fg='#B00000')
        load_lbl.place(relx=0.08, rely=0.33, anchor=NW)
        while thread_get_paths.is_alive():
            count_point = load_lbl['text'].count('.')
            load_lbl['text'] = f'Parsing{"." * ((count_point % 3) + 1)} '
            load_lbl.update()
            time.sleep(0.35)
        load_lbl.destroy()
        if self.tree_paths:
            values = []
            total_len, total_count = 0, 0
            for path, dir_names, filenames in self.tree_paths:
                values.append(path)
                total_len += len(path)
                total_count += 1
            average_length = int(total_len / total_count)
            self.lbl_initial_path_ftp = Label(master=self, text='Path for parsing: ',
                                              font=('Arial', 10, 'italic'), fg='black')
            self.lbl_initial_path_ftp.place(relx=0.02, rely=0.32, anchor=NW)
            self.cmbx_path = ttk.Combobox(master=self, values=values, width=average_length)
            self.cmbx_path.current(0)
            self.cmbx_path.place(relx=0.285, rely=0.325, anchor=NW)
            self.place_parameters_for_parse_ftp()
        else:
            messagebox.showerror(title="Error", message=f'There are no files in the current connection!')

    def disable_login(self) -> None:
        if self.selected_anon.get():
            self.entry_login_ftp['state'] = 'disabled'
            self.entry_password_ftp['state'] = 'disabled'
        else:
            self.entry_login_ftp['state'] = 'normal'
            self.entry_password_ftp['state'] = 'normal'

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

    def disable_objects_on_frame(self) -> None:
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
        self.update()

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
                self.disable_objects_on_frame()
                progress_bar = MyProgressBar(master_frame=self)
                progress_bar.progress_bar_place(rel_x=0.5, rel_y=0.85, in_anchor=N)
                progress_bar.label_step_place(rel_x=0.5, rel_y=0.8, in_anchor=N)
                report = Search_type_files_FTP.run_search_types(initial_path=self.cmbx_path.get(),
                                                                search_type_files=types_search_files,
                                                                progress_bar=progress_bar,
                                                                tree_paths=self.tree_paths,
                                                                path_for_save=path_for_save)
                messagebox.showinfo(title="Feedback report", message=report)
                progress_bar.destroy()
                self.reset_frame()
            else:
                messagebox.showwarning(title="Warning", message="You need to select the search parameters!")
                return
