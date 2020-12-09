from PIL import ImageTk, Image

PART_W = 0
PART_H = 0
ALPHA = 100


def resize_image_by_width(img, basewidth):
    basewidth -= 5
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def resize_image_by_height(img, hsize):
    hsize -= 5
    wpercent = (hsize / float(img.size[1]))
    basewidth = int((float(img.size[0]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def resize_image_to_grid(img):
    img = resize_image_by_height(img, PART_H)
    return resize_image_by_width(img, PART_W)


def calculate_coords(i, j, rows, cols):
    one_row = 480 / rows
    one_col = 900 / cols
    return (j * one_col) + 10 + (one_row / 2), (i * one_row) + 60 + (one_col / 2)


# def calculate_x_y(row, col, canvas, xs, ys):
#
#     # canvas.create_rectangle(10, 60, 10 + one_row + 20, 60 + one_col + 10, fill="blue", width=5)
#     # return xs[i]
#
#     for i in range(cols):
#         for j in range(rows):
#             # print(i, j)
#             x = xs[i]
#             y = ys[j]
#             canvas.create_oval(x + 10 , y + 10, x - 10, y - 10, fill="blue")

def translate_color(color):
    if color == "black":
        return (0, 0, 0, ALPHA)
    elif color == "white":
        return (255, 255, 255, ALPHA)
    elif color == "red":
        return (255, 0, 0, ALPHA)
    elif color == "green":
        return (64, 255, 0, ALPHA)
    elif color == "yellow":
        return (255, 255, 0, ALPHA)
    return (0, 0, 0, ALPHA)


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

        image = Image.new('RGBA', (PART_W, PART_H), translate_color(self.grid_col))

        self.trajectory_img = ImageTk.PhotoImage(image)
        # image = Image.new('RGBA', (200, 200), (0, 0, 0, 80))
        # image.save("obrazky/guarding_bg.png")
        # image2 = Image.open("obrazky/guarding_x.png")
        # image2 = image2.resize((200, 200))
        # image2.save("obrazky/guarding_x2.png")

        image2 = Image.open("obrazky/delete.png")
        image2 = image2.resize((int(PART_W), int(PART_H)), Image.ANTIALIAS)
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
                    obj = Player(self, i, j)
                    self.player = obj
                arr[i][j] = obj

        self.array = arr
        # print(self.array, self.rows, self.cols)

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

    def draw_map(self):
        self.draw_grid()
        self.draw_objects()


class Player:
    def __init__(self, map, i, j):
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
        img = Image.open("mapy/{}/character.png".format(self.map.name))
        # img = resize_image_to_grid(img)
        img = img.resize((PART_W, PART_H))
        self.image = ImageTk.PhotoImage(img)

    def draw(self):
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')
        # self.id = self.map.canvas.create_image(self.x, self.y, image=self.map.trajectory_img, anchor='c')

    def remove(self):
        self.map.canvas.delete(self.img_id)

    def __repr__(self):
        return "p"

    def move_down(self):
        if self.row + 1 < self.map.rows:
            self.row += 1
            self.y = self.map.xs[self.row]
            self.remove()
            self.draw()
            self.map.task.parent.parent.road.add_move('basic', 'down')

    def move_up(self):
        if self.row - 1 >= 0:
            self.row -= 1
            self.y = self.map.xs[self.row]
            self.remove()
            self.draw()
            self.map.task.parent.parent.road.add_move('basic', 'up')

    def move_right(self):
        if self.col + 1 < self.map.cols:
            self.col += 1
            self.x = self.map.ys[self.col]
            self.remove()
            self.draw()
            self.map.task.parent.parent.road.add_move('basic', 'right')

    def move_left(self):
        if self.col - 1 >= 0:
            self.col -= 1
            self.x = self.map.ys[self.col]
            self.remove()
            self.draw()
            self.map.task.parent.parent.road.add_move('basic', 'left')


class Blank:
    def __init__(self, map, i, j):
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
        self.guarded = False

    def draw(self):pass

    def remove(self): pass

    def __repr__(self):
        return "."


class Collectible:
    def __init__(self, name, map, i, j):
        self.name = name
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
        img = Image.open("mapy/{}/objects/{}.png".format(self.map.name, self.name))
        # img = resize_image_to_grid(img)
        img = img.resize((PART_W, PART_H))
        self.image = ImageTk.PhotoImage(img)

    def draw(self):
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')

    def remove(self):
        self.map.canvas.delete(self.img_id)

    def __repr__(self):
        return self.name


class Obstacle:
    def __init__(self, name, map, guarding, i, j):
        self.name = name
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]

        self.guarding = guarding
        self.row = i
        self.col = j
        img = Image.open("mapy/{}/obstacles/{}.png".format(self.map.name, self.name))
        # img = resize_image_to_grid(img)
        img = img.resize((PART_W, PART_H))
        self.image = ImageTk.PhotoImage(img)
        self.guardians_ids = []
        self.guarded_pos = []

    def draw(self):
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')
        # self.map.canvas.create_oval(self.x + 10, self.y + 10, self.x  - 10, self.y - 10, fill="black")
        self.draw_guardings()

    def draw_guardings(self):
        # x = self.x
        # y = self.y
        i = self.row
        j = self.col
        if self.guarding != "bod":
            for a, b in [(i-1, j), (i+1,j), (i,j+1), (i,j-1)]:
                id = self.draw_at(a, b, self.map.guarding_img)
                if id is not None:
                    self.guarded_pos.append((a, b))
                    self.guardians_ids.append(id)

            if self.guarding == "stvorec":
                for a, b in [(i - 1, j - 1), (i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
                    id = self.draw_at(a, b, self.map.guarding_img)
                    if id is not None:
                        self.guarded_pos.append((a, b))
                        self.guardians_ids.append(id)

    def draw_at(self, i, j, img):
        if i >= 0 and i < self.map.rows and j >= 0 and j < self.map.cols:
            y, x = self.map.xs[i], self.map.ys[j]
            id = self.map.canvas.create_image(x, y, image=img, anchor="c")
            return id
        return None

    def get_guarded(self):
        return self.guarded_pos

    def remove(self):
        self.map.canvas.delete(self.img_id)
        for guard in self.guardians_ids:
            self.map.canvas.delete(guard)

    def __repr__(self):
        return self.name