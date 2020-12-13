from Screen import Screen
from ColorButton import ColorButton
from CanvasObject import CanvasObject
from Options import Options
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from ObjectList import ObjectList
import os
import threading
import unicodedata

MAP_NAME_LENGTH = 15
CHARACTER_NAME_LENGTH = 10
FILE_TYPES = (("Png files", "*.png"), ("JPG files", "*.jpg"))
ERROR1 = 'Chyba pri ukladaní mapy: nezadaný názov mapy'
ERROR2 = 'Chyba pri ukladaní mapy: nepovolený názov mapy'
ERROR3 = 'Chyba pri ukladaní mapy: nezadaný názov postavičky'
ERROR4 = 'Chyba pri ukladaní mapy: nepovolený názov postavičky'
ERROR5 = 'Chyba pri ukladaní mapy: nezadaný obrázok postaviky'
ERROR6 = 'Chyba pri ukladaní mapy: nezadané pozadie mapy'
ERROR7 = 'Chyba pri ukladaní mapy: nezadané predmety'
ERROR8 = 'Chyba pri ukladaní mapy: nezadané prekážky'


def resize_image_by_width(img, basewidth):
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def resize_image_by_height(img, hsize):
    wpercent = (hsize / float(img.size[1]))
    basewidth = int((float(img.size[0]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


class CreateMapScreen(Screen):
    def __init__(self, parent):
        super(CreateMapScreen, self).__init__(parent)

    def load_screen(self):
        self.map_preview = None
        self.map_preview_img = None
        self.character_preview = None
        self.character_preview_img = None
        self.backgrounds_init()
        self.panel_init()
        self.map_settings_init()
        self.collectibles_init()
        self.obstacles_init()
        self.player_settings_init()

    def panel_init(self):
        self.task_name_text = self.canvas.create_text(650, 25, fill="#0a333f",
                                                      font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                      width=330, text='Vytváranie mapy')
        self.save_btn = ColorButton(self, 1205, 25, 100, 36, 'violet', 'Ulož')
        self.save_btn.bind(self.check_inputs)
        self.menu_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Menu')

        self.menu_btn.bind(self.go_to_menu)

    def go_to_menu(self):
        self.destroy_screen()
        self.parent.main_menu_screen_init()

    def display_error(self, text):
        self.canvas.itemconfig(self.saving_error_text, text=text)
        self.canvas.itemconfig(self.saving_error_text, state=tk.NORMAL)
        if 30 < len(text) < 40:
            self.canvas.itemconfig(self.saving_error_text, font=('Comic Sans MS', 16, 'italic bold'))
        elif len(text) >= 40:
            self.canvas.itemconfig(self.saving_error_text, font=('Comic Sans MS', 15, 'italic bold'))
        else:
            self.canvas.itemconfig(self.saving_error_text, font=('Comic Sans MS', 17, 'italic bold'))

    def check_inputs(self):
        if self.map_name.get() == "":
            self.display_error(ERROR1)

        elif not self.map_name.get().isalnum():
            self.display_error(ERROR2)

        elif self.character_name.get() == "":
            self.display_error(ERROR3)

        elif not self.character_name.get().isalnum():
            self.display_error(ERROR4)

        elif self.canvas.itemcget(self.player_file_text, 'text') == "":
            self.display_error(ERROR5)

        elif self.canvas.itemcget(self.map_file_text, 'text') == "":
            self.display_error(ERROR6)

        elif len(self.collectibles_list.items) < 1:
            self.display_error(ERROR7)

        elif len(self.obstacles_list.items) < 1:
            self.display_error(ERROR8)
        else:
            self.canvas.itemconfig(self.saving_error_text, state=tk.HIDDEN)
            threading.Thread(target=self.save_map, args=(self.map_name.get(),)).start()

    def save_map(self, name):
        dir = "mapy/" + name + "/"
        for path in [dir, dir + "obstacles", dir + "collectibles"]:
            os.mkdir(path)

        while not os.path.isdir(dir):
            pass

        all_obs = "x"
        all_col = "a"

        if len(self.obstacles_list.items) == 2:
            all_obs += ",y"
        elif len(self.obstacles_list.items) == 3:
            all_obs += ",y,z"

        if len(self.collectibles_list.items) == 2:
            all_col += ",b"
        elif len(self.collectibles_list.items) == 3:
            all_col += ",b,c"
        elif len(self.collectibles_list.items) == 4:
            all_col += ",b,c,d"

        text = "Nazov: {}\n\n# Nastavenia postavicky #\nMeno: {}\nOtacanie: {}\nSmerovanie: {}" \
               "\nTrajektoria: {}\n\n# Predmety #\n{}\n\n# Prekazky #\n{}"

        file_txt = text.format(name, strip_accents(self.character_name.get()),
                           strip_accents(self.rotate_options.checkboxes[self.rotate_options.checked_index].text),
                           strip_accents(self.rotated_choices.text), strip_accents(self.path_color_choices.text), all_col, all_obs)

        with open(dir + "map_settings.txt", "w") as file:
            file.write(file_txt)
        self.save_images(name)

    def save_images(self, name):
        dir = "mapy/" + name + "/"
        obstacles_dir = dir + "obstacles"
        objects_dir = dir + "collectibles"
        img_char = Image.open(self.character_img_path)
        img_map = Image.open(self.map_img_path)
        char_filename = "character.png"
        map_filename = "map.png"
        if img_char.size[1] > 200:
            img_char = resize_image_by_height(img_char, 200)

        img_char.save(dir + char_filename)
        img_map.save(dir + map_filename)
        col_names = ["a.png", "b.png", "c.png", "d.png"]
        obs_names = ["x.png","y.png","z.png"]

        for obstacle in self.obstacles_list.items:
            img = Image.open(obstacle.file_path)
            if img.size[1] > 200:
                img = resize_image_by_height(img, 200)
            img.save(obstacles_dir + '/' + obs_names.pop(0))

        for obj in self.collectibles_list.items:
            img = Image.open(obj.file_path)
            if img.size[1] > 200:
                img = resize_image_by_height(img, 200)
            img.save(objects_dir + '/' + col_names.pop(0))

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

    def map_name_text_changed(self, *args):
        if len(self.map_name.get()) > MAP_NAME_LENGTH:
            self.map_name.set(self.map_name.get()[:-1])

    def char_name_text_changed(self, *args):
        if len(self.character_name.get()) > CHARACTER_NAME_LENGTH:
            self.character_name.set(self.character_name.get()[:-1])

    def open_file_browser(self, multiple_files=False):
        if multiple_files:
            return filedialog.askopenfilenames(initialdir="/", title="Select a File", filetypes=FILE_TYPES)
        else:
            return filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=FILE_TYPES)

    def shorten_text(self, text, max_len):
        if len(text) < max_len:
            return text
        while len(text) - 3 > max_len:
            text = self.remove_middle_character(text)

        return text[:len(text) // 2] + "..." + text[len(text) // 2:]

    def remove_middle_character(self, s):
        h = len(s) // 2
        mod = (len(s) + 1) % 2
        return s[:h - mod] + s[h + 1:]

    def open_browser_character(self, _):
        path = self.open_file_browser()
        if path:
            file_name = path.split("/")[-1]
            self.character_img_path = path
            self.canvas.itemconfig(self.player_file_text, text=self.shorten_text(file_name, 15), state="normal")
            if self.character_preview is not None:
                self.canvas.delete(self.character_preview)

            image = Image.open(path)
            resized_img = resize_image_by_height(image, 110)
            self.character_preview_img = ImageTk.PhotoImage(resized_img)
            self.character_preview_img2 = image
            self.character_preview = self.canvas.create_image(440, 170, image=self.character_preview_img, anchor='nw')

    def open_browser_map(self, _):
        path = self.open_file_browser()
        if path:
            file_name = path.split("/")[-1]
            self.map_img_path = path
            self.canvas.itemconfig(self.map_file_text, text=self.shorten_text(file_name, 15), state="normal")
            if self.map_preview is not None:
                self.canvas.delete(self.map_preview)

            image = Image.open(path)
            resized_img = resize_image_by_height(image, 120)
            self.map_preview_img = ImageTk.PhotoImage(resized_img)
            self.map_preview_img2 = image
            self.map_preview = self.canvas.create_image(954, 180, image=self.map_preview_img, anchor='c')

    def open_browser_collectibles(self, _):
        path = self.open_file_browser(multiple_files=True)
        if path and len(path) <= 4 - len(self.collectibles_list.items):
            for item in path:
                self.collectibles_list.add_item(item)

    def open_browser_obstacles(self, _):
        path = self.open_file_browser(multiple_files=True)
        if path and len(path) <= 3 - len(self.obstacles_list.items):
            for item in path:
                self.obstacles_list.add_item(item)

    def map_settings_init(self):
        map_name_text = self.canvas.create_text(70, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Názov mapy:\n(môže obsahovať iba písmená a čísla)')

        # toto treba dokoncit - zarovnat asi doprava, obmedzit dlzku, ziskavat nejako text
        self.character_name = tk.StringVar()
        self.map_name = tk.StringVar()
        self.map_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=20,
                                       justify='right', textvariable=self.map_name)
        self.canvas.create_window(345, 95, window=self.map_name_entry)
        self.char_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 13, 'italic bold'), width=10,
                                        justify="right", textvariable=self.character_name)

        self.map_name.trace("w", self.map_name_text_changed)
        self.character_name.trace("w", self.char_name_text_changed)
        self.canvas.create_window(360, 265, window=self.char_name_entry)

        map_choice_text = self.canvas.create_text(690, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Pozadie mapy:')

        image = Image.open('obrazky/plus.png')
        image = image.resize((28, 28), Image.ANTIALIAS)
        self.plus_btn_img = ImageTk.PhotoImage(image)
        self.plus_btn = self.canvas.create_image(860, 82, image=self.plus_btn_img, anchor='nw')

        self.map_file_text = self.canvas.create_text(900, 85, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                     anchor='nw', width=330, text='', state="hidden")

        self.canvas.tag_bind(self.plus_btn, '<ButtonPress-1>', self.open_browser_map)

        self.saving_error_text = self.canvas.create_text(70, 600, fill="darkred",
                                                         font=('Comic Sans MS', 17, 'italic bold'),
                                                         anchor='nw', width=530,
                                                         text='Chyba pri ukladaní mapy: nezadaný názov',
                                                         state="hidden")

    def collectibles_init(self):
        collectibles_text = self.canvas.create_text(690, 250, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                    anchor='nw', width=330, text='Predmety:\n(max 4)')
        self.plus_btn = self.canvas.create_image(810, 253, image=self.plus_btn_img, anchor='nw')

        self.canvas.tag_bind(self.plus_btn, '<ButtonPress-1>', self.open_browser_collectibles)

        self.collectibles_list = ObjectList(850, 252, self.canvas, [])

    def obstacles_init(self):
        player_settings_text = self.canvas.create_text(690, 460, fill="#0a333f",
                                                       font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                       width=330, text='Prekážky:\n(max 3)')
        self.plus_btn = self.canvas.create_image(810, 463, image=self.plus_btn_img, anchor='nw')
        self.canvas.tag_bind(self.plus_btn, '<ButtonPress-1>', self.open_browser_obstacles)

        self.obstacles_list = ObjectList(850, 462, self.canvas, [])

    def player_settings_init(self):
        player_settings_text = self.canvas.create_text(70, 170, fill="#0a333f",
                                                       font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                       width=330, text='Postavička:')
        self.plus_btn = self.canvas.create_image(205, 173, image=self.plus_btn_img, anchor='nw')
        self.canvas.tag_bind(self.plus_btn, '<ButtonPress-1>', self.open_browser_character)

        self.player_file_text = self.canvas.create_text(245, 176, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                        anchor='nw', width=330, text='', state="hidden")

        name_text = self.canvas.create_text(300, 250, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                            anchor='ne', width=330, text='Meno:')

        rotate_text = self.canvas.create_text(300, 290, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                              anchor='ne', width=330, text='Otáčanie obrázku:\n(pri pohybe)')
        self.rotate_options = Options(self, 330, 308, ['žiadne', 'vľavo/vpravo', 'dole/hore', 'všetky smery'], 0)

        rotated_text = self.canvas.create_text(300, 450, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                               anchor='ne', width=230, text='Otočenie nahratého obrázku postavičky:')

        self.rotated_choices = ColorButton(self, 360, 490, 100, 30, 'light_blue', '-')

        for i in range(len(self.rotate_options.checkboxes)):
            self.rotate_options.checkboxes[i].disable = self.rotated_choices

        self.rotated_choices.bind2()

        self.rotated_choices.change_color("grey")

        path_color__text = self.canvas.create_text(300, 520, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                                   anchor='ne', width=230, text='Farba trajektórie\na mriežky:')
        self.path_color_choices = ColorButton(self, 360, 533, 100, 30, 'light_blue', 'čierna')

        self.path_color_choices.bind(self.trajectory_and_grid_color_changed)

    def trajectory_and_grid_color_changed(self):
        actual_text = self.path_color_choices.text
        color_choices = ["čierna", "biela", "červená", "zelená", "žltá"]
        index = color_choices.index(actual_text)
        index += 1
        if index == len(color_choices):
            index = 0
        self.path_color_choices.change_text(color_choices[index])

    def rotation_changed(self):
        actual_text = self.rotated_choices.text
        color_choices = ["-", "vpravo", "vľavo", "hore", "dole"]
        index = color_choices.index(actual_text)
        index += 1
        if index == len(color_choices):
            index = 0
        self.rotated_choices.change_text(color_choices[index])

    def destroy_screen(self):
        self.canvas.delete("all")
        self.parent.background_set()
