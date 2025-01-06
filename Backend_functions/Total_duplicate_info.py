import os
import time
from Backend_functions.Common_functions import write_data_json, create_dir, get_max_str_size, \
    check_similarity_subfolders
from GUI.My_progressbar import MyProgressBar

# Name of directory
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_NAME_DIR = "Info duplicate files"
PATH_SAVE_RESULT = os.path.join(CUR_DIR, MAIN_NAME_DIR)

# INFO OF FILES STORAGES
DICT_ALL_FILES, LIST_DUPLICATE_FILES = dict(), list()
TOTAL_COUNT_FILES, TOTAL_DUPLICATE_FILES = 0, 0


def zeroing_values(path_for_save: str) -> None:
    """ Clearing old values before a new call """
    global PATH_SAVE_RESULT, CUR_DIR, TOTAL_COUNT_FILES, TOTAL_DUPLICATE_FILES, DICT_ALL_FILES, LIST_DUPLICATE_FILES
    CUR_DIR = path_for_save
    PATH_SAVE_RESULT, name_folder = create_dir(folder_creation_path=CUR_DIR, main_name_dir=MAIN_NAME_DIR,
                                               create_folder=False)
    DICT_ALL_FILES, LIST_DUPLICATE_FILES = dict(), list()
    TOTAL_COUNT_FILES, TOTAL_DUPLICATE_FILES = 0, 0


def get_dict_total_info(initial_path: str) -> dict:
    total_info_dict, duplicate_paths = dict(), dict()
    total_size_duplicate_files = 0
    total_info_dict["Initial path"] = initial_path
    total_info_dict["Total files"] = TOTAL_COUNT_FILES
    total_info_dict["Total duplicate files"] = TOTAL_DUPLICATE_FILES
    for name in LIST_DUPLICATE_FILES:
        file_size = os.path.getsize(DICT_ALL_FILES[name][0])
        total_size_duplicate_files += (file_size * (len(DICT_ALL_FILES[name]) - 1))
        duplicate_paths[name] = {"File size": get_max_str_size(file_size),
                                 "Paths": DICT_ALL_FILES[name]}
    total_info_dict["Total size duplicate files"] = get_max_str_size(total_size_duplicate_files)
    total_info_dict["duplicate files"] = duplicate_paths
    return total_info_dict


def parse_info_abot_files(dir_path: str, filenames: list[str], exception_files: list[str] = None,
                          search_type_files: list[str] = None) -> None:
    global TOTAL_COUNT_FILES, TOTAL_DUPLICATE_FILES, DICT_ALL_FILES, LIST_DUPLICATE_FILES
    TOTAL_COUNT_FILES += len(filenames)

    for name in filenames:
        if exception_files and name in exception_files:
            print(name, name in exception_files)
            continue
        path_name = os.path.join(dir_path, name)

        cur_file_name, file_extension = os.path.splitext(name)
        file_extension = file_extension.lower()
        if not file_extension:
            file_extension = 'None'
        if search_type_files is None or file_extension in search_type_files:
            if name in DICT_ALL_FILES:
                TOTAL_DUPLICATE_FILES += 1
                if name in LIST_DUPLICATE_FILES:
                    DICT_ALL_FILES[name].append(path_name)
                else:
                    DICT_ALL_FILES[name].append(path_name)
                    LIST_DUPLICATE_FILES.append(name)
            else:
                DICT_ALL_FILES[name] = [path_name]


def run_total_search(initial_path: str, progress_bar: MyProgressBar, path_for_save: str,
                     exception_files: list[str] = None, exception_dirs: list[str] = None,
                     search_type_files: list[str] = None) -> str:
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

    for dir_path, dir_names, filenames in os.walk(initial_path):  # , topdown=False
        check_key = check_similarity_subfolders(check_path=dir_path, list_paths=exception_dirs)
        if check_key:
            continue
        progress_bar.pb_step()
        parse_info_abot_files(dir_path=dir_path, filenames=filenames, exception_files=exception_files,
                              search_type_files=search_type_files)
        time.sleep(time_pause)

    if TOTAL_DUPLICATE_FILES:
        dict_total_info = get_dict_total_info(initial_path=initial_path)
        report_str = create_dir(folder_creation_path=path_for_save, main_name_dir=MAIN_NAME_DIR,
                                create_folder=True)

        report_str += write_data_json(way_dir=PATH_SAVE_RESULT, file_name="Info duplicate files",
                                      dump_dict=dict_total_info)
        return report_str
    else:
        return "There are no duplicate files in this directory!"
