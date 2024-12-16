from tkinter import Entry, Button, CENTER, END, Event
from Backend_functions import Common_functions


class MyWidgetPrompts:
    def __init__(self, master_frame):
        self.btn_prompts = []
        self.master_frame = master_frame

    def focus_in_widget(self, key_prompt: str, widget_entry: Entry) -> None:
        prompts = Common_functions.get_prompts_dict()
        widget_size, widget_x, widget_y = widget_entry.winfo_geometry().split('+')
        widget_place_x, widget_place_y = int(widget_x), int(widget_y)
        widget_size_x, widget_size_y = map(int, widget_size.split('x'))
        if prompts[key_prompt]:
            if widget_entry.get() == "":
                prompts_list = prompts[key_prompt]
            else:
                prompts_list = Common_functions.search_prompts(key=key_prompt, input_data=widget_entry.get())
            self.focus_out_widget()
            index_btn = 1
            for prompt_name in prompts_list:
                btn_prompt = Button(master=self.master_frame, text=prompt_name,
                                    font=('Arial', 10), background='#B5B8B1', fg='#CD7F32', bd=1)
                btn_prompt.configure(
                    command=lambda i=index_btn: self.autofill_prompt(btn_num=i, widget_entry=widget_entry))
                btn_prompt.place(x=widget_place_x + 1, y=widget_place_y + widget_size_y * index_btn + 1,
                                 width=int(widget_size_x - widget_size_x * 0.16),
                                 height=widget_size_y - 1)
                btn_del_prompt = Button(master=self.master_frame, text='x', font=('Arial', 10), background='#B5B8B1',
                                        fg='#900020', bd=1, anchor=CENTER)
                btn_del_prompt.configure(
                    command=lambda i=index_btn: self.delete_choose_prompt(btn_num=i, key_prompt=key_prompt,
                                                                          widget_entry=widget_entry))
                btn_del_prompt.place(x=widget_place_x + int(widget_size_x - widget_size_x * 0.16) + 1,
                                     y=widget_place_y + widget_size_y * index_btn + 1, width=int(widget_size_x * 0.15),
                                     height=widget_size_y - 1)
                index_btn += 1
                self.btn_prompts.append((btn_prompt, btn_del_prompt))
        else:
            self.focus_out_widget()

    def focus_out_widget(self, widget_event: Event = None) -> None:
        for prompt_btn in self.btn_prompts:
            prompt_btn[0].destroy()
            prompt_btn[1].destroy()
        self.btn_prompts = []

    def autofill_prompt(self, btn_num: int, widget_entry: Entry) -> None:
        btn_text = self.btn_prompts[btn_num - 1][0]['text']
        widget_entry.delete(0, END)
        widget_entry.insert(0, btn_text)
        self.focus_out_widget()

    def delete_choose_prompt(self, btn_num: int, key_prompt: str, widget_entry: Entry) -> None:
        btn_text = self.btn_prompts[btn_num - 1][0]['text']
        Common_functions.delete_prompt(selected_key=key_prompt, deleted_value=btn_text)
        self.focus_out_widget()
        self.focus_in_widget(key_prompt=key_prompt, widget_entry=widget_entry)
