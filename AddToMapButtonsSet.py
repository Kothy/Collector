from PIL import Image, ImageTk
from CommonFunctions import resize_image
from CanvasObject import CanvasObject

class AddToMapButtonsSet(CanvasObject):

    def __init__(self, parent, folder_name, x, y):
        self.parent, self.canvas = parent, parent.canvas
        self.folder_name = folder_name
        self.x, self.y = x, y
        self.selected = ('character', 0)
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.imgs = {'character':[], 'collectible':[], 'obstacle':[]}
        for obstacle in 'xyz':
            try:
                img = Image.open('mapy/' + self.folder_name + '/obstacles/' + obstacle + '.png')
                img = resize_image(img, 32, 32)
                self.imgs['obstacle'].append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                break
        for collectible in 'abcd':
            try:
                img = Image.open('mapy/' + self.folder_name + '/collectibles/' + collectible + '.png')
                img = resize_image(img, 32, 32)
                self.imgs['collectible'].append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                break
        img = Image.open('mapy/' + self.folder_name + '/character.png')
        img = resize_image(img, 32, 32)
        self.imgs['character'].append(ImageTk.PhotoImage(img))

    def create_buttons(self):
        character = [AddToMapButton(self, 'character', 0, self.imgs['character'][0])]
        collectibles = [AddToMapButton(self, 'collectible', i, self.imgs['collectible'][i])
                        for i in range(len(self.imgs['collectible']))]
        obstacles = [AddToMapButton(self, 'obstacle', i, self.imgs['obstacle'][i])
                     for i in range(len(self.imgs['obstacle']))]
        self.buttons = {'character': character, 'obstacle': obstacles, 'collectible': collectibles}
        self.parts = character + collectibles + obstacles

    def button_clicked(self, identifier):
        if self.selected != identifier:
            self.buttons[self.selected[0]][self.selected[1]].deselect()
            self.selected = identifier

class AddToMapButton(CanvasObject):

    def __init__(self, parent, type, index, img):
        self.parent, self.canvas = parent, parent.canvas
        self.type = type
        self.index = index
        self.x = self.parent.x + self.index * 50
        self.y = self.parent.y + {'character': 2, 'obstacle': 1, 'collectible': 0}[self.type] * 45
        self.img = img
        self.border = None
        self.create_button()

    def create_button(self):
        self.parts = [self.canvas.create_image(self.x, self.y+16, anchor='w', image=self.img)]
        self.canvas.tag_bind(self.parts[0], '<ButtonPress-1>', self.clicked)
        if self.type == 'character':
            self.select()

    def get_name(self):
        return 'character' if type == 'character' else ('abcd'[self.index] if type == 'collectible' else 'xyz'[self.index])

    def select(self):
        if self.border is not None:
            return
        self.border = self.canvas.create_rectangle(self.x - 3, self.y - 3, self.x + 35, self.y + 35,
                                                   fill=None, outline='darkviolet', width=2)
        self.parts.append(self.border)

    def deselect(self):
        self.canvas.delete(self.border)
        self.border = None
        self.parts = self.parts[:1]

    def clicked(self, _):
        self.select()
        self.parent.button_clicked((self.type, self.index))
