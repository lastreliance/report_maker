import tkinter as tk
import traceback
import os
from functools import reduce

import settings

from typing import List, Tuple, Optional
from os.path import join, isfile

from tkinter import filedialog
from tkinter import messagebox

from tkinter.ttk import Progressbar

from PIL import ImageTk, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm

from container import Container


# add brim to the document


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
        self.scrollbar: tk.Scrollbar = None

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

        self.scrollbar = tk.Scrollbar(frame, orient="vertical")
        self.image_field.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.image_field.yview, bg="black")
        self.scrollbar.pack(side="right", fill="y")

        self.container.expand(select_image, add_folder, delete_image, delete_all, frame, self.image_field,
                              self.scrollbar)

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
        self.container.disable([self.image_field])

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

        bar, progress = self._progressbar_setup(len(images))

        for image in images:
            self.add_image(image)
            self._progressbar_inc(bar, progress, 1)

        self._progressbar_destroy(bar)
        self.window.config(cursor='')
        self.container.enable([self.image_field])

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
        self.container.disable([self.image_field])
        self._image_process()
        self.container.enable([self.image_field])

    @staticmethod
    def _ask_save(filename="output") -> Optional[str]:
        try:
            path = filedialog.asksaveasfile(filetypes=[("PDF-document", ".pdf")],
                                            confirmoverwrite=True,
                                            initialfile=filename + ".pdf")
        except PermissionError:
            messagebox.showerror("Файл занят другой программой.")
            return
        return path.name if path is not None else None

    @staticmethod
    def _get_canvas_scale(image: Image.Image) -> float:
        if image.width > image.height:
            return A4[0] / image.width
        return A4[1] / image.height

    @staticmethod
    def image_scale(image: Image.Image) -> Image.Image:
        if max(image.size) > 2000:
            scale = 1 / (max(image.size) / 2000)
            height = round(image.height * scale)
            width = round(image.width * scale)
            image.thumbnail((width, height))
        return image

    def _image_process(self):
        def get_pos(pic: Image.Image) -> List[int]:
            if pic.height < pic.width:
                return [0, pic.height]
            return [pic.width, 0]

        if not self.images:
            messagebox.showerror("Error", "Выберите хотя бы одно изображение")
            return
        self.window.config(cursor='wait')

        name = self._ask_save()
        if name is None:
            return
        if os.path.isfile(name):
            os.remove(name)
        if not name.endswith(".pdf"):
            name += ".pdf"
        canvas = Canvas(name, pagesize=A4)

        bar, progress = self._progressbar_setup(len(self.images))

        image: Image.Image
        for path in self.images:
            image = Image.open(path)
            self.image_scale(image)
            if image.mode != "RGB":
                image = image.convert(mode='RGB')
            # https://stackoverflow.com/questions/48553162/generate-pdf-using-reportlab-with-custom-size-page-and-best-image-resolution
            scale = self._get_canvas_scale(image)
            canvas.scale(scale, scale)
            canvas.drawImage(ImageReader(image), *get_pos(image))
            canvas.showPage()
            image.close()

            self._progressbar_inc(bar, progress, 1)

        canvas.save()
        self._progressbar_destroy(bar)
        self.window.config(cursor='')
        messagebox.showinfo(message="Success!")

    def _progressbar_setup(self, max_progress: int) -> Tuple[Progressbar, tk.IntVar]:
        if max_progress <= 0:
            raise Exception("max_progress field should be natural number")
        window = tk.Toplevel(self.window, width=500)

        progress = tk.IntVar(window, value=0, name="progress")
        progress_bar = Progressbar(window,
                                   maximum=max_progress,
                                   orient="horizontal",
                                   variable=progress,
                                   value=0,
                                   length=400)
        self.window.eval(f'tk::PlaceWindow {str(window)} center')
        progress_bar.pack()
        window.update()
        return progress_bar, progress

    @staticmethod
    def _progressbar_destroy(bar: Progressbar):
        bar.master.destroy()

    @staticmethod
    def _progressbar_inc(bar: Progressbar, var: tk.IntVar, value: int):
        var.set(var.get() + value)
        bar.master.update_idletasks()

    @staticmethod
    def image_scale(image: Image.Image) -> Tuple[float, float]:
        x, y = image.size
        ratio = x / y
        if ratio > (210 / 297):  # if image is wider than A4
            x *= 297 / y
            y = 297
        else:
            y *= 210 / x
            x = 210

        return x * mm, y * mm


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
