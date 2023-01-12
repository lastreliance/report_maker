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
from reportlab.lib.units import cm

from container import Container


class App:
    loaded_images: List[ImageTk.PhotoImage] = list()

    # noinspection PyTypeChecker
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry(settings.geometry)
        self.window.update_idletasks()
        self.images: List[str] = list()
        self.container = Container()
        self.image_field: tk.Text = None

    def init_ui(self):
        self.container.destroy()
        frame = tk.Frame(self.window)
        self.image_field = tk.Text(frame, bg="green", fg="black", state="disabled", **settings.main_frame_size)
        self.image_field.pack(side="left")
        frame.place(x=38, y=38)

        select_image = tk.Button(text="Добавить картинку",
                                 command=self.add_image_with_dialog,
                                 width=settings.button_width,
                                 height=2)
        select_image.place(x=540, y=38)

        add_folder = tk.Button(text="Выбрать папку",
                               command=self.select_folder,
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
                               height=4,
                               font=("Calibri", 12))
        delete_all.place(x=540, y=473)

        self.container.expand(select_image, add_folder, delete_image, delete_all, frame, self.image_field)

    def start(self):
        self.init_ui()
        self.window.mainloop()

    def update_image_field(self):
        self.window.config(cursor='wait')
        self.image_field.config(state='normal')
        self.image_field.delete('1.0', 'end')

        for image in self.loaded_images:
            self.image_field.insert('end', ' ')
            self.image_field.image_create('end', image=image)
            self.image_field.insert('end', '\n\n')

        self.image_field.see('end')
        self.image_field.config(state='disabled')
        self.window.config(cursor='')

    def add_image_with_dialog(self):
        if len(self.images) >= settings.max_images_count:
            messagebox.showerror("Error", "Достигнуто максимальное количество картинок.")
            return
        path: str = filedialog.askopenfilename(filetypes=(settings.image_types,))
        self.add_image(path)

    def add_image(self, path: str):
        if not path:
            return
        self.images.append(path)

        image = Image.open(path)
        blank = Image.open("images/blank_A4.jpg")
        image.thumbnail(settings.image_show_size, 1)
        blank.paste(image)
        App.loaded_images.append(ImageTk.PhotoImage(blank))

        self.update_image_field()

    def select_folder(self):
        path: str = filedialog.askdirectory()
        if not path:
            self.window.config(cursor='')
            return
        self.window.config(cursor='wait')
        images: List[str] = list()
        for obj in sorted(os.listdir(path)):
            filename = join(path, obj)
            if isfile(filename):
                if any(obj.endswith(end[1:]) for end in settings.image_formats):
                    images.append(filename)

        if len(images) >= settings.max_images_count:
            messagebox.showerror("Error", "Достигнуто максимальное количество картинок.")
            self.window.config(cursor='')
            return
        for image in images:
            self.add_image(image)
        self.window.config(cursor='')

    def delete_image(self):
        if not self.images:
            return
        self.images.pop()
        App.loaded_images.pop()
        self.update_image_field()

    def delete_all(self):
        self.images.clear()
        App.loaded_images.clear()
        self.update_image_field()

    def image_process(self):
        def get_pos(pic: Image.Image) -> List[int]:
            if pic.size[1] < A4[1]:
                return [0, 29.7 * cm - pic.size[1]]
            return [21 * cm - pic.size[0], 0]

        if not self.images:
            messagebox.showerror("Error", "Выберите хотя бы одно изображение")
            return
        self.window.config(cursor='wait')
        try:
            path = filedialog.asksaveasfile(filetypes=[("PDF-document", ".pdf")],
                                            confirmoverwrite=True,
                                            initialfile="filename.pdf")
        except PermissionError:
            messagebox.showerror("Файл занят другой программой.")
            return
        if path is None:
            return
        canvas = Canvas(path.name, pagesize=A4)
        image: Image.Image
        for path in self.images:
            image = Image.open(path)
            image.thumbnail(A4)
            # image = image.convert(mode='RGB')
            filepath = os.getcwd() + '\\image.jpg'
            image.save(filepath)

            canvas.drawInlineImage(filepath, *get_pos(image))
            canvas.showPage()
            os.remove(filepath)

        canvas.save()
        self.window.config(cursor='')


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
