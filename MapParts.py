from Map import *


class Blank:
    def __init__(self, map, i, j):
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
        self.guarded = False
        self.guards = []
        self.img_id = 0

    def draw(self): pass

    def remove(self):
        for guard in self.guards:
            self.map.canvas.delete(guard)
        self.guard = []

    def draw_guard(self):
        self.remove()
        self.guards.append(
                self.map.canvas.create_image(self.x, self.y, image=self.map.guarding_img, anchor='c'))
        self.guards.append(
        self.map.canvas.create_image(self.x, self.y, image=self.map.guarding_img_x, anchor='c'))

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
        img = resize_image(img, self.map.part_w - 6, self.map.part_h - 6)
        self.img = img
        self.image = ImageTk.PhotoImage(img)
        self.img_id = 0

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
        img = resize_image(img, self.map.part_w - 6, self.map.part_h - 6)
        # img_sizes = img.size
        img2 = Image.open("obrazky/guarding.png").resize((self.map.part_w - 4, self.map.part_h - 4))
        self.bg_img = ImageTk.PhotoImage(img2)
        self.img = img
        self.image = ImageTk.PhotoImage(img)
        self.guardians_ids = []
        self.guarded_pos = []

    def draw(self):
        self.bg_img_id = self.map.canvas.create_image(self.x, self.y, image=self.bg_img, anchor='c')
        self.img_id = self.map.canvas.create_image(self.x, self.y, image=self.image, anchor='c')
        self.draw_guardings()

    def draw_guardings(self):
        i = self.row
        j = self.col
        if self.guarding != "bod":
            for a, b in [(i-1, j), (i+1,j), (i,j+1), (i,j-1)]:
                id, id2 = self.draw_at(a, b, self.map.guarding_img)
                if id is not None:
                    self.map.array[a][b].guarded = True
                    self.map.array[a][b].guarded_by = self.name
                    self.guarded_pos.append((a, b))
                    self.guardians_ids.append(id)
                    self.guardians_ids.append(id2)
                    self.map.array[a][b].guards.append(id)
                    self.map.array[a][b].guards.append(id2)

            if self.guarding == "stvorec":
                for a, b in [(i - 1, j - 1), (i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
                    id,id2 = self.draw_at(a, b, self.map.guarding_img)
                    if id is not None:
                        self.map.array[a][b].guarded = True
                        self.map.array[a][b].guarded_by = self.name
                        self.guarded_pos.append((a, b))
                        self.guardians_ids.append(id)
                        self.guardians_ids.append(id2)
                        self.map.array[a][b].guards.append(id)
                        self.map.array[a][b].guards.append(id2)

    def draw_at(self, i, j, img):
        if i >= 0 and i < self.map.rows and j >= 0 and j < self.map.cols and isinstance(self.map.array[i][j], Blank):
            y, x = self.map.xs[i], self.map.ys[j]

            id, id2 = None, None
            if not self.map.array[i][j].guarded:
                id = self.map.canvas.create_image(x, y, image=img, anchor="c")
                id2 = self.map.canvas.create_image(x, y,
                                                   image=self.map.guarding_img_x, anchor="c")

            return id, id2
        return None,None

    def get_guarded(self):
        return self.guarded_pos

    def remove(self):
        self.map.canvas.delete(self.img_id)
        self.map.canvas.delete(self.bg_img_id)
        for guard in self.guardians_ids:
            self.map.canvas.delete(guard)

    def __repr__(self):
        return self.name
