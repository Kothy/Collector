from CanvasObject import CanvasObject
from CommonFunctions import *
from PIL import Image, ImageTk

class MapCreator(CanvasObject):

    def __init__(self, parent, folder, field=''):
        self.parent, self.canvas = parent, parent.canvas
        self.buttons = self.parent.add_to_map_buttons
        self.folder = folder
        self.lines = []
        self.field = [[char for char in line] for line in field.split('\n')]
        self.grid_parts = []
        self.color = self.read_map_grid_color()
        self.map = None
        self.rows, self.cols = 0, 0
        self.load_imgs()
        self.redraw(self.rows, self.cols)

    def read_map_grid_color(self):
        with open('mapy/' + self.folder + '/map_settings.txt', 'r') as file:
            line = file.readlines()[6].strip().split(':')
            color = line[1].strip()
        return {'cierna': 'black', 'biela': 'white', 'cervena': 'red', 'zelena': 'green', 'zlta': 'yellow'}[color]

    def load_imgs(self):
        self.imgs = {'character': [], 'collectible': [], 'obstacle': []}
        for obstacle in 'xyz':
            try:
                self.imgs['obstacle'].append(Image.open('mapy/' + self.folder + '/obstacles/' + obstacle + '.png'))
            except FileNotFoundError:
                break
        for collectible in 'abcd':
            try:
                self.imgs['collectible'].append(Image.open('mapy/' + self.folder + '/collectibles/' + collectible + '.png'))
            except FileNotFoundError:
                break
        self.imgs['character'].append(Image.open('mapy/' + self.folder + '/character.png'))

    def redraw(self, rows=None, cols=None):
        if self.map is None:
            img = Image.open('mapy/' + self.folder + '/map.png')
            self.map_img = ImageTk.PhotoImage(resize_image(img, 650, 370))
            self.map = self.canvas.create_image(380, 347, image=self.map_img, anchor='c')
            self.width, self.height = self.map_img.width(), self.map_img.height()
            self.canvas.tag_bind(self.map, '<ButtonPress-1>', self.map_clicked)
        if self.rows == rows and self.cols == cols:
            return
        self.clear()
        self.rows, self.cols = rows if rows is not None else self.rows, cols if cols is not None else self.cols
        self.create_parts()
        if self.rows != 0 and self.cols != 0 and self.rows * self.cols > 1:
            self.draw_lines()

    def clear(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        for line in self.grid_parts:
            for part in line:
                part.destroy()
        self.grid_parts = [[]]

    def create_parts(self):
        if self.rows == 0 or self.cols == 0:
            return
        row_height = self.height // self.rows
        col_width = self.width // self.cols
        self.prepare_imgs(row_height-8, col_width-8)
        x0, y0 = 380 + col_width//2 - self.width//2, 347 + row_height//2 - self.height//2
        self.grid_parts = []
        for i in range(self.rows):
            self.grid_parts.append([])
            for j in range(self.cols):
                self.grid_parts[-1].append(MapCreatorPart(self, i, j, x0 + j*col_width, y0 + i*row_height))

    def prepare_imgs(self, height, width):
        self.resized_imgs = {'character': [], 'collectible': [], 'obstacle': []}
        for type in self.imgs:
            for img in self.imgs[type]:
                self.resized_imgs[type].append(ImageTk.PhotoImage(resize_image(img, width, height)))

    def draw_lines(self):
        x0, x1, y0, y1 = 380 - self.width//2, 380 + self.width//2, 347 - self.height//2, 347 + self.height//2
        row_height = self.height//self.rows
        col_width = self.width//self.cols
        for i in range(1, self.rows):
            self.lines.append(self.canvas.create_line(x0, y0 + i*row_height, x1, y0 + i*row_height, width=3, fill=self.color))
        for i in range(1, self.cols):
            self.lines.append(self.canvas.create_line(x0 + i * col_width, y0, x0 + i * col_width, y1, width=3, fill=self.color))

    def map_clicked(self, event):
        if self.lines == []:
            return
        x0, y0 = 380 - self.width//2, 347 - self.height//2
        row_height = self.height // self.rows
        col_width = self.width // self.cols
        i, j = (event.y - y0)//row_height, (event.x - x0)//col_width
        selected = self.buttons.selected
        char = {'character': ['p'], 'collectible': ['a', 'b', 'c', 'd'], 'obstacle': ['x', 'y', 'z']}
        self.grid_parts[i][j].add_item(char[selected[0]][selected[1]], self.resized_imgs[selected[0]][selected[1]])

    def destroy(self):
        self.clear()
        self.canvas.delete(self.map)


class MapCreatorPart(CanvasObject):

    def __init__(self, parent, i, j, x, y):
        self.parent, self.canvas = parent, parent.canvas
        self.parts = []
        self.i, self.j = i, j
        self.x, self.y = x, y
        self.item = None

    def add_item(self, item, img):
        if self.item == item:
            return
        self.clear(None)
        self.item = item
        item_img = self.canvas.create_image(self.x, self.y, image=img)
        self.parts = [item_img]
        self.canvas.tag_bind(item_img, '<ButtonPress-3>', self.clear)
        self.canvas.tag_bind(item_img, '<ButtonPress-1>', self.clicked)

    def clear(self, _):
        if self.item != None:
            self.item = None
            self.canvas.delete(self.parts[0])
            self.item_img = None

    def clicked(self, event):
        self.parent.map_clicked(event)