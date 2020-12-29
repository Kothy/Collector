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
        self.screen_init()
        self.root.mainloop()

    def canvas_init(self):
        self.root = tk.Tk()
        self.root.title("Zberateľ")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=1280, height=650)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.click)

    def background_set(self):
        image = Image.open("obrazky/bg.jpg")
        image = image.resize((1280, 600), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(image)
        self.bg = self.canvas.create_image(0, 50, image=self.bg_img, anchor='nw')
        image = Image.open("obrazky/panel.jpg")
        image = image.resize((1280, 50), Image.ANTIALIAS)
        self.panel_img = ImageTk.PhotoImage(image)
        self.panel = self.canvas.create_image(0, 0, image=self.panel_img, anchor='nw')

    def screen_init(self):
        self.screen = None
        self.main_menu_screen_init()
        # self.solve_screen_init()
        # self.create_map_screen_init()
        # self.create_set_screen_init()
        # self.create_task_screen_init()

    def main_menu_screen_init(self):
        self.destroy_old_screen()
        self.screen = MenuScreen(self)

    def solve_screen_init(self):
        self.destroy_old_screen()
        self.screen = SolveScreen(self)

    def create_map_screen_init(self):
        self.destroy_old_screen()
        self.screen = CreateMapScreen(self)

    def create_set_screen_init(self):
        self.destroy_old_screen()
        self.screen = CreateTaskSetScreen(self)

    def create_task_screen_init(self, folder, task=None):
        self.screen.hide()
        self.task_screen = CreateTaskScreen(self, folder, task)

    def close_task_screen(self, task):
        self.delete_task_screen()
        if task is not None:
            if task.index is None:
                self.screen.add_task(task)
            else:
                self.screen.task_edited(task)

    def delete_task_screen(self):
        self.task_screen.destroy()
        self.task_screen = None
        self.screen.show()

    def destroy_old_screen(self):
        if self.screen is not None:
            self.screen.destroy()

    def click(self, event):
        print(event.x, event.y)


Collector()
