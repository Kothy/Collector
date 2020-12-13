from PIL import ImageTk, Image
from CommonFunctions import *

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

        # image = Image.new('RGBA', (200, 200), (0, 0, 0, 80))
        # image.save("obrazky/guarding_bg.png")
        # image2 = Image.open("obrazky/guarding_x.png")
        # image2 = image2.resize((200, 200))
        # image2.save("obrazky/guarding_x2.png")

        image2 = Image.open("obrazky/guarding.png")
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


class Player:
    def __init__(self, map, i, j):
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
        self.start_x = self.x
        self.start_y = self.y
        self.start_row = i
        self.start_col = j
        self.trajectory_lines = []
        self.coll_collected = {}
        img = Image.open("mapy/{}/character.png".format(self.map.name))
        self.trajectory = []
        # img = img.resize((PART_W, PART_H))
        img = resize_image(img, PART_W, PART_H)
        self.image = ImageTk.PhotoImage(img)
        image = Image.new('RGBA', (PART_W, PART_H), translate_color(self.map.grid_col))
        self.trajectory_img = ImageTk.PhotoImage(image)
        self.planned_move = False

    def draw(self):
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')
        # self.id = self.map.canvas.create_image(self.x, self.y, image=self.trajectory_img, anchor='c')

    def remove(self):
        self.map.canvas.delete(self.img_id)

    def __repr__(self):
        return "p"

    def remove_draw_add_road_part(self, part_mode, direction):
        if not self.planned_move:
            self.map.task.parent.parent.road.add_move(part_mode, direction)
        self.remove()
        self.draw()
        colectible = self.check_collectible(self.row, self.col)
        return colectible

    def check_guarding_obstacle(self, row, col):
        if not (col >= 0 and row>=0 and row<self.map.rows and col<self.map.cols):
            return True, "out"
        if (isinstance(self.map.array[row][col], Blank) and self.map.array[row][col].guarded):
            return True, "guarded"
        if (isinstance(self.map.array[row][col], Obstacle)):
            return True, self.map.array[row][col].name
        return False, None

    def check_collectible(self, row, col):
        if isinstance(self.map.array[row][col], Collectible):
            collectible_name = self.map.array[row][col].name
            self.map.array[row][col].remove()
            self.map.array[row][col].remove()
            blank = Blank(self.map, row, col)
            self.map.array[row][col] = blank
            if collectible_name not in self.coll_collected:
                self.coll_collected[collectible_name] = 1
            else:
                self.coll_collected[collectible_name] += 1
            return collectible_name
        return None

    def hide(self):
        self.map.canvas.itemconfig(self.img_id, state="hidden")

    def show(self):
        self.map.canvas.itemconfig(self.img_id, state="normal")

    def move_down(self):
        if self.map.task.parent.parent.actual_regime == "planovaci" and self.planned_move==False:
            self.map.task.parent.parent.road.add_move("basic", "down")
            return None, None
        wrong_move, obsta = self.check_guarding_obstacle(self.row + 1, self.col)
        if wrong_move:
            return "wrong", obsta
        if self.row + 1 < self.map.rows:
            row, col = self.row + 1, self.col
            self.trajectory.append([self.row, self.col, self.x, self.y, None, self.map.array[row][col]])
            self.row += 1
            self.y = self.map.xs[self.row]
            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part("ok", "down")
            return "ok", colectible
        else:
            return "wrong", obsta

    def move_up(self):
        if self.map.task.parent.parent.actual_regime == "planovaci" and self.planned_move == False:
            self.map.task.parent.parent.road.add_move("basic", "up")
            return None, None
        wrong_move, obsta = self.check_guarding_obstacle(self.row - 1, self.col)
        if wrong_move:
            return "wrong", obsta
        if self.row - 1 >= 0:
            row, col = self.row - 1, self.col
            self.trajectory.append([self.row, self.col, self.x, self.y, None, self.map.array[row][col]])
            self.row -= 1
            self.y = self.map.xs[self.row]
            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part('ok', 'up')
            return "ok", colectible
        else:
            return "wrong", obsta

    def move_right(self):
        if self.map.task.parent.parent.actual_regime == "planovaci" and self.planned_move == False:
            self.map.task.parent.parent.road.add_move("basic", "right")
            return None, None
        wrong_move, obsta = self.check_guarding_obstacle(self.row, self.col + 1)
        if wrong_move:
            return "wrong", obsta
        if self.col + 1 < self.map.cols:
            row, col = self.row, self.col + 1
            self.trajectory.append([self.row, self.col, self.x, self.y, None, self.map.array[row][col]])
            self.col += 1
            self.x = self.map.ys[self.col]
            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part('ok', 'right')
            return "ok", colectible
        else:
            return "wrong", obsta

    def move_left(self):
        if self.map.task.parent.parent.actual_regime == "planovaci" and self.planned_move == False:
            self.map.task.parent.parent.road.add_move("basic", "left")
            return None, None
        wrong_move, obsta = self.check_guarding_obstacle(self.row, self.col-1)
        if wrong_move:
            return "wrong", obsta
        if self.col - 1 >= 0:
            row, col = self.row, self.col-1
            self.trajectory.append([self.row, self.col + 1, self.x, self.y, None, self.map.array[row][col]])
            self.col -= 1
            self.x = self.map.ys[self.col]
            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part('ok', 'left')
            return "ok", colectible
        else:
            return "wrong", obsta

    def remove_trajectory(self):
        while self.trajectory_lines:
            self.map.canvas.delete(self.trajectory_lines.pop(0))

    def step_back(self, plan=False):
        if len(self.trajectory) > 0:
            row, col, x, y, t, obj = self.trajectory.pop(-1)
            self.map.array[obj.row][obj.col] = obj
            obj.draw()
            self.row = row
            self.col = col
            self.x = x
            self.y = y
            self.remove()
            self.draw()
            if plan == False:
                self.map.canvas.delete(t)
                self.map.task.parent.parent.road.remove_last_part()

        if plan == True:
            for traj in self.trajectory_lines:
                self.map.canvas.tag_raise(traj)
            self.map.canvas.tag_raise(self.img_id)

    def draw_trajectory(self):
        row, col, x, y, _, obj = self.trajectory[-1]
        t = self.map.canvas.create_line(x, y, self.x, self.y, fill=self.map.grid_col, width=10)
        self.trajectory[-1][4] = t
        self.trajectory_lines.append(t)

    def reset_game(self, plan=False):
        while len(self.trajectory) > 0:
            self.step_back(plan)

        self.coll_collected = {}
        self.row = self.start_row
        self.col = self.start_col
        self.x = self.start_x
        self.y = self.start_y
        self.trajectory = []


class Blank:
    def __init__(self, map, i, j):
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
        # self.was = None
        self.guarded = False

    def draw(self): pass

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
        img = Image.open("mapy/{}/collectibles/{}.png".format(self.map.name, self.name))
        # img = resize_image_to_grid(img)
        # img = img.resize((PART_W, PART_H))
        img = resize_image(img, PART_W, PART_H)
        self.img = img
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
        # img = img.resize((PART_W, PART_H))
        img = resize_image(img, PART_W, PART_H)
        self.img = img
        self.image = ImageTk.PhotoImage(img)
        self.guardians_ids = []
        self.guarded_pos = []

    def draw(self):
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')
        self.draw_guardings()

    def draw_guardings(self):
        i = self.row
        j = self.col
        if self.guarding != "bod":
            for a, b in [(i-1, j), (i+1,j), (i,j+1), (i,j-1)]:
                id = self.draw_at(a, b, self.map.guarding_img)
                if id is not None:
                    self.map.array[a][b].guarded = True
                    self.guarded_pos.append((a, b))
                    self.guardians_ids.append(id)

            if self.guarding == "stvorec":
                for a, b in [(i - 1, j - 1), (i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
                    id = self.draw_at(a, b, self.map.guarding_img)
                    if id is not None:
                        self.map.array[a][b].guarded = True
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