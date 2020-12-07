from CanvasObject import CanvasObject

class Keyboard(CanvasObject):
    def __init__(self, parent, parts):
        super(Keyboard, self).__init__(parent, parts)
        self.bind_keys()

    def bind_keys(self):
        pass