import os.path
from tkinter import *
from tkinter import ttk
from GUI.GUI_common_functions import get_size_monitor, get_path_file_dir

# CONSTs
APP_WIDTH, APP_HEIGHT = 500, 350


class ExceptionTreeView(Toplevel):
    def __init__(self, master: ttk.Frame, hide: bool = True):
        super().__init__(master=master)
        if hide:
            self.withdraw()
        self.set_win_configurations()
        # Elements
        self.tree = ttk.Treeview(self, show="headings", columns=("Paths",), selectmode="browse")
        self.set_tree_configurations()
        self.btn_add_path_dir = Button(master=self)
        self.btn_add_path_file = Button(master=self)
        self.btn_del_path = Button(master=self)
        self.add_objects()

    def set_win_configurations(self) -> None:
        self.title("Exception dirs/files")
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        self.resizable(width=False, height=False)
        win_width, win_height = get_size_monitor()
        offset_width, offset_height = win_width // 2 - APP_WIDTH // 2 - 50, win_height // 2 - APP_HEIGHT // 2 - 50
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{offset_width}+{offset_height}")
        self.configure(background="#F5F5DC")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_tree_configurations(self) -> None:
        self.tree.column("Paths", width=550, anchor="w", stretch=True)
        self.tree.heading("Paths", text="Paths")
        self.tree.bind("<<TreeviewSelect>>", lambda _: self.activate_del_btn())
        self.tree.bind("<Delete>", lambda _: self.delete_data())

    def add_objects(self) -> None:
        # SCROLLBARS
        ysb = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.pack(side=RIGHT, fill=Y, anchor=E)

        xsb = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=xsb.set)
        self.tree.pack(side=TOP, fill=X, anchor=W, padx=1)
        xsb.pack(side=TOP, fill=X, anchor=N)

        # BUTTON FOR ADD PATH DIR
        self.btn_add_path_dir = Button(master=self, text="Add folder", font=('Comic Sans MC', 14, 'italic', 'bold'),
                                       command=lambda: self.add_path("dir"),
                                       activeforeground="blue", activebackground="pink", relief='groove',
                                       fg='#9966CC', bg='#B5B8B1', bd=2, width=10, height=1)
        self.btn_add_path_dir.pack(side=LEFT, anchor=NW, padx=30, pady=20)

        # BUTTON FOR ADD PATH FILE
        self.btn_add_path_file = Button(master=self, text="Add file", font=('Comic Sans MC', 14, 'italic', 'bold'),
                                        command=lambda: self.add_path("file"),
                                        activeforeground="blue", activebackground="pink", relief='groove',
                                        fg='#9966CC', bg='#B5B8B1', bd=2, width=10, height=1)
        self.btn_add_path_file.pack(side=RIGHT, anchor=NE, padx=30, pady=20)

        # BUTTON FOR DELETE PATH
        self.btn_del_path = Button(master=self, text="Delete path", font=('Comic Sans MC', 12, 'italic', 'bold'),
                                   command=lambda: self.delete_data(),
                                   activeforeground="blue", activebackground="pink",
                                   fg='#AB274F', bg='#B5B8B1', bd=2, width=12, height=1)
        self.btn_del_path.pack(side=BOTTOM, anchor=N, pady=10)
        self.btn_del_path['state'] = "disabled"

    def add_path(self, mode: str):
        path = get_path_file_dir(mode=mode, parent=self)
        prev_data = self.get_all_data_tree()
        if path and path not in prev_data:
            if mode == "dir":
                self.tree.insert("", END, text="D", tags="dir", values=(path,))
            elif mode == "file":
                filepath, filename = os.path.split(path)
                if filename not in self.get_exception_files():
                    self.tree.insert("", END, text="F", tags="file", values=(filename,))

    def delete_data(self):
        if self.tree.focus():
            self.tree.delete(self.tree.focus())
            self.btn_del_path['state'] = "disabled"
        else:
            self.btn_del_path['state'] = "disabled"

    def activate_del_btn(self) -> None:
        self.btn_del_path['state'] = "normal"

    def get_all_data_tree(self) -> list[str]:
        all_paths = []
        for k in self.tree.get_children(""):
            all_paths.append(self.tree.set(k, 0))
        return all_paths

    def get_exception_files(self) -> list[str]:
        all_paths = []
        for k in self.tree.get_children(""):
            if self.tree.item(k)["tags"][0] == "file":
                all_paths.append(self.tree.set(k, 0))
        return all_paths

    def get_exception_dirs(self) -> list[str]:
        all_paths = []
        for k in self.tree.get_children(""):
            if self.tree.item(k)["tags"][0] == "dir":
                all_paths.append(self.tree.set(k, 0))
        return all_paths

    def display(self) -> None:
        self.deiconify()
        self.update()
        self.grab_set()

    def on_closing(self) -> None:
        self.withdraw()
        self.grab_release()


if __name__ == "__main__":
    app = ExceptionTreeView(Frame(), hide=False)
    app.mainloop()
