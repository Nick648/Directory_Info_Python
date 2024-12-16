from tkinter import *
from tkinter import messagebox, ttk
from GUI.GUI_common_functions import get_size_monitor
from GUI.Frame_path_dir_info import FramePathDirInfo
from GUI.Frame_ftp_dir_info import FrameFTPDirInfo
from data import Consts

# CONSTs
APP_WIDTH, APP_HEIGHT = 400, 600


class DirectoryInfoApp:
    """The main class of the application, which describes all the GUI elements."""

    def __init__(self):
        # Main window
        self.root = Tk()
        # Tabs/Pages
        tab_control = ttk.Notebook(self.root)
        self.tab_1 = FramePathDirInfo(master_frame=tab_control)
        self.tab_2 = FrameFTPDirInfo(master_frame=tab_control)
        tab_control.add(self.tab_1, text='Use path')
        tab_control.add(self.tab_2, text='Use FTP')
        tab_control.pack(expand=1, fill='both')
        # Creating another configurations
        self.set_options_window()

    def set_options_window(self) -> None:
        self.set_sizes_and_position()
        self.set_configures()

    def set_sizes_and_position(self) -> None:
        self.root.resizable(width=False, height=False)
        win_width, win_height = get_size_monitor()
        offset_width, offset_height = win_width // 2 - APP_WIDTH // 2, win_height // 2 - APP_HEIGHT // 2
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{offset_width}+{offset_height}")

    def set_configures(self) -> None:
        self.root.title("Directory Info")
        self.root.iconbitmap(default=fr"{Consts.PATH_DATA_DIR}/Open-folder-search.ico")
        # self.root.configure(background="grey")
        # self.root.wm_attributes('-transparentcolor', self.root['bg'])  # Прозрачное приложение!
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add event for close window

    def display(self) -> None:
        self.root.update()
        self.root.mainloop()

    def on_closing(self) -> None:
        if messagebox.askokcancel("Exit", "Do you want to quit?"):
            self.root.destroy()
            exit()


if __name__ == '__main__':
    a = DirectoryInfoApp()
    a.display()
