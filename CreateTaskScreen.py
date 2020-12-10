from Screen import Screen
from PIL import Image, ImageTk
from CanvasObject import CanvasObject
from ColorButton import ColorButton
from Options import Options
import tkinter as tk

class CreateTaskScreen(Screen):

    SET_NAME_LENGTH = 28

    def __init__(self, parent):
        super(CreateTaskScreen, self).__init__(parent)

    def load_screen(self):
        self.panel_init()
        self.error_text_init()
        self.backgrounds_init()
        self.task_name_init()
        self.task_type_init()
        self.task_objects_init()
        self.map_sizes_init()
        self.map_init()
        self.task_bar_init()

    def panel_init(self):
        task_name_text = self.canvas.create_text(650, 25, fill="#0a333f",
                                                 font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                 width=330, text='Vytváranie úlohy')
        save_btn = ColorButton(self, 1205, 25, 100, 36, 'violet', 'Ulož')
        back_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Späť')
        save_btn.bind_clicked()
        back_btn.bind_clicked()
        self.panel_obj = CanvasObject(self, [task_name_text, save_btn, back_btn], hidden=False)

    def backgrounds_init(self):
        image = Image.new('RGBA', (670, 480), (255, 170, 79, 100))
        self.left_bg_img = ImageTk.PhotoImage(image)
        left_bg = self.canvas.create_image(45, 60, image=self.left_bg_img, anchor='nw')
        left_bg_border = self.canvas.create_rectangle(45, 60, 715, 540, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (470, 480), (141, 202, 73, 100))
        self.right_bg_img = ImageTk.PhotoImage(image)
        right_bg = self.canvas.create_image(765, 60, image=self.right_bg_img, anchor='nw')
        right_bg_border = self.canvas.create_rectangle(765, 60, 665 + 570, 540, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (665 + 570 - 45, 75), (141, 202, 73, 100))
        self.bottom_bg_img = ImageTk.PhotoImage(image)
        right_bg = self.canvas.create_image(45, 560, image=self.bottom_bg_img, anchor='nw')
        bottom_bg_border = self.canvas.create_rectangle(45, 560, 665 + 570, 635, outline='#b6e5da', width=2)

        self.background_obj = CanvasObject(self,
                                           [left_bg, left_bg_border, right_bg, right_bg_border, bottom_bg_border],
                                           hidden=False)

    def task_name_init(self):
        task_name_text = self.canvas.create_text(70, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Názov úlohy:')
        self.set_name = tk.StringVar()
        self.set_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=38,
                                       justify='right', textvariable=self.set_name)
        name_entry_window = self.canvas.create_window(455, 95, window=self.set_name_entry)
        self.set_name.trace("w", self.set_name_text_changed)

        self.name_input_obj = CanvasObject(self, [task_name_text, name_entry_window], hidden=False)

    def task_type_init(self):
        task_type_text = self.canvas.create_text(790, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Typ úlohy:')
        self.task_type_options = Options(self, 935, 98, ['voľná', 'počty', 'postupnosť'])

        task_mode_text = self.canvas.create_text(790, 200, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Povolený režim:')

    def task_objects_init(self):
        self.collectibles_text = self.canvas.create_text(790, 390, fill="#0a333f",
                                                      font=('Comic Sans MS', 17, 'italic bold'),
                                                      anchor='nw', width=530,
                                                      text='Predmety:')
        self.collectibles = None

        self.obstacles_text = self.canvas.create_text(790, 440, fill="#0a333f",
                                                      font=('Comic Sans MS', 17, 'italic bold'),
                                                      anchor='nw', width=530,
                                                      text='Prekážky:')
        self.obstacles = None

        self.character_text = self.canvas.create_text(790, 490, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Postavička:')
        self.character = None

    def map_sizes_init(self):
        rows_text = self.canvas.create_text(70, 120, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Počet riadkov:')
        self.set_rows = tk.StringVar()
        self.set_rows_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=38,
                                       justify='right', textvariable=self.set_rows)
        name_entry_window = self.canvas.create_window(455, 95, window=self.set_rows_entry)
        # self.set_name.trace("w", self.set_count_text_changed)

        self.name_input_obj = CanvasObject(self, [rows_text, name_entry_window], hidden=False)

    def map_init(self):
        pass

    def task_bar_init(self):
        pass

    def error_text_init(self):
        self.error_text = self.canvas.create_text(70, 600, fill="darkred",
                                                  font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=530,
                                                  text='',
                                                  state="normal")

    def set_name_text_changed(self, *args):
        if len(self.set_name.get()) > self.SET_NAME_LENGTH:
            self.set_name.set(self.set_name.get()[:-1])
        if len(self.set_name.get()) > 0:
            self.set_error_text('')

    # def set_count_text_changed(self, *args):
    #     if len(self.set_name.get()) > 1 or self.:
    #         self.set_name.set(self.set_name.get()[:-1])
    #     if len(self.set_name.get()) > 0:
    #         self.set_error_text('')

    def set_error_text(self, text):
        self.canvas.itemconfig(self.error_text, text=text)