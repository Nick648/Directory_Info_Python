import json
import os
import re
import datetime
from data import Consts

MAX_SIZE_PROMPTS = 3


def create_dir(folder_creation_path: str, main_name_dir: str, create_folder: bool = True) -> tuple[str, str] | str:
    """ Creating a folder for files
    Return: WAY_DIRECTORY, NAME_DIRECTORY, REPORT
    """
    today = datetime.datetime.today()
    date_y, date_m, date_d = today.year, today.month, today.day
    name_dir = f'{main_name_dir} {date_d}_{date_m}_{date_y}'
    way_dir = os.path.join(folder_creation_path, name_dir)

    if not os.path.exists(way_dir) and create_folder:  # Creating a folder for files
        os.mkdir(way_dir)

    else:  # If the folder is created, an additional one will be created with the version specified
        version = 1
        while os.path.exists(way_dir):
            name_dir = f'{main_name_dir} {date_d}_{date_m}_{date_y} version=={version}'
            way_dir = os.path.join(folder_creation_path, name_dir)
            version += 1
        if create_folder:
            os.mkdir(way_dir)

    if create_folder:
        return f"Folder: {way_dir} -> was created!\n\n"
    else:
        return way_dir, name_dir


def write_data_json(way_dir: str, file_name: str, dump_dict: dict) -> str:
    """ Writes the dictionary to a json file """
    file_path = os.path.join(way_dir, f"{file_name}.json")
    with open(file=file_path, mode="w", encoding="utf-8") as write_file:
        json.dump(dump_dict, write_file, ensure_ascii=False, indent=4)
    return f"  File: {file_name}.json -> was created! \n"  # or file_path


def write_data_txt(way_dir: str, file_name: str, write_text: str) -> str:
    """ Writes the text to a txt file """
    file_path = os.path.join(way_dir, f"{file_name}.txt")
    with open(file=file_path, mode="w", encoding="utf-8") as txt_file:
        txt_file.write(write_text)
    return f"  File: {file_name}.txt -> was created! \n"  # or file_path


def write_data_html(way_dir: str, file_name: str, write_text: str) -> str:
    """ Writes the text to a html file """
    file_path = os.path.join(way_dir, f"{file_name}.html")
    with open(file=file_path, mode="w", encoding="utf-8") as html_file:
        html_file.write(write_text)
    return f"  File: {file_name}.html -> was created! \n"  # or file_path


def get_prompts_dict() -> dict:
    try:
        with open(file=fr"{Consts.PATH_DATA_DIR}/Input_prompts.json", mode="r", encoding="utf-8") as json_file:
            prompts = json.load(json_file)
        return prompts
    except FileNotFoundError:
        prompts = {"host": [], "port": [], "login": [], "password": []}
        write_prompts_dict(prompts)
        return prompts


def write_prompts_dict(prompts: dict) -> None:
    try:
        with open(file=fr"{Consts.PATH_DATA_DIR}/Input_prompts.json", mode="w", encoding="utf-8") as json_file:
            json.dump(prompts, json_file, ensure_ascii=False, indent=4)
    except Exception as ex:
        print(f'Error in Common_functions.py in write_prompts_dict() -> {ex}')


def get_max_str_size(size_bytes: int) -> str:
    """ Return str of max format of size """
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


def get_all_str_sizes(size_bytes: int) -> str:
    """ Return str of different format of size """
    size_kilobytes = size_bytes / 1024
    size_megabytes = size_kilobytes / 1024
    size_gigabytes = size_megabytes / 1024

    size_kilobytes = "{:.3f}".format(size_kilobytes)
    size_megabytes = "{:.3f}".format(size_megabytes)
    size_gigabytes = "{:.3f}".format(size_gigabytes)
    return f"{size_bytes} bytes = {size_kilobytes} KB = {size_megabytes} MB = {size_gigabytes} GB"


def overwrite_input_prompts(**kwargs) -> None:
    prompts = get_prompts_dict()
    for key, val in kwargs.items():
        need_list = prompts[key]
        if val in need_list:
            need_list[need_list.index(val)], need_list[0] = need_list[0], need_list[need_list.index(val)]
        elif len(need_list) >= MAX_SIZE_PROMPTS:
            need_list.insert(0, val)
            need_list.pop(-1)
        else:
            need_list.insert(0, val)
    write_prompts_dict(prompts)


def delete_prompt(selected_key: str, deleted_value: [str | int]) -> None:
    prompts = get_prompts_dict()
    prompts[selected_key].remove(deleted_value)
    write_prompts_dict(prompts)


def search_prompts(key: str, input_data: [str | int]) -> list[str | int]:
    prompts = get_prompts_dict()
    search_list = prompts[key]
    return_list = []
    for item in search_list:
        finder = re.match(input_data, str(item))
        if finder and input_data != str(item):
            return_list.append(item)
    return return_list


def check_similarity_subfolders(check_path: str, list_paths: list[str]) -> bool:
    check_path = os.path.normpath(check_path)
    for path in list_paths:
        path = os.path.normpath(path)
        if check_path == path or path in check_path:
            return True
    return False
