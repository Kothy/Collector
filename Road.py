from CanvasObject import CanvasObject
from RoadPart import RoadPart


class Road(CanvasObject):
    def __init__(self, move_imgs, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.move_imgs = move_imgs
        self.create_road_parts()

    def create_road_parts(self):
        self.road_parts = [RoadPart(i, self) for i in range(21)]
        self.number_of_active_road_parts = 0
        # print(self.move_imgs)
        # for i in range(16):           # len test, nechavam to tu, aby si videla, ako to cca vyzera
        #     self.add_move('basic', ['left', 'right', 'up', 'down'][i%4])
        #     self.road_parts[i].add_obstacle(self.move_imgs['ok'][i%4])        # tu by mal byt spracovany obrazok danej

    def add_move(self, move_type, direction):
        if self.number_of_active_road_parts > 15:
            return
        direction_dict = {'right': 0, 'up': 1, 'left': 2, 'down': 3}
        self.road_parts[self.number_of_active_road_parts].set_move_img(
            self.move_imgs[move_type][direction_dict[direction]])
        self.road_parts[self.number_of_active_road_parts].show()
        self.road_parts[self.number_of_active_road_parts].direction = direction
        self.number_of_active_road_parts += 1

    def remove_last_part(self):
        self.road_parts[self.number_of_active_road_parts - 1].hide()
        self.number_of_active_road_parts -= 1

    def road_part_clicked(self, index):
        pass

    def hide(self):
        for part in self.road_parts:
            part.hide()

    def show(self):
        for part in self.road_parts:
            part.show()

    def clear_road(self):
        for part in self.road_parts:
            part.hide()
        self.number_of_active_road_parts = 0
