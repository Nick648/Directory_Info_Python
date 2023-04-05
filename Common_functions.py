from tkinter import ttk, Label
import json
import os


def update_tkinter_window(progress_bar: ttk.Progressbar, lb_step: Label, current_step: int, max_val: int,
                          colors_dict: dict, step_color: float) -> None:
    """ Update progressbar and Label of main window Tkinter """

    current_style = ttk.Style()
    current_style.theme_use('alt')
    colors_dict['red'] -= step_color
    colors_dict['green'] += step_color
    if colors_dict['red'] < 0:
        colors_dict['red'] = 0
    if colors_dict['green'] > 255:
        colors_dict['green'] = 255
    progress_bar.step()
    red_color, green_color = int(colors_dict['red']), int(colors_dict['green'])
    new_color = f"#{red_color:0>2x}{green_color:0>2x}00"
    current_style.configure('new_color.Horizontal.TProgressbar', background=new_color)
    progress_bar.config(style='new_color.Horizontal.TProgressbar')
    lb_step['text'] = f"Step {current_step}/{max_val}"
    lb_step.configure(fg=new_color)
    lb_step.update()
    progress_bar.update()


def write_data_json(way_dir: str, file_name: str, dump_dict: dict) -> str:
    """ Writes the dictionary to a json file """
    file_path = os.path.join(way_dir, f"{file_name}.json")
    with open(file=file_path, mode="w", encoding="utf-8") as write_file:
        json.dump(dump_dict, write_file, ensure_ascii=False, indent=4)
    return f"  File: {file_name}.json -> was created!\n"  # or file_path


def write_data_txt(way_dir: str, file_name: str, write_text: str) -> str:
    """ Writes the text to a txt file """
    file_path = os.path.join(way_dir, f"{file_name}.txt")
    with open(file=file_path, mode="w", encoding="utf-8") as txt_file:
        txt_file.write(write_text)
    return f"  File: {file_name}.txt -> was created!\n"  # or file_path


def write_data_html(way_dir: str, file_name: str, write_text: str) -> str:
    """ Writes the text to a html file """
    file_path = os.path.join(way_dir, f"{file_name}.html")
    with open(file=file_path, mode="w", encoding="utf-8") as html_file:
        html_file.write(write_text)
    return f"  File: {file_name}.html -> was created!\n"  # or file_path
