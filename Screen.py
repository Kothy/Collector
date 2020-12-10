from CanvasObject import CanvasObject


class Screen:
    def __init__(self, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.objects = []
        self.load_screen()

    def load_screen(self):
        pass

    def close_screen(self):
        for obj in self.objects:
            obj.destroy()

    def show_canvas_item(self, item):
        if isinstance(item, CanvasObject):
            item.show()
        else:
            self.canvas.itemconfigure(item, state='normal')

    def hide_canvas_item(self, item):
        if isinstance(item, CanvasObject):
            item.hide()
        else:
            self.canvas.itemconfigure(item, state='hidden')

    def destroy_canvas_item(self, item):
        if isinstance(item, CanvasObject):
            item.destroy()
        else:
            self.canvas.delete(item)

    def destroy(self):
        for object in self.objects:
            self.destroy_canvas_item(object)