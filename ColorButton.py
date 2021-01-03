from CanvasObject import CanvasObject
from PIL import Image, ImageTk


class ColorButton(CanvasObject):
    def __init__(self, parent, x, y, width, height, color, text, font_size=15):
        self.parent, self.canvas = parent, parent.canvas
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.text = text
        self.font_size = font_size
        self.command = None
        self.args = None
        self.create_button()

    def remove(self):
        self.canvas.delete(self.btn_bg)
        self.canvas.delete(self.text_obj)

    def create_button(self):
        image = Image.open("obrazky/buttons/" + self.color + ".png")
        image = image.resize((self.width, self.height), Image.ANTIALIAS)
        self.btn_img = ImageTk.PhotoImage(image)
        self.btn_bg = self.canvas.create_image(self.x, self.y + 2, image=self.btn_img, anchor='center')
        text_color = 'white' if self.color in ('violet', 'red', 'blue', 'green3', 'green4') else '#0a333f'
        self.text_obj = self.canvas.create_text(self.x, self.y, fill=text_color,
                                                font=('Comic Sans MS', self.font_size, 'italic bold'), anchor='center', width=330,
                                                text=self.text)

        self.parts = [self.btn_bg, self.text_obj]

    def bind(self, command, *args):
        self.canvas.tag_bind(self.btn_bg, '<ButtonPress-1>', lambda _: command(*args))
        self.canvas.tag_bind(self.text_obj, '<ButtonPress-1>', lambda _: command(*args))

    def bind2(self):
        self.canvas.tag_bind(self.btn_bg, '<ButtonPress-1>', lambda _: self.parent.rotation_changed())
        self.canvas.tag_bind(self.text_obj, '<ButtonPress-1>', lambda _: self.parent.rotation_changed())

    def bind_clicked(self):
        self.canvas.tag_bind(self.btn_bg, '<ButtonPress-1>', self.clicked)
        self.canvas.tag_bind(self.text_obj, '<ButtonPress-1>', self.clicked)

    def clicked(self, _):
        self.parent.clicked_btn(self.text)

    def change_text(self, text):
        self.text = text
        self.canvas.itemconfig(self.text_obj, text=text)

    def change_state(self, state):
        self.canvas.itemconfig(self.btn_bg, state=state)
        self.canvas.itemconfig(self.text_obj, state=state)

    def change_color(self, color):
        self.remove()
        self.color = color
        self.create_button()
        if color != "grey":
            self.bind2()
        else:
            self.change_text("-")

    def to_the_front(self):
        self.canvas.tag_raise(self.btn_bg, 'all')
        self.canvas.tag_raise(self.text_obj, 'all')