from PIL import ImageTk
from CommonFunctions import *
from Player import Player
from MapParts import Blank, Collectible, Obstacle


PART_W = 0
PART_H = 0
ALPHA = 100


class Map:
    def __init__(self, name, string, canvas, task, grid_col):
        self.name = name
        self.map_string = string
        self.canvas = canvas
        self.task = task
        self.array = []
        self.grid_col = grid_col
        self.rows, self.cols = 0, 0
        w, h = self.task.map_bg_w, self.task.map_bg_h
        # self.width = self.task.map_bg_w - 5
        # self.height = self.task.map_bg_h - 5
        self.width = w - 5
        self.height = h - 5

        self.trajectory_col = self.task.trajectory_color
        self.read_map()

    def find_guarding(self, name):
        for guard in self.task.parent.obstacles_arr:
            if guard[0] == name:
                return guard[1]
        return ""

    def read_map(self):
        lines = self.map_string.split("\n")
        if lines[-1] == "":
            lines.pop(-1)

        self.rows = len(lines)
        self.cols = len(lines[0])
        self.do_grid2()

        self.calculate_dims2()
        arr = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == ".":
                    obj = Blank(self, i, j)
                elif lines[i][j] == "x" or lines[i][j] == "y" or lines[i][j] == "z":
                    obj = Obstacle(lines[i][j], self, self.find_guarding(lines[i][j]), i, j)
                elif lines[i][j] == "a" or lines[i][j] == "b" or lines[i][j] == "c" or lines[i][j] == "d":
                    obj = Collectible(lines[i][j], self, i, j)
                else:
                    self.player = Player(self, i, j)
                    obj = Blank(self, i,j)

                arr[i][j] = obj

        self.array = arr

        for i in range(len(lines)):
            for j in range(len(lines[i])):

                if isinstance(self.array[i][j], Obstacle):
                    for a, b in self.array[i][j].get_guarded():
                        self.array[a][b].guarded = True

    def remove(self):
        for line in self.grid_lines:
            self.canvas.delete(line)

        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                self.array[i][j].remove()

        for trajectory in self.player.trajectory:
            self.canvas.delete(trajectory[4])

        self.player.remove()

    def calculate_dims2(self):
        global PART_W, PART_H

        PART_H = int(self.height / self.rows)
        PART_W = int(self.width / self.cols)

        self.part_h = PART_H
        self.part_w = PART_W

        image2 = Image.open("obrazky/guarding.png")

        image2 = image2.resize((PART_W - 6, PART_H - 6))
        self.guarding_img = ImageTk.PhotoImage(image2)
        image3 = Image.open("obrazky/guarding_x.png")
        image3 = resize_image(image3, int((PART_W - 6)/4.5), int((PART_H - 6)/4.5))
        self.guarding_img_x = ImageTk.PhotoImage(image3)

    def do_grid2(self):
        one_row = (self.height) / self.rows
        one_col = (self.width) / self.cols

        y = 300 - (self.height / 2)
        xs = []
        ys = []
        for row in range(self.rows + 1):
            ys.append(y + (one_row/2))
            y += one_row

        x = 460 - (self.width / 2)
        for row in range(self.cols + 1):
            xs.append(x + (one_col/2))
            x += one_col

        self.xs = ys
        self.ys = xs

    def draw_grid2(self):
        one_row = (self.height) / self.rows
        one_col = self.width / self.cols
        self.grid_lines = []

        x1 = 460 - (self.width / 2)
        x2 = 460 + (self.width / 2)
        y = 300 - (self.height / 2)
        for row in range(self.rows + 1):
            self.grid_lines.append(self.canvas.create_line(x1, y, x2, y, width=5, fill=self.grid_col))
            y += one_row

        x = 460 - ((self.width) / 2)
        y1 = 300 - ((self.height) / 2)
        y2 = 300 + ((self.height) / 2)
        for row in range(self.cols + 1):
            self.grid_lines.append(self.canvas.create_line(x, y1, x, y2, width=5, fill=self.grid_col))
            x += one_col

    def draw_objects(self):
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                self.array[i][j].draw()

        self.player.draw()

    def draw_guards(self):
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                if isinstance(self.array[i][j], Blank) and self.array[i][j].guarded:
                    self.array[i][j].draw_guard()

    def draw_map(self):
        self.draw_grid2()
        self.player.draw_full_trajectory()
        self.draw_objects()
