import os
import time
from art import tprint
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd
import json
import datetime

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
NAME_DIR = f'Directory Info {date_d}_{date_m}_{date_y}'
WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)


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
            NAME_DIR = f'Directory Info {date_d}_{date_m}_{date_y} version=={version}'
            WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)
            version += 1
        os.mkdir(WAY_DIR)


def write_data_json(file_name: str, dump_dict: dict) -> None:
    """ Writes the dictionary to a json file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.json")
    with open(file=file_path, mode="w", encoding="utf-8") as write_file:
        json.dump(dump_dict, write_file, ensure_ascii=False, indent=5)
    print(f"File: {file_path} {GREEN}was created!")


def write_data_txt(file_name: str, write_text: str) -> None:
    """ Writes the text to a txt file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.txt")
    with open(file=file_path, mode="w", encoding="utf-8") as txt_file:
        txt_file.write(write_text)
    print(f"File: {file_path} {GREEN}was created!")


def write_data_html(file_name: str, write_text: str) -> None:
    """ Writes the text to a html file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.html")
    with open(file=file_path, mode="w", encoding="utf-8") as html_file:
        html_file.write(write_text)
    print(f"File: {file_path} {GREEN}was created!")


def write_dict_info_paths_to_html(file_name: str, dict_paths: dict) -> None:
    str_html = f"<font color='green' size=7>{file_name}</font><br><br>"
    str_html += f"<font size=4>"
    for path in dict_paths:
        str_html += f"&emsp;&emsp;<font color=Magenta>Current path:&nbsp;{path}</font><br>"
        for key_info in dict_paths[path]:
            if "Number of" in key_info:
                str_html += f"<font color=DarkGreen>{key_info}:&nbsp;{dict_paths[path][key_info]}</font><br>"
            else:
                str_html += f"{key_info}:&nbsp;{dict_paths[path][key_info]}<br>"
        str_html += f"<font color=DarkOrange size=5>{'*' * 150}</font><br>"
    write_data_html(file_name, str_html)


def write_dict_total_info_path_to_html(file_name: str, dict_path_info: dict) -> None:
    str_html = f"<font color='green' size=7>{file_name}</font><br><br>"
    str_html += f"<font size=5>"
    for key_info in dict_path_info:
        if key_info == "Initial path":
            str_html += f"&emsp;{key_info}:&nbsp;<font color=Magenta>{dict_path_info[key_info]}</font><br>"
        elif key_info == "Formats (count)":
            str_html += f"{key_info}:&nbsp;<br>"
            for key_format in dict_path_info[key_info]:
                str_html += f"&emsp;&emsp;{key_format:5}:&nbsp;{dict_path_info[key_info][key_format]:7}<br>"
        else:
            str_html += f"{key_info}:&nbsp;{dict_path_info[key_info]}<br>"
    str_html += f"</font><br>"
    write_data_html(file_name, str_html)


def display_tree_dir(initial_path: str, size_dirs: dict) -> None:
    """ Output of the directory tree and percent size """

    tree_str = f"Output of the directory tree and their percentage of the total size:\n" \
               f"P.S. In parentheses, the size of all subfolders relative to the main directory is indicated.\n\n"

    tree_html = f"<font color='green' size=7>Directory tree</font><br>" \
                f"<font color='DarkOrange' size=5.5>Output of the directory tree and their percentage of the total size:" \
                f"<br>" \
                f"P.S. In parentheses, the size of all subfolders relative to the main directory is indicated." \
                f"<br><br></font>"
    tree_html += f"<font size=5>"

    # done_out('\nOutput of the directory tree and their percentage of the total size:')
    # done_out('P.S. In parentheses, the size of all subfolders relative to the main directory is indicated.\n')

    # Combining directory sizes into a tuple:
    for path, size in size_dirs.items():
        if path == initial_path:
            continue
        t_size = 0
        for item in size_dirs:
            if item != path and path in item:
                t_size += size_dirs[item]
        if t_size:
            size_dirs[path] = (size, size + t_size)

    max_size_dir, min_size_dir = 0, size_dirs[initial_path]
    max_size_path, min_size_path = "", initial_path
    lower_level = initial_path.count("\\")
    for dir_path, size_dir in size_dirs.items():
        dif_level = dir_path.count("\\") - lower_level
        if dif_level > 0:
            indent = '\t' * dif_level
            if isinstance(size_dir, tuple):
                if size_dir[1] > max_size_dir:
                    max_size_dir = size_dir[1]
                    max_size_path = dir_path
                if size_dir[1] < min_size_dir:
                    min_size_dir = size_dir[1]
                    min_size_path = dir_path

                perc_size = "{:.3f}".format(size_dir[0] / size_dirs[initial_path] * 100) + '%'
                common_perc_size = "{:.2f}".format(size_dir[1] / size_dirs[initial_path] * 100) + '%'
                # print(f'{indent}{dir_path}  ->  {YELLOW + perc_size}  ({YELLOW + common_perc_size})')

                tree_str += f"{indent}{dir_path}  ->  {perc_size}  ({common_perc_size})\n"
                tree_html += f"{'&emsp;' * dif_level * 2}{dir_path}&emsp;->&emsp;{perc_size}&emsp;" \
                             f"<font color='Chocolate'>({common_perc_size})</font><br>"
                continue

            if size_dir > max_size_dir:
                max_size_dir = size_dir
                max_size_path = dir_path
            if size_dir < min_size_dir:
                min_size_dir = size_dir
                min_size_path = dir_path
            perc_size = "{:.3f}".format(size_dir / size_dirs[initial_path] * 100) + '%'
            # print(f'{indent}{dir_path}  ->  {YELLOW + perc_size}')

            tree_str += f"{indent}{dir_path}  ->  {perc_size}\n"
            tree_html += f"{'&emsp;' * dif_level * 2}{dir_path}&emsp;->&emsp;{perc_size}<br>"
        else:
            # print(dir_path)
            tree_str += f"{dir_path}\n"
            tree_html += f"<font color='magenta'>{dir_path}</font><br>"
    tree_html += f"</font>"
    try:
        max_perc_size = "{:.3f}".format(max_size_dir / size_dirs[initial_path] * 100) + '%'
        min_perc_size = "{:.3f}".format(min_size_dir / size_dirs[initial_path] * 100) + '%'
        str_max_size_dir, str_min_size_dir = get_max_str_size(max_size_dir), get_max_str_size(min_size_dir)

        max_file = get_max_file(max_size_path)
        # print(f'\nMaximum directory size: {max_size_path} = {str_max_size_dir}  ->  {YELLOW + max_perc_size}')

        tree_str += f"\n\nMaximum directory size: {max_size_path} = {str_max_size_dir}  ->  {max_perc_size}\n"
        tree_html += f"<font size=5>"
        tree_html += f"<br><br>Maximum directory size: {max_size_path} = {str_max_size_dir}&emsp;->&emsp;" \
                     f"<font color='purple'>{max_perc_size}</font><br>"
        if max_file:
            path_max_file, size_max_file = max_file
            max_perc_size_file = "{:.3f}".format(size_max_file / max_size_dir * 100) + '%'
            # print(f"\tMaximum file size: {path_max_file} = {get_max_str_size(size_max_file)}  ->  "
            #       f"{YELLOW}In folder {max_perc_size_file}")

            tree_str += f"\tMaximum file size: {path_max_file} = {get_max_str_size(size_max_file)}  ->  " \
                        f"In folder {max_perc_size_file}\n"
            tree_html += f"&emsp;&emsp;Maximum file size: {path_max_file} = " \
                         f"{get_max_str_size(size_max_file)}&emsp;->&emsp;" \
                         f"<font color='purple'>In folder {max_perc_size_file}</font><br>"

        # print(f'Minimum directory size: {min_size_path} = {str_min_size_dir}  ->  {YELLOW + min_perc_size}')
        tree_str += f"Minimum directory size: {min_size_path} = {str_min_size_dir}  ->  {min_perc_size}\n"
        tree_html += f"Minimum directory size: {min_size_path} = {str_min_size_dir}&emsp;->&emsp;" \
                     f"<font color='purple'>{min_perc_size}</font><br>"
        tree_html += f"</font>"
    except ZeroDivisionError:
        pass

    write_data_txt("Directory tree", tree_str)
    write_data_html("Directory tree", tree_html)


def get_max_file(path_with_max_file: str):
    size_max_file, path_max_file = 0, ""
    for dir_path, dir_names, filenames in os.walk(path_with_max_file):
        for name in filenames:
            path_filename = os.path.join(dir_path, name)
            size_cur_file = os.path.getsize(path_filename)
            if size_cur_file > size_max_file:
                size_max_file = size_cur_file
                path_max_file = path_filename
    if size_max_file:
        return path_max_file, size_max_file
    else:
        return None


def get_max_str_size(size_bytes: int) -> str:
    """
    Return str of max format of size
    :param size_bytes: int
    :return: str of max size
    """
    if size_bytes // 1024 == 0:
        size_bytes = "{:.3f}".format(size_bytes)
        return f'{size_bytes} bytes'
    size_kilobytes = size_bytes / 1024
    if size_kilobytes // 1024 == 0:
        size_kilobytes = "{:.3f}".format(size_kilobytes)
        return f'{size_kilobytes} KB'
    size_megabytes = size_kilobytes / 1024
    if size_megabytes // 1024 == 0:
        size_megabytes = "{:.3f}".format(size_megabytes)
        return f'{size_megabytes} MB'

    size_gigabytes = size_megabytes / 1024
    size_gigabytes = "{:.3f}".format(size_gigabytes)
    return f'{size_gigabytes} GB'


def get_str_size(size_bytes: int) -> str:  #
    """ Return str of different format of size """
    size_kilobytes = size_bytes / 1024
    size_megabytes = size_kilobytes / 1024
    size_gigabytes = size_megabytes / 1024

    size_kilobytes = "{:.3f}".format(size_kilobytes)
    size_megabytes = "{:.3f}".format(size_megabytes)
    size_gigabytes = "{:.3f}".format(size_gigabytes)
    return f"{size_bytes} bytes = {size_kilobytes} KB = {size_megabytes} MB = {size_gigabytes} GB"


def display_info_dir_path(dir_names: list, filenames: list, format_files_dir: dict, total_size_dir: int,
                          dif_level: int) -> dict:
    """
    Return dict with all information about directory
    :param dir_names: list
    :param filenames: list
    :param format_files_dir: dict
    :param total_size_dir: int
    :param dif_level: int
    :return: dict with info
    """

    path_info = {
        "Level": dif_level
    }
    if dir_names:
        path_info["List of folders"] = f"{dir_names}"
        path_info["Number of folders"] = len(dir_names)
    if filenames:
        path_info["List of files"] = f"{filenames}"
        path_info["Number of files"] = len(filenames)
    if format_files_dir:
        path_info["Formats (count)"] = f"{format_files_dir}"
        path_info["Number of formats"] = len(format_files_dir)
    path_info["Total size files"] = get_str_size(total_size_dir)

    return path_info


def dir_info(initial_path: str) -> None:
    """ Main algorithm of program """

    master = Tk()
    master.title("Progress")
    master.geometry("250x100")
    max_val = 0
    for _ in os.walk(initial_path):
        max_val += 1
    progress_bar = ttk.Progressbar(master, orient="horizontal", mode="determinate", maximum=max_val, value=0)

    label_1 = Label(master, text="Progress Bar")
    label_1.grid(row=0, column=0)
    progress_bar.grid(row=0, column=1)
    label_2 = Label(master, text=f"Value = {0}")
    label_2.grid(row=1, column=0)

    lower_level = initial_path.count("\\")
    info_paths_for_json, total_info_for_json = dict(), dict()

    format_files, size_dirs = dict(), dict()
    total_files, total_dirs, total_size = 0, 0, 0
    for dir_path, dir_names, filenames in os.walk(initial_path):  # , topdown=False
        progress_bar['value'] += 1
        label_2['text'] = f"Value = {progress_bar['value']}"
        master.update()

        total_filenames, total_dir_names, total_size_dir = len(filenames), len(dir_names), 0
        total_files += len(filenames)
        total_dirs += len(dir_names)
        format_files_dir = dict()

        for name in filenames:
            path_name = os.path.join(dir_path, name)
            total_size_dir += os.path.getsize(path_name)  # os.stat(path_name).st_size

            if name.rfind('.') != -1:
                key = name[name.rfind('.'):].lower()
            else:
                key = name.lower()

            if key in format_files:
                format_files[key] += 1
            else:
                format_files[key] = 1

            if key in format_files_dir:
                format_files_dir[key] += 1
            else:
                format_files_dir[key] = 1

        total_size += total_size_dir
        size_dirs[dir_path] = total_size_dir

        dif_level = dir_path.count("\\") - lower_level
        path_info = display_info_dir_path(dir_names, filenames, format_files_dir, total_size_dir, dif_level)
        info_paths_for_json[dir_path] = path_info

    if info_paths_for_json:
        write_data_json("Detailed info dirs", info_paths_for_json)
        write_dict_info_paths_to_html("Detailed info dirs", info_paths_for_json)
    if total_dirs or total_files:
        total_info_for_json["Initial path"] = initial_path
        total_info_for_json["Total folders"] = total_dirs
        total_info_for_json["Total files"] = total_files
        total_info_for_json["Total size"] = get_str_size(total_size)
        total_info_for_json["Number of formats"] = len(format_files)
        sorted_format_files = dict(sorted(format_files.items(), key=lambda x: x[1], reverse=True))
        total_info_for_json["Formats (count)"] = sorted_format_files
        write_data_json("Total info directory", total_info_for_json)
        write_dict_total_info_path_to_html("Total info directory", total_info_for_json)

    size_dirs[initial_path] = total_size
    display_tree_dir(initial_path, size_dirs)
    # write_data_html("Directory tree", tree_str)


def main():
    """ Start program """

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    initial_path = fd.askdirectory(title="Select a folder", initialdir="/")

    if os.path.exists(initial_path):
        print(f"Path: '{initial_path}' status: {GREEN}OK\n")
        create_dir()
        dir_info(initial_path)
    else:
        error_out(f"Path: '{initial_path}' status: Not found")
    exi_t()


if __name__ == '__main__':  # Program entry point
    hello = YELLOW + " Program for displaying directory information " + RESET
    print("\n", "{:*^80}".format(hello), "\n", sep='')
    tprint("Directory_info")
    time.sleep(1)
    print(f'Current Working Directory is: {os.getcwd()}\n')
    main()
