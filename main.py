import tkinter as tk


class App:
    # noinspection PyTypeChecker
    def __init__(self):
        self.window: tk.Tk = None

    def start(self):
        self.init_ui()
        self.window.mainloop()


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()
