from tkinter import ttk, Label
import tkinter.constants


class MyProgressBar(ttk.Progressbar):
    def __init__(self, master_frame: ttk.Frame):
        super().__init__(master=master_frame)
        self.master_frame = master_frame
        self.progress_bar = ttk.Progressbar(master=master_frame, orient="horizontal", length=170, value=0)
        self.lb_step = Label(master=master_frame, text='', font=('Arial', 12, 'italic', 'bold'), fg='orange red')
        self.current_style = ttk.Style()
        self.current_style.theme_use('alt')
        self.colors_dict = {"red": 255, "green": 0, "blue": 0}
        self.current_step, self.step_value, self.max_value = 0, 1, 0

    def progress_bar_place(self, rel_x: float, rel_y: float, in_anchor: tkinter.constants):
        self.progress_bar.place(relx=rel_x, rely=rel_y, anchor=in_anchor)

    def label_step_place(self, rel_x: float, rel_y: float, in_anchor: tkinter.constants):
        self.lb_step.place(relx=rel_x, rely=rel_y, anchor=in_anchor)

    def set_max_val(self, max_value: int):
        self.max_value = max_value
        self.progress_bar['maximum'] = max_value

    def set_step_value(self, step_value: float):
        self.step_value = step_value

    def pb_step(self) -> None:
        """ Update progressbar and Label of main window Tkinter """
        self.current_step += 1
        self.colors_dict['red'] -= self.step_value
        self.colors_dict['green'] += self.step_value
        if self.colors_dict['red'] < 0:
            self.colors_dict['red'] = 0
        if self.colors_dict['green'] > 255:
            self.colors_dict['green'] = 255
        self.progress_bar.step()
        red_color, green_color = int(self.colors_dict['red']), int(self.colors_dict['green'])
        new_color = f"#{red_color:0>2x}{green_color:0>2x}00"
        self.current_style.configure('new_color.Horizontal.TProgressbar', background=new_color)
        self.progress_bar.config(style='new_color.Horizontal.TProgressbar')
        self.lb_step['text'] = f"Step {self.current_step}/{self.max_value}"
        self.lb_step.configure(fg=new_color)
        self.update()

    def destroy(self) -> None:
        self.progress_bar.destroy()
        self.lb_step.destroy()
        super().destroy()
