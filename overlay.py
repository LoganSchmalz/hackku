#inspired by https://github.com/notatallshaw/fall_guys_ping_estimate/blob/main/fgpe/overlay.py

import sys
import logging
import tkinter as tk
import signal

logger = logging.getLogger(__name__)

def report_callback_exception(exc_type, val, tb):
    if issubclass(exc_type, GracefulExit):
        sys.exit(0)

    logger.error('Exception occured, exiting:', exc_info=(exc_type, val, tb))
    sys.exit(1)


class GracefulExit(Exception):
    "Allows callbacks to gracefully exit without logging error"


class Overlay:
    height = "400"
    width = "500"
    x = "100"
    y = "100"
    msg_q = []

    def __init__(self, get_new_text_callback):
        self.get_new_text_callback = get_new_text_callback

        self.initial_delay = 0
        self.initial_text = "Caption overlay"

        self.root = tk.Tk()
        self.root.report_callback_exception = report_callback_exception
        self.root.overrideredirect(True)
        self.root.geometry(self.geo_str(self.width, self.height, self.x, self.y))
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        self.caption_text = tk.StringVar()
        self.caption_label = tk.Label(self.root, textvariable=self.caption_text, font=('Consolas','28'), fg='white', bg='black')
        self.caption_label.grid(row=0,column=1)

        signal.signal(signal.SIGINT, lambda x,y : self.destroy())
        self.root.bind_all('<Control-c>', self.destroy)
        self.root.after(500, self.check_exit)
        
        self.root.attributes("-alpha", 0.5)

    def check_exit(self) -> None:
        self.root.after(500, self.check_exit)

    def destroy(self) -> None:
        self.root.destroy()

    def update_label(self) -> None:
        wait_time, update_text = self.get_new_text_callback()
        self.caption_text.set(update_text)
        self.root.after(wait_time, self.update_label)
        pass

    def geo_str(self, height, width, x, y) -> str:
        return height + "x" + width + "+" + x + "+" + y

    def set_width(self, width) -> None:
        self.width = str(width)
        self.root.geometry(self.geo_str(self.width, self.height, self.x, self.y))
    
    def set_height(self, height) -> None:
        self.height = str(height)
        self.root.geometry(self.geo_str(self.width, self.height, self.x, self.y))
    
    def set_x(self, x) -> None:
        self.x = str(x)
        self.root.geometry(self.geo_str(self.width, self.height, self.x, self.y))

    def set_y(self, y) -> None:
        self.y = str(y)
        self.root.geometry(self.geo_str(self.width, self.height, self.x, self.y))

    def insert_msg(self, msg) -> None:
        self.msg_q.append(msg)
        if (len(self.msg_q) > 4): self.msg_q.pop(0)


    def run(self) -> None:
        self.caption_text.set(self.initial_text)
        self.root.after(self.initial_delay, self.update_label)
        self.root.mainloop()
