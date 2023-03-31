import os
import time
from art import tprint
from tkinter import *
import tkinter.filedialog as fd
import json
import datetime
from progress.bar import IncrementalBar

from colorama import Fore, Style, init

init(autoreset=True)  # Not need RESET at the end massage

# Const module colorama
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
RESET = Style.RESET_ALL

# Consts for time and date
today = datetime.datetime.today()
date_y, date_m, date_d = today.year, today.month, today.day
# time_h, time_m, time_s = today.hour, today.minute, today.second

# Name of directory
DESKTOP_DIR = os.path.expanduser('~') + r'\Desktop'  # Full path to the desktop
CUR_DIR_FILE = os.path.abspath(__file__)  # Full path to the file, with name file.py
CUR_DIR = os.path.dirname(os.path.abspath(__file__))  # Without name file.py
NAME_DIR = f'File Search {date_d}_{date_m}_{date_y}'
WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)

# Files to search for
SEARCH_FILES = [".jpg", ".jpeg", ".png", ".mov", ".mp4", ".mp3"]
PATHS_FILES_DICT = {}
TOTAL_COUNT_FILES = {}


def error_out(text: str) -> None:
    """ Red text output """
    print(RED + text, sep='')


def done_out(text: str) -> None:
    """ Green text output """
    print(GREEN + text, sep='')


def yellow_out(text: str) -> None:
    """ Yellow text output """
    print(YELLOW + text, sep='')


def exi_t() -> None:
    """ Exiting the program """
    text = '\nThank you for using our program!\nHave a nice day!\n'
    for sym in text:
        print(GREEN + sym, end='')
        time.sleep(0.02)
    time.sleep(2)
    exit()


def create_dir() -> None:
    """ Creating a folder for files """
    global WAY_DIR, NAME_DIR

    if not os.path.exists(WAY_DIR):  # Creating a folder for files
        os.mkdir(WAY_DIR)

    # If the folder is created, an additional one will be created with the version specified
    else:
        version = 1
        while os.path.exists(WAY_DIR):
            NAME_DIR = f'File Search {date_d}_{date_m}_{date_y} version=={version}'
            WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)
            version += 1
        os.mkdir(WAY_DIR)


def write_data_json(file_name: str, dump_dict: dict) -> None:
    """ Writes the dictionary to a json file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.json")
    with open(file=file_path, mode="w", encoding="utf-8") as write_file:
        json.dump(dump_dict, write_file, ensure_ascii=False, indent=4)
    print(f"File: {file_path} -> {GREEN}was created!")


def write_data_html(file_name: str, write_text: str) -> None:
    """ Writes the text to a html file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.html")
    with open(file=file_path, mode="w", encoding="utf-8") as html_file:
        html_file.write(write_text)
    print(f"File: {file_path} -> {GREEN}was created!")


def path_tree_to_html_str(initial_path: str, dict_paths: dict) -> str:
    tree_html = f"<font color='green' size=7>Tree of found paths</font><br>"
    tree_html += f"<font size=5>"
    tree_html += f"&emsp;Initial path:&nbsp;<font color=Magenta>{initial_path}</font><br><br>"
    for path in dict_paths:
        # str_html += f"&emsp;&emsp;<font color=Magenta>Current path:&nbsp;{path}</font><br>"
        dif_level = dict_paths[path]["Level"]
        tree_html += f"{'&emsp;' * dif_level * 2}{path}<br>"
    tree_html += f"</font><br><br>"
    return tree_html


def dict_total_info_to_str_html(dict_paths: dict) -> str:
    str_html = f"<font color='green' size=7>Information about found files</font><br><br>"
    str_html += f"<font size=5>"
    for path in dict_paths:
        str_html += f"&emsp;&emsp;<font color=Magenta>Current path:&nbsp;{path}</font><br>"
        for key_info in dict_paths[path]:
            if key_info == "Formats (count)":
                str_html += f"{key_info}:&nbsp;<br>"
                for key_format in dict_paths[path][key_info]:
                    str_html += f"&emsp;&emsp;{key_format:5}:&nbsp;{dict_paths[path][key_info][key_format]:5};<br>"
            else:
                str_html += f"{key_info}:&nbsp;{dict_paths[path][key_info]}<br>"
        str_html += f"<font color=DarkOrange>{'*' * 150}</font><br>"
    str_html += f"</font><br><br>"
    return str_html


def total_count_types_to_str_html(dict_types: dict) -> str:
    str_html = f"<font color='green' size=7>Total number of file types</font><br><br>"
    str_html += f"<font size=5>"
    str_html += f"<b>&emsp;&emsp;{'Type':5}:&nbsp;{'Count':5};</b><br>"
    for key_type in dict_types:
        str_html += f"&emsp;&emsp;{key_type:5}:&nbsp;{dict_types[key_type]:5};<br>"
    str_html += f"</font><br><br>"
    return str_html


def check_path(dir_path: str, filenames: list[str], dif_level: int) -> bool:
    global PATHS_FILES_DICT, TOTAL_COUNT_FILES
    dict_found_files = {}
    total_found_files = 0
    list_filenames = []
    for file in filenames:
        for search_file in SEARCH_FILES:
            if search_file.lower() in file.lower():
                total_found_files += 1
                list_filenames.append(file)
                if search_file.lower() in dict_found_files:
                    dict_found_files[search_file.lower()] += 1
                else:
                    dict_found_files[search_file.lower()] = 1
    if total_found_files:
        info_found_files = {"Level": dif_level,
                            "List of found files": list_filenames,
                            "Total found files": total_found_files,
                            "Number of formats": len(dict_found_files),
                            "Formats (count)": dict_found_files
                            }
        PATHS_FILES_DICT[dir_path] = info_found_files

        for type_file in dict_found_files:
            if type_file in TOTAL_COUNT_FILES:
                TOTAL_COUNT_FILES[type_file] += dict_found_files[type_file]
            else:
                TOTAL_COUNT_FILES[type_file] = dict_found_files[type_file]

        return True
    return False


def find_paths(initial_path: str) -> None:
    """ Main algorithm of program """
    max_val = 0
    for _ in os.walk(initial_path):
        max_val += 1
    bar = IncrementalBar('Progress', max=max_val)
    lower_level = initial_path.count("\\")
    for dir_path, dir_names, filenames in os.walk(initial_path):  # , topdown=False
        bar.next()
        # print(f"{dir_path=}; {dir_names=}; {filenames=}")
        dif_level = dir_path.count("\\") - lower_level
        check_path(dir_path, filenames, dif_level)
        time.sleep(0.01)
    if PATHS_FILES_DICT:
        create_dir()
        sorted_format_files = dict(sorted(TOTAL_COUNT_FILES.items(), key=lambda x: x[1], reverse=True))
        write_data_json("Info found files", PATHS_FILES_DICT)
        write_data_json("Total number of file types", sorted_format_files)

        str_html = dict_total_info_to_str_html(PATHS_FILES_DICT)
        write_data_html("Info found files", str_html)

        total_info_str_html = path_tree_to_html_str(initial_path, PATHS_FILES_DICT)
        total_info_str_html += total_count_types_to_str_html(sorted_format_files)
        write_data_html("Total number of file types", total_info_str_html)

    else:
        yellow_out("There are no required files in the current directory!")


def main():
    """ Start program """

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    initial_path = fd.askdirectory(title="Select a folder", initialdir="/")

    if os.path.exists(initial_path):
        print(f"Path: '{initial_path}' status: {GREEN}OK\n")
        find_paths(initial_path)
    else:
        error_out(f"Path: '{initial_path}' status: Not found")
    exi_t()


if __name__ == '__main__':  # Program entry point
    hello = YELLOW + " Program for finding paths with files " + RESET
    print("\n", "{:*^80}".format(hello), "\n", sep='')
    tprint("Paths_Find")
    time.sleep(1)
    print(f'Current Working Directory is: {os.getcwd()}\n')
    main()
