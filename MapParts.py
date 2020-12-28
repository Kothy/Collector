from Map import *


class Blank:
    def __init__(self, map, i, j):
        self.map = map
        self.x, self.y = calculate_coords(i, j, self.map.rows, self.map.cols)
        self.y, self.x = self.map.xs[i], self.map.ys[j]
        self.row = i
        self.col = j
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
        img = resize_image(img, self.map.part_w - 4, self.map.part_h - 4)
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
        img = resize_image(img, self.map.part_w - 4, self.map.part_h - 4)
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
                id = self.draw_at(a, b, self.map.guarding_img)
                if id is not None:
                    self.map.array[a][b].guarded = True
                    self.map.array[a][b].guarded_by = self.name
                    self.guarded_pos.append((a, b))
                    self.guardians_ids.append(id)

            if self.guarding == "stvorec":
                for a, b in [(i - 1, j - 1), (i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1)]:
                    id = self.draw_at(a, b, self.map.guarding_img)
                    if id is not None:
                        self.map.array[a][b].guarded = True
                        self.map.array[a][b].guarded_by = self.name
                        self.guarded_pos.append((a, b))
                        self.guardians_ids.append(id)

    def draw_at(self, i, j, img):
        if i >= 0 and i < self.map.rows and j >= 0 and j < self.map.cols:
            y, x = self.map.xs[i], self.map.ys[j]
            id = self.map.canvas.create_image(x, y, image=img, anchor="c")
            part_w = self.map.part_w
            part_h = self.map.part_h
            id2 = self.map.canvas.create_image(x + (part_w/2) - 6, y - (part_h/2) + 6, image=self.map.guarding_img_x, anchor="ne")
            return id
        return None

    def get_guarded(self):
        return self.guarded_pos

    def remove(self):
        self.map.canvas.delete(self.img_id)
        self.map.canvas.delete(self.bg_img_id)
        for guard in self.guardians_ids:
            self.map.canvas.delete(guard)

    def __repr__(self):
        return self.name