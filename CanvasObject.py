class CanvasObject:
    def __init__(self, parent, parts, hidden=True):
        self.parent, self.canvas = parent, parent.canvas
        self.parts = parts
        if hidden:
            self.hide()

    def show(self):
        self.hidden = False
        for part in self.parts:
            if isinstance(part, CanvasObject):
                part.show()
            else:
                self.canvas.itemconfigure(part, state='normal')

    def hide(self):
        self.hidden = True
        for part in self.parts:
            if isinstance(part, CanvasObject):
                part.hide()
            else:
                self.canvas.itemconfigure(part, state='hidden')

    def destroy(self):
        for part in self.parts:
            if part is None:
                continue
            if isinstance(part, CanvasObject):
                part.destroy()
            else:
                self.canvas.delete(part)
        self.parts = []

    def to_the_front(self):
        for part in self.parts:
            self.canvas.tag_raise(part, 'all')