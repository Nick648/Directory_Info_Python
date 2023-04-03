import os
import time
import json
import datetime
from tkinter import ttk, Label

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


def write_data_json(file_name: str, dump_dict: dict) -> str:
    """ Writes the dictionary to a json file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.json")
    with open(file=file_path, mode="w", encoding="utf-8") as write_file:
        json.dump(dump_dict, write_file, ensure_ascii=False, indent=4)
    return f"  File: {file_name}.json -> was created!\n"  # or file_path


def write_data_html(file_name: str, write_text: str) -> str:
    """ Writes the text to a html file """
    file_path = os.path.join(WAY_DIR, f"{file_name}.html")
    with open(file=file_path, mode="w", encoding="utf-8") as html_file:
        html_file.write(write_text)
    return f"  File: {file_name}.html -> was created!\n"  # or file_path


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
        for search_file in search_type_files:
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


def update_tkinter_window(progress_bar: ttk.Progressbar, lb_step: Label, current_step: int, max_val: int,
                          colors_dict: dict, step_color: float) -> None:
    current_style = ttk.Style()
    current_style.theme_use('alt')
    colors_dict['red'] -= step_color
    colors_dict['green'] += step_color
    if colors_dict['red'] < 0:
        colors_dict['red'] = 0
    if colors_dict['green'] > 255:
        colors_dict['green'] = 255
    progress_bar.step()
    lb_step['text'] = f"Step {current_step}/{max_val}"
    red_color, green_color = int(colors_dict['red']), int(colors_dict['green'])
    new_color = f"#{red_color:0>2x}{green_color:0>2x}00"
    current_style.configure('new_color.Horizontal.TProgressbar', background=new_color)
    progress_bar.config(style='new_color.Horizontal.TProgressbar')
    lb_step.configure(fg=new_color)
    lb_step.update()
    progress_bar.update()


def run_search_types(initial_path: str, search_type_files: list[str], progress_bar: ttk.Progressbar,
                     lb_step: Label) -> str:
    """ Main algorithm of program """
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
        update_tkinter_window(progress_bar, lb_step, current_step, max_val, colors_dict, step_color)
        check_path(dir_path=dir_path, filenames=filenames, lower_level=lower_level, search_type_files=search_type_files)
        time.sleep(time_pause)

    if PATHS_FILES_DICT:
        report_str = ''
        report_str += create_dir()
        sorted_format_files = dict(sorted(TOTAL_COUNT_FILES.items(), key=lambda x: x[1], reverse=True))

        report_str += write_data_json("Info found files", PATHS_FILES_DICT)
        report_str += write_data_json("Total number of file types", sorted_format_files)

        str_html = dict_total_info_to_str_html(PATHS_FILES_DICT)
        report_str += write_data_html("Info found files", str_html)

        total_info_str_html = path_tree_to_html_str(initial_path, PATHS_FILES_DICT)
        total_info_str_html += total_count_types_to_str_html(sorted_format_files)
        report_str += write_data_html("Total number of file types", total_info_str_html)

        return report_str
    else:
        return "There are no required files in the current directory!"
