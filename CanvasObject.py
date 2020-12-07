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