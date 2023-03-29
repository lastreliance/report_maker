import tkinter as tk
from typing import List, Tuple, Iterable, Optional, Union


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

    def disable(self, exceptions: Optional[List[tk.Widget]] = None):
        self._set_state("disabled", exceptions)

    def _set_state(self, state: str, exceptions: Optional[List[tk.Widget]] = None):
        type_exc = [tk.Frame, tk.Scrollbar]
        if exceptions is None:
            exceptions = list()
        for widget in self.widgets:
            if widget not in exceptions:
                if type(widget) not in type_exc:
                    widget['state'] = state

    def enable(self, exceptions: Optional[List[tk.Widget]] = None):
        self._set_state("normal", exceptions)

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
