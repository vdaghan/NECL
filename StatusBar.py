# See https://coderslegacy.com/python/create-a-status-bar-in-tkinter/

import tkinter


class StatusBar(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.label = tkinter.Label(self)
        self.label.pack(side=tkinter.LEFT)

    def set(self, newText):
        self.label.config(text=newText)

    def clear(self):
        self.label.config(text="")
