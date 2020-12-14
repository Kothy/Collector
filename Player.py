from Map import *


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
        img = Image.open("mapy/{}/character.png".format(self.map.name))
        img = resize_image(img, self.map.part_w, self.map.part_h)
        self.image = ImageTk.PhotoImage(img)
        # image = Image.new('RGBA', (self.map.part_w, self.map.part_h), translate_color(self.map.grid_col, 100))
        # self.trajectory_img = ImageTk.PhotoImage(image)
        self.planned_move = False

    def draw(self):
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')

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
            return True, self.map.array[row][col].guarded_by
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