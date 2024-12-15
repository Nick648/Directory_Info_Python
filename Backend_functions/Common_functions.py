import json
import os
import re
from data import Consts

MAX_SIZE_PROMPTS = 3


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


def overwrite_input_prompts(**kwargs):
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


def delete_prompt(selected_key: str, deleted_value: [str | int]):
    prompts = get_prompts_dict()
    prompts[selected_key].remove(deleted_value)
    write_prompts_dict(prompts)


def search_prompts(key: str, input_data: [str | int]):
    prompts = get_prompts_dict()
    search_list = prompts[key]
    return_list = []
    for item in search_list:
        finder = re.match(input_data, str(item))
        if finder and input_data != str(item):
            return_list.append(item)
    return return_list
