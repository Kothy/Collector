import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Screen import Screen
from ColorButton import ColorButton
from CanvasObject import CanvasObject
from ObstacleOptions import ObstacleOptions
from CreateMapScreen import resize_image_by_height

def resize_image(img, max_width, max_height):
    w_percent = (max_width / float(img.size[0]))
    height = int((float(img.size[1]) * float(w_percent)))
    if height > max_height:
        wpercent = (max_height / float(img.size[1]))
        width = int((float(img.size[0]) * float(wpercent)))
        return img.resize((width, max_height), Image.ANTIALIAS)
        return img.resize((max_width, height), Image.ANTIALIAS)

class CreateTaskSetScreen(Screen):

    SET_NAME_LENGTH = 15

    def load_screen(self):
        self.panel_init()
        self.backgrounds_init()
        self.set_name_input_init()
        self.map_preview_init()
        self.obstacles_init()
        self.save_text_init()
        self.tasks_list_init()

    def panel_init(self):
        self.task_name_text = self.canvas.create_text(650, 25, fill="#0a333f",
                                                      font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                      width=330, text='Vytváranie sady úloh')
        self.save_btn = ColorButton(self, 1205, 25, 100, 36, 'violet', 'Ulož')
        self.menu_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Menu')

    def backgrounds_init(self):
        image = Image.new('RGBA', (570, 580), (255, 170, 79, 100))
        self.left_bg_img = ImageTk.PhotoImage(image)
        left_bg = self.canvas.create_image(45, 60, image=self.left_bg_img, anchor='nw')
        left_bg_border = self.canvas.create_rectangle(45, 60, 615, 640, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (570, 580), (141, 202, 73, 100))
        self.right_bg_img = ImageTk.PhotoImage(image)
        right_bg = self.canvas.create_image(665, 60, image=self.right_bg_img, anchor='nw')
        right_bg_border = self.canvas.create_rectangle(665, 60, 665 + 570, 640, outline='#b6e5da', width=2)

        self.background = CanvasObject(self, [left_bg, left_bg_border, right_bg, right_bg_border], hidden=False)

    def set_name_input_init(self):
        map_name_text = self.canvas.create_text(70, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Názov sady:\n(môže obsahovať iba písmená a čísla)')
        self.set_name = tk.StringVar()
        self.set_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=13,
                                       justify='right', textvariable=self.set_name)
        self.canvas.create_window(305, 95, window=self.set_name_entry)
        self.set_name.trace("w", self.set_name_text_changed)

    def map_preview_init(self):
        self.map_preview = None

        map_choice_text = self.canvas.create_text(70, 160, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Mapa:')

        image = Image.open('obrazky/plus.png')
        image = image.resize((28, 28), Image.ANTIALIAS)
        self.plus_btn_img = ImageTk.PhotoImage(image)
        self.plus_btn = self.canvas.create_image(150, 163, image=self.plus_btn_img, anchor='nw')

        self.map_file_text = self.canvas.create_text(190, 165, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                     anchor='nw', width=330, text='<-- vyber mapu', state="normal")
        self.canvas.tag_bind(self.plus_btn, '<ButtonPress-1>', self.show_map_preview)

    def obstacles_init(self):
        obstacles_mode_text = self.canvas.create_text(70, 450, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Režimy stráženia:')
        self.obstacle_options = ObstacleOptions()

    def save_text_init(self):
        self.saving_error_text = self.canvas.create_text(70, 600, fill="darkred",
                                                         font=('Comic Sans MS', 17, 'italic bold'),
                                                         anchor='nw', width=530,
                                                         text='Chyba pri ukladaní sady: nezadaný názov',
                                                         state="normal")

    def tasks_list_init(self):
        pass

    def set_name_text_changed(self, *args):
        if len(self.set_name.get()) > self.SET_NAME_LENGTH:
            self.set_name.set(self.set_name.get()[:-1])

    def show_map_preview(self, _):
        folder_name = self.open_browser_map()
        if folder_name is None:
            return
        self.map_img_path = 'mapy/'+ folder_name + '/map.png'
        self.canvas.itemconfig(self.map_file_text, text=self.split_to_name(folder_name), state="normal")

        if self.map_preview is not None:
            self.canvas.delete(self.map_preview)

        image = Image.open(self.map_img_path)
        resized_img = resize_image(image, 500, 200)
        self.map_preview_img = ImageTk.PhotoImage(resized_img)
        self.map_preview = self.canvas.create_image(330, 320, image=self.map_preview_img, anchor='c')
        self.obstacle_options.fill_options(folder_name)

    def open_browser_map(self):
        path = self.open_file_browser()
        if path:
            return path.split("/")[-1]
        return None

    def open_file_browser(self):
        return filedialog.askdirectory(initialdir=os.getcwd()+"/mapy", title="Vyber priečinok")

    def split_to_name(self, text):
        return ' '.join(text.split('_'))
