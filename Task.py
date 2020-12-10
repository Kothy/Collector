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
        self.col = col
        self.map = map_str
        self.steps_count = steps
        self.assign = assign
        self.solvable = solvable
        self.obstacles = 3
        self.map_name = map_name
        self.char_name = char_name
        self.collectibles = 4

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
                    img = count[0]
                    count2 = int(count.replace("<", "")[1:])
                    count = count.replace("<", " najviac ").replace(str(count2), "")
                    count2 -= 1
                else:  #"="  in count
                    count2 = int(count.replace("=", "")[1:])
                    count = count.replace("=", " presne ").replace(str(count2), "")
                count = count[1:] + str(count2) + " _"
                text += count + " ,"
        images = self.attach_postfix(images, self.map_name, "objects")
        print(images)
        print(text)
        return text[:-1], images

    def parse_assign(self):
        images = []
        if self.type == "pocty":
            counts = self.assign.split(",")
            tex, imgs = self.parse_counts(counts)
            images += imgs
            text = "{} chce pozbierať{} {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name, tex, "s použitím najviac {} krokov".format(self.steps_count))

        elif self.type == "cesta":
            images_col = self.assign.split(",")
            images_col = self.attach_postfix(images_col,self.map_name, "objects")
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
