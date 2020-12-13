from CanvasObject import CanvasObject
import CheckBox as ch
from PIL import ImageTk, Image

class Options(CanvasObject):
    def __init__(self, parent, x, y, texts, checked_id=0, let_parent_know_about_changed=False):
        self.parent, self.canvas = parent, parent.canvas
        self.x, self.y = x, y
        self.checked_index = 0
        self.let_parent_know_about_changes = let_parent_know_about_changed
        self.create_checkboxes(texts, checked_id)

    def create_checkboxes(self, texts, checked_id):
        image = Image.open("obrazky/checkbox_checked.png")
        image = image.resize((30, 30), Image.ANTIALIAS)
        self.checked_img = ImageTk.PhotoImage(image)

        image = Image.open("obrazky/checkbox_un.png")
        image = image.resize((30, 30), Image.ANTIALIAS)
        self.unchecked_img = ImageTk.PhotoImage(image)

        ##        self.id = self.parent.canvas.create_image(100,500,image=self.checked_img, anchor='center') # skusala som, ci to vykresli aspon tu, nevykreslilo

        self.checkboxes = [ch.CheckBox(self, i, self.x, self.y, texts[i], self.checked_img, self.unchecked_img,
                                    True if checked_id == i else False) for i in range(len(texts))]
        self.parts = self.checkboxes

    def destroy(self):
        for checkbox in self.checkboxes:
            checkbox.destroy()

    def checkbox_clicked(self, index):
        if self.checked_index != index:
            self.checkboxes[self.checked_index].uncheck()
            if self.let_parent_know_about_changes:
                self.parent.options_changed(index)
        self.checked_index = index

