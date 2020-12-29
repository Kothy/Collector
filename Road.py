from CanvasObject import CanvasObject
from RoadPart import RoadPart


class Road(CanvasObject):
    def __init__(self, move_imgs, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.move_imgs = move_imgs
        self.selected_parts = []
        self.create_road_parts()

    def create_road_parts(self):
        self.road_parts = [RoadPart(i, self) for i in range(16)]
        self.number_of_active_road_parts = 0
        # print(self.move_imgs)
        # for i in range(16):           # len test, nechavam to tu, aby si videla, ako to cca vyzera
        #     self.add_move('basic', ['left', 'right', 'up', 'down'][i%4])
        #     self.road_parts[i].add_obstacle(self.move_imgs['ok'][i%4])        # tu by mal byt spracovany obrazok danej

    def add_move(self, move_type, direction):
        if self.number_of_active_road_parts > 15:
            return
        direction_dict = {'right': 0, 'up': 1, 'left': 2, 'down': 3}
        self.road_parts[self.number_of_active_road_parts].hide()
        self.road_parts[self.number_of_active_road_parts].set_move_img(
            self.move_imgs[move_type][direction_dict[direction]])
        self.road_parts[self.number_of_active_road_parts].show()
        self.road_parts[self.number_of_active_road_parts].color = move_type
        self.road_parts[self.number_of_active_road_parts].direction = direction
        self.number_of_active_road_parts += 1

    def wrong_in_road(self):
        for part in self.road_parts:
            if part.color == "wrong":
                return True
        return False


    def count_active_parts(self):
        count = 0
        for part in self.road_parts:
            if part.move is not None:
                count += 1
        return count

    def remove_last_part(self):
        active = self.number_of_active_road_parts
        if active < 16 and self.parent.actual_regime == "priamy" and self.road_parts[active].move is not None:
            self.road_parts[active].hide()
            self.road_parts[active].deselect()

        if self.number_of_active_road_parts > 0:
            self.road_parts[self.number_of_active_road_parts - 1].hide()
            self.road_parts[self.number_of_active_road_parts - 1].deselect()
            self.number_of_active_road_parts -= 1

    def remove_part(self, index):
        self.road_parts[index].remove()

    def road_part_clicked(self, index):
        pass

    def hide(self):
        for part in self.road_parts:
            part.hide()

    def show(self):
        for part in self.road_parts:
            part.show()

    def remove_all_selected(self):
        dirs = []
        for part in self.road_parts:
            if part.index not in self.selected_parts and part.move is not None:
                dirs.append([part.color, part.direction, None])
                if part.obstacle is not None:
                    dirs[-1][2] = part.obstacle_img

        self.clear_road()
        self.road_parts = []
        self.create_road_parts()

        for color, dir, obs in dirs:
            self.add_move(color, dir)
            if obs is not None:
                self.road_parts[self.number_of_active_road_parts - 1].add_obstacle(obs)

        self.selected_parts = []

    def clear_road(self):
        for part in self.road_parts:
            part.deselect()
            part.hide()
            part.selected = False
        self.number_of_active_road_parts = 0

    def clear_wrong_ingnored(self):
        active = self.number_of_active_road_parts
        num = self.number_of_active_road_parts
        for i in range(active):
            road_p = self.road_parts[i]
            color = self.road_parts[i].color
            if color == "wrong" or color == "ignored":
                road_p.hide()
                road_p.remove()
                num -= 1
        self.number_of_active_road_parts = num

    def wrong_ignored_in_road(self):
        for part in self.road_parts:
            if part.color == "wrong" or part.color == "ignored":
                return True
        return False
