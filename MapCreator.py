from CanvasObject import CanvasObject
from CommonFunctions import *
from PIL import Image, ImageTk

class MapCreator(CanvasObject):

    def __init__(self, parent, folder):
        self.parent, self.canvas = parent, parent.canvas
        self.buttons = self.parent.add_to_map_buttons
        self.folder = folder
        self.lines = []
        self.grid_parts = []
        self.color = self.read_map_grid_color()
        self.map = None
        self.rows, self.cols = 0, 0
        self.load_obstacle_options()
        self.load_imgs()
        self.redraw(self.rows, self.cols)

    def load_obstacle_options(self):
        self.options = self.parent.parent.screen.obstacle_options.get_options()

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
        self.guarding_imgs = [Image.open('obrazky/guarding.png'), Image.open('obrazky/guarding_x.png')]

    def load_field(self, field):
        self.field = [[char for char in line] for line in field.split('\n')]
        if self.field != [[]]:
            for i in range(len(self.field)):
               for j in range(len(self.field[0])):
                   char = self.field[i][j]
                   if char != '.':
                       if char == 'p':
                           self.grid_parts[i][j].add_item(char, self.resized_imgs['character'][0])
                       elif char in 'abcd':
                           self.grid_parts[i][j].add_item(char, self.resized_imgs['collectible']['abcd'.find(char)])
                       else:
                           self.grid_parts[i][j].add_item(char, self.resized_imgs['obstacle']['xyz'.find(char)])
                           guarded_parts = self.get_guarded_parts(char, i, j)
                           if guarded_parts != [None]:
                               for part_indices in guarded_parts:
                                   self.grid_parts[part_indices[0]][part_indices[1]].add_guard((i, j))

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
        self.field = [['.' for i in range(self.cols)] for j in range(self.rows)]
        row_height = self.height // self.rows
        col_width = self.width // self.cols
        self.prepare_imgs(row_height, col_width)
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
                self.resized_imgs[type].append(ImageTk.PhotoImage(resize_image(img, width-8, height-8)))
        self.resized_guarding_imgs = [
            ImageTk.PhotoImage(self.guarding_imgs[0].resize((width-2, height-2), Image.ANTIALIAS)),
            ImageTk.PhotoImage(resize_image(self.guarding_imgs[1], width//3, height//3))
        ]

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
            self.parent.set_error_text('Chyba: Najprv zadaj počet riadkov a stĺpcov')
            return
        self.parent.set_error_text('')
        x0, y0 = 380 - self.width//2, 347 - self.height//2
        row_height = self.height // self.rows
        col_width = self.width // self.cols
        i, j = (event.y - y0)//row_height, (event.x - x0)//col_width
        selected = self.buttons.selected
        char = {'character': ['p'], 'collectible': ['a', 'b', 'c', 'd'], 'obstacle': ['x', 'y', 'z']}[selected[0]][selected[1]]
        if char == self.grid_parts[i][j].item:
            return
        if not self.is_valid_target(char, i, j):
            return
        if self.field[i][j] in 'xyz':
            self.cancel_guarding(i, j)
        if char in 'xyz':
            guarded_parts = self.get_guarded_parts(char, i, j)
            if guarded_parts == []:
                return
            if guarded_parts != [None]:
                for part_indices in guarded_parts:
                    self.grid_parts[part_indices[0]][part_indices[1]].add_guard((i, j))
        self.field[i][j] = char
        self.grid_parts[i][j].add_item(char, self.resized_imgs[selected[0]][selected[1]])

    def is_valid_target(self, char, i, j):
        if char == 'p':
            if char in self.get_map_repr():
                self.parent.set_error_text('Chyba: Postavička môže byť v mape iba raz')
                return False
        if char in 'abcdp' and self.grid_parts[i][j].is_guarded():
            self.parent.set_error_text('Chyba: Zvolené políčko je ohrozené')
            return False
        return True

    def get_guarded_parts(self, char, i, j):
        guarding_type = self.options['xyz'.find(char)]
        if guarding_type == 0:
            return [None]
        guarded_parts = []
        if i > 0:
            if self.check_field_availability(i - 1, j):
                guarded_parts.append((i - 1, j))
            else:
                return []
        if i < self.rows - 1:
            if self.check_field_availability(i + 1, j):
                guarded_parts.append((i + 1, j))
            else:
                return []
        if j > 0:
            if self.check_field_availability(i, j - 1):
                guarded_parts.append((i, j - 1))
            else:
                return []
        if j < self.cols - 1:
            if self.check_field_availability(i, j + 1):
                guarded_parts.append((i, j + 1))
            else:
                return []
        if guarding_type == 2:
            if i > 0 and j > 0:
                if self.check_field_availability(i - 1, j - 1):
                    guarded_parts.append((i - 1, j - 1))
                else:
                    return []
            if i < self.rows - 1 and j > 0:
                if self.check_field_availability(i + 1, j - 1):
                    guarded_parts.append((i + 1, j - 1))
                else:
                    return []
            if i > 0 and j < self.cols - 1:
                if self.check_field_availability(i - 1, j + 1):
                    guarded_parts.append((i - 1, j + 1))
                else:
                    return []
            if i < self.rows - 1 and j < self.cols - 1:
                if self.check_field_availability(i + 1, j + 1):
                    guarded_parts.append((i + 1, j + 1))
                else:
                    return []
        return guarded_parts

    def check_field_availability(self, i, j):
        checked_item = self.grid_parts[i][j].item
        if checked_item is not None and checked_item in 'abcdp':
            self.parent.set_error_text('Chyba: Objekt by ohrozil obsadené políčko')
            return False
        return True

    def map_part_deleted(self, i, j):
        self.parent.set_error_text('')
        if self.grid_parts[i][j].item in 'xyz':
            self.cancel_guarding(i, j)
        self.grid_parts[i][j].delete_item()
        self.field[i][j] = '.'

    def cancel_guarding(self, i, j):
        for row in range(i - 1, i + 2):
            if row < 0 or row == self.rows:
                continue
            for col in range(j - 1, j + 2):
                if col < 0 or col == self.cols:
                    continue
                self.grid_parts[row][col].remove_guard((i, j))

    def destroy(self):
        self.clear()
        self.canvas.delete(self.map)

    def get_map_repr(self):
        return '\n'.join([''.join(line) for line in self.field])

    def get_char_position(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] == 'p':
                    return i,j
        return None


class MapCreatorPart(CanvasObject):

    def __init__(self, parent, i, j, x, y):
        self.parent, self.canvas = parent, parent.canvas
        self.parts = [None]
        self.i, self.j = i, j
        self.x, self.y = x, y
        self.item = None
        self.guarded_by = set()
        self.create_guarding_obj()

    def create_guarding_obj(self):
        guarding_bg = self.canvas.create_image(self.x, self.y, image=self.parent.resized_guarding_imgs[0], anchor='c')
        guarding_x = self.canvas.create_image(self.x, self.y, image=self.parent.resized_guarding_imgs[1], anchor='c')
        self.parts.append(CanvasObject(self, [CanvasObject(self, [guarding_bg]), CanvasObject(self, [guarding_x])]))
        self.canvas.tag_bind(guarding_bg, '<ButtonPress-1>', self.clicked)
        self.canvas.tag_bind(guarding_x, '<ButtonPress-1>', self.clicked)

    def add_item(self, item, img):
        if self.item == item:
            return
        self.delete_item()
        if item in 'xyz':
            self.add_guarding_img(only_bg=True)
        self.item = item
        item_img = self.canvas.create_image(self.x, self.y, image=img)
        self.parts[0] = item_img
        self.canvas.tag_bind(item_img, '<ButtonPress-3>', self.clear)
        self.canvas.tag_bind(item_img, '<ButtonPress-1>', self.clicked)

    def delete_item(self):
        if self.item != None:
            self.item = None
            self.canvas.delete(self.parts[0])
            self.parts[0] = None
            self.remove_guard()

    def clear(self, _):
        self.parent.map_part_deleted(self.i, self.j)

    def clicked(self, event):
        self.parent.map_clicked(event)

    def add_guard(self, index):
        self.guarded_by.add(index)
        self.add_guarding_img(self.item is not None and self.item in 'xyz')

    def add_guarding_img(self, only_bg=False):
        self.parts[1].show()
        if only_bg:
            self.parts[1].parts[1].hide()

    def remove_guard(self, index=None):
        if index in self.guarded_by:
            self.guarded_by.remove(index)
        if len(self.guarded_by) == 0 and (self.item is None or self.item not in 'xyz'):
            self.parts[1].hide()
        elif self.item is None or self.item not in 'xyz':
            self.parts[1].show()

    def is_guarded(self):
        return len(self.guarded_by) > 0