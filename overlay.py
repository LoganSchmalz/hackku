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
    def __init__(self, get_new_text_callback):
        self.get_new_text_callback = get_new_text_callback

        self.initial_delay = 10
        self.initial_text = "Caption overlay"

        self.root = tk.Tk()
        self.root.report_callback_exception = report_callback_exception
        self.root.overrideredirect(True)
        self.root.geometry("+700+500")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        self.caption_text = tk.StringVar()
        self.caption_label = tk.Label(self.root, textvariable=self.caption_text, font=('Consolas','28'), fg='white', bg='black')
        self.caption_label.grid(row=0,column=1)

        signal.signal(signal.SIGINT, lambda x,y : self.destroy())
        self.root.bind_all('<Control-c>', self.destroy)
        self.root.after(500, self.check_exit)

    def check_exit(self) -> None:
        self.root.after(500, self.check_exit)

    def destroy(self) -> None:
        self.root.destroy()

    def update_label(self) -> None:
        wait_time, update_text = self.get_new_text_callback()
        self.caption_text.set(update_text)
        self.root.after(wait_time, self.update_label)
        pass

    def run(self) -> None:
        self.caption_text.set(self.initial_text)
        self.root.after(self.initial_delay, self.update_label)
        self.root.mainloop()
