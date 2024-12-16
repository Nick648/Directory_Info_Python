from tkinter import Tk, filedialog, Entry, END, PhotoImage, TclError
import os

# CONSTs
ROW_OPTIONS_COUNT = 4
COL_OPTIONS_COUNT = 3

# FILE TYPES
MEDIA_FILES = ["jpg", "jpeg", "png", "bmp", "dcm", "gif", "tif", "ico", "webp", "raw", "svg", "img"]
VIDEO_FILES = ["mp4", "mov", "avi", "mpeg", "webm", "vob", "mkv"]
AUDIO_FILES = ["mp3", "mp2", "wav", "mpc", "wma", "aac", "midi"]
DOCUMENT_FILES = ["pdf", "wps", "wpd", "txt", "log", "json", "xml", "ini", "yaml"]
OFFICE_FILES = ["doc", "docx", "ppt", "pptx", "xls", "xlsx", "odt", "xpc"]
DATABASE_FILES = ["pdb", "dbf", "db", "mdb", "sql", "dat"]
ARCHIVE_FILES = ["zip", "zipx", "gzip", "rar", "7z", "arj", "tar", "apk", "iso"]
WEBSITE_FILES = ["html", "htm", "xhtml", "php", "js", "apk", "css", "kml"]
EXECUTABLE_FILES = ["exe", "com", "bat", "torrent", "iso"]
PROGRAM_FILES = ["cs", "cpp", "h", "cc", "cp", "c++", "h++", "html", "css", "js", "php", "cp",
                 "cps", "pas", "py", "ini", "cfg", "java", "dfm", "dfm", "dfm", "ini", "yaml"]
LIST_OPTION_NAMES = ['Media files', 'Audio files', 'Video files',
                     'Document files', 'Office files', 'Database files',
                     'Archive files', 'Website files', 'Executable files',
                     'Program files']


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


def get_initial_path(mode: str, entry_path: Entry) -> None:
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
        entry_path.delete(0, END)
        entry_path.insert(0, initial_path)


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
