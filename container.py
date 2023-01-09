import tkinter as tk
from typing import List, Tuple, Iterable


class Container:
    def __init__(self):
        self.widgets: List[tk.Widget] = list()
        self.places: List[Tuple[int, int]] = list()

    def destroy(self):
        for widget in self.widgets[::-1]:
            widget.destroy()
            self.widgets.pop()

    def add(self, widget: tk.Widget):
        self.widgets.append(widget)
        info = widget.place_info()
        # self.places.append((int(info['x']), int(info['y'])))

    def expand(self, *widgets: tk.Widget):
        for widget in widgets:
            self.add(widget)

    def hide(self):
        for i in range(len(self.widgets)):
            self.places[i] = Container.get_position(self.widgets[i])
            self.widgets[i].place_forget()

    @staticmethod
    def get_position(widget: tk.Widget) -> Tuple[int, int]:
        data = widget.place_info()
        return int(data.get("x")), int(data.get("y"))


class WindowContainer:
    def __init__(self):
        self.widgets: List[tk.Toplevel] = list()

    def add(self, window: tk.Toplevel):
        self.widgets.append(window)

    def destroy(self):
        for widget in self.widgets[::-1]:
            widget.destroy()
            self.widgets.pop()
