import tkinter as tk


def check_1():
    def change_color(step=0):
        r = abs((step * 8) % 512 - 255)
        g = 255 - r
        print(f"#{r:0>2x}{g:0>2x}00 -> {r=}; {g=}")
        lbl.configure(fg=f"#{r:0>2x}{g:0>2x}00")
        root.after(5000 * 8 // 256, lambda: change_color(step + 1))

    root = tk.Tk()
    lbl = tk.Label(root, text="Переливающийся текст", font="-size 20")
    lbl.pack(fill=tk.BOTH)
    root.after(1, change_color)
    root.mainloop()


def check_2():
    def rgb_hack(rgb):
        print("#%02x%02x%02x" % rgb)
        return "#%02x%02x%02x" % rgb

    ws = tk.Tk()
    ws.title('PythonGuides')
    ws.geometry('400x300')
    ws.config(bg=rgb_hack((255, 0, 122)))
    ws.mainloop()


def check_3():
    def change_color(r, g):
        print(f"#{r:0>2x}{g:0>2x}00")

    ws = tk.Tk()
    ws.title('PythonGuides')
    ws.geometry('400x300')
    # ws.config(bg='#ff0000')  # RED
    # ws.config(bg='#00ff00')  # GREEN
    step = 255 // 10
    ws.after(2, lambda: change_color(step + 1))
    ws.mainloop()


if __name__ == '__main__':
    print(1/234)
    # check_1()
    # check_2()
    # check_3()
