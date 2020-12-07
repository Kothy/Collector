import CanvasObject as co

class CheckBox(co.CanvasObject):
    def __init__(self, parent, index, x, y, text, checked_img, unchecked_img, options,checked=False):
        self.parent, self.canvas = parent, parent.canvas
        self.index = index
        self.options = options
        self.x, self.y = x, y
        self.text = text
        self.imgs = [checked_img, unchecked_img]
        self.checked = checked
        self.id = None
        self.create_checkbox()

    def check(self):
        if not self.checked:
            self.checked = True
            self.destroy()
            if self.options.checked_index is not None:
                self.options.checkboxes[self.options.checked_index].uncheck()
            self.options.checked_index = self.index
            self.create_checkbox()

    def uncheck(self):
        self.checked = False
        self.options.checked_index = None
        self.destroy()
        self.create_checkbox()

    def click(self, _):
        self.check()
        # if self.checked:
        #     self.uncheck()
        # else:
        #     self.check()

    def create_checkbox(self):
        self.id = self.canvas.create_image(self.x, self.y + self.index * 40, image=self.imgs[0 if self.checked else 1],
                                           anchor='center')
        self.text_id = self.canvas.create_text(self.x + 20, self.y + self.index * 40, fill="#114c32",
                                               font=('Comic Sans MS', 13, 'italic bold'), anchor='w', width=330,
                                               text=self.text)
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.click)

    def destroy(self):
        if self.id is not None:
            self.canvas.delete(self.id)
            self.canvas.delete(self.text_id)
            self.id, self.text_id = None, None