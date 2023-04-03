from tkinter import ttk, Label


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
