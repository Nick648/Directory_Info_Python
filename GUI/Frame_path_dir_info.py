from tkinter import *
from tkinter import messagebox
from GUI.My_check_button import get_frame_options
from Backend_functions import Total_info_files_dir, Search_type_files
from GUI.GUI_common_functions import *
from data import Consts


class FramePathDirInfo(ttk.Frame):

    def __init__(self, master_frame: ttk.Notebook):
        super().__init__(master=master_frame)
        self.master_frame = master_frame
        # Elements Page Path
        self.entry_path_parse = Entry(master=self)
        self.btn_folder_parse = Button(master=self)
        self.lb_valid_parse = Label(master=self)
        self.correct_path_parse = False
        self.entry_path_save = Entry(master=self)
        self.btn_folder_save = Button(master=self)
        self.lb_valid_save = Label(master=self)
        self.correct_path_save = False
        self.selected_op_rad = IntVar()
        self.rad_options = []
        self.frame_options = LabelFrame(master=self, text="Options")
        self.cb_options = []
        self.btn_start = Button(master=self)
        self.add_objects()

    def add_objects(self) -> None:
        # TITLE PC
        lb_title = Label(master=self, text=' DIR_INFO_PC ', font=('Cooper Black', 18, 'italic'), fg='magenta')
        lb_title.place(relx=0.5, rely=0.01, anchor=N)

        # LABEL PATH FOR PARSING
        lb_path_parsing = Label(master=self, text='Path for parsing', font=('Arial', 10, 'italic'), fg='black')
        lb_path_parsing.place(relx=0.06, rely=0.06, anchor=NW)

        # ENTRY PATH PARSING
        check_path_parse = (self.register(self.is_valid_path_parse), "%P")
        self.entry_path_parse = Entry(master=self, validate="key", validatecommand=check_path_parse, width=34,
                                      bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil')
        self.entry_path_parse.place(relx=0.05, rely=0.1, anchor=NW)

        # BUTTON FOR PATH PARSING
        photo_folder_load = PhotoImage(file=fr"{Consts.PATH_DATA_DIR}/folder_load.png")  # icon button
        photo_folder_load = photo_folder_load.subsample(15, 15)  # photo size reduction (less)
        self.btn_folder_parse = Button(master=self,
                                       command=lambda: get_initial_path(mode='parse', entry_path=self.entry_path_parse),
                                       image=photo_folder_load, activebackground="pink", borderwidth=0)
        self.btn_folder_parse.image = photo_folder_load
        self.btn_folder_parse.place(relx=0.865, rely=0.09, anchor=NW)

        # LABEL VALID PATH PARSING
        self.lb_valid_parse = Label(master=self, text='', font=('Times', 9))
        self.lb_valid_parse.place(relx=0.1, rely=0.14, anchor=NW)

        # LABEL PATH TO SAVE
        lb_path_saving = Label(master=self, text='Path to save the result',
                               font=('Arial', 10, 'italic'), fg='black')
        lb_path_saving.place(relx=0.06, rely=0.18, anchor=NW)

        # ENTRY PATH SAVE
        check_path_save = (self.register(self.is_valid_path_save), "%P")
        self.entry_path_save = Entry(master=self, validate="key", validatecommand=check_path_save, width=34,
                                     bg='light grey', font=('Times', 13,), fg='purple', cursor='pencil')
        self.entry_path_save.place(relx=0.05, rely=0.22, anchor=NW)

        # BUTTON FOR PATH SAVING
        photo_folder_save = PhotoImage(file=fr"{Consts.PATH_DATA_DIR}/folder_save.png")
        photo_folder_save = photo_folder_save.subsample(16, 16)
        self.btn_folder_save = Button(master=self,
                                      command=lambda: get_initial_path(mode='save', entry_path=self.entry_path_save),
                                      image=photo_folder_save, activebackground="pink", borderwidth=0)
        self.btn_folder_save.image = photo_folder_save
        self.btn_folder_save.place(relx=0.865, rely=0.205, anchor=NW)

        # LABEL VALID PATH SAVING
        self.lb_valid_save = Label(master=self, text='', font=('Times', 9))
        self.lb_valid_save.place(relx=0.1, rely=0.26, anchor=NW)

        # LABEL PARAMETERS
        options_label = Label(master=self, text='Data collection parameters',
                              font=('Arial', 14, 'italic', 'bold'), fg='chocolate2')
        options_label.place(relx=0.5, rely=0.3, anchor=N)

        # RADIOBUTTON FOR OPTIONS
        self.selected_op_rad = IntVar()
        self.selected_op_rad.set(0)
        rad_1 = Radiobutton(master=self, text='All', value=1, variable=self.selected_op_rad,
                            font=2, activeforeground='yellow', command=lambda: self.frame_options.place_forget())
        rad_2 = Radiobutton(master=self, text='Selectively', value=2, variable=self.selected_op_rad, font=2,
                            activeforeground='yellow',
                            command=lambda: self.frame_options.place(relx=0.07, rely=0.4, anchor=NW))
        self.rad_options.append(rad_1)
        self.rad_options.append(rad_2)
        rad_1.place(relx=0.3, rely=0.345, anchor=N)
        rad_2.place(relx=0.7, rely=0.345, anchor=N)

        # CHECKBUTTON FOR OPTIONS
        self.cb_options = get_frame_options(master_frame=self.frame_options, row_options_count=ROW_OPTIONS_COUNT,
                                            col_options_count=COL_OPTIONS_COUNT, option_names=LIST_OPTION_NAMES)

        # BUTTON FOR START APP
        self.btn_start = Button(master=self, text="Start parsing", font=('Comic Sans MC', 16, 'italic', 'bold'),
                                command=self.start_app_path,
                                activeforeground="blue", activebackground="pink", relief='groove',
                                fg='coral', bg='green', bd=2, width=14, height=2)
        # some_relief = ['flat', 'raised', 'sunken', 'ridge', 'solid', 'groove']
        self.btn_start.place(relx=0.5, rely=0.85, anchor=N)

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

    def disable_objects_on_frame(self) -> None:
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
        self.update()

    def activate_object_on_frame(self) -> None:
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
        self.update()

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
            self.disable_objects_on_frame()
            progress_bar = ttk.Progressbar(master=self, orient="horizontal", length=170, value=0)
            progress_bar.place(relx=0.5, rely=0.78, anchor=N)
            lb_step = Label(master=self, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
            lb_step.place(relx=0.5, rely=0.72, anchor=N)
            report = Total_info_files_dir.run_total_search(initial_path=self.entry_path_parse.get(),
                                                           progress_bar=progress_bar, lb_step=lb_step,
                                                           path_for_save=path_for_save)
            messagebox.showinfo(title="Feedback report", message=report)
            progress_bar.destroy()
            lb_step.destroy()
            self.activate_object_on_frame()

        if self.selected_op_rad.get() == 2:  # Search type files
            types_search_files = []
            for cb_item in self.cb_options:
                if cb_item.var_select.get():
                    name_cb = cb_item.title.replace(' ', '_').upper()
                    for type_file in globals()[name_cb]:  # accessing a variable via a string
                        types_search_files.append('.' + type_file.lower())
            if types_search_files:
                self.disable_objects_on_frame()
                progress_bar = ttk.Progressbar(master=self, orient="horizontal", length=170, value=0)
                progress_bar.place(relx=0.5, rely=0.78, anchor=N)
                lb_step = Label(master=self, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
                lb_step.place(relx=0.5, rely=0.73, anchor=N)
                report = Search_type_files.run_search_types(initial_path=self.entry_path_parse.get(),
                                                            search_type_files=types_search_files,
                                                            progress_bar=progress_bar, lb_step=lb_step,
                                                            path_for_save=path_for_save)
                messagebox.showinfo(title="Feedback report", message=report)
                progress_bar.destroy()
                lb_step.destroy()
                self.activate_object_on_frame()
            else:
                messagebox.showwarning(title="Warning", message="You need to select the search parameters!")
                return
