from CanvasObject import CanvasObject


class RoadPart(CanvasObject):
    def __init__(self, index, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.obstacle = None
        self.border = None
        self.move = None
        self.move_img = None

    def set_move_img(self, img):
        self.move_img = img

    def add_obstacle(self, obstacle_img):
        self.obstacle = self.canvas.create_image(25 + self.index * 50, 600, image=obstacle_img, anchor='nw')

    def remove_obstacle(self):
        if self.obstacle is not None:
            self.canvas.delete(self.obstacle)
            self.obstacle = None

    def clicked(self, _):
        if self.border is None:
            self.select()
        else:
            self.deselect()
        self.parent.road_part_clicked(self.index)

    def select(self):
        if self.border is not None:
            return
        self.border = self.canvas.create_rectangle(20 + self.index * 50, 553, 62 + self.index * 50, 595,
                                                   outline='darkviolet', width=3)

    def deselect(self):
        if self.border is None:
            return
        self.canvas.remove(self.border)
        self.border = None

    def hide(self):
        if self.move is not None:
            self.canvas.delete(self.move)
            self.move = None
            self.remove_obstacle()

    def show(self):
        if self.move_img is None:
            return
        self.move = self.canvas.create_image(25 + self.index * 50, 558, image=self.move_img, anchor='nw')
        self.canvas.tag_bind(self.move, "<Button-1>", self.clicked)