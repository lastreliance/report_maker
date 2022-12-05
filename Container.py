import tkinter as tk
from typing import List


class Container:
    def __init__(self):
        self.widgets: List[tk.Widget] = list()
        self.places: List[tuple] = list()

    def destroy(self):
        for widget in self.widgets[::-1]:
            widget.destroy()
            self.widgets.pop()

    def add(self, widget: tk.Widget):
        self.widgets.append(widget)
        info = widget.place_info()
        self.places.append((int(info['x']), int(info['y'])))

    def hide(self):
        for i in range(len(self.widgets)):
            self.places[i] = self.widgets[i].place_info()
            self.widgets[i].place_forget()

    def show(self):



class WindowContainer:
    def __init__(self):
        self.widgets: List[tk.Toplevel] = list()

    def add(self, window: tk.Toplevel):
        self.widgets.append(window)

    def destroy(self):
        for widget in self.widgets[::-1]:
            widget.destroy()
            self.widgets.pop()
