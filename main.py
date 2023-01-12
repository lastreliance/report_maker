import tkinter as tk
import traceback
import os

import settings

from typing import List
from os.path import join, isfile

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
        self.window.config(background="blue")
        self.window.geometry(settings.geometry)
        self.images: List[str] = list()
        self.container = Container()
        self.image_field: tk.Text = None

    def init_ui(self):
        frame = tk.Frame(self.window)
        self.image_field = tk.Text(frame, bg="green", fg="black", state="disabled", **settings.main_frame_size)
        frame.place(x=38, y=38)

        select_image = tk.Button(text="Добавить картинку",
                                 command=self.add_image_with_dialog,
                                 width=settings.button_width,
                                 height=2)
        select_image.place(x=540, y=38)

        add_folder = tk.Button(text="Выбрать папку",
                               command=self.add_folder,
                               width=settings.button_width,
                               height=2)
        add_folder.place(x=540, y=110)

        delete_image = tk.Button(text="Удалить картинку",
                                 command=self.delete_image,
                                 width=settings.button_width,
                                 height=2)
        delete_image.place(x=540, y=276)

        delete_all = tk.Button(text="Удалить всё",
                               command=self.delete_all,
                               width=settings.button_width,
                               height=2)
        delete_all.place(x=540, y=348)

        delete_all = tk.Button(text="Начать",
                               command=self.image_process,
                               width=settings.button_width,
                               height=4)
        delete_all.place(x=540, y=473)

        self.container.expand(select_image, add_folder, delete_image, delete_all, frame, self.image_field)

    def start(self):
        self.init_ui()
        self.window.mainloop()

    def add_image_with_dialog(self):
        if len(self.images) >= settings.max_images_count:
            messagebox.showerror("Error", "Достигнуто максимальное количество картинок.")
            return
        path: str = filedialog.askopenfilename(filetypes=(settings.image_types,))
        self.add_image(path)

    def add_image(self, path: str):
        self.images.append(path)
        image = Image.open(path)
        image.thumbnail(settings.image_show_size, 1)

    def select_folder(self):
        path: str = filedialog.askdirectory()
        images: List[str] = list()
        for obj in sorted(os.listdir(path)):
            filename = join(path, obj)
            if isfile(filename):
                if any(obj.endswith(end) for end in settings.image_types):
                    images.append(filename)

        if len(images) >= settings.max_images_count:
            messagebox.showerror("Error", "Достигнуто максимальное количество картинок.")
            return
        for image in images:
            self.add_image(image)


def main():
    try:
        app = App()
        app.start()
    except Exception as exc:
        if exc:
            pass
        with open('log.txt', 'w') as file:
            file.write(traceback.format_exc())


if __name__ == "__main__":
    main()
