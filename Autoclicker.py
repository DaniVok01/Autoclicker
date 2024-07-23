
import pyautogui
from tkinter import ttk
import tkinter
import threading
import time
import keyboard
from pathlib import Path
import os
import customtkinter as tk


path = Path( __file__ ).parent.absolute()
icon_path = os.path.join(path, "autoclicker.ico")
ablak = tkinter.Tk()
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
class autoclicker:
    def __init__(self) -> None:
        x_tengely = [i for i in range(1,5001)]
        y_tengely = [i for i in range(1,5001)]
        self.intervalllabel = ttk.LabelFrame(ablak, text="Kattintások száma\n")
        self.intervalllabel.grid(row=0, column=0)
        self.intervallentry = tk.CTkEntry(self.intervalllabel, width=100)
        self.intervallentry.grid(row=0,column=0)
        self.intervallentry.insert("end", "10")
        self.speedlabel = ttk.LabelFrame(ablak, text="Kattintás gyakorisága\n")
        self.speedlabel.grid(row=0, column=1)
        self.speedentry = tk.CTkEntry(self.speedlabel, width=100)
        self.speedentry.grid(row=0, column=0)
        self.speedentry.insert("end", "0.1")
        self.coordlabel = ttk.LabelFrame(ablak, text="Kattintás Helye\nX és Y koordináta")
        self.coordlabel.grid(row=0, column=2)
        self.coordxentry = ttk.Combobox(self.coordlabel, width=15, values=x_tengely)
        self.coordxentry.grid(row=0, column=0)
        self.coordyentry = ttk.Combobox(self.coordlabel, width=15, values=y_tengely)
        self.coordyentry.grid(row=1, column=0)
        self.hotkeylabel = ttk.LabelFrame(ablak, text="Hotkeys")        
        self.hotkeylabel.grid(row=1, column=0)
        self.start_hotkey = tk.CTkLabel(self.hotkeylabel, text="Start:  ")
        self.start_hotkey.grid(row=0, column=0)
        self.stop_hotkey = tk.CTkLabel(self.hotkeylabel, text="Stop:  ")
        self.stop_hotkey.grid(row=1, column=0)
        value = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "ctrl+s", "ctrl+v", "ctrl+1", "ctrt+2", "ctrl+3", "ctrl+4", "ctrl+5","ctrl+shift+h"]
        self.start_hotkeys = ttk.Combobox(self.hotkeylabel, values=value, width=15)
        self.start_hotkeys.grid(row=0, column=1)
        self.start_hotkeys.set("F1")
        self.stop_hotkeys = ttk.Combobox(self.hotkeylabel, values=value, width=15)
        self.stop_hotkeys.grid(row=1, column=1)
        self.stop_hotkeys.set("F2")
    def autoclick(self):
        kattintasgyorsasag = None
        self.coordx = None
        self.coordy = None
        kattintasszam = int(self.intervallentry.get()) if self.intervallentry.get().isdigit() else 0
        kattintasgyorsasag = float(self.speedentry.get()) if self.speedentry.get() else 0.1
        self.coordx = int(self.coordxentry.get()) if self.coordxentry.get().isdigit() else None
        self.coordy = int(self.coordyentry.get()) if self.coordyentry.get().isdigit() else None
        global megszakitas
        global fut
        if fut:
            pass
        else:
            fut = True
            while kattintasszam != 0:
                if self.coordx is not None and self.coordy is not None:
                        pyautogui.click(x=self.coordx, y=self.coordy)
                else:
                    pyautogui.click()
                kattintasszam -= 1
                if kattintasgyorsasag:
                    time.sleep(kattintasgyorsasag)
                if kattintasszam == 0 or megszakitas:
                    fut = False
                    break
            fut = False

clicker = autoclicker()
fut = False

def start(event=None):
    global megszakitas
    megszakitas = False
    global fut
    thread = threading.Thread(target=clicker.autoclick)
    thread.start()

def stop(event=None):
    global megszakitas
    megszakitas = True

def start_selected(event=None):
    keyboard.add_hotkey(clicker.start_hotkeys.get(), start)

def stop_selected(event=None):
    keyboard.add_hotkey(clicker.stop_hotkeys.get(), stop)


def remove_hooks(event=None):
    keyboard.remove_all_hotkeys()
    start_selected()
    stop_selected()

ablak.attributes("-topmost", True)
ablak.title(string="autoclicker")
ablak.iconbitmap(icon_path)


start_selected()
stop_selected()
clicker.start_hotkeys.bind("<<ComboboxSelected>>", remove_hooks)
clicker.stop_hotkeys.bind("<<ComboboxSelected>>", remove_hooks)




ablak.maxsize(560,240)
ablak.geometry("560x240")
ablak.mainloop()
