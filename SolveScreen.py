from Screen import Screen
from ColorButton import ColorButton
from CanvasObject import CanvasObject
from PIL import Image, ImageTk
from Keyboard import Keyboard
from Road import Road
from ClickableList import ClickableList
from Task import TaskSet
import time
from tkinter import messagebox
import re
import copy
from os import path
import math
from CommonFunctions import playsound


COLLECTION_SOUND = 'sounds/Collection.mp3'
CORRECT_ANS_SOUND = 'sounds/Correct_Answer.mp3'
WRONG_SOUND = "sounds/wrong_sound.mp3"
SPEED = 30


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
        self.actual_regime = None
        self.task_not_draw = True
        self.moving = False
        self.plan_traj = []

    def check_move(self, move, dir, obsta):
        map_name = self.tasks_set.get_actual_task().map.name
        active = self.tasks_set.get_actual_task().road.number_of_active_road_parts
        if self.actual_regime == "priamy" and move == "wrong":
            self.tasks_set.get_actual_task().road.add_move(move, dir)

            if obsta == "x" or obsta == "y" or obsta == "z":
                self.tasks_set.get_actual_task().road.road_parts[active].add_obstacle("mapy/{}/obstacles/{}.png".format(map_name, obsta))
            elif obsta == "guarding":
                self.tasks_set.get_actual_task().road.road_parts[active].add_obstacle("obrazky/guarding.png")
            else:
                self.tasks_set.get_actual_task().road.road_parts[active].add_obstacle("obrazky/guarding.png")

            self.tasks_set.get_actual_task().road.number_of_active_road_parts -= 1

        elif self.actual_regime == "priamy" and move == "ok" and obsta is not None:
            active = self.tasks_set.get_actual_task().road.number_of_active_road_parts
            self.tasks_set.get_actual_task().road.road_parts[active - 1].add_obstacle("mapy/{}/collectibles/{}.png".format(map_name, obsta))

    def check_changed(self, index, removed=False):
        rp = self.tasks_set.get_actual_task().road.road_parts[index]
        active = self.tasks_set.get_actual_task().road.number_of_active_road_parts
        if rp.color == "ok" or rp.color == "wrong":
            for i in range(index, active):
                self.tasks_set.get_actual_task().road.road_parts[i].change_color("basic")
        self.tasks_set.get_actual_task().road.selected_parts = []

    def change_direction(self, direction):
        for part in self.tasks_set.get_actual_task().road.selected_parts:
            rp = self.tasks_set.get_actual_task().road.road_parts[part]
            rp.change_direction(direction)
            self.check_changed(part)

    def move_down(self, _):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return
        if len(self.tasks_set.get_actual_task().road.selected_parts) == 1 and self.actual_regime == "planovaci":
            self.change_direction("down")
            return
        active_parts = self.tasks_set.get_actual_task().road.number_of_active_road_parts
        actual = self.tasks_set.get_actual_task()
        if active_parts >= 16 or active_parts >= actual.steps_count:
            playsound(WRONG_SOUND, 3)
            return
        move, obsta = player.move_down()
        self.check_move(move, "down", obsta)

    def move_up(self, _):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return
        if len(self.tasks_set.get_actual_task().road.selected_parts) == 1 and self.actual_regime == "planovaci":
            self.change_direction("up")
            return
        active_parts = self.tasks_set.get_actual_task().road.number_of_active_road_parts
        actual = self.tasks_set.get_actual_task()
        if active_parts >= 16 or active_parts >= actual.steps_count:
            playsound(WRONG_SOUND, 3)
            return
        move, obsta = player.move_up()
        self.check_move(move, "up", obsta)

    def move_right(self, _):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return
        if len(self.tasks_set.get_actual_task().road.selected_parts) == 1 and self.actual_regime == "planovaci":
            self.change_direction("right")
            return
        active_parts = self.tasks_set.get_actual_task().road.number_of_active_road_parts
        actual = self.tasks_set.get_actual_task()
        if active_parts >= 16 or active_parts >= actual.steps_count:
            playsound(WRONG_SOUND, 3)
            return
        move, obsta = player.move_right()
        self.check_move(move, "right", obsta)

    def move_left(self, _):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return
        if len(self.tasks_set.get_actual_task().road.selected_parts) == 1 and self.actual_regime == "planovaci":
            self.change_direction("left")
            return
        active_parts = self.tasks_set.get_actual_task().road.number_of_active_road_parts
        actual = self.tasks_set.get_actual_task()
        if active_parts >= 16 or active_parts >= actual.steps_count:
            playsound(WRONG_SOUND, 3)
            return
        move, obsta = player.move_left()
        self.check_move(move, "left", obsta)

    def step_back(self, _):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return
        if self.actual_regime == "planovaci":
            self.tasks_set.get_actual_task().road.remove_last_part()
            return
        self.tasks_set.step_back()

    def go_to_menu(self):
        # print("Prechod do menu")
        if self.task_not_draw:
            self.unbind_all()
            return
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return
        self.unbind_all()

    def remove_lines(self, arr, num):
        for i in range(num):
            arr.pop(0)
        return arr

    def read_task(self, lines, map_name):
        self.task_not_draw = False
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

        lines = self.remove_lines(lines, 1)
        self.tasks_set.add_task(name, typ, regime, row, col, steps, assign, map_string, map_name.replace(" ", "_"), "", solvable)
        return lines

    def check_task_file(self, lines, filename):

        lines2 = copy.copy(lines)
        for i in range(len(lines2)):
            if lines2[i] == "":
                lines2[i] = "**BLANK_LINE**"
            lines2[i] += "\n"

        if len(lines2) > 0 and lines2[0] == "":
            return "Chyba súboru {}.".format(filename) + " Chyba: " + repr("")
        text = "".join(lines2)
        lines2 = text.split("**BLANK_LINE**\n")

        message = "Chyba súboru {}.".format(filename)
        nums = []

        sett = lines2[0].split("\n")
        obs = lines2[1].split("\n")
        tasks_sett = lines2[2].split("\n")
        tasks = []

        for i in range(3, len(lines2)):
            tasks.append(lines2[i].split("\n"))

        if len(sett) != 3:
            return message

        if len(sett) < 2 and len(sett) > 5:
            return message

        if len(tasks_sett) != 3:
            return message

        if not (sett[0].startswith("Nazov: ") and sett[0].split(": ")[1].replace("_", "").replace(" ", "").isalnum()):
            nums.append(sett[0])

        elif re.fullmatch("Mapa: [a-zA-Z0-9_]{1,15}", sett[1]) is None:
            nums.append(sett[1])
        elif re.fullmatch("", sett[2]) is None:
            nums.append(sett[2])
        elif obs[0] != "# Nastavenie prekazok #":
            nums.append(obs[0])

        map_name = sett[1].split(": ")[1]

        if not path.exists("mapy/{}".format(map_name)):
            nums.append("Neexistujúca mapa")

        for i in range(1, len(obs) - 1):
            if re.fullmatch("([xyz]): (stvorec|kriz|bod)", obs[i]) is None:
                nums.append(obs[i])

        if re.fullmatch("", obs[-1]) is None:
            nums.append(obs[-1])

        if tasks_sett[0] != "# Ulohy #":
            nums.append(tasks_sett[0])

        if re.fullmatch("Volny prechod: (nie|ano)", tasks_sett[1]) is None:
            nums.append(tasks_sett[1])

        if tasks_sett[2] != "":
            nums.append(tasks_sett[2])


        for i in range(len(tasks)):
            check, line = self.check_task_full_assignment(tasks[i], map_name)
            if check == False:
                nums.append(line)

        if len(nums) == 0:
            return ""
        else:
            return nums[0]

    def check_task_full_assignment(self, lines, map_name):
        if len(lines) > 0 and len(lines) == lines.count(""):
            return True, ""

        if len(lines) < 10:
            return False, "Chyba v počte riadkov"

        if lines[0] == "":
            return False, "Nový riadok navyše."

        if re.fullmatch("[0-9]{1,2}\.", lines[0]) is None:
            return False, lines[0]
        if not (lines[1].startswith("Nazov: ") and lines[1].split(": ")[1].replace("_","").replace(" ", "").isalnum()):
            return False, lines[1]
        if re.fullmatch("Typ: (pocty|volna|cesta)", lines[2]) is None:
            return False, lines[2]
        if re.fullmatch("Rezim: (planovaci|priamy|oba)", lines[3]) is None:
            return False, lines[3]
        if re.fullmatch("Riadkov: [0-9]{1,2}", lines[4]) is None:
            return False, lines[4]
        if re.fullmatch("Stlpcov: [0-9]{1,2}", lines[5]) is None:
            return False, lines[5]
        if re.fullmatch("Krokov: {0,1}[0-9]{0,2}", lines[6]) is None:
            return False, lines[6]
        if lines[7].startswith("Zadanie: "):  #(a|b|c|d)(|>|<|=|<=|>=)[0-9]{1,2}
            if "pocty" in lines[2]:
                assign = lines[7].split(": ")[1]
                ass = assign.split(",")

                for i in range(len(ass)):
                    if re.fullmatch("((a|b|c|d)=\?)|((a|b|c|d)(>|<|=|<=|>=)[0-9]{1,2})", ass[i]) is None:
                        return False, lines[7]

                assign = lines[7].split(": ")[1]
                for char in "abcd":
                    if char in assign and not path.exists("mapy/{}/collectibles/{}.png".format(map_name, char)):
                        return False, lines[7] + " Neexistujúci predmet."

            elif "cesta" in lines[2]:
                assign = lines[7].split(": ")[1]
                if re.fullmatch("([abcd]){1,16}", assign) is None:
                    return False, lines[7]

                for char in assign:
                    if not path.exists("mapy/{}/collectibles/{}.png".format(map_name, char)):
                        return False, lines[7]

            if "volna" in lines[2] and re.fullmatch("Zadanie: ", lines[7]) is None:
                return False, lines[7]

        if not lines[7].startswith("Zadanie: "):
            return False, lines[7]
        if re.fullmatch("Riesitelna: (ano|nie)", lines[8]) is None:
            return False, lines[8]

        for i in range(9, len(lines) - 1):
            if re.fullmatch("([\.pabcdxyz])+", lines[i]) is None:
                return False, lines[i]

        if re.fullmatch("", lines[-1]) is None:
            return False, lines[-1]

        player_count = 0
        for i in range(9, len(lines)):
            for char in lines[i]:
                if char == 'p':
                    player_count += 1
                if char != "." and char.isalnum():

                    if char != 'p' and not (path.exists("mapy/{}/collectibles/{}.png".format(map_name, char)) or
                         path.exists("mapy/{}/obstacles/{}.png".format(map_name, char))):
                        return False, lines[i]
                    elif char == 'p' and not path.exists("mapy/{}/character.png".format(map_name)):
                        return False, lines[i]
                if player_count > 1:
                    return False, lines[i] + "- Viac hráčov v hracom poli"

        return True, None

    def draw_task_assignment(self, name):
        self.canvas.itemconfig(self.task_text_set_choice, state="hidden")

        with open("sady_uloh/" + name + ".txt", "r", encoding="utf-8") as file:
            full = file.read()

        lines = full.split("\n")
        if lines[-1] == "":
            lines.pop(-1)

        answer = self.check_task_file(lines, "sady_uloh/" + name + ".txt")

        if answer != "":
            self.choose_taskset_menu()
            messagebox.showerror(title="Chyba", message="Chyba v súbore sady_uloh/" + name + ".txt\nChyba: " + str(answer))
            return

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

        self.tasks_set = TaskSet(tasks_set_name, self.canvas, next_without_solve, obstacles, self)

        # self.choose_taskset_btn.show()

        while len(lines) > 0 and lines[0] != "##!EOF##":
             lines = self.read_task(lines, map_name)

        if len(self.tasks_set.tasks) > 0 and self.tasks_set.tasks[0].map_error_message != "":
            self.choose_taskset_menu()
            error_message = "Chyba súboru mapy/{}/map_settings.txt\n".format(self.tasks_set.get_actual_task().map.name) + self.tasks_set.tasks[0].map_error_message
            messagebox.showerror(title="Chyba", message=error_message)
            return

        if (next_without_solve == "ano" and len(self.tasks_set.tasks) > 1) or self.tasks_set.get_actual_task().solvable == False:
            self.next_task_btn.show()

        if len(self.tasks_set.tasks) == 1:
            self.next_task_btn.hide()

        self.canvas.itemconfig(self.task_text_mode, state="normal")
        self.draw_task_and_map()

    def draw_task_and_map(self):
        self.tasks_set.draw_task_and_map()
        self.parent.root.bind('<Up>', self.move_up)
        self.parent.root.bind('<Down>', self.move_down)
        self.parent.root.bind('<Left>', self.move_left)
        self.parent.root.bind('<Right>', self.move_right)
        self.canvas.tag_bind(self.keyboard[0], '<ButtonPress-1>', self.move_down)
        self.canvas.tag_bind(self.keyboard[1], '<ButtonPress-1>', self.move_right)
        self.canvas.tag_bind(self.keyboard[2], '<ButtonPress-1>', self.move_up)
        self.canvas.tag_bind(self.keyboard[3], '<ButtonPress-1>', self.move_left)
        self.tasks_set.get_actual_task().map.draw_guards()

    def unbind_all(self):
        self.parent.root.unbind('<Up>')
        self.parent.root.unbind('<Down>')
        self.parent.root.unbind('<Left>')
        self.parent.root.unbind('<Right>')
        self.canvas.tag_unbind(self.keyboard[0], '<ButtonPress-1>')
        self.canvas.tag_unbind(self.keyboard[1], '<ButtonPress-1>')
        self.canvas.tag_unbind(self.keyboard[2], '<ButtonPress-1>')
        self.canvas.tag_unbind(self.keyboard[3], '<ButtonPress-1>')
        self.destroy_screen()
        self.parent.main_menu_screen_init()

    def destroy_screen(self):
        self.canvas.delete("all")
        self.parent.background_set()

    def panel_init(self):
        self.task_name_text = self.canvas.create_text(530, 25, fill="#0a333f",
                                                      font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                      width=330, text='Uloha1')

        self.next_task_btn = ColorButton(self, 1180, 25, 150, 36, 'violet', 'Ďalšia úloha')

        self.prev_task_btn = ColorButton(self, 1015, 25, 160, 36, 'orange', 'Predošlá úloha')
        self.menu_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Menu')
        # self.choose_taskset_btn = ColorButton(self, 225, 25, 180, 36, 'green3', 'Výber sady úloh')
        # self.choose_taskset_btn.hide()
        # self.choose_taskset_btn.bind(self.choose_taskset_menu)
        self.menu_btn.bind(self.go_to_menu)


        self.screen_panel = CanvasObject(self, [self.task_name_text, self.menu_btn])

        self.prev_task_btn.hide()
        self.next_task_btn.hide()
        self.next_task_btn.bind(self.next_task)
        self.prev_task_btn.bind(self.prev_task)

    def choose_taskset_menu(self):
        self.canvas.delete("all")
        self.parent.background_set()
        self.parent.solve_screen_init()

    def remove_task(self):
        self.tasks_set.remove_task_and_map()

    def next_task(self):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return

        if self.tasks_set.actual < len(self.tasks_set.tasks) - 1:
            self.prev_task_btn.show()
            player.remove_trajectory()
            self.remove_task()
            # self.tasks_set.get_actual_task().road.clear_road()
            self.tasks_set.get_actual_task().road.unshow()
            self.tasks_set.get_actual_task().actual_regime = self.actual_regime
            self.tasks_set.next_task()
            self.draw_task_and_map()
            actual = self.tasks_set.get_actual_task()
            actual.road.show()
            self.set_actual_mode()
            # print(actual.name, actual.road.number_of_active_road_parts)
            if actual.actual_regime == "planovaci":
                actual.road.change_color("basic")
            #     print("Trajektoria v next:", player.trajectory)
            #     self.recostruct_road(actual, actual.road)

            if self.tasks_set.actual == len(self.tasks_set.tasks) - 1 or (self.tasks_set.next == "nie" and actual.solvable):
                self.next_task_btn.hide()

    def prev_task(self):
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            return

        if self.tasks_set.actual > 0:
            self.next_task_btn.show()
            self.remove_task()
            player.remove_trajectory()
            self.tasks_set.get_actual_task().road.unshow()
            # self.tasks_set.get_actual_task().road.clear_road()
            # self.remove_plan_traj()
            self.tasks_set.prev_task()
            self.draw_task_and_map()
            self.tasks_set.get_actual_task().map.draw_guards()
            act = self.tasks_set.get_actual_task()
            # print(act.name, act.road.number_of_active_road_parts)
            self.actual_regime = act.actual_regime
            self.set_actual_mode()
            act.road.show()
            if act.actual_regime == "planovaci":
                act.road.change_color("basic")
            #     self.recostruct_road(act, act.road)
            #     print("Trajectoria v prev: ",player.trajectory)
            if self.tasks_set.actual == 0:
                self.prev_task_btn.hide()

    def show_next_task_button(self):
        if self.tasks_set.actual < len(self.tasks_set.tasks) - 1:
            self.next_task_btn.show()

    def map_window_init(self):
        image = Image.new('RGBA', (900, 480), (141, 202, 73, 100))
        self.screen_map_bg_img = ImageTk.PhotoImage(image)
        screen_map_bg = self.canvas.create_image(10, 60, image=self.screen_map_bg_img, anchor='nw')
        screen_map_bg_border = self.canvas.create_rectangle(10, 60, 910, 540, outline='#b6e5da', width=2)

        self.solve_screen_map_bg = CanvasObject(self, [screen_map_bg, screen_map_bg_border])

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
        self.keyboard = keyboard

        image = Image.open("obrazky/controls/back.png")
        image = image.resize((75, 75), Image.ANTIALIAS)
        self.backspace_img = ImageTk.PhotoImage(image)
        self.back = self.canvas.create_image(1080, 558, image=self.backspace_img, anchor='nw')
        self.canvas.tag_bind(self.back, '<ButtonPress-1>', self.step_back)

        image = Image.open("obrazky/controls/clear.png")
        image = image.resize((75, 75), Image.ANTIALIAS)
        self.clear_image = ImageTk.PhotoImage(image)
        self.clear = self.canvas.create_image(1185, 558, image=self.clear_image, anchor='nw')

        self.canvas.tag_bind(self.clear, '<ButtonPress-1>', self.clear_road)

        self.solve_screen_keyboard = CanvasObject(self,
                                                  [screen_keys_bg_border, Keyboard(self, keyboard),
                                                   self.back, self.clear])

    def clear_road(self, _):
        # print("stlacena metlicka")
        # print("Aktualny rezim", self.tasks_set.get_actual_task().actual_regime)
        player = self.tasks_set.get_player()
        if player.planned_move == True or self.moving:
            # print("prva vetva")
            return

        if self.tasks_set.get_actual_task().actual_regime == "priamy":
            # print("druha vetva")
            player = self.tasks_set.get_player()
            player.reset_game()
        else:
            # print("else vetva")
            if len(self.tasks_set.get_actual_task().road.selected_parts) == 1:
                # print("sem")
                part_index = self.tasks_set.get_actual_task().road.selected_parts[0]
                part_color = self.tasks_set.get_actual_task().road.road_parts[part_index].color
                self.tasks_set.get_actual_task().road.remove_all_selected()
                active = self.tasks_set.get_actual_task().road.number_of_active_road_parts
                if part_color == "ok" or part_color == "wrong":
                    # print("sem2")
                    for i in range(part_index, active):
                        self.tasks_set.get_actual_task().road.road_parts[i].change_color("basic")
                return

            if self.tasks_set.get_actual_task().road.wrong_ignored_in_road() == True:
                # print("sem3")
                self.tasks_set.get_actual_task().road.clear_wrong_ingnored()
            else:
                # print("uplny else")
                self.tasks_set.get_actual_task().road.clear_road()

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

        self.canvas.tag_bind(self.play, '<ButtonPress-1>', self.play_moves)

        self.move_imgs = {'basic': [], 'ok': [], 'wrong': [], 'ignored': []}
        for move_type in self.move_imgs:
            image = Image.open("obrazky/moves/" + move_type + ".png")
            image = image.resize((32, 32), Image.ANTIALIAS)
            for i in range(4):
                self.move_imgs[move_type].append(
                    ImageTk.PhotoImage(image))  # obrazky v poli v poradi: right, up, left, down
                image = image.rotate(90)

        # print(self.move_imgs)
        self.road = Road(self.move_imgs, self)

        self.solve_screen_road = CanvasObject(self, [self.solve_screen_road_bg, self.play])
        self.solve_screen_road.show()
        self.canvas.itemconfig(self.play, state="hidden")

    def play_moves(self, _):
        player = self.tasks_set.get_player()
        if player.planned_move == True:
            return
        player.planned_move = True
        player.remove_trajectory()
        for i in range(self.tasks_set.get_actual_task().road.number_of_active_road_parts):
            self.tasks_set.get_actual_task().road.road_parts[i].change_color("basic")

        self.canvas.update()
        time.sleep(0.01)
        ignored = False
        for i in range(self.tasks_set.get_actual_task().road.number_of_active_road_parts):
            if ignored == True:
                self.tasks_set.get_actual_task().road.road_parts[i].change_color("ignored")
                continue

            move = None
            obsta = None
            if self.tasks_set.get_actual_task().road.road_parts[i].direction == "down":
                move, obsta = player.move_down()
            if self.tasks_set.get_actual_task().road.road_parts[i].direction == "up":
                move, obsta = player.move_up()
            if self.tasks_set.get_actual_task().road.road_parts[i].direction == "right":
                move, obsta = player.move_right()
            if self.tasks_set.get_actual_task().road.road_parts[i].direction == "left":
                move, obsta = player.move_left()
            if move is not None:
                self.tasks_set.get_actual_task().road.road_parts[i].change_color(move)
                map_name = self.tasks_set.get_actual_task().map.name
                if move == "wrong":
                    self.tasks_set.get_actual_task().road.road_parts[i].change_color("wrong")
                    if obsta == "x" or obsta == "y" or obsta == "z":
                        self.tasks_set.get_actual_task().road.road_parts[i].add_obstacle("mapy/{}/obstacles/{}.png".format(map_name, obsta))
                    elif obsta == "guarding":
                        self.tasks_set.get_actual_task().road.road_parts[i].add_obstacle("obrazky/guarding.png")
                    else:
                        self.tasks_set.get_actual_task().road.road_parts[i].add_obstacle("obrazky/guarding.png")
                    ignored = True

                elif move == "ok" and obsta is not None:
                    if self.tasks_set.get_actual_task().type == "cesta":
                        act_task = self.tasks_set.get_actual_task()
                        len_col = len(act_task.map.player.coll_path)
                        if act_task.assign[:len_col] == "".join(act_task.map.player.coll_path):
                            playsound(COLLECTION_SOUND, 1)
                        else:
                            playsound(WRONG_SOUND, 3)
                        # print(act_task.assign, act_task.map.player.coll_path, act_task.assign[:len_col])
                    if self.tasks_set.get_actual_task().type == "pocty":
                        act_task = self.tasks_set.get_actual_task()
                        colle = player.coll_collected
                        was = False
                        for count in act_task.col_counts:
                            col = count[0]
                            sign = count[1]
                            num = count[2]
                            if sign == "=" and col in colle and colle[col] > num and col == obsta:
                                was = True
                                break
                            elif sign == "<=" and col in colle and colle[col] > num and col == obsta:
                                was = True
                                break
                        if was == False:
                            playsound(COLLECTION_SOUND, 1)
                        else:
                            playsound(WRONG_SOUND, 3)


                    self.tasks_set.get_actual_task().road.road_parts[i].add_obstacle("mapy/{}/collectibles/{}.png".format(map_name, obsta))
            else:
                self.tasks_set.get_actual_task().road.road_parts[i].change_color("ok")

            self.canvas.update()
            time.sleep(0.6)

        answer = self.tasks_set.get_actual_task().check_answer(play=False)
        # print("Odpoved je:", answer)
        if answer:
            playsound(CORRECT_ANS_SOUND, 2)

        # player.draw_full_trajectory()
        player.reset_game(plan=True)

        player.planned_move = False

    def move_img_smoothly(self, img, x1, y1, x2, y2):
        player = self.tasks_set.get_player()
        edge_len = math.hypot(x1 - x2,y1 - y2)
        start_x = x1
        start_y = y1
        end_x = x2
        end_y = y2
        id = self.canvas.create_image(x1, y1, image=img, anchor='c')
        self.moving = True

        def step(pos, id):
            player.hide()
            pos += SPEED / edge_len
            x = start_x * (1 - pos) + end_x * pos
            y = start_y * (1 - pos) + end_y * pos
            self.canvas.delete(id)
            id = self.canvas.create_image(x, y, image=img, anchor='c')

            if pos < 1:
                time.sleep(0.1)
                self.canvas.update()
                step(pos, id)
            else:
                self.canvas.delete(id)

        step(0, id)
        self.moving = False

        player.show()

    def task_window_init(self):
        image = Image.new('RGBA', (350, 480), (255, 170, 79, 100))
        self.screen_task_bg_img = ImageTk.PhotoImage(image)
        screen_task_bg = self.canvas.create_image(920, 60, image=self.screen_task_bg_img, anchor='nw')
        screen_task_bg_border = self.canvas.create_rectangle(920, 60, 1270, 540, outline='#b6e5da', width=2)

        self.solve_screen_task_bg = CanvasObject(self, [screen_task_bg, screen_task_bg_border])

        self.task_text_collect = self.canvas.create_text(930, 70, fill="#0a333f",
                                                         font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
                                                         width=330, text='{} chce pozbierat')
        # self.task_text_collectibles = [
        #     self.canvas.create_text(1095, 110, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'), anchor='n',
        #                             width=330, text='práve 5 aaa, najviac 6 ccc'),
        #     self.canvas.create_text(1095, 150, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'), anchor='n',
        #                             width=330, text='najviac 6 bbb a 0 ddd')]

        # self.task_text_steps = self.canvas.create_text(930, 220, fill="#0a333f",
        #                                                font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
        #                                                width=330, text='s použítim najviac {} krokov.')
        # self.task_text_path_info = self.canvas.create_text(930, 185, fill="#0a333f",
        #                                                    font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
        #                                                    width=330, text='(v tomto počte aj poradí)')
        # self.task_text_obstacle = self.canvas.create_text(930, 255, fill="#0a333f",
        #                                                   font=('Comic Sans MS', 17, 'italic bold'), anchor='nw',
        #                                                   width=330, text='Musí sa ale vyhnúť políčkam, ktoré ohrozuje')
        # self.task_text_obstacles = self.canvas.create_text(1095, 330, fill="#0a333f",
        #                                                    font=('Comic Sans MS', 15, 'italic bold'), anchor='n',
        #                                                    width=330, text='Liska alebo Voda')
        #
        self.task_text_mode = self.canvas.create_text(930, 370, fill="#114c32",
                                                      font=('Comic Sans MS', 17, 'italic bold'), anchor='nw', width=330,
                                                      text='{}\n"Pomôžeš mi, prosím, naplánovať cestu?"\n\n\tRežim: priamy')

        self.task_text_set_choice = self.canvas.create_text(1095, 285, fill="#0a333f",
                                                            font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                            width=330, text='Vyber sadu úloh')

        # task_text_collectibles_obj = CanvasObject(self, self.task_text_collectibles)
        self.solve_screen_task_collectibles = CanvasObject(self, [self.task_text_collect])
        # self.solve_screen_task_obstacles = CanvasObject(self, [self.task_text_obstacle, self.task_text_obstacles])

        image = Image.open('obrazky/swap_mode.png')
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.swap_mode_btn_img = ImageTk.PhotoImage(image)
        self.swap_mode_btn = self.canvas.create_image(1230, 500, image=self.swap_mode_btn_img, anchor='nw')
        self.canvas.itemconfig(self.swap_mode_btn, state="hidden")
        self.canvas.tag_bind(self.swap_mode_btn, '<ButtonPress-1>', self.swap_mode)


        self.solve_screen_task_mode = CanvasObject(self, [self.task_text_mode, self.swap_mode_btn])

        # self.solve_screen_task_mode = CanvasObject(self, [self.task_text_mode])

        # self.solve_screen_task_mode.show()

        # self.solve_screen_task_window = CanvasObject(self, [self.solve_screen_task_bg,
        #                                                     self.task_text_steps, self.task_text_path_info,
        #                                                     self.task_text_set_choice,
        #                                                     self.solve_screen_task_obstacles,
        #                                                     self.solve_screen_task_mode])

        self.solve_screen_task_window = CanvasObject(self, [self.solve_screen_task_bg])

    def set_actual_mode(self):
        # print("Aktualny mod:", self.tasks_set.get_actual_task().actual_regime)
        mode = self.tasks_set.get_actual_task().actual_regime
        if mode == 'priamy':
            text = self.canvas.itemcget(self.task_text_mode, 'text')
            text = text.replace("naplánovať", "nájsť")
            text = text.replace("plánovací", "priamy")
            self.canvas.itemconfig(self.task_text_mode, text=text)
        elif mode == "planovaci":
            text = self.canvas.itemcget(self.task_text_mode, 'text')
            text = text.replace("nájsť", "naplánovať")
            text = text.replace("priamy", "plánovací")
            self.canvas.itemconfig(self.task_text_mode, text=text)

    def swap_mode(self, _):
        player = self.tasks_set.get_player()

        if player.planned_move == True or self.moving:
            return
        text = self.canvas.itemcget(self.task_text_mode, 'text')
        if "plánovací" in text:
            text = text.replace("naplánovať", "nájsť")
            text = text.replace("plánovací", "priamy")
            self.canvas.itemconfig(self.task_text_mode, text=text)
            self.canvas.itemconfig(self.play, state="hidden")
            self.actual_regime = "priamy"
            self.tasks_set.get_actual_task().actual_regime = "priamy"
        else:
            text = text.replace("nájsť", "naplánovať")
            text = text.replace("priamy","plánovací")
            self.canvas.itemconfig(self.task_text_mode, text=text)
            self.canvas.itemconfig(self.play, state="normal")
            self.actual_regime = "planovaci"
            self.tasks_set.get_actual_task().actual_regime = "planovaci"

        task = self.tasks_set.get_actual_task()
        task.map.player.reset_game()
        task.map.player.remove_trajectory()
        self.tasks_set.get_actual_task().road.clear_road()

    def show_common(self):

        starting_canvas_items = [self.menu_btn,
                                 self.solve_screen_map_bg,
                                 self.solve_screen_keyboard,
                                 self.solve_screen_road_bg, #self.road,
                                 self.solve_screen_task_bg#, self.task_text_set_choice
                                 ]

        for item in starting_canvas_items:
            self.show_canvas_item(item)
