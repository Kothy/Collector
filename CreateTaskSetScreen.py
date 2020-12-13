import os
from os import path
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Screen import Screen
from ColorButton import ColorButton
from CanvasObject import CanvasObject
from ObstacleOptions import ObstacleOptions
from Task import Task
from TaskList import TaskList
from Options import Options
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
        self.error_text_init()
        self.tasks_list_init()
        self.objects = [self.panel_obj, self.background_obj, self.name_input_obj, self.map_preview_obj,
                        self.obstacles_obj, self.tasks_obj, self.error_text]

    def panel_init(self):
        task_name_text = self.canvas.create_text(650, 25, fill="#0a333f",
                                                      font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                      width=330, text='Vytváranie sady úloh')
        save_btn = ColorButton(self, 1205, 25, 100, 36, 'violet', 'Ulož')
        menu_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Menu')
        save_btn.bind_clicked()
        menu_btn.bind_clicked()
        self.panel_obj = CanvasObject(self, [task_name_text, save_btn, menu_btn], hidden=False)

    def backgrounds_init(self):
        image = Image.new('RGBA', (570, 580), (255, 170, 79, 100))
        self.left_bg_img = ImageTk.PhotoImage(image)
        left_bg = self.canvas.create_image(45, 60, image=self.left_bg_img, anchor='nw')
        left_bg_border = self.canvas.create_rectangle(45, 60, 615, 640, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (570, 580), (141, 202, 73, 100))
        self.right_bg_img = ImageTk.PhotoImage(image)
        right_bg = self.canvas.create_image(665, 60, image=self.right_bg_img, anchor='nw')
        right_bg_border = self.canvas.create_rectangle(665, 60, 665 + 570, 640, outline='#b6e5da', width=2)

        self.background_obj = CanvasObject(self, [left_bg, left_bg_border, right_bg, right_bg_border], hidden=False)

    def set_name_input_init(self):
        map_name_text = self.canvas.create_text(70, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Názov sady:\n(povolené znaky: písmená, čísla, medzery)')
        self.set_name = tk.StringVar()
        self.set_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=20,
                                       justify='center', textvariable=self.set_name)
        name_entry_window = self.canvas.create_window(345, 95, window=self.set_name_entry)
        self.set_name.trace("w", self.set_name_text_changed)

        self.name_input_obj = CanvasObject(self, [map_name_text, name_entry_window], hidden=False)

    def map_preview_init(self):
        self.preview_object = None

        map_choice_text = self.canvas.create_text(70, 160, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Mapa:')

        image = Image.open('obrazky/plus.png')
        image = image.resize((28, 28), Image.ANTIALIAS)
        self.plus_btn_img = ImageTk.PhotoImage(image)
        plus_map_btn = self.canvas.create_image(150, 163, image=self.plus_btn_img, anchor='nw')

        self.map_file_text = self.canvas.create_text(190, 165, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                     anchor='nw', width=330, text='<-- vyber mapu', state="normal")
        self.canvas.tag_bind(plus_map_btn, '<ButtonPress-1>', self.show_map_preview)

        self.map_preview_obj = CanvasObject(self, [map_choice_text, plus_map_btn, self.map_file_text], hidden=False)

    def obstacles_init(self):
        obstacles_mode_text = self.canvas.create_text(70, 450, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Režimy stráženia:\n(pre prekážky)')
        self.obstacle_options = ObstacleOptions(self)

        self.obstacles_obj = CanvasObject(self, [obstacles_mode_text, self.obstacle_options], False)

    def error_text_init(self):
        self.error_text = self.canvas.create_text(70, 600, fill="darkred",
                                                  font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=530,
                                                  text='',
                                                  state="normal")

    def tasks_list_init(self):
        self.task_list = TaskList(self)
        task_set_text = self.canvas.create_text(690, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Zoznam úloh:')
        plus_task_btn = self.canvas.create_image(850, 82, image=self.plus_btn_img, anchor='nw')
        add_task_help_text = self.canvas.create_text(890, 85, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                     anchor='nw', width=330, text='<-- pridaj úlohu (maximálne 10)')
        self.canvas.tag_bind(plus_task_btn, '<ButtonPress-1>', self.create_task)

        self.task_add_obj = CanvasObject(self, [plus_task_btn, add_task_help_text], False)

        passage_text = self.canvas.create_text(690, 560, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=330, text='Prechod medzi úlohami:')
        self.options = Options(self, 990, 575, ['voľný', 'po vyriešení predošlej'])

        self.tasks_obj = CanvasObject(self, [self.task_list, task_set_text, self.task_add_obj, passage_text,
                                             self.options], False)

    def set_name_text_changed(self, *args):
        if len(self.set_name.get()) > self.SET_NAME_LENGTH:
            self.set_name.set(self.set_name.get()[:-1])
        if len(self.set_name.get()) > 0:
            self.set_error_text('')

    def show_map_preview(self, _):
        folder_name = self.open_browser_map()
        if folder_name is None:
            return
        if not self.map_folder_is_valid(folder_name):
            self.set_error_text('Chyba: Preičinok s mapou nie je validný')
            return
        self.folder_name = folder_name
        self.set_error_text('')
        self.task_list.destroy()
        map_img_path = 'mapy/'+ folder_name + '/map.png'
        self.canvas.itemconfig(self.map_file_text, text=self.split_to_name(folder_name), state="normal")

        if self.preview_object is not None:
            self.preview_object.destroy()
            self.objects = self.objects[:-1]

        image = Image.open(map_img_path)
        image = resize_image(image, 450, 200)
        self.map_preview_img = ImageTk.PhotoImage(image)
        map_preview = self.canvas.create_image(137, 320, image=self.map_preview_img, anchor='w')
        collectibles_imgs = self.show_collectibles(folder_name)
        self.obstacle_options.fill_options(folder_name)
        self.preview_object = CanvasObject(self, [map_preview, collectibles_imgs, self.obstacle_options], False)
        self.objects.append(self.preview_object)

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
                img = Image.open('mapy/' + folder_name + '/collectibles/' + collectible + '.png')
                img = resize_image(img, 32, 32)
                self.collectibles_imgs_tk.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                break

    def create_task(self, _):
        if self.preview_object is None:
            self.set_error_text('Chyba: Pred pridaním úlohy vyber mapu')
            return
        self.set_error_text('')
        self.parent.create_task_screen_init(self.folder_name)

    def add_task(self, task):
        self.task_list.add_task(task)
        if self.task_list.is_full():
            self.task_add_obj.hide()

    def edit_task(self, task):
        self.parent.create_task_screen_init(self.folder_name, task)

    def task_edited(self, task):
        self.task_list.task_edited(task)

    def task_space_freed(self):
        self.task_add_obj.show()

    def save_set(self):
        set_name = self.set_name.get()
        if set_name == '':
            self.set_error_text('Chyba: Pred uložením zadaj názov sady úloh')
            return
        for char in set_name:
            if (char not in '0123456789' and char not in ' aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž' and
                char not in 'aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž'.upper()):
                self.set_error_text('Chyba: Názov sady obsahuje nepovolené znaky')
                return
        if self.task_list.is_empty():
            self.set_error_text('Chyba: Pred uložením pridaj aspoň 1 úlohu')
            return
        self.create_file()
        self.set_error_text('Sada úspešne uložená!')

    def clicked_btn(self, btn_text):
        if btn_text == 'Ulož':
            self.save_set()
        if btn_text == 'Menu':
            self.parent.main_menu_screen_init()

    def set_error_text(self, text):
        self.canvas.itemconfig(self.error_text, text=text)

    def map_folder_is_valid(self, folder_name):
        for subpath in ('/map.png', '/character.png', '/obstacles', '/collectibles/a.png'):
            if not path.exists(os.getcwd()+ '/mapy/' + folder_name + subpath):
                return False
        return True

    def create_file(self):
        set_string = 'Nazov: ' + self.set_name.get() + '\n'
        set_string += 'Mapa: ' + self.folder_name + '\n\n# Nastavenie prekazok #\n'
        for i in range(len(self.obstacle_options.parts)):
            set_string += 'x' if i == 0 else ('y' if i == 1 else 'z')
            guard_mode = self.obstacle_options.parts[i].get_selected_mode()
            set_string += ': ' + ('bod' if guard_mode == 0 else ('kriz' if guard_mode == 1 else 'stvorec')) + '\n'
        set_string += '\n# Ulohy #\n'
        set_string += 'Volny prechod: ' + ('ano' if self.options.checked_index == 0 else 'nie') + '\n\n'

        for i in range(len(self.task_list.tasks)):
            task = self.task_list.tasks[i]
            set_string += str(i+1) + '.\n'
            set_string += 'Nazov: ' + task.name + '\n'
            set_string += 'Typ: ' + ['volna', 'pocty', 'cesta'][task.type] + '\n'
            set_string += 'Rezim: ' + ('planovaci' if task.mode == 'plánovací' else task.mode) + '\n'
            set_string += 'Riadkov: ' + task.row + '\n'
            set_string += 'Stlpcov: ' + task.col + '\n'
            set_string += 'Krokov: ' + task.steps_count + '\n'
            set_string += 'Zadanie: ' + task.assign + '\n'
            set_string += 'Riesitelna: ' + ('ano' if task.solvable else 'nie') + '\n'
            set_string += task.map_str + '\n\n'

        with open('sady_uloh/' + self.set_name.get().replace(' ', '_') + '.txt', 'w', encoding='utf8') as file:
            file.write(set_string)