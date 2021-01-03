from CanvasObject import CanvasObject
from PIL import Image, ImageTk


class RoadPart(CanvasObject):
    def __init__(self, index, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.obstacle = None
        self.border = None
        self.move = None
        self.direction = None
        self.move_img = None
        self.color = "basic"
        self.obstacle_img = None

    def set_move_img(self, img):
        self.move_img = img

    def add_obstacle(self, obstacle_img):
        if isinstance(obstacle_img, str):
            img = Image.open(obstacle_img)
            img = img.resize((30, 30))
            self.obstacle_img = ImageTk.PhotoImage(img)
        else:
            self.obstacle_img = obstacle_img

        self.obstacle = self.canvas.create_image(25 + self.index * 50, 600, image=self.obstacle_img, anchor='nw')

    def remove_obstacle(self):
        if self.obstacle is not None:
            self.canvas.delete(self.obstacle)
            self.obstacle = None
            self.obstacle_img = None

    def clicked(self, _):
        if self.border is None:
            self.select()
        else:
            self.deselect()
        self.parent.road_part_clicked(self.index)

    def select(self):
        if self.border is not None:
            return
        for index in self.parent.selected_parts:
            self.parent.road_parts[index].deselect()

        self.parent.selected_parts.append(self.index)
        self.border = self.canvas.create_rectangle(20 + self.index * 50, 553, 62 + self.index * 50, 595,
                                                   outline='darkviolet', width=3)

    def deselect(self, rem_from_arr=True):
        if self.border is None:
            return
        self.canvas.delete(self.border)
        self.border = None
        if rem_from_arr and self.index in self.parent.selected_parts:
            self.parent.selected_parts.remove(self.index)

    def change_color(self, color):
        self.hide()
        self.remove()
        self.color = color
        direction_dict = {'right': 0, 'up': 1, 'left': 2, 'down': 3}
        img = self.parent.move_imgs[color][direction_dict[self.direction]]
        self.move_img = img
        self.show()

    def change_direction(self, dir):
        color = self.color
        self.hide()
        self.remove(rem_from_arr=False)
        self.color = color
        self.direction = dir
        direction_dict = {'right': 0, 'up': 1, 'left': 2, 'down': 3}
        img = self.parent.move_imgs[self.color][direction_dict[dir]]
        self.move_img = img
        self.show()

    def hide(self):
        if self.move is not None:
            self.canvas.delete(self.move)
            self.move = None
            self.remove_obstacle()

    def unshow(self):
        if self.move is not None:
            self.canvas.itemconfig(self.move, state="hidden")
            if self.obstacle is not None:
                self.canvas.itemconfig(self.obstacle, state="hidden")

    def show(self):
        if self.move_img is None:
            return
        self.move = self.canvas.create_image(25 + self.index * 50, 558, image=self.move_img, anchor='nw')
        if self.obstacle is not None:
            self.obstacle = self.canvas.create_image(25 + self.index * 50, 600, image=self.obstacle_img, anchor='nw')
        self.canvas.tag_bind(self.move, "<Button-1>", self.clicked)

    def remove(self, rem_from_arr=True):
        if self.move_img is None:
            return
        self.canvas.delete(self.move_img)
        if self.obstacle is not None:
            self.canvas.delete(self.obstacle)

        self.deselect(rem_from_arr)
        self.hide()

        self.color = None
        self.move_img = None
        self.obstacle = None
        self.obstacle_img = None
