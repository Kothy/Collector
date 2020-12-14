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
        self.read_map()

    def calculate_dims(self):
        global PART_W, PART_H

        PART_H = int(480 / self.rows)
        PART_W = int(900 / self.cols)

        self.part_h = PART_H
        self.part_w = PART_W

        image2 = Image.open("obrazky/guarding.png")

        image2 = resize_image(image2, PART_W, PART_H)
        self.guarding_img = ImageTk.PhotoImage(image2)

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
        self.do_grid()

        self.calculate_dims()
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

    def do_grid(self):
        one_row = 480 / self.rows
        one_col = 900 / self.cols

        y = 60
        xs = []
        ys = []
        for row in range(self.rows + 1):
            ys.append(y + (one_row/2))
            y += one_row

        x = 10
        for row in range(self.cols + 1):
            xs.append(x + (one_col/2))
            x += one_col

        self.xs = ys
        self.ys = xs

    def draw_grid(self):
        one_row = 480 / self.rows
        one_col = 900 / self.cols
        self.grid_lines = []

        x1 = 10
        x2 = 910
        y = 60
        for row in range(self.rows + 1):
            self.grid_lines.append(self.canvas.create_line(x1, y, x2, y, width=5, fill=self.grid_col))
            y += one_row

        x = 10
        y1, y2 = 60, 540
        for row in range(self.cols + 1):
            self.grid_lines.append(self.canvas.create_line(x, y1, x, y2, width=5, fill=self.grid_col))
            x += one_col

    def draw_objects(self):
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                self.array[i][j].draw()

        self.player.draw()

    def draw_map(self):
        self.draw_grid()
        self.draw_objects()