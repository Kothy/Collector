import Screen as screen
import ColorButton as cb
import CanvasObject as co
import Option as opt
from PIL import Image, ImageTk
import tkinter as tk

class CreateMapScreen(screen.Screen):
    def __init__(self, parent):
        super(CreateMapScreen, self).__init__(parent)

    def load_screen(self):
        self.backgrounds_init()
        self.panel_init()
        self.map_settings_init()
        self.collectibles_init()
        self.obstacles_init()
        self.player_settings_init()

    def panel_init(self):
        self.task_name_text = self.canvas.create_text(650, 25, fill="#0a333f",
                                                      font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                      width=330, text='Vytvaranie mapy')
        self.save_btn = cb.ColorButton(self, 1205, 25, 100, 36, 'violet', 'Ulož')
        self.menu_btn = cb.ColorButton(self, 75, 25, 100, 36, 'green3', 'Menu')

    def backgrounds_init(self):
        image = Image.new('RGBA', (570, 580), (255, 170, 79, 100))
        self.left_bg_img = ImageTk.PhotoImage(image)
        left_bg = self.canvas.create_image(45, 60, image=self.left_bg_img, anchor='nw')
        left_bg_border = self.canvas.create_rectangle(45, 60, 615, 640, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (570, 580), (141, 202, 73, 100))
        self.right_bg_img = ImageTk.PhotoImage(image)
        right_bg = self.canvas.create_image(665, 60, image=self.right_bg_img, anchor='nw')
        right_bg_border = self.canvas.create_rectangle(665, 60, 665 + 570, 640, outline='#b6e5da', width=2)

        self.background = co.CanvasObject(self, [left_bg, left_bg_border, right_bg, right_bg_border], hidden=False)

    def map_settings_init(self):
        map_name_text = self.canvas.create_text(70, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Názov mapy:\n(môže obsahovať iba písmená a čísla)')
        # toto treba dokoncit - zarovnat asi doprava, obmedzit dlzku, ziskavat nejako text, mozes pouzit aj ine objekty ako tk.Entry kludne
        name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=20)
        self.canvas.create_window(345, 95, window=name_entry)

        map_choice_text = self.canvas.create_text(690, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                  anchor='nw', width=330, text='Pozadie mapy:')

        image = Image.open('obrazky/plus.png')
        image = image.resize((28, 28), Image.ANTIALIAS)
        self.plus_btn_img = ImageTk.PhotoImage(image)
        self.plus_btn = self.canvas.create_image(860, 82, image=self.plus_btn_img, anchor='nw')

        map_file_text = self.canvas.create_text(900, 85, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                anchor='nw', width=330, text='tu_by_bol_nazov_filu.jpg')

        saving_error_text = self.canvas.create_text(70, 600, fill="darkred", font=('Comic Sans MS', 17, 'italic bold'),
                                                    anchor='nw', width=530,
                                                    text='Chyba pri ukladaní mapy: nezadaný názov')

    def collectibles_init(self):
        collectibles_text = self.canvas.create_text(690, 250, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                    anchor='nw', width=330, text='Predmety:\n(max 4)')
        self.plus_btn = self.canvas.create_image(810, 253, image=self.plus_btn_img, anchor='nw')

    def obstacles_init(self):
        player_settings_text = self.canvas.create_text(690, 460, fill="#0a333f",
                                                       font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                       width=330, text='Prekážky:\n(max 3)')
        self.plus_btn = self.canvas.create_image(810, 463, image=self.plus_btn_img, anchor='nw')

    def player_settings_init(self):
        player_settings_text = self.canvas.create_text(70, 170, fill="#0a333f",
                                                       font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                       width=330, text='Postavička:')
        self.plus_btn = self.canvas.create_image(205, 173, image=self.plus_btn_img, anchor='nw')
        player_file_text = self.canvas.create_text(245, 176, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                   anchor='nw', width=330, text='tu_by_bol_nazov_filu.jpg')

        name_text = self.canvas.create_text(300, 250, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                            anchor='ne', width=330, text='Meno:')
        # toto treba dokoncit - zarovnat asi doprava, obmedzit dlzku, ziskavat nejako text, mozes pouzit aj ine objekty ako tk.Entry kludne
        name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 13, 'italic bold'), width=10)
        self.canvas.create_window(360, 265, window=name_entry)

        rotate_text = self.canvas.create_text(300, 290, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                              anchor='ne', width=330, text='Otáčanie obrázku:\n(pri pohybe)')
        self.rotate_options = opt.Options(self, 330, 308, ['vobec', 'vlavo/vpravo', 'dole/hore', 'vsetky smery'], 0)

        rotated_text = self.canvas.create_text(300, 450, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                               anchor='ne', width=230, text='Otočenie nahratého obrázku postavičky:')
        self.rotated_choices = cb.ColorButton(self, 360, 490, 100, 30, 'light_blue', 'vpravo')

        path_color__text = self.canvas.create_text(300, 520, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                                   anchor='ne', width=230, text='Farba trajektórie:')
        self.path_color_choices = cb.ColorButton(self, 360, 533, 100, 30, 'light_blue', 'čierna')