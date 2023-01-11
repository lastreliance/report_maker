import tkinter as tk
import settings


from typing import List

from tkinter import filedialog
from tkinter import messagebox

from PIL import ImageTk, Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from container import Container


class App:
    # noinspection PyTypeChecker
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Report Maker")
        self.window.geometry(settings.geometry)
        self.images: List[str] = list()
        self.container = Container()
        self.image_field: tk.Frame = None
    
    def init_ui(self):

        self.image_field = tk.Frame(self.window, background="grey")
        self.image_field.place(**settings.main_frame_place)

        select_image_button = tk.Button(text="Добавить картинку",
                                        command=self.add_image_with_dialog)
        select_image_button.place(**settings.select_image_button_place)
        self.container.expand(select_image_button, self.image_field)

    def start(self):
        self.init_ui()
        self.window.mainloop()

    def add_image_with_dialog(self):
        if len(self.images) >= settings.max_images_count:
            messagebox.showerror("Error", "Достигнуто максимальное количество картинок.")
            return
        path: str = filedialog.askopenfilename(filetypes=(settings.image_types,))
        self.add_image(path)

    def add_image(self, image: str):
        self.images.append(image)


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()
