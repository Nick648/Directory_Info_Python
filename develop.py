import tkinter as tk
import magic

import os
from os.path import join, getsize
import usb.core
import usb.backend.libusb1
# pip install libusb, pyusb
# Download libusb-1.0.dll to C:\Windows\System32
import sys
import psutil
from psutil._common import bytes2human
from ftplib import FTP


def mime_magic():  # Not good
    path = input('path: ')
    print(magic.Magic(mime=True).from_file(path))  # mime-тип
    return magic.Magic(mime=True).from_file(path)


def check_colors_1():
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


def check_colors_2():
    def change_color(r, g):
        print(f"{r=};{g=}; -> Color = #{r:0>2x}{g:0>2x}00")
        r -= 1
        g += 1
        ws.config(bg=f'#{r:0>2x}{g:0>2x}00')
        if r == 0 or g == 255:
            return
        ws.after(2, lambda: change_color(r, g))

    ws = tk.Tk()
    ws.title('Iridescent text')
    ws.geometry('400x300+600+300')
    # ws.config(bg='#ff0000')  # RED
    # ws.config(bg='#00ff00')  # GREEN
    ws.after(2, lambda: change_color(r=255, g=0))
    ws.mainloop()


def check_psutil():
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # пропускаем приводы cd-rom, в которых нет диска;
                # они могут вызвать ошибку графического интерфейса
                # Windows для неготового раздела или просто зависнуть
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))


def check_os():
    s = input(">>> ")
    print(os.path.exists(s))
    for root, dirs, files in os.walk(s):
        print(root, "consumes")
        print(sum(getsize(join(root, name)) for name in files))
        print("bytes in", len(files), "non-directory files")


def check_usb():
    devices = usb.core.find(find_all=True)

    for device in devices:
        print("VID: {:04x}, PID: {:04x}".format(device.idVendor, device.idProduct))
        print(device[0])
        # for dev in usb.core.find(find_all=True):
        #     # print(dev)
        #     print("device bus:", dev.bus)
        #     print("device address:", dev.address)
        #     print("device port:", dev.port_number)
        #     print("device speed:", dev.speed)
        #     print("dev.bLength", dev.bLength)
        #     print("dev.bNumConfigurations", dev.bNumConfigurations)
        #     print("dev.bDeviceClass", dev.bDeviceClass)

        print(f"\n{'~' * 50}\n")


def check_ftp(host: str = r'ftp://', port: int = 2030, user: str = 'user', password: str = 'password'):
    ftp = FTP()
    ftp.connect(host=host, port=port)
    ftp.login(user=user, passwd=password)
    # print(ftp.getwelcome())
    # ftp.dir()
    # files = ftp.nlst()
    ftp.retrlines(cmd='LIST')
    # ftp = FTP()  # connect to host, default port
    # print(ftp.login(user=user, passwd=password))


if __name__ == '__main__':
    # mime_magic()
    # check_colors_1()
    # check_colors_2()
    # check_psutil()
    # check_os()
    # check_usb()
    check_ftp(host=r'192.168.1.136', port=4632, user='user0', password='pass')
    sys.exit()
