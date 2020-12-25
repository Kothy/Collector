from PIL import Image, ImageTk
import copy

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
        self.textWithPictures(x, y, text, copy.deepcopy(self.images), width)

    def resize(self, imgName, w, h):
        img = Image.open(imgName)
        return img.resize((w, h), Image.ANTIALIAS)

    def text_dims(self, txt):
        bounds = self.canvas.bbox(txt)
        w = bounds[2] - bounds[0]
        h = bounds[3] - bounds[1]
        ch = abs(bounds[1] - bounds[3]) / 2
        return w, h, ch

    def text_coords(self, txt):
        return self.canvas.bbox(txt)

    def textWithPictures(self, x, y, text, pictures, row_width):
        image_height = 38
        # self.canvas.create_rectangle(x, y - 25, x + row_width, y + 200)
        texts = text.split(" ")
        x_start = x
        id = None
        for word in texts:
            if word == "_":
                word_w = 45
            elif word == "\n":
                x = x_start
                y += 40
                continue
            else:
                id = self.canvas.create_text(x, y, fill="#0a333f",
                            font=('Comic Sans MS', 16, 'italic bold'), text=word + " ", anchor="w")
                self.objects.append(id)
                w, h, text_center_height = self.text_dims(id)
                word_w = w

            if x + word_w > x_start + row_width:
                y += 40
                x = x_start

            if word == "_":
                picture = pictures.pop(0)
                img = ImageTk.PhotoImage(self.resize(picture, image_height, image_height))
                img_id = self.canvas.create_image(x, y, image=img, anchor="w")
                self.objects.append(img_id)
                self.images_on_canvas.append(img)
            else:
                self.canvas.coords(id, x, y)
            x += word_w

    def remove(self):
        for obj in self.objects:
            self.canvas.delete(obj)