from CanvasObject import CanvasObject
from PIL import Image, ImageTk


class ColorButton(CanvasObject):
    def __init__(self, parent, x, y, width, height, color, text):
        self.parent, self.canvas = parent, parent.canvas
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.text = text
        self.create_button()

    def create_button(self):
        image = Image.open("obrazky/buttons/" + self.color + ".png")
        image = image.resize((self.width, self.height), Image.ANTIALIAS)
        self.btn_img = ImageTk.PhotoImage(image)
        self.btn_bg = self.canvas.create_image(self.x, self.y + 2, image=self.btn_img, anchor='center')
        text_color = 'white' if self.color in ('violet', 'red', 'blue', 'green3', 'green4') else '#0a333f'
        self.text_obj = self.canvas.create_text(self.x, self.y, fill=text_color,
                                                font=('Comic Sans MS', 15, 'italic bold'), anchor='center', width=330,
                                                text=self.text)

        self.parts = [self.btn_bg, self.text_obj]

    def change_text(self, text):
        pass