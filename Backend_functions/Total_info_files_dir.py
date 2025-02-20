import os
import time
from Backend_functions.Common_functions import write_data_json, write_data_html, write_data_txt, create_dir, \
    get_max_str_size, get_all_str_sizes
from GUI.My_progressbar import MyProgressBar

# Name of directory
CUR_DIR = os.path.dirname(os.path.abspath(__file__))  # Without name file.py
MAIN_NAME_DIR = 'Total parse info dir'
PATH_SAVE_RESULT = os.path.join(CUR_DIR, MAIN_NAME_DIR)

# INFO OF FILES
INFO_PATHS_FOR_JSON = dict()
TOTAL_FORMAT_FILES, SIZE_DIRS = dict(), dict()
TOTAL_FILES, TOTAL_DIRS, TOTAL_SIZE = 0, 0, 0


def zeroing_values(path_for_save: str) -> None:
    """ Clearing old values before a new call """
    global PATH_SAVE_RESULT, CUR_DIR, INFO_PATHS_FOR_JSON, TOTAL_FORMAT_FILES, SIZE_DIRS, \
        TOTAL_FILES, TOTAL_DIRS, TOTAL_SIZE
    CUR_DIR = path_for_save
    PATH_SAVE_RESULT, name_folder = create_dir(folder_creation_path=CUR_DIR, main_name_dir=MAIN_NAME_DIR,
                                               create_folder=False)
    INFO_PATHS_FOR_JSON = dict()
    TOTAL_FORMAT_FILES, SIZE_DIRS = dict(), dict()
    TOTAL_FILES, TOTAL_DIRS, TOTAL_SIZE = 0, 0, 0


def write_dict_info_paths_to_html(file_name: str, dict_paths: dict) -> str:
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

    return write_data_html(way_dir=PATH_SAVE_RESULT, file_name=file_name, write_text=str_html)


def write_dict_total_info_path_to_html(file_name: str, dict_path_info: dict) -> str:
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

    return write_data_html(way_dir=PATH_SAVE_RESULT, file_name=file_name, write_text=str_html)


def write_tree_dir_html_txt(initial_path: str, size_dirs: dict) -> str:
    """ Output of the directory tree and percent size """

    tree_str = f"Output of the directory tree and their percentage of the total size:\n" \
               f"P.S. In parentheses, the size of all subfolders relative to the main directory is indicated.\n\n"

    tree_html = f"<font color='green' size=7>Directory tree</font><br>" \
                f"<font color='DarkOrange' size=5.5>" \
                f"Output of the directory tree and their percentage of the total size:" \
                f"<br>" \
                f"P.S. In parentheses, the size of all subfolders relative to the main directory is indicated." \
                f"<br><br></font>"
    tree_html += f"<font size=5>"

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

            tree_str += f"{indent}{dir_path}  ->  {perc_size}\n"
            tree_html += f"{'&emsp;' * dif_level * 2}{dir_path}&emsp;->&emsp;{perc_size}<br>"
        else:
            tree_str += f"{dir_path}\n"
            tree_html += f"<font color='magenta'>{dir_path}</font><br>"
    tree_html += f"</font>"
    try:
        max_perc_size = "{:.3f}".format(max_size_dir / size_dirs[initial_path] * 100) + '%'
        min_perc_size = "{:.3f}".format(min_size_dir / size_dirs[initial_path] * 100) + '%'
        str_max_size_dir, str_min_size_dir = get_max_str_size(max_size_dir), get_max_str_size(min_size_dir)

        max_file = get_max_file(max_size_path)

        tree_str += f"\n\nMaximum directory size: {max_size_path} = {str_max_size_dir}  ->  {max_perc_size}\n"
        tree_html += f"<font size=5>"
        tree_html += f"<br><br>Maximum directory size: {max_size_path} = {str_max_size_dir}&emsp;->&emsp;" \
                     f"<font color='purple'>{max_perc_size}</font><br>"
        if max_file:
            path_max_file, size_max_file = max_file
            max_perc_size_file = "{:.3f}".format(size_max_file / max_size_dir * 100) + '%'

            tree_str += f"\tMaximum file size: {path_max_file} = {get_max_str_size(size_max_file)}  ->  " \
                        f"In folder {max_perc_size_file}\n"
            tree_html += f"&emsp;&emsp;Maximum file size: {path_max_file} = " \
                         f"{get_max_str_size(size_max_file)}&emsp;->&emsp;" \
                         f"<font color='purple'>In folder {max_perc_size_file}</font><br>"

        tree_str += f"Minimum directory size: {min_size_path} = {str_min_size_dir}  ->  {min_perc_size}\n"
        tree_html += f"Minimum directory size: {min_size_path} = {str_min_size_dir}&emsp;->&emsp;" \
                     f"<font color='purple'>{min_perc_size}</font><br>"
        tree_html += f"</font>"
    except ZeroDivisionError:
        pass

    report_str = ''
    report_str += write_data_txt(way_dir=PATH_SAVE_RESULT, file_name="Directory tree", write_text=tree_str)
    report_str += write_data_html(way_dir=PATH_SAVE_RESULT, file_name="Directory tree", write_text=tree_html)
    return report_str


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


def get_dict_info_dir_path(dir_names: list, filenames: list, format_files_dir: dict, total_size_dir: int,
                           dif_level: int) -> dict:
    """ Return dict with all information about directory """

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
    path_info["Total size files"] = get_all_str_sizes(total_size_dir)

    return path_info


def parse_info_abot_files(dir_path: str, dir_names: list[str], filenames: list[str], lower_level: int):
    global TOTAL_FORMAT_FILES, SIZE_DIRS, TOTAL_FILES, TOTAL_DIRS, TOTAL_SIZE, INFO_PATHS_FOR_JSON
    total_size_dir = 0
    TOTAL_FILES += len(filenames)
    TOTAL_DIRS += len(dir_names)
    format_files_dir = dict()

    for name in filenames:
        path_name = os.path.join(dir_path, name)
        total_size_dir += os.path.getsize(path_name)  # os.stat(path_name).st_size

        cur_file_name, file_extension = os.path.splitext(name)
        file_extension = file_extension.lower()
        if not file_extension:
            file_extension = 'None'

        if file_extension in TOTAL_FORMAT_FILES:
            TOTAL_FORMAT_FILES[file_extension] += 1
        else:
            TOTAL_FORMAT_FILES[file_extension] = 1

        if file_extension in format_files_dir:
            format_files_dir[file_extension] += 1
        else:
            format_files_dir[file_extension] = 1

    TOTAL_SIZE += total_size_dir
    SIZE_DIRS[dir_path] = total_size_dir

    dif_level = dir_path.count("\\") - lower_level
    path_info = get_dict_info_dir_path(dir_names, filenames, format_files_dir, total_size_dir, dif_level)
    INFO_PATHS_FOR_JSON[dir_path] = path_info


def get_dict_total_info(initial_path: str) -> dict:
    total_info_dict = dict()
    total_info_dict["Initial path"] = initial_path
    total_info_dict["Total folders"] = TOTAL_DIRS
    total_info_dict["Total files"] = TOTAL_FILES
    total_info_dict["Total size"] = get_all_str_sizes(TOTAL_SIZE)
    total_info_dict["Number of formats"] = len(TOTAL_FORMAT_FILES)
    sorted_format_files = dict(sorted(TOTAL_FORMAT_FILES.items(), key=lambda x: x[1], reverse=True))
    total_info_dict["Formats (count)"] = sorted_format_files
    return total_info_dict


def run_total_search(initial_path: str, progress_bar: MyProgressBar, path_for_save: str = '') -> str:
    """ Main algorithm of program """
    # deleting old values and setting the path to save!
    zeroing_values(path_for_save=path_for_save)

    # parameters for tkinter
    max_val = 0
    for _ in os.walk(initial_path):
        max_val += 1
    progress_bar.set_max_val(max_value=max_val)
    step_color = 255 / max_val
    progress_bar.set_step_value(step_value=step_color)
    time_pause = 1 / max_val

    lower_level = initial_path.count("\\")
    for dir_path, dir_names, filenames in os.walk(initial_path):  # , topdown=False
        progress_bar.pb_step()
        parse_info_abot_files(dir_path=dir_path, dir_names=dir_names, filenames=filenames, lower_level=lower_level)
        time.sleep(time_pause)

    if TOTAL_DIRS or TOTAL_FILES:
        report_str = create_dir(folder_creation_path=path_for_save, main_name_dir=MAIN_NAME_DIR,
                                create_folder=True)

        report_str += write_data_json(way_dir=PATH_SAVE_RESULT, file_name="Detailed info dirs",
                                      dump_dict=INFO_PATHS_FOR_JSON)
        report_str += write_dict_info_paths_to_html("Detailed info dirs", INFO_PATHS_FOR_JSON)

        total_info_dict = get_dict_total_info(initial_path=initial_path)
        report_str += write_data_json(way_dir=PATH_SAVE_RESULT, file_name="Total info directory",
                                      dump_dict=total_info_dict)
        report_str += write_dict_total_info_path_to_html("Total info directory", total_info_dict)

        SIZE_DIRS[initial_path] = TOTAL_SIZE
        report_str += write_tree_dir_html_txt(initial_path, SIZE_DIRS)

        return report_str
    else:
        return "There are no files and folders in the current directory!"
