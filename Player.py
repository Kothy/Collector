from MapParts import *
from PIL import ImageOps
import playsound

WRONG_SOUND = "sounds/wrong_sound.mp3"
COLLECTION_SOUND = 'sounds/Collection.mp3'


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
        self.trajectory = []
        self.steps_count = 0
        img = Image.open("mapy/{}/character.png".format(self.map.name))
        img = resize_image(img, self.map.part_w - 4, self.map.part_h - 4)
        self.image = ImageTk.PhotoImage(img)
        self.images = {"vlavo": None, "vpravo": None,
                       "dole": None, "hore": None}
        self.coll_path = []
        self.start_rotation = None
        self.actual_rotation = None

        self.routing = self.map.task.routing  # vpravo, vlavo, hore, dole, -
        self.rotation = self.map.task.char_rotation  # ziadne, vlavo/vpravo, dole/hore, vsetky smery

        if self.routing == "hore":
            rotating = ["vlavo", "dole", "vpravo"]
            self.images["hore"] = ImageTk.PhotoImage(img)
            self.actual_rotation = "hore"

        elif self.routing == "vlavo":
            rotating = ["dole", "vpravo", "hore"]
            self.images["vlavo"] = ImageTk.PhotoImage(img)
            self.actual_rotation = "vlavo"

        elif self.routing == "dole":
            rotating = ["vpravo", "hore", "vlavo"]
            self.images["dole"] = ImageTk.PhotoImage(img)
            self.actual_rotation = "dole"

        elif self.routing == "vpravo":
            rotating = ["hore", "vlavo", "dole"]
            self.images["vpravo"] = ImageTk.PhotoImage(img)
            self.actual_rotation = "vpravo"

        else:
            rotating = ["vlavo", "dole", "vpravo"]
            self.images["hore"] = ImageTk.PhotoImage(img)
            self.actual_rotation = "hore"

        self.start_rotation = self.actual_rotation

        angle = 90
        for move in rotating:
            self.images[move] = ImageTk.PhotoImage(img.rotate(angle, expand=True))
            angle += 90

        if self.rotation == "dole/hore":
            if self.routing == "hore":
                self.images["hore"] = ImageTk.PhotoImage(img)
                im_flip = ImageOps.flip(img)
                self.images["dole"] =  ImageTk.PhotoImage(im_flip)
            elif self.routing == "dole":
                self.images["dole"] = ImageTk.PhotoImage(img)
                im_flip = ImageOps.flip(img)
                self.images["hore"] = ImageTk.PhotoImage(im_flip)

            elif self.routing == "vpravo":
                self.images["hore"] = ImageTk.PhotoImage(img.rotate(angle, expand=True))
                im_flip = ImageOps.flip(img.rotate(angle, expand=True))
                self.images["dole"] = ImageTk.PhotoImage(im_flip)
            else:
                self.images["dole"] = ImageTk.PhotoImage(img.rotate(angle, expand=True))
                im_flip = ImageOps.flip(img.rotate(angle, expand=True))
                self.images["hore"] = ImageTk.PhotoImage(im_flip)

        elif self.rotation == "vlavo/vpravo":
            if self.routing == "vpravo":
                self.images["vpravo"] = ImageTk.PhotoImage(img)
                im_flip = ImageOps.mirror(img)
                self.images["vlavo"] =  ImageTk.PhotoImage(im_flip)
            elif self.routing == "vlavo":
                self.images["vlavo"] = ImageTk.PhotoImage(img)
                im_flip = ImageOps.mirror(img)
                self.images["vpravo"] = ImageTk.PhotoImage(im_flip)
            elif self.routing == "hore":
                self.images["vlavo"] = ImageTk.PhotoImage(img.rotate(angle, expand=True))
                im_flip = ImageOps.mirror(img.rotate(angle, expand=True))
                self.images["vpravo"] = ImageTk.PhotoImage(im_flip)

            else:
                self.images["vpravo"] = ImageTk.PhotoImage(img.rotate(angle, expand=True))
                im_flip = ImageOps.mirror(img.rotate(angle, expand=True))
                self.images["vlavo"] = ImageTk.PhotoImage(im_flip)


        self.planned_move = False

    def turn_right(self):
        if self.rotation == "vlavo/vpravo" or self.rotation == "vsetky smery":
            self.actual_rotation = "vpravo"

    def turn_left(self):
        if self.rotation == "vlavo/vpravo" or self.rotation == "vsetky smery":
            self.actual_rotation = "vlavo"

    def turn_up(self):
        if self.rotation == "dole/hore" or self.rotation == "vsetky smery":
            self.actual_rotation = "hore"

    def turn_down(self):
        if self.rotation == "dole/hore" or self.rotation == "vsetky smery":
            self.actual_rotation = "dole"

    def draw(self):
        if self.rotation == "-":
            self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')
        else:
            self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.images[self.actual_rotation],
                                                       anchor='c')

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
        if not (col >= 0 and row >= 0 and row < self.map.rows and col < self.map.cols):
            playsound.playsound(WRONG_SOUND, False)
            return True, "out"
        if isinstance(self.map.array[row][col], Blank) and self.map.array[row][col].guarded:
            playsound.playsound(WRONG_SOUND, False)
            return True, self.map.array[row][col].guarded_by
        if isinstance(self.map.array[row][col], Obstacle):
            playsound.playsound(WRONG_SOUND, False)
            return True, self.map.array[row][col].name
        return False, None

    def check_collectible(self, row, col):
        if isinstance(self.map.array[row][col], Collectible):
            collectible_name = self.map.array[row][col].name
            self.map.array[row][col].remove()
            self.map.array[row][col].remove()
            blank = Blank(self.map, row, col)
            self.map.array[row][col] = blank
            self.coll_path.append(collectible_name)
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
        if self.map.task.parent.parent.actual_regime == "planovaci" and self.planned_move == False:
            self.map.task.parent.parent.road.add_move("basic", "down")
            return None, None
        wrong_move, obsta = self.check_guarding_obstacle(self.row + 1, self.col)
        if wrong_move:
            return "wrong", obsta
        if self.row + 1 < self.map.rows:
            row, col = self.row + 1, self.col
            self.trajectory.append([self.row, self.col, self.x, self.y, None, self.map.array[row][col], self.actual_rotation])
            self.row += 1
            self.turn_down()
            rot = self.actual_rotation
            self.map.task.parent.parent.move_img_smoothly(self.images[rot], self.x, self.y, self.x, self.map.xs[self.row])
            self.y = self.map.xs[self.row]

            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part("ok", "down")
            self.steps_count += 1
            if self.map.task.parent.parent.actual_regime == "priamy":
                self.map.task.check_answer()
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
            self.trajectory.append([self.row, self.col, self.x, self.y, None, self.map.array[row][col], self.actual_rotation])
            self.row -= 1
            self.turn_up()
            rot = self.actual_rotation
            self.map.task.parent.parent.move_img_smoothly(self.images[rot], self.x, self.y, self.x, self.map.xs[self.row])
            self.y = self.map.xs[self.row]
            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part('ok', 'up')
            self.steps_count += 1
            if self.map.task.parent.parent.actual_regime == "priamy":
                self.map.task.check_answer()
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
            self.trajectory.append([self.row, self.col, self.x, self.y, None, self.map.array[row][col], self.actual_rotation])
            self.col += 1
            self.turn_right()
            rot = self.actual_rotation
            self.map.task.parent.parent.move_img_smoothly(self.images[rot], self.x, self.y, self.map.ys[self.col], self.y)
            self.x = self.map.ys[self.col]
            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part('ok', 'right')

            self.steps_count += 1
            if self.map.task.parent.parent.actual_regime == "priamy":
                self.map.task.check_answer()
            return "ok", colectible
        else:
            return "wrong", obsta

    def move_left(self):
        if self.map.task.parent.parent.actual_regime == "planovaci" and self.planned_move == False:
            self.map.task.parent.parent.road.add_move("basic", "left")
            return None, None
        wrong_move, obsta = self.check_guarding_obstacle(self.row, self.col - 1)
        if wrong_move:
            return "wrong", obsta
        if self.col - 1 >= 0:
            row, col = self.row, self.col - 1
            self.trajectory.append([self.row, self.col + 1, self.x, self.y, None, self.map.array[row][col], self.actual_rotation])
            self.col -= 1
            self.turn_left()
            rot = self.actual_rotation
            self.map.task.parent.parent.move_img_smoothly(self.images[rot], self.x, self.y, self.map.ys[self.col], self.y)
            self.x = self.map.ys[self.col]

            self.draw_trajectory()
            colectible = self.remove_draw_add_road_part('ok', 'left')

            self.steps_count += 1
            if self.map.task.parent.parent.actual_regime == "priamy":
                self.map.task.check_answer()
            return "ok", colectible
        else:
            return "wrong", obsta

    def remove_trajectory(self):
        while self.trajectory_lines:
            self.map.canvas.delete(self.trajectory_lines.pop(0))

    def step_back(self, plan=False, move=True):
        if len(self.trajectory) > 0:
            row, col, x, y, t, obj, rotation = self.trajectory.pop(-1)
            self.map.array[obj.row][obj.col] = obj
            if isinstance(obj, Collectible):
                self.coll_path.remove(obj.name)
                self.coll_collected[obj.name] -= 1

                if self.coll_collected[obj.name] == 0:
                    del self.coll_collected[obj.name]

            obj.draw()
            self.steps_count -= 1
            self.row = row
            self.col = col
            self.actual_rotation = rotation
            if move:
                self.map.task.parent.parent.move_img_smoothly(self.images[rotation], self.x, self.y, x, y)
            self.x = x
            self.y = y

            self.remove()
            self.draw()
            if len(self.trajectory) == 0:
                self.row = self.start_row
                self.col = self.start_col
            if plan == False:
                self.map.canvas.delete(t)
                self.map.task.parent.parent.road.remove_last_part()

        if plan == True:
            for traj in self.trajectory_lines:
                self.map.canvas.tag_raise(traj)
            self.map.canvas.tag_raise(self.img_id)

    def draw_trajectory(self):
        row, col, x, y, _, obj, rotation = self.trajectory[-1]
        t = self.map.canvas.create_line(x, y, self.x, self.y, fill=self.map.trajectory_col, width=10)
        self.trajectory[-1][4] = t
        self.trajectory_lines.append(t)

    def draw_full_trajectory(self):
        x, y = self.start_x, self.start_y
        for i in range(len(self.trajectory)):
            row, col, xx, yy, _, obj, rotation = self.trajectory[i]
            t = self.map.canvas.create_line(x, y, xx, yy, fill=self.map.trajectory_col, width=10)
            self.trajectory_lines.append(t)

            x = xx
            y = yy

        t = self.map.canvas.create_line(x, y, self.x, self.y, fill=self.map.trajectory_col, width=10)
        self.trajectory_lines.append(t)


    def reset_game(self, plan=False):
        while len(self.trajectory) > 0:
            self.step_back(plan=plan, move=False)

        self.actual_rotation = self.start_rotation
        self.coll_collected = {}
        self.coll_path = []
        self.row = self.start_row
        self.col = self.start_col
        self.x = self.start_x
        self.y = self.start_y
        self.steps_count = 0
        self.trajectory = []
        self.remove()
        self.draw()
