from CanvasObject import CanvasObject
from ObstacleOptionsItem import ObstacleOptionsItem
from CommonFunctions import *
from PIL import Image, ImageTk

class ObstacleOptions(CanvasObject):

    def __init__(self, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.mode_imgs = []
        self.obstacle_imgs = []

    def load_images(self, folder_name):
        self.mode_imgs = []
        self.obstacle_imgs = []
        for mode in ('point', 'cross', 'grid'):
            img = Image.open('obrazky/guard_modes/' + mode + '.png')
            self.mode_imgs.append(ImageTk.PhotoImage(img))

        for obstacle in 'xyz':
            try:
                img = Image.open('mapy/' + folder_name + '/obstacles/' + obstacle + '.png')
                img = resize_image(img, 32, 32)
                self.obstacle_imgs.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                break

    def fill_options(self, folder_name):
        self.load_images(folder_name)
        self.create_items()

    def create_items(self):
        self.parts = [ObstacleOptionsItem(self, i, self.obstacle_imgs[i], self.mode_imgs)
                      for i in range(len(self.obstacle_imgs))]