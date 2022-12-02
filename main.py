import tkinter as tk
import settings

from container import Container


class App:
    # noinspection PyTypeChecker
    def __init__(self):
        self.window: tk.Tk = None
        self.containers: List[Container] = list()
    
    def init_ui(self):
        self.window = tk.Tk()
        self.window.geometry = settings.geometry
        self.containers = [Container()]

    def start(self):
        self.init_ui()
        self.window.mainloop()


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()
