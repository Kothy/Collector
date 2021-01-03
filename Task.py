from TextWithPicures import TextWithImages
from PIL import Image, ImageTk
from Map import Map
import copy
from CommonFunctions import resize_image
from CommonFunctions import playsound, strip_accents
from MapParts import Collectible
import re
from Road import Road


COLLECTION_SOUND = 'sounds/Collection.mp3'
CORRECT_ANS_SOUND = 'sounds/Correct_Answer.mp3'
WRONG_SOUND = "sounds/wrong_sound.mp3"


class Task:
    def __init__(self, parent, index, name, typ, mode, row, col,
                 steps, assign, map_str, map_name, char_name, solvable=True, parse=True):
        self.parent = parent
        self.index = index
        self.name = name
        self.type = typ
        self.mode = mode
        self.actual_regime = "priamy"
        if self.mode == "planovaci":
            self.actual_regime = "planovaci"
        self.row = row
        self.map_str = map_str
        self.col = col
        if parse:
            self.road = Road(self.parent.parent.move_imgs, self.parent.parent)
        self.steps_count = int(steps) if steps != '' else 16
        self.assign = assign
        self.col_counts = []
        self.solvable = True if solvable == "ano" else False
        self.obstacles = []
        self.map_name = map_name
        self.char_name = char_name
        self.collectibles = 0
        img = Image.open("mapy/{}/map.png".format(self.map_name))

        # img = img.resize((900, 480))
        img = resize_image(img, 899, 479)
        self.map_bg_w, self.map_bg_h = img.size
        self.map_bg_img = ImageTk.PhotoImage(img)
        if parse:
            self.parse_assign()

    def attach_postfix(self, images, map_name, dir):
        for i in range(len(images)):
            images[i] = "mapy/{}/{}/{}.png".format(map_name, dir, images[i])
        return images

    def parse_counts(self, arr):
        images = []
        text = ""
        for count in arr:
            if not "?" in count:

                images.append(count[0])
                if "<=" in count:
                    self.col_counts.append((count[0], "<=", int(count.replace("<=", "")[1:])))
                    count2 = int(count.replace("<=", "")[1:])
                    count = count.replace("<=", " najviac ").replace(str(count2), "")
                elif ">=" in count:
                    self.col_counts.append((count[0], ">=", int(count.replace(">=", "")[1:])))
                    count2 = int(count.replace(">=", "")[1:])
                    count = count.replace(">=", " najmenej ").replace(str(count2), "")
                elif ">" in count:
                    self.col_counts.append((count[0], ">=", int(count.replace(">", "")[1:]) + 1))
                    count2 = int(count.replace(">", "")[1:])
                    count = count.replace(">", " najmenej ").replace(str(count2), "")
                    count2 += 1
                elif "<" in count:
                    self.col_counts.append((count[0], "<=", int(count.replace("<", "")[1:]) - 1))
                    count2 = int(count.replace("<", "")[1:])
                    count = count.replace("<", " najviac ").replace(str(count2), "")
                    count2 -= 1
                else:  # "="  in count
                    self.col_counts.append((count[0], "=", int(count.replace("=", "")[1:])))
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
            text = "{} chce pozbierať \n {} {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name, tex, "s použitím najviac {} krokov".format(self.steps_count))
            self.assign_text2 = tex

        elif self.type == "cesta":

            images_col = self.assign.strip()
            path = []
            for part in images_col:
                path.append(part)

            images_col = self.attach_postfix(path, self.map_name, "collectibles")
            images = images + images_col

            text = "{} chce pozbierať \n {}. Musí sa ale vyhnúť všetkým políčkam, ktoré ohrozuje _".format(
                self.char_name,
                "{} (v tomto počte a poradí) s použitím najviac {} krokov".format(("_ " * len(images_col)),
                                                                                  self.steps_count))
            self.assign_text2 = ("_ " * len(images_col))[:-1]

        else:
            text = ""

        if "x" in self.map_str:
            self.obstacles.append("x")
        if "y" in self.map_str:
            self.obstacles.append("y")
        if "z" in self.map_str:
            self.obstacles.append("z")

        if len(self.obstacles) == 3:
            text += " , _ a _ ."
            t =  "_ , _ a _ ."
        elif len(self.obstacles) == 2:
            text += " a _ ."
            t = "_ a _ ."
        else:
            text += " ."
            t = "_ ."
        self.obstacles_assign = t

        arr = copy.deepcopy(self.obstacles)

        for obs in range(len(self.obstacles)):
            images.append("mapy/{}/obstacles/{}.png".format(self.map_name, arr.pop(0)))

        self.assign_text = text
        self.assign_images = images

    def remove_lines(self, arr, num):
        for i in range(num):
            arr.pop(0)
        return arr

    def check_answer(self, play=True):
        if self.type == "pocty":
            return self.check_count_answer(play)
        elif self.type == "cesta":
            return self.check_path_answer(play)
        elif self.type == "volna" and isinstance(self.map.player.trajectory[-1][5], Collectible):
            playsound(COLLECTION_SOUND, 1)
            self.parent.parent.show_next_task_button()
        return True

    def check_path_answer(self, play=True):
        answer = "".join(self.map.player.coll_path) == self.assign and self.steps_count >= self.map.player.steps_count
        if answer:
            # answer = not self.parent.parent.road.wrong_in_road()
            answer = not self.road.wrong_in_road()
        if answer:
            # print("spravne")
            self.parent.parent.show_next_task_button()
            if play:
                playsound(CORRECT_ANS_SOUND, 2)

        if len(self.map.player.trajectory) and isinstance(self.map.player.trajectory[-1][5], Collectible) and not answer:
            # print("collectible")
            if play:
                len_col = len(self.map.player.coll_path)
                if self.map.task.assign[:len_col] == "".join(self.map.player.coll_path):
                    # print(self.map.task.assign, self.map.player.coll_path, self.map.task.assign[:len_col])
                    playsound(COLLECTION_SOUND, 1)
                else:
                    playsound(WRONG_SOUND, 3)


        return answer

    def check_count_answer(self, play=True):
        colle = self.map.player.coll_collected
        answers = []
        for count in self.col_counts:
            if "?" not in count:
                col = count[0]
                sign = count[1]
                num = count[2]
                if sign == "=" and col in colle and colle[col] == num:
                    answers.append(True)
                elif sign == "<=" and col in colle and self.map.player.coll_collected[col] <= num:
                    answers.append(True)
                elif sign == "<=" and col not in colle:
                    answers.append(True)
                elif sign == ">=" and col in colle and self.map.player.coll_collected[col] >= num:
                    answers.append(True)
                elif sign == ">=" and col not in colle and num == 0:
                    answers.append(True)
                else:
                    answers.append(False)

        answer = False not in answers and self.steps_count >= self.map.player.steps_count

        if answer:
            # answer = not self.parent.parent.road.wrong_in_road()
            answer = not self.road.wrong_in_road()
        if answer:
            if play:
                playsound(CORRECT_ANS_SOUND, 2)
            self.parent.parent.show_next_task_button()

        if len(self.map.player.trajectory) and isinstance(self.map.player.trajectory[-1][5], Collectible) and not answer:
            col_name = self.map.player.trajectory[-1][5].name
            if play:
                colle = self.map.player.coll_collected
                was = False
                for count in self.col_counts:
                    col = count[0]
                    sign = count[1]
                    num = count[2]
                    if sign == "=" and col in colle and colle[col] > num and col == col_name:
                        was = True
                        break
                    elif sign == "<=" and col in colle and colle[col] > num and col == col_name:
                        was = True
                        break

                if was == False:
                    playsound(COLLECTION_SOUND, 1)
                else:
                    playsound(WRONG_SOUND, 3)

        return False not in answers and self.steps_count >= self.map.player.steps_count

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

    def check_map_file(self, lines):
        if len(lines) < 14:
            return "Chýbajúce riadky súboru"

        message = "Chyba: {}"
        nums = []
        if not (lines[0].startswith("Názov: ") and lines[0].split(": ")[1].replace("_","").replace(" ", "").isalnum()):
        # if re.fullmatch("Názov: [a-zA-Z0-9_]{1,15}", lines[0]) is None:
            nums.append(lines[0])
        elif lines[1] != "":
            nums.append(lines[1])
        elif lines[2] != "# Nastavenia postavičky #":
            nums.append(lines[2])
        elif not (lines[3].startswith("Meno: ") and lines[3].split(": ")[1].replace("_", "").replace(" ", "").isalnum()):
        # elif re.fullmatch("Meno: [a-zA-Z0-9_]{1,10}", lines[3]) is None:
            nums.append(lines[3])
        elif re.fullmatch("Otáčanie: (všetky smery|žiadne|vľavo/vpravo|dole/hore)", lines[4]) is None:
            nums.append(lines[4])
        elif re.fullmatch("Smerovanie: (-|vpravo|hore|dole|vľavo)", lines[5]) is None:
            nums.append(lines[5])
        elif re.fullmatch("Mriežka: (čierna|biela|červená|zelená|žltá)", lines[6]) is None:
            nums.append(lines[6])
        elif re.fullmatch("Trajektória: (čierna|biela|červená|zelená|žltá)", lines[7]) is None:
            nums.append(lines[7])
        elif lines[8] != "":
            nums.append(lines[8])
        elif lines[9] != "# Predmety #":
            nums.append(lines[9])
        elif re.fullmatch("(a,b,c,d|a,b,c|a,b|a)", lines[10]) is None:
            nums.append(lines[10])
        elif lines[11] != "":
            nums.append(lines[11])
        elif lines[12] != "# Prekážky #":
            nums.append(lines[12])
        elif re.fullmatch("(x,y,z|x,y|x)", lines[13]) is None:
            nums.append(lines[13])

        map_name = lines[0].split(": ")[1]
        if self.map_name != map_name:
            return message.format("Neexistujúci názov mapy: {}.".format(map_name))

        if len(lines) > 14:
            new_lines = lines[14:]
            new_lines = list(set(new_lines))
            if not (len(new_lines) == 1 and new_lines[0] == ""):
                return message.format("Na konci súboru sa nachádzajú nepovolené riadky.")

        if len(nums) == 0:
            return ""

        return message.format(nums[0])

    def read_map_file(self):

        with open("mapy/" + self.map_name + "/map_settings.txt","r", encoding="utf=8") as file:
            full = file.read()

        lines = full.split("\n")

        self.map_error_message = self.check_map_file(lines)

        lines = self.remove_lines(lines, 3)

        self.char_name = lines.pop(0).split(":")[1].strip()

        text = self.parent.parent.canvas.itemcget(self.parent.parent.task_text_mode, 'text')
        if "{}" in text:
            self.parent.parent.canvas.itemconfig(self.parent.parent.task_text_mode,
                                                 text=text.format(self.char_name + ": "))

        self.char_rotation = strip_accents(lines.pop(0).split(":")[1].strip())  # ziadne, vlavo/vpravo, dole/hore, vsetky smery
        self.routing = strip_accents(lines.pop(0).split(":")[1].strip())  # vpravo, vlavo, hore, dole, -

        col = lines.pop(0).split(":")[1].strip()
        self.traject_and_grid_color = self.translate_color(strip_accents(col))
        self.trajectory_color = self.translate_color(strip_accents(lines.pop(0).split(":")[1].strip()))

        lines = self.remove_lines(lines, 2)
        self.collectibles = len(lines.pop(0).split(","))
        lines = self.remove_lines(lines, 2)
        lines.pop(0).split(",")

        # self.draw_map_bg()
        self.map = Map(self.map_name, self.map_str, self.parent.canvas, self, self.traject_and_grid_color)

    def draw_map_bg(self):
        img = Image.open("mapy/{}/map.png".format(self.map_name))

        # img = img.resize((900, 480))
        img = resize_image(img, 899, 479)
        self.map_bg_w, self.map_bg_h = img.size
        self.map_bg_img = ImageTk.PhotoImage(img)

        self.map_bg_img_id = self.parent.canvas.create_image(460, 300, image=self.map_bg_img, anchor='c')

    def __repr__(self):
        return " ".join([str(self.index), self.name, self.type,
                         self.mode, self.row, self.map_str,
                         self.col, self.steps_count, self.assign,
                         self.solvable])

    def draw(self):
        self.draw_map_bg()
        w = 340
        self.text_w_images = None
        self.text_w_images2 = None
        self.assign_ids = []
        text = self.assign_text
        images = self.assign_images
        if self.mode == "oba" or self.mode == "priamy":
            self.parent.canvas.itemconfig(self.parent.parent.play, state="hidden")
            # self.parent.parent.actual_regime = "priamy"
            # self.actual_regime = "priamy"
        else:
            # self.parent.parent.actual_regime = "planovaci"
            # self.actual_regime = "planovaci"
            self.parent.canvas.itemconfig(self.parent.parent.play, state="normal")
            text2 = self.parent.parent.canvas.itemcget(self.parent.parent.task_text_mode, 'text')
            text2 = text2.replace("nájsť", "naplánovať")
            text2 = text2.replace("priamy", "plánovací")
            self.parent.parent.canvas.itemconfig(self.parent.parent.task_text_mode, text=text2)

        if self.actual_regime== "planovaci":
            self.parent.canvas.itemconfig(self.parent.parent.play, state="normal")

        self.parent.parent.actual_regime = self.actual_regime

        if self.mode == "oba":
            self.parent.canvas.itemconfig(self.parent.parent.swap_mode_btn, state="normal")
        else:
            self.parent.canvas.itemconfig(self.parent.parent.swap_mode_btn, state="hidden")

        if self.type != "volna":

            # self.text_w_images = TextWithImages(self.parent.canvas, 930, 90, w, text, images)
            x = 30
            if self.type == "cesta":
                x = 0

            self.text_w_images = TextWithImages(self.parent.canvas, 930, 125, w - 20, self.assign_text2, images[:self.assign_text2.count("_") + 1])
            self.text_w_images2 = TextWithImages(self.parent.canvas, 930, 345 - x, w - 20, self.obstacles_assign,
                                                images[self.assign_text2.count("_"):])

            id1 = self.parent.canvas.create_text(930, 70, fill="#0a333f",
                                                             font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                             width=330, text='{} chce pozbierať'.format(self.char_name))
            id2 = self.parent.canvas.create_text(930, 220 - x, fill="#0a333f",
                                                           font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                           width=330, text='s použitím najviac {} krokov.'.format(self.steps_count))
            id3 = self.parent.canvas.create_text(930, 185, fill="#0a333f",
                                                               font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                               width=330, text='(v tomto počte aj poradí)')
            id4 = self.parent.canvas.create_text(930, 255 - x, fill="#0a333f",
                                                              font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                              width=330,
                                                              text='Musí sa ale vyhnúť políčkam, ktoré ohrozuje')

            self.assign_ids = [id1, id2, id3, id4]
            if self.type == "pocty":
                self.parent.canvas.itemconfig(id3, state="hidden")

        self.parent.canvas.itemconfig(self.parent.parent.task_name_text, text=str(self.index + 1) + ". " + self.name)
        self.parent.canvas.itemconfig(self.parent.parent.task_name_text, state="normal")
        self.map.draw_map()
        # self.map.draw_guards()

    def remove(self):
        self.map.remove()
        if self.text_w_images is not None:
            self.text_w_images.remove()
        if self.text_w_images is not None:
            self.text_w_images2.remove()
        for id in self.assign_ids:
            self.parent.canvas.delete(id)


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
        if self.actual < len(self.tasks) - 1:
            self.actual += 1
            return True
        else:
            return False

    def prev_task(self):
        if self.actual > 0:
            self.actual -= 1
            return True
        else:
            return False

    def get_actual_task(self):
        return self.tasks[self.actual]

    def get_player(self):
        return self.tasks[self.actual].map.player

    def step_back(self):
        self.tasks[self.actual].map.player.step_back()
