from tkinter import Event, Entry, Button, CENTER, END
from Backend_functions import Common_functions


class MyWidgetPrompts:
    def __init__(self, master_frame, widget_name: str, widget_entry: Entry):
        self.btn_prompts = []
        self.master_frame = master_frame
        self.widget_name = widget_name
        self.widget_entry = widget_entry

    def focus_in_for_prompt(self, entry_event: Event = None) -> None:
        print(f"{self.master_frame=}; {self.widget_name=}; {self.widget_entry=}")
        prompts = Common_functions.get_prompts_dict()
        widget_size, widget_x, widget_y = self.widget_entry.winfo_geometry().split('+')
        widget_place_x, widget_place_y = int(widget_x), int(widget_y)
        widget_size_x, widget_size_y = map(int, widget_size.split('x'))
        if prompts[self.widget_name]:
            if self.widget_entry.get() == "":
                prompts_list = prompts[self.widget_name]
            else:
                prompts_list = Common_functions.search_prompts(key=self.widget_name, input_data=self.widget_entry.get())
            self.focus_out_for_prompt()
            index_btn = 1
            for prompt_name in prompts_list:
                btn_prompt = Button(master=self.master_frame, text=prompt_name,
                                    font=('Arial', 10), background='#B5B8B1', fg='#CD7F32', bd=1)
                btn_prompt.configure(command=lambda i=index_btn: self.autofill_prompt(btn_num=i))
                btn_prompt.place(x=widget_place_x + 1, y=widget_place_y + widget_size_y * index_btn + 1,
                                 width=int(widget_size_x - widget_size_x * 0.16),
                                 height=widget_size_y - 1)
                btn_del_prompt = Button(master=self.master_frame, text='x', font=('Arial', 10), background='#B5B8B1',
                                        fg='#900020', bd=1, anchor=CENTER)
                btn_del_prompt.configure(
                    command=lambda i=index_btn: self.delete_choose_prompt(btn_num=i))
                btn_del_prompt.place(x=widget_place_x + int(widget_size_x - widget_size_x * 0.16) + 1,
                                     y=widget_place_y + widget_size_y * index_btn + 1, width=int(widget_size_x * 0.15),
                                     height=widget_size_y - 1)
                index_btn += 1
                self.btn_prompts.append((btn_prompt, btn_del_prompt))
        else:
            self.focus_out_for_prompt()
        self.master_frame.update()

    def focus_out_for_prompt(self, entry_event: Event = None) -> None:
        print(f"{self.widget_name=} -> Focus out")
        for prompt_btn in self.btn_prompts:
            prompt_btn[0].destroy()
            prompt_btn[1].destroy()
        self.btn_prompts = []

    def autofill_prompt(self, btn_num: int) -> None:
        print(f"{self.widget_name=} -> autofill_prompt ")
        btn_text = self.btn_prompts[btn_num - 1][0]['text']
        self.widget_entry.delete(0, END)
        self.widget_entry.insert(0, btn_text)
        self.focus_out_for_prompt()

    def delete_choose_prompt(self, btn_num: int) -> None:
        print(f"{self.widget_name=} -> delete_choose_prompt ")
        btn_text = self.btn_prompts[btn_num - 1][0]['text']
        Common_functions.delete_prompt(selected_key=self.widget_name, deleted_value=btn_text)
        self.focus_out_for_prompt()
        self.focus_in_for_prompt()
