from PIL import Image, ImageTk


def resize_image_by_height(img, hsize):
    wpercent = (hsize / float(img.size[1]))
    basewidth = int((float(img.size[0]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


class ObjectList:
    def __init__(self, x, y, canvas, items):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.items = []
        for item in items:
            self.add_item(item)

    def add_item(self, img):
        self.items.append(ObjectListItem(img, len(self.items), self, self.canvas))

    def move_items(self):
        for i in range(len(self.items)):
            self.items[i].index = i
            self.items[i].draw()

    def remove_item(self, index):
        self.items.pop(index)


class ObjectListItem:
    def __init__(self, img, index, list, canvas):
        self.x = list.x
        self.y = list.y
        self.index = index
        self.canvas = canvas
        self.list = list
        self.file_name = img.split("/")[-1]
        self.text_id = 0
        self.delete_id = 0
        self.preview_id = 0

        image = Image.open('obrazky/delete.png')
        image = image.resize((35, 35), Image.ANTIALIAS)
        self.delete_img = ImageTk.PhotoImage(image)

        image2 = Image.open(img)
        image2 = image2.resize((35, 35), Image.ANTIALIAS)
        self.preview_img = ImageTk.PhotoImage(image2)

        self.draw()

    def remove(self):
        self.canvas.delete(self.preview_id)
        self.canvas.delete(self.text_id)
        self.canvas.delete(self.delete_id)

    def draw(self):
        self.remove()
        y = self.y + (self.index * 53)
        self.delete_id = self.canvas.create_image(self.x, y, image=self.delete_img, anchor='nw')
        self.preview_id = self.canvas.create_image(self.x + 40, y, image=self.preview_img, anchor='nw')
        self.text_id = self.canvas.create_text(self.x + 40 + self.preview_img.width() + 20, y, fill="#114c32",
                                               font=('Comic Sans MS', 13, 'italic'),
                                               anchor='nw', width=330, text=self.file_name)
        self.canvas.tag_bind(self.delete_id, "<ButtonPress-1>", self.remove_and_move_others)

    def remove_and_move_others(self, _):
        self.remove()
        self.list.items.pop(self.index)
        self.list.move_items()
