from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join
import math
from CommonFunctions import resize_image_by_height


class ClickableList:
    def __init__(self, x, y, w, h, canvas, parent):
        self.parent = parent
        self.x = x
        self.y = y
        img_prev = Image.open('obrazky/prev.png')
        img_prev = resize_image_by_height(img_prev, 40)
        img_next = Image.open('obrazky/next.png')
        img_next = resize_image_by_height(img_next, 40)
        self.prev_arrow = ImageTk.PhotoImage(img_prev)
        self.next_arrow = ImageTk.PhotoImage(img_next)
        self.height = h
        self.width = w
        self.buttons = []
        self.canvas = canvas
        self.parent.solve_screen_keyboard.hide()
        self.line_h = 60
        self.item_h = 45
        self.bottom_pad = 40
        self.top_pad = 40
        self.shift = int(self.width / 15)
        self.col_width = int(w/2)
        self.on_one_page = math.floor((self.height - self.bottom_pad - self.top_pad) / self.line_h) * 2
        self.current_page = 0
        self.pages = []
        self.load_buttons()
        self.draw_page_buttons()

        self.selected = None
        self.draw()

    def remove(self):
        self.remove_current_page()
        self.canvas.delete(self.prev_arrow_obj)
        self.canvas.delete(self.next_arrow_obj)

    def load_buttons(self):
        x = self.x + self.width / 2.1 + self.shift
        y = self.y + self.top_pad
        mypath = "sady_uloh"
        all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for button in all_files:
            self.buttons.append(ListButton(x - self.col_width/2, y, int((self.width/2) - 100),
                                           self.item_h, button.split(".")[0], self.canvas, self.shift, self))
            y += self.line_h

        i = 0
        while i < len(self.buttons):
            self.pages.append((i, i + self.on_one_page - 1))
            i += self.on_one_page

    def deselect_all(self):
        for button in self.buttons:
            if button.selected == True:
                button.leave(None)

    def draw_page_buttons(self):
        x = self.x + self.width / 2
        y = self.y + self.height - 40
        self.prev_arrow_obj = self.canvas.create_image(x - self.bottom_pad, y, image=self.prev_arrow, anchor="c")
        self.next_arrow_obj = self.canvas.create_image(x + self.bottom_pad, y, image=self.next_arrow, anchor="c")
        self.canvas.tag_bind(self.prev_arrow_obj, '<ButtonPress-1>', self.prev_page)
        self.canvas.tag_bind(self.next_arrow_obj, '<ButtonPress-1>', self.next_page)

    def generate_colors(self):
        return ["red2", "orange", "yellow2", "green2", "blue", "violet"]

    def draw(self):
        y = self.y + self.top_pad
        middle = False
        start_i = self.pages[self.current_page][0]
        end_i = self.pages[self.current_page][1]
        middle_i = (self.current_page * self.on_one_page) + int(self.on_one_page/2)

        colors = self.generate_colors()
        for i in range(len(self.buttons)):
            if i >= start_i and i <= end_i and i < middle_i:
                # lava strana
                self.buttons[i].y = y
                self.buttons[i].change_color(colors.pop(0))
                self.buttons[i].draw()
                y += self.line_h

            elif i >= middle_i and i <= end_i:
                # prava strana
                if not middle:
                    middle = True
                    y = self.y + self.top_pad
                    colors = self.generate_colors()
                self.buttons[i].y = y
                self.buttons[i].shifted = True
                self.buttons[i].change_color(colors.pop(0))
                self.buttons[i].draw()
                y += self.line_h

    def next_page(self, _):
        self.remove_current_page()
        self.current_page += 1
        if self.current_page > len(self.pages) - 1:
            self.current_page = 0
        self.draw()

    def prev_page(self, _):
        self.remove_current_page()
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = len(self.pages) - 1
        self.draw()

    def remove_current_page(self):
        start_i = self.pages[self.current_page][0]
        end_i = self.pages[self.current_page][1]
        for i in range(len(self.buttons)):
            if i >= start_i and i <= end_i:
                self.buttons[i].remove()


class ListButton:
    def __init__(self, x, y, w, h, text, canvas, fold_img_h, list):
        self.x = x
        self.y = y
        self.text = text
        self.canvas = canvas
        self.folder_img_h = fold_img_h
        self.width = w
        self.height = h
        self.is_selected = False
        self.list = list
        self.outline_id = 0
        self.shifted = False
        self.alt_x = self.x + self.width + 58 + 30
        self.color = "green3"
        self.selected = False
        self.text_color = 'white' if self.color in ('violet', 'red', 'blue', 'green3', 'green4') else '#0a333f'
        self.load_images()

    def get_upper_corner(self):
        return self.x - self.width / 2, self.y - self.height / 2

    def get_lower_corner(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def remove(self):
        self.canvas.delete(self.textObj)
        self.canvas.delete(self.imageObj)
        self.canvas.delete(self.outline_id)
        self.canvas.delete(self.folderObj)
        self.canvas.delete(self.hoveredObj)

    def click(self, _):
        self.list.parent.solve_screen_keyboard.show()
        self.list.remove()
        self.list.parent.draw_task_assignment(self.text)

    def choose_text_color(self):
        if self.color in ('violet', 'red', 'blue', 'green3', 'green4', "red2"):
            self.text_color = "white"
        else:
            self.text_color = '#0a333f'

    def change_color(self, color):
        self.color = color
        self.choose_text_color()
        self.load_images()

    def load_images(self):
        img = Image.open('obrazky/buttons/{}.png'.format(self.color))
        img = img.resize((self.width, self.height), Image.ANTIALIAS)
        img3 = Image.open('obrazky/buttons/green.png')
        img3 = img3.resize((self.width, self.height), Image.ANTIALIAS)
        img2 = Image.open('obrazky/folder_icon.png')
        img2 = img2.resize((self.height + 10, self.height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(img)
        self.folder_img = ImageTk.PhotoImage(img2)
        self.hovered_img = ImageTk.PhotoImage(img3)

    def enter(self, _):
        self.list.deselect_all()
        self.canvas.itemconfigure(self.imageObj, state="hidden")
        self.canvas.itemconfigure(self.hoveredObj, state='normal')
        self.canvas.itemconfigure(self.textObj, fill='#0a333f')
        self.selected = True

    def leave(self, _):
        self.selected = False
        self.canvas.itemconfigure(self.hoveredObj, state='hidden')
        self.canvas.itemconfigure(self.imageObj, state="normal")
        self.canvas.itemconfigure(self.textObj, fill=self.text_color)

    def draw(self):
        fih = self.folder_img_h
        x = self.x
        if self.shifted:
            x = self.alt_x

        self.hoveredObj = self.canvas.create_image(x, self.y, image=self.hovered_img, anchor="c")
        self.imageObj = self.canvas.create_image(x, self.y, image=self.image, anchor="c")
        self.folderObj = self.canvas.create_image(x - self.width / 2.2- fih, self.y, image=self.folder_img,
                                                  anchor="c")
        self.textObj = self.canvas.create_text(x, self.y, font=("Comic Sans MS", 15), fill=self.text_color, text=self.text.replace("_"," "),
                                               anchor="c")

        self.canvas.tag_bind(self.folderObj, '<ButtonPress-1>', self.click)
        self.canvas.tag_bind(self.hoveredObj, '<ButtonPress-1>', self.click)
        self.canvas.tag_bind(self.textObj, '<ButtonPress-1>', self.click)

        self.canvas.tag_bind(self.imageObj, '<Enter>', self.enter)
        self.canvas.tag_bind(self.textObj, '<Enter>', self.enter)
        self.canvas.tag_bind(self.hoveredObj, '<Leave>', self.leave)
        self.canvas.tag_bind(self.textObj, '<Leave>', self.leave)
