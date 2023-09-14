# classes/Tooltip.py

import tkinter as tk


class ToolTip:
    def __init__(self,
                 widget: tk.Widget,
                 text: str) -> None:
        self.__widget = widget
        self.__text = text
        self.__tooltip = None
        self.__id = None
        self.__x = self.__y = 0
        self.__widget.bind("<Enter>", self.__schedule)
        self.__widget.bind("<Leave>", self.__hide)
        self.__widget.bind("<ButtonPress>", self.__hide)

    def __schedule(self,
                   event: tk.Event = None) -> None:
        self.__x, self.__y, _, _ = self.__widget.bbox("insert")
        self.__x += self.__widget.winfo_rootx() + 25
        self.__y += self.__widget.winfo_rooty() + 25
        self.__id = self.__widget.after(100, self.__show)

    def __show(self,
               event: tk.Event = None) -> None:
        self.__tooltip = tk.Toplevel(self.__widget)
        self.__tooltip.wm_overrideredirect(True)
        self.__tooltip.wm_geometry(f"+{self.__x}+{self.__y}")
        label = tk.Label(self.__tooltip,
                         text=self.__text,
                         background="#fff",
                         relief="solid",
                         borderwidth=1)
        label.pack()

    def __hide(self,
               event: tk.Event = None) -> None:
        if self.__tooltip:
            self.__tooltip.destroy()
        if self.__id:
            self.__widget.after_cancel(self.__id)
        self.__tooltip = None
        self.__id = None
