import tkinter as tk
from typing import List


class Container:
    def __init__(self):
        self.widgets: List[tk.Widget] = list()

    def destroy(self):
        for widget in self.widgets[::-1]:
            widget.destroy()
            self.widgets.pop()

    def add(self, widget: tk.Widget):
        self.widgets.append(widget)

    def hide(self):
        for widget in self.widgets:
            widget.place_info()