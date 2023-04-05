import os
import time
import datetime
from tkinter import ttk, Label
from Common_functions import update_tkinter_window, write_data_json, write_data_html

# Consts for time and date
today = datetime.datetime.today()
date_y, date_m, date_d = today.year, today.month, today.day
# time_h, time_m, time_s = today.hour, today.minute, today.second

# Name of directory
DESKTOP_DIR = os.path.expanduser('~') + r'\Desktop'  # Full path to the desktop
CUR_DIR_FILE = os.path.abspath(__file__)  # Full path to the file, with name file.py
CUR_DIR = os.path.dirname(os.path.abspath(__file__))  # Without name file.py
MAIN_NAME_DIR = f'File types parse'
NAME_DIR = f'{MAIN_NAME_DIR} {date_d}_{date_m}_{date_y}'
WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)

# Files to search for
PATHS_FILES_DICT = {}
TOTAL_COUNT_FILES = {}


def zeroing_values() -> None:
    """ Clearing old values before a new call """
    global today, date_y, date_m, date_d, NAME_DIR, WAY_DIR, PATHS_FILES_DICT, TOTAL_COUNT_FILES
    today = datetime.datetime.today()
    date_y, date_m, date_d = today.year, today.month, today.day
    NAME_DIR = f'{MAIN_NAME_DIR} {date_d}_{date_m}_{date_y}'
    WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)
    PATHS_FILES_DICT = {}
    TOTAL_COUNT_FILES = {}


def create_dir() -> str:
    """ Creating a folder for files """
    global WAY_DIR, NAME_DIR

    if not os.path.exists(WAY_DIR):  # Creating a folder for files
        os.mkdir(WAY_DIR)

    # If the folder is created, an additional one will be created with the version specified
    else:
        version = 1
        while os.path.exists(WAY_DIR):
            NAME_DIR = f'{MAIN_NAME_DIR} {date_d}_{date_m}_{date_y} version=={version}'
            WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)
            version += 1
        os.mkdir(WAY_DIR)

    return f"Folder: {WAY_DIR} -> was created!\n\n"


def path_tree_to_html_str(initial_path: str, dict_paths: dict) -> str:
    tree_html = f"<font color='green' size=7>Tree of found paths</font><br>"
    tree_html += f"<font size=5>"
    tree_html += f"&emsp;Initial path:&nbsp;<font color=Magenta>{initial_path}</font><br><br>"
    for path in dict_paths:
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
    total_count_files = sum([dict_types[key_type] for key_type in dict_types])
    str_html += f"<font size=6 color=brown>&emsp;Total files found: {total_count_files}</font><br>"
    str_html += f"<font size=5>"
    str_html += f"<b>&emsp;&emsp;{'Type':5}:&nbsp;{'Count':5};</b><br>"
    for key_type in dict_types:
        str_html += f"&emsp;&emsp;{key_type:5}:&nbsp;{dict_types[key_type]:5};<br>"
    str_html += f"</font><br><br>"
    return str_html


def check_path(dir_path: str, filenames: list[str], lower_level: int, search_type_files: list[str]) -> bool:
    global PATHS_FILES_DICT, TOTAL_COUNT_FILES
    dict_found_files = {}
    total_found_files = 0
    list_filenames = []
    dif_level = dir_path.count("\\") - lower_level
    for file in filenames:
        cur_file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()
        if file_extension in search_type_files:
            total_found_files += 1
            list_filenames.append(file)
            if file_extension in dict_found_files:
                dict_found_files[file_extension] += 1
            else:
                dict_found_files[file_extension] = 1

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


def run_search_types(initial_path: str, search_type_files: list[str], progress_bar: ttk.Progressbar,
                     lb_step: Label, path_for_save: str = '') -> str:
    """ Main algorithm of program """
    global CUR_DIR, WAY_DIR

    # deleting old values!
    zeroing_values()

    # setting the path to save
    if path_for_save:
        CUR_DIR = path_for_save
        WAY_DIR = os.path.join(CUR_DIR, NAME_DIR)

    # parameters for tkinter
    max_val = 0
    for _ in os.walk(initial_path):
        max_val += 1
    progress_bar['maximum'] = max_val
    colors_dict = {'red': 255, 'green': 0, 'blue': 0}
    step_color = 255 / max_val
    current_step = 0
    time_pause = 1 / max_val

    lower_level = initial_path.count("\\")
    for dir_path, dir_names, filenames in os.walk(initial_path):  # , topdown=False
        current_step += 1
        update_tkinter_window(progress_bar=progress_bar, lb_step=lb_step, current_step=current_step,
                              max_val=max_val, colors_dict=colors_dict, step_color=step_color)
        check_path(dir_path=dir_path, filenames=filenames, lower_level=lower_level, search_type_files=search_type_files)
        time.sleep(time_pause)

    if PATHS_FILES_DICT:
        report_str = ''
        report_str += create_dir()
        sorted_format_files = dict(sorted(TOTAL_COUNT_FILES.items(), key=lambda x: x[1], reverse=True))

        report_str += write_data_json(way_dir=WAY_DIR, file_name="Info found files", dump_dict=PATHS_FILES_DICT)
        report_str += write_data_json(way_dir=WAY_DIR, file_name="Total number of file types",
                                      dump_dict=sorted_format_files)

        str_html = dict_total_info_to_str_html(PATHS_FILES_DICT)
        report_str += write_data_html(way_dir=WAY_DIR, file_name="Info found files", write_text=str_html)

        total_info_str_html = path_tree_to_html_str(initial_path, PATHS_FILES_DICT)
        total_info_str_html += total_count_types_to_str_html(sorted_format_files)
        report_str += write_data_html(way_dir=WAY_DIR, file_name="Total number of file types",
                                      write_text=total_info_str_html)

        return report_str
    else:
        return "There are no required files in the current directory!"
