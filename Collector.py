import tkinter as tk
from PIL import ImageTk, Image
from SolveScreen import SolveScreen
from MenuScreen import MenuScreen
from CreateTaskScreen import CreateTaskScreen
from CreateMapScreen import CreateMapScreen
from CreateTaskSetScreen import CreateTaskSetScreen


class Collector:
    def __init__(self):
        self.canvas_init()
        self.background_set()
        self.screens_init()
        self.root.mainloop()

    def canvas_init(self):
        self.root = tk.Tk()
        self.root.title("Zberateľ")
        ##        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=1300, height=650)
        self.canvas.pack()

    def background_set(self):
        image = Image.open("obrazky/bg.jpg")
        image = image.resize((1300, 600), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(image)
        self.bg = self.canvas.create_image(0, 50, image=self.bg_img, anchor='nw')
        image = Image.open("obrazky/panel.jpg")
        image = image.resize((1300, 50), Image.ANTIALIAS)
        self.panel_img = ImageTk.PhotoImage(image)
        self.panel = self.canvas.create_image(0, 0, image=self.panel_img, anchor='nw')

    def screens_init(self):
        # funckia na testovanie screenov, nebude vo finalnej verzii - odkomentuj, ktoru screen chces robit, ostatne zakomentuj
        # self.main_menu_screen_init()
        # self.solve_screen_init()
        self.create_map_screen_init()
        # self.create_set_screen_init()
        # self.create_task_screen_init()

    def main_menu_screen_init(self):
        self.menu_screen = MenuScreen(self)

    def solve_screen_init(self):
        self.solve_screen = SolveScreen(self)

    def create_map_screen_init(self):
        self.create_map_screen = CreateMapScreen(self)

    def create_set_screen_init(self):
        self.create_set_screen = CreateTaskSetScreen(self)

    def create_task_screen_init(self):
        self.creat_task_screen = CreateTaskSetScreen(self)


Collector()
