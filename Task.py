from TextWithPicures import TextWithImages


class Task:
    def __init__(self, parent, index, name, typ, regime, row, col, steps, assign, map_str, map_name, char_name,
                 solvable=True):
        self.parent = parent
        self.index = index
        self.name = name
        self.type = typ
        self.regime = regime
        self.row = row
        self.map = map_str
        self.col = col
        self.steps_count = steps
        self.assign = assign
        self.solvable = solvable
        self.obstacles = 3
        self.map_name = map_name
        self.char_name = char_name
        self.collectibles = 4

    def attach_postfix(self, images, map_name):
        for i in range(len(images)):
            images[i] = "mapy/{}/objects/{}.png".format(map_name, images[i])
        return images

    def parse_assign(self):
        images = []
        print(self.type)
        if self.type == "pocty":
            text = "{} chce pozbierať [niečo] {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name, "s použitím najviac {} krokov".format(self.steps_count))
        elif self.type == "cesta":
            images_col = self.assign.split(",")
            images_col = self.attach_postfix(images_col, self.map_name)
            images = images + images_col

            text = "{} chce pozbierať {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name,
                "{} (v tomto počte a poradí) s použitím najviac {} krokov".format(("_ , " * len(images_col))[:-2],
                                                                                  self.steps_count))

        if self.obstacles == 3:
            text += " a _ a _ ."
        elif self.obstacles == 2:
            text += " a_ ."
        else:
            text += " ."
        print(text)

        arr = ["x", "y", "z"]
        for obs in range(self.obstacles):
            images.append("mapy/{}/obstacles/{}.png".format(self.map_name, arr.pop(0)))

        w = 340
        self.parent.text_w_images = TextWithImages(self.parent.canvas, 930, 90, w, text, images)

    def read_map(self):
        pass

    def __repr__(self):
        return " ".join([str(self.index), self.name, self.type,
                         self.regime, self.row, self.map,
                         self.col, self.steps_count, self.assign,
                         self.solvable])


class TaskSet:
    def __init__(self, name, canvas, next_without_solve):
        self.name = name
        self.canvas = canvas
        self.tasks = []
        self.next = next_without_solve

    def add_task(self, name, typ, regime, row, col, steps, assign, maps_str, map_name, char_name, solvable):
        self.tasks.append(
            Task(self, len(self.tasks), name, typ, regime, row, col, steps, assign, maps_str, map_name, char_name,
                 solvable))
