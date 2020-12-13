from CanvasObject import CanvasObject


class CheckBox(CanvasObject):
    def __init__(self, parent, index, x, y, text, checked_img, unchecked_img, checked=False):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.x, self.y = x, y
        self.text = text
        self.imgs = [checked_img, unchecked_img]
        self.checked = checked
        self.id = None
        self.disable = None
        self.create_checkbox()

    def check(self):
        if not self.checked:
            self.checked = True
            self.destroy()
            self.create_checkbox()
            if self.disable is not None and self.text == "žiadne":
                self.disable.change_color("grey")
            elif self.disable is not None and self.text != "žiadne":
                self.disable.change_color("light_blue")


    def uncheck(self):
        self.checked = False
        self.destroy()
        self.create_checkbox()

    def click(self, _):
        self.parent.checkbox_clicked(self.index)
        self.check()

    def create_checkbox(self):
        self.id = self.canvas.create_image(self.x, self.y + self.index * 40, image=self.imgs[0 if self.checked else 1],
                                           anchor='center')
        self.text_id = self.canvas.create_text(self.x + 20, self.y + self.index * 40, fill="#114c32",
                                               font=('Comic Sans MS', 13, 'italic bold'), anchor='w', width=330,
                                               text=self.text)

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.click)
        self.canvas.tag_bind(self.text_id, "<ButtonPress-1>", self.click)

        self.parts = [self.id, self.text_id]

    def destroy(self):
        if self.id is not None:
            self.canvas.delete(self.id)
            self.canvas.delete(self.text_id)
            self.id, self.text_id = None, None