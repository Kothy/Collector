import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Screen import Screen
from ColorButton import ColorButton
from CanvasObject import CanvasObject
from ObstacleOptions import ObstacleOptions
from Task import Task
from TaskList import TaskList
from CommonFunctions import *
from CreateMapScreen import resize_image_by_height

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
        self.save_btn.bind_clicked()

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
        self.set_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=20,
                                       justify='right', textvariable=self.set_name)
        self.canvas.create_window(345, 95, window=self.set_name_entry)
        self.set_name.trace("w", self.set_name_text_changed)

    def map_preview_init(self):
        self.preview_object = None

        map_choice_text = self.canvas.create_text(70, 160, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Mapa:')

        image = Image.open('obrazky/plus.png')
        image = image.resize((28, 28), Image.ANTIALIAS)
        self.plus_btn_img = ImageTk.PhotoImage(image)
        self.plus_map_btn = self.canvas.create_image(150, 163, image=self.plus_btn_img, anchor='nw')

        self.map_file_text = self.canvas.create_text(190, 165, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                     anchor='nw', width=330, text='<-- vyber mapu', state="normal")
        self.canvas.tag_bind(self.plus_map_btn, '<ButtonPress-1>', self.show_map_preview)

    def obstacles_init(self):
        obstacles_mode_text = self.canvas.create_text(70, 450, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Režimy stráženia:\n(pre prekážky)')
        self.obstacle_options = ObstacleOptions(self)

    def save_text_init(self):
        self.saving_error_text = self.canvas.create_text(70, 600, fill="darkred",
                                                         font=('Comic Sans MS', 17, 'italic bold'),
                                                         anchor='nw', width=530,
                                                         text='',
                                                         state="normal")

    def tasks_list_init(self):
        self.counter = 0
        self.task_list = TaskList(self)
        task_set_text = self.canvas.create_text(690, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Zoznam úloh:')
        self.plus_task_btn = self.canvas.create_image(850, 82, image=self.plus_btn_img, anchor='nw')
        add_task_help_text = self.canvas.create_text(890, 85, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                     anchor='nw', width=330, text='<-- pridaj úlohu')
        self.canvas.tag_bind(self.plus_task_btn, '<ButtonPress-1>', self.add_task)

    def set_name_text_changed(self, *args):
        if len(self.set_name.get()) > self.SET_NAME_LENGTH:
            self.set_name.set(self.set_name.get()[:-1])
        if len(self.set_name.get()) > 0:
            self.hide_error_text()

    def show_map_preview(self, _):
        folder_name = self.open_browser_map()
        if folder_name is None:
            return
        self.hide_error_text()
        self.task_list.destroy()
        self.map_img_path = 'mapy/'+ folder_name + '/map.png'
        self.canvas.itemconfig(self.map_file_text, text=self.split_to_name(folder_name), state="normal")

        if self.preview_object is not None:
            self.preview_object.destroy()

        image = Image.open(self.map_img_path)
        resized_img = resize_image(image, 450, 200)
        self.map_preview_img = ImageTk.PhotoImage(resized_img)
        map_preview = self.canvas.create_image(137, 320, image=self.map_preview_img, anchor='w')
        collectibles_imgs = self.show_collectibles(folder_name)
        self.obstacle_options.fill_options(folder_name)
        self.preview_object = CanvasObject(self, [map_preview, collectibles_imgs, self.obstacle_options], False)

    def open_browser_map(self):
        path = self.open_file_browser()
        if path:
            return path.split("/")[-1]
        return None

    def open_file_browser(self):
        return filedialog.askdirectory(initialdir=os.getcwd()+"/mapy", title="Vyber priečinok")

    def split_to_name(self, text):
        return ' '.join(text.split('_'))

    def show_collectibles(self, folder_name):
        self.create_collectible_imgs(folder_name)
        return CanvasObject(self, [self.canvas.create_image(91, 250 + 50*i, anchor='c',
                                                            image=self.collectibles_imgs_tk[i])
                                               for i in range(len(self.collectibles_imgs_tk))],
                                              hidden=False)

    def create_collectible_imgs(self, folder_name):
        self.collectibles_imgs_tk = []
        for collectible in 'abcd':
            try:
                img = Image.open('mapy/' + folder_name + '/objects/' + collectible + '.png')
                img = resize_image(img, 32, 32)
                self.collectibles_imgs_tk.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                break

    def add_task(self, _):
        if self.preview_object is None:
            self.show_error_text('Chyba: Pred pridaním úlohy vyber mapu')
            return
        self.hide_error_text()
        self.task_list.add_task(Task('parent', 'index', 'Nova Uloha' + str(self.counter), 'pocty', 'oba', 'row', 'col', 'steps', 'assign', 'map_str',
                                     'map_name', 'char_name'))
        self.counter += 1

    def save_set(self):
        if self.set_name.get() == '':
            self.show_error_text('Chyba: Pred uložením zadaj názov sady úloh')
            return
        if self.task_list.is_empty():
            self.show_error_text('Chyba: Pred uložením pridaj aspoň 1 úlohu')
            return
        self.show_error_text('Sada úspešne uložená!')

    def clicked_btn(self, btn_text):
        if btn_text == 'Ulož':
            self.save_set()

    def show_error_text(self, text):
        self.canvas.itemconfig(self.saving_error_text, text=text)

    def hide_error_text(self):
        self.canvas.itemconfig(self.saving_error_text, text='')