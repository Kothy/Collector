from CanvasObject import CanvasObject
from PIL import Image, ImageTk
from CommonFunctions import *

class TaskList(CanvasObject):

    def __init__(self, parent):
        self.parent, self.canvas = parent, parent.canvas
        self.parts = []
        self.tasks = []
        self.create_imgs()

    def create_imgs(self):
        image = Image.open('obrazky/delete.png')
        image = image.resize((35, 35), Image.ANTIALIAS)
        self.delete_img = ImageTk.PhotoImage(image)

        image = Image.open('obrazky/edit.png')
        image = image.resize((35, 35), Image.ANTIALIAS)
        self.edit_img = ImageTk.PhotoImage(image)

        image = Image.open('obrazky/up_down.png')
        image = resize_image(image, 30, 30)
        up_img = ImageTk.PhotoImage(image)
        image = image.rotate(180)
        down_img = ImageTk.PhotoImage(image)
        self.move_imgs = [up_img, down_img]

    def add_task(self, task):
        if len(self.tasks) >= 10:
            return
        self.tasks.append(task)
        self.parts.append(TaskListItem(self, task.name, len(self.parts), self.move_imgs, self.edit_img, self.delete_img))
        self.check_list_arrows()

    def remove_task(self, index):
        self.tasks = self.tasks[:index] + self.tasks[index+1:]
        self.parts[-1].destroy()
        self.parts = self.parts[:-1]
        self.rename_parts(index)
        self.check_list_arrows()
        if len(self.parts) == 9:
            self.parent.task_space_freed()

    def edit_task(self, index):
        pass

    def rename_parts(self, index, swap=False):
        if swap:
            self.parts[index].rename(self.tasks[index].name, index)
            self.parts[index - 1].rename(self.tasks[index - 1].name, index - 1)
            return
        for i in range(index, len(self.parts)):
            self.parts[i].rename(self.tasks[i].name, i)

    def move_task_up(self, index):
        self.tasks[index], self.tasks[index-1] = self.tasks[index-1], self.tasks[index]
        self.rename_parts(index, True)
        self.check_list_arrows()

    def check_list_arrows(self):
        if len(self.parts) == 0:
            return
        if len(self.parts) == 1:
            self.parts[0].hide_arrows()
            return
        self.parts[0].show_down_arrow()
        self.parts[0].hide_up_arrow()
        self.parts[-1].show_up_arrow()
        self.parts[-1].hide_down_arrow()
        for i in range(1, len(self.parts)-1):
            self.parts[i].show_arrows()

    def destroy(self):
        super(TaskList, self).destroy()
        self.tasks = []
        self.parent.task_space_freed()

    def is_empty(self):
        return self.parts == []

    def is_full(self):
        return len(self.parts) == 10

    def show(self):
        super(TaskList, self).show()
        self.check_list_arrows()

class TaskListItem(CanvasObject):

    def __init__(self, parent, task_name, index, move_imgs, edit_img, delete_img):
        self.parent, self.canvas = parent, parent.canvas
        self.index, self.name = index, task_name
        self.move_imgs, self.edit_img, self.delete_img = move_imgs, edit_img, delete_img
        self.create_task()

    def create_task(self):
        self.parts = [
            self.canvas.create_text(865, 135 + self.index*40, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                                  anchor='nw', width=330, text=str(self.index + 1) + '. ' + self.name),
            self.canvas.create_image(710, 138 + self.index * 40, image=self.move_imgs[0], anchor='nw'),
            self.canvas.create_image(740, 138 + self.index * 40, image=self.move_imgs[1], anchor='nw'),
            self.canvas.create_image(770, 135 + self.index * 40, image=self.edit_img, anchor='nw'),
            self.canvas.create_image(805, 135 + self.index * 40, image=self.delete_img, anchor='nw')
        ]
        self.canvas.tag_bind(self.parts[1], '<ButtonPress-1>', self.move_up_request)
        self.canvas.tag_bind(self.parts[2], '<ButtonPress-1>', self.move_down_request)
        self.canvas.tag_bind(self.parts[3], '<ButtonPress-1>', self.edit_request)
        self.canvas.tag_bind(self.parts[4], '<ButtonPress-1>', self.delete_request)

    def edit_request(self, _):
        self.parent.edit_task(self.index)

    def delete_request(self, _):
        self.parent.remove_task(self.index)

    def move_up_request(self, _):
        self.parent.move_task_up(self.index)

    def move_down_request(self, _):
        self.parent.move_task_up(self.index+1)

    def rename(self, new_name, index):
        self.name, self.index = new_name, index
        self.canvas.itemconfig(self.parts[0], text=str(index + 1) + '. ' + new_name)

    def show_up_arrow(self):
        self.canvas.itemconfig(self.parts[1], state='normal')

    def show_down_arrow(self):
        self.canvas.itemconfig(self.parts[2], state='normal')

    def show_arrows(self):
        self.show_up_arrow()
        self.show_down_arrow()

    def hide_up_arrow(self):
        self.canvas.itemconfig(self.parts[1], state='hidden')

    def hide_down_arrow(self):
        self.canvas.itemconfig(self.parts[2], state='hidden')

    def hide_arrows(self):
        self.hide_up_arrow()
        self.hide_down_arrow()