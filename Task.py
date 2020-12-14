from TextWithPicures import TextWithImages
from PIL import Image, ImageTk
from Map import Map
import copy


class Task:
    def __init__(self, parent, index, name, typ, mode, row, col,
                 steps, assign, map_str, map_name, char_name, solvable=True, parse=True):
        self.parent = parent
        self.index = index
        self.name = name
        self.type = typ
        self.mode = mode
        self.actual_regime = None
        self.row = row
        self.map_str = map_str
        self.col = col
        self.steps_count = steps
        self.assign = assign
        self.solvable = solvable
        self.obstacles = []
        self.map_name = map_name
        self.char_name = char_name
        self.collectibles = 0
        if parse:
            self.parse_assign()

    def attach_postfix(self, images, map_name, dir):
        for i in range(len(images)):
            images[i] = "mapy/{}/{}/{}.png".format(map_name, dir,images[i])
        return images

    def parse_counts(self, arr):
        images = []
        text = ""
        for count in arr:
            if not "?" in count:
                images.append(count[0])
                if "<=" in count:
                    count2 = int(count.replace("<=", "")[1:])
                    count = count.replace("<=", " najviac ").replace(str(count2), "")
                elif ">=" in count:
                    count2 = int(count.replace(">=", "")[1:])
                    count = count.replace(">=", " najmenej ").replace(str(count2), "")
                elif ">" in count:
                    count2 = int(count.replace(">", "")[1:])
                    count = count.replace(">", " najmenej ").replace(str(count2), "")
                    count2 += 1
                elif "<" in count:
                    count2 = int(count.replace("<", "")[1:])
                    count = count.replace("<", " najviac ").replace(str(count2), "")
                    count2 -= 1
                else:  #"="  in count
                    count2 = int(count.replace("=", "")[1:])
                    count = count.replace("=", " presne ").replace(str(count2), "")
                count = count[1:] + str(count2) + " _"
                text += count + " ,"
        images = self.attach_postfix(images, self.map_name, "collectibles")
        return text[:-1], images

    def parse_assign(self):
        self.read_map_file()
        images = []
        if self.type == "pocty":
            counts = self.assign.split(",")
            tex, imgs = self.parse_counts(counts)
            images += imgs
            text = "{} chce pozbierať{} {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name, tex, "s použitím najviac {} krokov".format(self.steps_count))

        elif self.type == "cesta":
            # images_col = self.assign.split(",")
            images_col = self.assign.strip()
            path = []
            for part in images_col:
                path.append(part)

            # images_col = self.attach_postfix(images_col, self.map_name, "collectibles")
            images_col = self.attach_postfix(path, self.map_name, "collectibles")
            images = images + images_col

            text = "{} chce pozbierať {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name,
                "{} (v tomto počte a poradí) s použitím najviac {} krokov".format(("_ " * len(images_col)),# [:-2]
                                                                                    self.steps_count))

        else:
            text = ""

        if "x" in self.map_str:
            self.obstacles.append("x")
        if "y" in self.map_str:
            self.obstacles.append("y")
        if "z" in self.map_str:
            self.obstacles.append("z")

        if len(self.obstacles) == 3:
            text += " a _ a _ ."
        elif len(self.obstacles) == 2:
            text += " a _ ."
        else:
            text += " ."

        arr = copy.deepcopy(self.obstacles)

        for obs in range(len(self.obstacles)):
            images.append("mapy/{}/obstacles/{}.png".format(self.map_name, arr.pop(0)))

        self.assign_text = text
        self.assign_images = images

    def remove_lines(self, arr, num):
        for i in range(num):
            arr.pop(0)
        return arr

    def translate_color(self, color):
        if color == "cierna":
            return "black"
        elif color == "biela":
            return "white"
        elif color == "cervena":
            return "red"
        elif color == "zelena":
            return "green"
        elif color == "zlta":
            return "yellow"
        return "black"

    def read_map_file(self):
        with open("mapy/" + self.map_name + "/map_settings.txt") as file:
            full = file.read()

        lines = full.split("\n")

        lines = self.remove_lines(lines, 3)

        self.char_name = lines.pop(0).split(":")[1].strip()

        text = self.parent.parent.canvas.itemcget(self.parent.parent.task_text_mode, 'text')
        if "{}" in text:
            self.parent.parent.canvas.itemconfig(self.parent.parent.task_text_mode, text=text.format(self.char_name + ": "))

        self.char_rotation = lines.pop(0).split(":")[1].strip() # žiadne, vľavo/vpravo, dole/hore, všetky smery
        self.routing = lines.pop(0).split(":")[1].strip() # vpravo, vľavo, hore, dole, -

        self.traject_and_grid_color = self.translate_color(lines.pop(0).split(":")[1].strip())

        lines = self.remove_lines(lines, 2)
        self.collectibles = len(lines.pop(0).split(","))
        lines = self.remove_lines(lines, 2)
        lines.pop(0).split(",")

        self.draw_map_bg()
        self.map = Map(self.map_name, self.map_str, self.parent.canvas, self, self.traject_and_grid_color)

    def draw_map_bg(self):
        img = Image.open("mapy/{}/map.png".format(self.map_name))
        img = img.resize((900, 480))
        self.map_bg_img = ImageTk.PhotoImage(img)

        self.map_bg_img_id = self.parent.canvas.create_image(10, 60, image=self.map_bg_img, anchor='nw')

    def __repr__(self):
        return " ".join([str(self.index), self.name, self.type,
                         self.mode, self.row, self.map_str,
                         self.col, self.steps_count, self.assign,
                         self.solvable])

    def draw(self):
        w = 340
        text = self.assign_text
        images = self.assign_images
        if self.mode == "oba" or self.mode == "priamy":
            self.parent.canvas.itemconfig(self.parent.parent.play, state="hidden")
            self.parent.parent.actual_regime = "priamy"
        else:
            self.parent.parent.actual_regime = "planovaci"
            self.parent.canvas.itemconfig(self.parent.parent.play, state="normal")
            text2 = self.parent.parent.canvas.itemcget(self.parent.parent.task_text_mode, 'text')
            text2 = text2.replace("nájsť", "naplánovať")
            text2 = text2.replace("priamy", "plánovací")
            self.parent.parent.canvas.itemconfig(self.parent.parent.task_text_mode, text=text2)

        if self.mode == "oba":
            self.parent.canvas.itemconfig(self.parent.parent.swap_mode_btn, state="normal")
        else:
            self.parent.canvas.itemconfig(self.parent.parent.swap_mode_btn, state="hidden")

        if self.type != "volna":
            self.text_w_images = TextWithImages(self.parent.canvas, 930, 90, w, text, images)

        self.parent.canvas.itemconfig(self.parent.parent.task_name_text, text=str(self.index + 1)+". " + self.name)
        self.parent.canvas.itemconfig(self.parent.parent.task_name_text, state="normal")
        self.map.draw_map()

    def remove(self):
        self.map.remove()
        self.text_w_images.remove()


class TaskSet:
    def __init__(self, name, canvas, next_without_solve, obstacles, parent):
        self.parent = parent
        self.name = name
        self.canvas = canvas
        self.tasks = []
        self.actual = 0
        self.obstacles_arr = obstacles
        self.next = next_without_solve

    def add_task(self, name, typ, regime, row, col, steps, assign, maps_str, map_name, char_name, solvable):
        t = Task(self, len(self.tasks), name, typ, regime, row, col, steps, assign, maps_str, map_name, char_name,
             solvable)
        self.tasks.append(t)

    def draw_task_and_map(self):
        self.tasks[self.actual].draw()

    def remove_task_and_map(self):
        self.tasks[self.actual].remove()

    def next_task(self):
        self.actual += 1
        if self.actual == len(self.tasks):
            self.actual = 0

    def prev_task(self):
        self.actual -= 1
        if self.actual == 0:
            self.actual = len(self.tasks) - 1

    def get_actual_task(self):
        return self.tasks[self.actual]

    def get_player(self):
        return self.tasks[self.actual].map.player

    # def move_player_down(self):
    #     self.tasks[self.actual].map.player.move_down()
    #
    # def move_player_up(self):
    #     self.tasks[self.actual].map.player.move_up()
    #
    # def move_player_right(self):
    #     self.tasks[self.actual].map.player.move_right()
    #
    # def move_player_left(self):
    #     self.tasks[self.actual].map.player.move_left()

    def step_back(self):
        self.tasks[self.actual].map.player.step_back()