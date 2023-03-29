from tkinter import *

if __name__ == '__main__':
    root = Tk()
    photo_folder = PhotoImage(file=r"data\folder_icon.png")
    photo_folder = photo_folder.subsample(15, 15)
    btn_folder = Button(root, command=lambda: print(0), image=photo_folder, borderwidth=0)
    btn_folder.pack()
    root.mainloop()
