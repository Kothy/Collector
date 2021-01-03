from PIL import Image, ImageTk
import copy
from CommonFunctions import resize_image

LINE_HEIGHT = 40


class TextWithImages:
    def __init__(self, canvas, x, y, width, text, images):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.text = text
        self.images_on_canvas = []
        self.images = images
        self.objects = []
        self.text_size = 16
        self.textWithPictures(self.x + 15, self.y, self.text, copy.deepcopy(self.images), self.width)

    def resize(self, imgName, w, h):
        img = Image.open(imgName)
        return resize_image(img, w, h)

    def text_dims(self, txt):
        bounds = self.canvas.bbox(txt)
        w = bounds[2] - bounds[0]
        h = bounds[3] - bounds[1]
        ch = abs(bounds[1] - bounds[3]) / 2
        return w, h, ch

    def text_coords(self, txt):
        return self.canvas.bbox(txt)

    def textWithPictures(self, x, y, text, pictures, row_width):
        image_height = LINE_HEIGHT
        # self.canvas.create_rectangle(x, y - 25, x + row_width, y + 200)
        texts = text.split(" ")
        x_start = x
        id = None
        lines = 1
        for i in range(len(texts)):
            # print(repr(text[i]))
            if texts[i] == "":
                continue
            if texts[i] == "_":
                word_w = 45
            elif texts[i] == "\n":
                x = x_start
                y += LINE_HEIGHT
                lines += 1
                continue
            else:
                t = texts[i] if texts[i] == "," else texts[i] + " "

                id = self.canvas.create_text(x, y, fill="#0a333f",
                            font=('Comic Sans MS', self.text_size, 'italic bold'), text=t, anchor="w")
                self.objects.append(id)
                w, h, text_center_height = self.text_dims(id)
                word_w = w

            if x + word_w > x_start + row_width:
                y += LINE_HEIGHT
                lines += 1
                x = x_start

            if texts[i] == "_":
                picture = pictures.pop(0)
                img = ImageTk.PhotoImage(self.resize(picture, image_height, image_height))
                img_id = self.canvas.create_image(x, y, image=img, anchor="w")
                self.objects.append(img_id)
                self.images_on_canvas.append(img)
            else:
                self.canvas.coords(id, x, y)
            x += word_w
        if lines > 2:
            self.remove()
            self.text_size -= 1
            self.images_on_canvas = []
            self.objects = []
            self.textWithPictures(self.x, self.y, self.text, copy.deepcopy(self.images), self.width)
        # print("pocet riadkov yadania", lines)

    def remove(self):
        for obj in self.objects:
            self.canvas.delete(obj)
