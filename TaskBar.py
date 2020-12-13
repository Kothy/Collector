from CanvasObject import CanvasObject
from CommonFunctions import resize_image
from PIL import Image, ImageTk
from ColorButton import ColorButton
import tkinter as tk

class TaskBar(CanvasObject):

    def __init__(self, parent, folder_name):
        self.parent, self.canvas = parent, parent.canvas
        self.folder_name = folder_name
        self.load_imgs()
        self.void_bar_init()
        self.count_bar_init()
        self.path_bar_init()
        self.parts = [self.void_bar, self.count_bar, self.path_bar]

    def load_imgs(self):
        self.button_imgs = []
        self.bar_imgs = []

        for collectible in 'abcd':
            try:
                img = Image.open('mapy/' + self.folder_name + '/collectibles/' + collectible + '.png')
                img = resize_image(img, 50, 50)
                self.bar_imgs.append(ImageTk.PhotoImage(img))
                img = resize_image(img, 35, 35)
                self.button_imgs.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                break

    def void_bar_init(self):
        self.void_bar = CanvasObject(self, [self.canvas.create_text(380, 580, fill="#0a333f",
                                                                    font=('Comic Sans MS', 20, 'italic bold'),
                                                                    anchor='nw', width=930,
                                                                    text='Pre vyriešenie úlohy '
                                                                         'nie je potrebné nič zozbierať')],
                                     False)

    def count_bar_init(self):
        collectibles_count = len(self.bar_imgs)
        dx = 780 // (collectibles_count - 1)
        self.count_bar = CanvasObject(self, [CountBarItem(self, self.bar_imgs[i], 340 + i*dx, 597, i)
                                             for i in range(collectibles_count)])

    def path_bar_init(self):
        collectibles_count = len(self.bar_imgs)

        buttons = [ImageButton(self, i, self.button_imgs[i]) for i in range(collectibles_count)]
        line = self.canvas.create_line(440, 560, 440, 635, fill='#b6e5da', width=4)

        img = Image.open('obrazky/mouse.png')
        self.mouse_img = ImageTk.PhotoImage(resize_image(img, 60, 110))
        mouse = self.canvas.create_image(1205, 597, image=self.mouse_img, anchor='c')

        img = Image.open('obrazky/controls/clear.png')
        self.clear_img = ImageTk.PhotoImage(resize_image(img, 60, 110))
        clear = self.canvas.create_image(1160, 598, image=self.clear_img, anchor='c')

        self.canvas.tag_bind(clear, '<ButtonPress-1>', self.clear_clicked)

        self.path = Path(self, self.bar_imgs)

        self.path_bar = CanvasObject(self, buttons + [line, mouse, clear, self.path])

    def set_bar(self, type):
        if type == 0:
            self.void_bar.show()
            self.count_bar.hide()
            self.path_bar.hide()
        elif type == 1:
            self.void_bar.hide()
            self.count_bar.show()
            self.path_bar.hide()
        else:
            self.void_bar.hide()
            self.count_bar.hide()
            self.path_bar.show()

    def button_clicked(self, index):
        self.path.add_item(index)

    def clear_clicked(self, _):
        self.path.destroy()

    def get_counts(self):
        return ','.join(item.get_string() for item in self.count_bar.parts)

    def assignment_is_valid(self):
        for item in self.count_bar.parts:
            btn_text = item.get_button_text()
            if btn_text in ('neurčené', 'menej ako'):
                continue
            count = int(item.get_count_text())
            if (btn_text == 'práve' and count > 0) or (btn_text == 'viac ako' and count >= 0):
                return True
        return False

    def fill(self, assignment, type):
        if type == 0:
            return
        if type == 1:
            split = assignment.split(',')
            for i in range(len(split)):
                item = split[i]
                if item[1] == '<':
                    self.count_bar.parts[i].set_item('menej ako', item[2])
                elif item[1] == '>':
                    self.count_bar.parts[i].set_item('viac ako', item[2])
                elif item[2] == '?':
                    self.count_bar.parts[i].set_item('neurčené', '')
                else:
                    self.count_bar.parts[i].set_item('práve', item[2])
        elif type == 2:
            self.path.set_path(assignment)

    def task_bar_changed(self):
        self.parent.task_bar_changed()

class CountBarItem(CanvasObject):

    def __init__(self, parent, img, x, y, index):
        self.parent, self.canvas = parent, parent.canvas
        self.img = img
        self.x, self.y = x, y
        self.index = index
        self.draw_item()

    def draw_item(self):
        self.set_count = tk.StringVar()
        self.set_count_entry = tk.Entry(self.parent.parent.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=2,
                                       justify='center', textvariable=self.set_count)
        rows_entry_window = self.canvas.create_window(self.x+80, self.y, window=self.set_count_entry)
        self.set_count.trace("w", self.set_count_text_changed)

        self.parts = [self.canvas.create_image(self.x-90, self.y, image=self.img, anchor='c'),
                      ColorButton(self, self.x, self.y, 115, 30, 'light_blue', 'neurčené'),
                      CanvasObject(self, [rows_entry_window])]

        self.parts[1].bind_clicked()

    def set_count_text_changed(self, *args):
        count = self.set_count.get()
        if (len(count) > 2 or
                (len(count) > 0 and count[-1] not in '0123456789') or
                (len(count) == 2 and count[0] == '0') or
                (self.get_button_text() == 'menej ako' and len(count) == 1 and count[0] == '0')):
            self.set_count.set(count[:-1])
        else:
            self.parent.task_bar_changed()

    def clicked_btn(self, text):
        self.parent.task_bar_changed()
        if text == 'neurčené':
            self.parts[2].show()
            self.parts[1].change_text('viac ako')
        elif text == 'viac ako':
            self.parts[1].change_text('menej ako')
        elif text == 'menej ako':
            self.parts[1].change_text('práve')
        elif text == 'práve':
            self.parts[2].hide()
            self.parts[1].change_text('neurčené')

    def show(self):
        super(CountBarItem, self).show()
        if self.get_button_text() == 'neurčené':
            self.parts[2].hide()

    def get_string(self):
        word_to_sign = {'neurčené': '=', 'práve': '=', 'viac ako': '>', 'menej ako': '<'}
        return 'abcd'[self.index] + word_to_sign[self.parts[1].text] + \
               ('?' if self.get_button_text() == 'neurčené' else self.set_count.get())

    def set_item(self, button_text, count):
        self.parts[1].change_text(button_text)
        if button_text != 'neurčené':
            self.parts[2].show()
        self.set_count.set(count)

    def get_button_text(self):
        return self.parts[1].text

    def get_count_text(self):
        return self.set_count.get()

class Path(CanvasObject):

    def __init__(self, parent, imgs):
        super(Path, self).__init__(parent, [])
        self.imgs = imgs
        self.path = []

    def add_item(self, index):
        self.parent.task_bar_changed()
        if len(self.path) > 11:
            return
        self.path.append(index)
        self.parts.append(PathBarItem(self, len(self.path)-1, self.imgs[index]))

    def delete_item(self, index):
        self.parts[index].destroy()
        self.parts = self.parts[:index] + self.parts[index+1:]
        self.path = self.path[:index] + self.path[index + 1:]
        for i in range(index, len(self.path)):
            self.parts[i].move(i)

    def destroy(self):
        super(Path, self).destroy()
        self.path = []

    def get_path(self):
        return ''.join(['abcd'[i] for i in self.path])

    def set_path(self, path):
        for char in path:
            self.add_item({'a': 0, 'b': 1, 'c': 2, 'd': 3}[char])

class PathBarItem(CanvasObject):

    def __init__(self, parent, index, img):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.img = img
        self.draw()

    def draw(self):
        self.parts = [self.canvas.create_image(505 + self.index*52, 595, image=self.img, anchor='c')]
        self.canvas.tag_bind(self.parts[0], '<ButtonPress-3>', self.delete)

    def delete(self, _):
        self.parent.delete_item(self.index)

    def move(self, index):
        self.index = index
        self.destroy()
        self.draw()

class ImageButton(CanvasObject):

    def __init__(self, parent, index, image):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.img = image
        self.draw_button()

    def draw_button(self):
        self.parts = [ColorButton(self, 240 + self.index * 55, 595, 50, 50, 'rainbow', ''),
                      self.canvas.create_image(240 + self.index*55, 595,  image=self.img, anchor='c')]
        self.parts[0].bind_clicked()
        self.canvas.tag_bind(self.parts[1], '<ButtonPress-1>', self.clicked_btn)

    def clicked_btn(self, _):
        self.parent.button_clicked(self.index)