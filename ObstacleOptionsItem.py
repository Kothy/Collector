from CanvasObject import CanvasObject

class ObstacleOptionsItem(CanvasObject):

    def __init__(self, parent, index, obstacle_img, guard_imgs):
        self.parent, self.canvas = parent, parent.canvas
        self.img = obstacle_img
        self.guard_imgs = guard_imgs
        self.index = index
        self.selected = 0
        self.x, self.y = 320, 470 + self.index*50
        self.obstacle, self.guard_modes = None, []
        self.create_obstacle_settings_item()

    def create_obstacle_settings_item(self):
        self.obstacle = self.canvas.create_image(self.x, self.y, image=self.img, anchor='c')
        self.guard_modes = [GuardMode(self, i, self.guard_imgs[i], self.x + (i+1) * 50, self.y) for i in range(3)]
        guard_modes_obj = CanvasObject(self, self.guard_modes, False)
        self.parts = [self.obstacle, guard_modes_obj]

    def mode_clicked(self, index):
        if self.selected != index:
            self.guard_modes[self.selected].deselect()
            self.selected = index

    def get_selected_mode(self):
        return self.selected

class GuardMode(CanvasObject):

    def __init__(self, parent, index, img, x, y):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.img = img
        self.x, self.y = x, y
        self.draw_mode()
        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.selected)

    def draw_mode(self):
        self.id = self.canvas.create_image(self.x, self.y, image=self.img, anchor='c')
        self.border = None
        self.parts = [self.id]
        if self.index == 0:
            self.selected(None)

    def selected(self, _):
        if self.border is not None:
            return
        self.parent.mode_clicked(self.index)
        self.border = self.canvas.create_rectangle(self.x - 20, self.y - 20, self.x + 20, self.y + 20,
                                                   outline='darkviolet', width=3)
        self.parts.append(self.border)

    def deselect(self):
        self.canvas.delete(self.border)
        self.border = None
        self.parts = self.parts[:-1]