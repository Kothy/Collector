from Screen import Screen
from ColorButton import ColorButton
from CanvasObject import CanvasObject
from PIL import Image, ImageTk
from Keyboard import Keyboard
from Road import Road
from ClickableList import ClickableList
from Task import TaskSet
from TextWithPicures import TextWithImages


class SolveScreen(Screen):
    def __init__(self, parent):
        super(SolveScreen, self).__init__(parent)

    def load_screen(self):
        self.panel_init()
        self.map_window_init()
        self.controls_window_init()
        self.road_window_init()
        self.task_window_init()
        self.show_common()

        self.clickeble_list = ClickableList(20, 70, 880, 460, self.canvas, self)

    def go_to_menu(self):
        print("Prechod do menu")

    def remove_lines(self, arr, num):
        for i in range(num):
            arr.pop(0)
        return arr

    def read_task(self, lines, map_name):
        task_index = int(float(lines.pop(0)))
        name = lines.pop(0).split(":")[1].strip()
        typ = lines.pop(0).split(":")[1].strip()
        regime = lines.pop(0).split(":")[1].strip()
        row = lines.pop(0).split(":")[1].strip()
        col = lines.pop(0).split(":")[1].strip()
        steps = lines.pop(0).split(":")[1].strip()
        assign = lines.pop(0).split(":")[1].strip()
        solvable = lines.pop(0).split(":")[1].strip()
        map_string = ""
        while lines[0] != "" and lines[0] != "##!EOF##":
            map_string += lines.pop(0) + "\n"

        char_name = "Emil"
        lines = self.remove_lines(lines, 1)
        self.tasks_set.add_task(name, typ, regime, row, col, steps, assign, map_string, map_name, char_name,solvable)
        # print(task_index, name, typ, regime, row, col, steps, assign, solvable, map_string)
        return lines


    def draw_task_assignment(self, name):
        self.canvas.itemconfig(self.task_text_set_choice, state="hidden")

        with open("sady_uloh/" + name + ".txt", "r") as file:
            full = file.read()

        lines = full.split("\n")
        lines.append("##!EOF##")
        tasks_set_name = lines.pop(0).split(":")[-1].strip()
        map_name = lines.pop(0).split(":")[-1].strip()

        lines = self.remove_lines(lines, 2)
        obstacles = []
        while lines[0] != "":
            splitted_obs = lines.pop(0).split(":")
            obstacles.append((splitted_obs[0], splitted_obs[1].strip()))

        lines = self.remove_lines(lines, 2)
        next_without_solve = lines.pop(0).split(":")[1].strip()

        lines = self.remove_lines(lines, 1)

        self.tasks_set = TaskSet(tasks_set_name, self.canvas, next_without_solve)
        while len(lines) > 0 and lines[0] != "##!EOF##":
             lines = self.read_task(lines, map_name)

        self.tasks_set.tasks[0].parse_assign()
        self.canvas.itemconfig(self.task_text_mode, state="normal")
        self.draw_map(map_name)

    def draw_map(self, map_name):
        img = Image.open("mapy/{}/map.png".format(map_name))
        img = img.resize((900, 480))
        self.map_bg_img = ImageTk.PhotoImage(img)

        self.map_bg_img_id = self.canvas.create_image(10, 60, image=self.map_bg_img, anchor='nw')

    def panel_init(self):
        self.task_name_text = self.canvas.create_text(530, 25, fill="#0a333f",
                                                      font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                      width=330, text='Uloha1')
        self.next_task_btn = ColorButton(self, 1180, 25, 150, 36, 'violet', 'Ďalšia úloha')
        self.prev_task_btn = ColorButton(self, 1015, 25, 160, 36, 'orange', 'Predošlá úloha')
        self.menu_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Menu')
        self.menu_btn.bind(self.go_to_menu)

        self.screen_panel = CanvasObject(self, [self.task_name_text,
                                                self.next_task_btn, self.prev_task_btn, self.menu_btn])

    def map_window_init(self):
        image = Image.new('RGBA', (900, 480), (141, 202, 73, 100))
        self.screen_map_bg_img = ImageTk.PhotoImage(image)
        screen_map_bg = self.canvas.create_image(10, 60, image=self.screen_map_bg_img, anchor='nw')
        screen_map_bg_border = self.canvas.create_rectangle(10, 60, 910, 540, outline='#b6e5da', width=2)

        self.solve_screen_map_bg = CanvasObject(self, [screen_map_bg, screen_map_bg_border])

        # TU BY SA MALI DO OKNA ROVNO NACITAT PRIECINKY SO SADAMI ULOH (najlepsie asi do 2 alebo 3 stlpcov, kedze je to siroke okno)
        # NA TLACIDLA POSUNUTIA BY MOHLO BYT POUZITE next_back.png z obrazkov, ak sa to bude dobre vyzerat

    def controls_window_init(self):
        image = Image.new('RGBA', (350, 90), (41, 175, 200, 100))
        self.screen_keys_bg_img = ImageTk.PhotoImage(image)
        screen_keys_bg = self.canvas.create_image(920, 550, image=self.screen_keys_bg_img, anchor='nw')
        screen_keys_bg_border = self.canvas.create_rectangle(920, 550, 1270, 640, outline='#b6e5da', width=2)

        self.arrows = []
        keyboard = []
        image = Image.open('obrazky/controls/key.png')
        image = image.resize((38, 38), Image.ANTIALIAS)
        for key, position in (('down', (980, 598)), ('right', (1020, 598)), ('up', (980, 555)), ('left', (940, 597))):
            self.arrows.append(ImageTk.PhotoImage(image))
            keyboard.append(self.canvas.create_image(position[0], position[1], image=self.arrows[-1], anchor='nw'))
            image = image.rotate(90)

        image = Image.open("obrazky/controls/back.png")
        image = image.resize((75, 75), Image.ANTIALIAS)
        self.backspace_img = ImageTk.PhotoImage(image)
        back = self.canvas.create_image(1080, 558, image=self.backspace_img, anchor='nw')

        image = Image.open("obrazky/controls/clear.png")
        image = image.resize((75, 75), Image.ANTIALIAS)
        self.clear_image = ImageTk.PhotoImage(image)
        clear = self.canvas.create_image(1185, 558, image=self.clear_image, anchor='nw')

        self.solve_screen_keyboard = CanvasObject(self,
                                                  [screen_keys_bg, screen_keys_bg_border, Keyboard(self, keyboard),
                                                   back, clear])

    def road_window_init(self):
        image = Image.new('RGBA', (900, 90), (41, 175, 200, 100))
        self.screen_road_bg_img = ImageTk.PhotoImage(image)
        screen_road_bg = self.canvas.create_image(10, 550, image=self.screen_road_bg_img, anchor='nw')
        screen_road_bg_border = self.canvas.create_rectangle(10, 550, 910, 640, outline='#b6e5da', width=2)

        self.solve_screen_road_bg = CanvasObject(self, [screen_road_bg, screen_road_bg_border])

        image = Image.open("obrazky/play.png")
        image = image.resize((72, 72), Image.ANTIALIAS)
        self.play_image = ImageTk.PhotoImage(image)
        self.play = self.canvas.create_image(825, 560, image=self.play_image, anchor='nw')

        self.move_imgs = {'basic': [], 'ok': [], 'wrong': [], 'ignored': []}
        for move_type in self.move_imgs:
            image = Image.open("obrazky/moves/" + move_type + ".png")
            image = image.resize((32, 32), Image.ANTIALIAS)
            for i in range(4):
                self.move_imgs[move_type].append(
                    ImageTk.PhotoImage(image))  # obrazky v poli v poradi: right, up, left, down
                image = image.rotate(90)
        self.road = Road(self.move_imgs, self)

        self.solve_screen_road = CanvasObject(self, [self.solve_screen_road_bg, self.road, self.play])

    def task_window_init(self):
        # texty tam su na skusku, daj ich potom odtialto prec :) self.task_text_obstacle potom vyuzi aj na info "Ziadne zadanie" v pripade volnej ulohy
        image = Image.new('RGBA', (350, 480), (255, 170, 79, 100))
        self.screen_task_bg_img = ImageTk.PhotoImage(image)
        screen_task_bg = self.canvas.create_image(920, 60, image=self.screen_task_bg_img, anchor='nw')
        screen_task_bg_border = self.canvas.create_rectangle(920, 60, 1270, 540, outline='#b6e5da', width=2)

        self.solve_screen_task_bg = CanvasObject(self, [screen_task_bg, screen_task_bg_border])

        self.task_text_collect = self.canvas.create_text(930, 70, fill="#0a333f",
                                                         font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                         width=330, text='Emil chce pozbierat')
        self.task_text_collectibles = [
            self.canvas.create_text(1095, 110, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'), anchor='n',
                                    width=330, text='práve 5 aaa, najviac 6 ccc'),
            self.canvas.create_text(1095, 150, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'), anchor='n',
                                    width=330, text='najviac 6 bbb a 0 ddd')]
        self.task_text_steps = self.canvas.create_text(930, 185, fill="#0a333f",
                                                       font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                       width=330, text='s pouzitim najviac 15 krokov.')
        self.task_text_path_info = self.canvas.create_text(930, 215, fill="#0a333f",
                                                           font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                           width=330, text='(v tomto pocte aj poradi)')
        self.task_text_obstacle = self.canvas.create_text(930, 255, fill="#0a333f",
                                                          font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                          width=330, text='Musi sa ale vyhnut polickam, ktore ohrozuje')
        self.task_text_obstacles = self.canvas.create_text(1095, 330, fill="#0a333f",
                                                           font=('Comic Sans MS', 15, 'italic bold'), anchor='n',
                                                           width=330, text='Liska alebo Voda')

        self.task_text_mode = self.canvas.create_text(930, 370, fill="#114c32",
                                                      font=('Comic Sans MS', 17, 'italic bold'), anchor='nw', width=330,
                                                      text='Emil:\n"Pomôžeš mi, prosím, naplánovať cestu?"\n\n\tRežim: plánovací')

        self.task_text_set_choice = self.canvas.create_text(1095, 285, fill="#0a333f",
                                                            font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                            width=330, text='Vyber sadu úloh')

        task_text_collectibles_obj = CanvasObject(self, self.task_text_collectibles)
        solve_screen_task_collectibles = CanvasObject(self, [self.task_text_collect, task_text_collectibles_obj])
        self.solve_screen_task_obstacles = CanvasObject(self, [self.task_text_obstacle, self.task_text_obstacles])

        image = Image.open('obrazky/swap_mode.png')
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.swap_mode_btn_img = ImageTk.PhotoImage(image)
        self.swap_mode_btn = self.canvas.create_image(1230, 500, image=self.swap_mode_btn_img, anchor='nw')

        self.solve_screen_task_mode = CanvasObject(self, [self.task_text_mode, self.swap_mode_btn])

        self.solve_screen_task_window = CanvasObject(self, [self.solve_screen_task_bg, solve_screen_task_collectibles,
                                                            self.task_text_steps, self.task_text_path_info,
                                                            self.task_text_set_choice,
                                                            self.solve_screen_task_obstacles,
                                                            self.solve_screen_task_mode])

    def show_common(
            self):  # zobrazi len to, co sa netyka konkretnych uloh, ak chces vidiet vsetko, daj si do CanvasObject initu hidden=False
        starting_canvas_items = [self.menu_btn,
                                 self.solve_screen_map_bg,
                                 self.solve_screen_keyboard,
                                 self.solve_screen_road_bg, self.road,
                                 self.solve_screen_task_bg, self.task_text_set_choice]
        for item in starting_canvas_items:
            self.show_canvas_item(item)
