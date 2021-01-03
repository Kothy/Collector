from Screen import Screen
from PIL import Image, ImageTk
from CanvasObject import CanvasObject
from ColorButton import ColorButton
from AddToMapButtonsSet import AddToMapButtonsSet
from Options import Options
from TaskBar import TaskBar
from Task import Task
from MapCreator import  MapCreator
from CommonFunctions import resize_image
import tkinter as tk
import time

class CreateTaskScreen(Screen):

    SET_NAME_LENGTH = 28

    def __init__(self, parent, folder, task=None):
        self.folder = folder
        self.task = task
        super(CreateTaskScreen, self).__init__(parent)

    def load_screen(self):
        self.panel_init()
        self.backgrounds_init()
        self.error_text_init()
        self.task_name_init()
        self.task_type_init()
        self.task_objects_init()
        self.map_sizes_init()
        self.map_init()
        self.task_bar_init()
        self.check_solution_obj_init()
        self.no_solution_obj_init()
        self.time_out_obj_init()
        self.objects = [self.panel_obj, self.background_obj, self.name_input_obj, self.task_type_obj,
                        self.add_to_map_obj, self.cols_input_obj, self.rows_input_obj, self.map_obj,
                        self.task_bar_obj, self.error_text, self.check_solution_obj, self.no_solution_obj,
                        self.time_out_obj]

    def panel_init(self):
        task_name_text = self.canvas.create_text(650, 25, fill="#0a333f",
                                                 font=('Comic Sans MS', 20, 'italic bold'), anchor='center',
                                                 width=330, text='Vytváranie úlohy')
        save_btn = ColorButton(self, 1205, 25, 100, 36, 'violet', 'Ulož')
        back_btn = ColorButton(self, 75, 25, 100, 36, 'green3', 'Späť')
        save_btn.bind_clicked()
        back_btn.bind_clicked()
        self.panel_obj = CanvasObject(self, [task_name_text, save_btn, back_btn], hidden=False)

    def backgrounds_init(self):
        image = Image.new('RGBA', (670, 480), (255, 170, 79, 100))
        self.left_bg_img = ImageTk.PhotoImage(image)
        left_bg = self.canvas.create_image(45, 60, image=self.left_bg_img, anchor='nw')
        left_bg_border = self.canvas.create_rectangle(45, 60, 715, 540, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (470, 480), (141, 202, 73, 100))
        self.right_bg_img = ImageTk.PhotoImage(image)
        right_bg = self.canvas.create_image(765, 60, image=self.right_bg_img, anchor='nw')
        right_bg_border = self.canvas.create_rectangle(765, 60, 665 + 570, 540, outline='#b6e5da', width=2)

        image = Image.new('RGBA', (665 + 570 - 45, 75), (41, 175, 200, 100))
        self.bottom_bg_img = ImageTk.PhotoImage(image)
        bottom_bg = self.canvas.create_image(45, 560, image=self.bottom_bg_img, anchor='nw')
        bottom_bg_border = self.canvas.create_rectangle(45, 560, 665 + 570, 635, outline='#b6e5da', width=4)

        self.background_obj = CanvasObject(self,
                                           [left_bg, left_bg_border, right_bg, right_bg_border, bottom_bg,
                                            bottom_bg_border],
                                           hidden=False)

    def task_name_init(self):
        task_name_text = self.canvas.create_text(70, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Názov úlohy:')
        self.set_name = tk.StringVar()
        self.set_name_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=38,
                                       justify='center', textvariable=self.set_name)
        name_entry_window = self.canvas.create_window(455, 95, window=self.set_name_entry)

        if self.task is not None:
            self.set_name.set(self.task.name)

        self.set_name.trace("w", self.task_name_text_changed)

        self.name_input_obj = CanvasObject(self, [task_name_text, name_entry_window], hidden=False)

    def task_type_init(self):
        task_mode_text = self.canvas.create_text(790, 80, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Povolený režim:')
        self.task_mode_btn = ColorButton(self, 1025, 95, 110, 30, 'light_blue', 'oba')
        self.task_mode_btn.bind_clicked()

        if self.task is not None:
            self.task_mode_btn.change_text(self.task.mode)

        task_type_text = self.canvas.create_text(790, 120, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Typ úlohy:')
        self.task_type_options = Options(self, 935, 138, ['voľná (bez zadania)',
                                                          'počty predmetov',
                                                          'postupnosť predmetov'],
                                         0 if self.task is None else self.task.type,
                                         True)

        steps_text = self.canvas.create_text(790, 240, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Počet krokov:\n(maximálny)')

        self.set_steps = tk.StringVar()
        self.set_steps_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=2,
                                       justify='center', textvariable=self.set_steps)
        steps_entry_window = self.canvas.create_window(965, 256, window=self.set_steps_entry)

        if self.task is not None:
            self.set_steps.set(self.task.steps_count)

        self.set_steps.trace("w", self.set_steps_text_changed)

        steps_help_text = self.canvas.create_text(990, 245, fill="#114c32", font=('Comic Sans MS', 13, 'italic'),
                                                  anchor='nw', width=330,
                                                  text='<-- ponechaj prázdne\n     pre maximálny možný\n     počet krokov (16)',
                                                  state="normal")

        self.steps_obj = CanvasObject(self, [steps_text, steps_entry_window, steps_help_text])

        self.task_type_obj = CanvasObject(self, [task_mode_text, self.task_mode_btn, task_type_text,
                                                 self.task_type_options, self.steps_obj], False)

    def task_objects_init(self):
        objects_text = self.canvas.create_text(790, 325, fill="#0a333f",
                                                         font=('Comic Sans MS', 17, 'italic bold'),
                                                         anchor='nw', width=530,
                                                         text='Pridaj do mapy:')

        collectibles_text = self.canvas.create_text(930, 365, fill="#0a333f",
                                                      font=('Comic Sans MS', 15, 'italic bold'),
                                                      anchor='ne', width=530,
                                                      text='Predmety:')

        obstacles_text = self.canvas.create_text(930, 410, fill="#0a333f",
                                                      font=('Comic Sans MS', 15, 'italic bold'),
                                                      anchor='ne', width=530,
                                                      text='Prekážky:')

        character_text = self.canvas.create_text(930, 455, fill="#0a333f", font=('Comic Sans MS', 15, 'italic bold'),
                                                 anchor='ne', width=530,
                                                 text='Postavička:')

        self.add_to_map_buttons = AddToMapButtonsSet(self, self.folder, 950, 365)

        img = Image.open('obrazky/mouse.png')
        self.mouse_img = ImageTk.PhotoImage(resize_image(img, 75, 75))
        mouse = self.canvas.create_image(1180, 450, image=self.mouse_img)

        self.add_to_map_obj = CanvasObject(self, [objects_text, collectibles_text, obstacles_text, character_text,
                                                  self.add_to_map_buttons, mouse], False)

    def map_sizes_init(self):
        rows_text = self.canvas.create_text(70, 120, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                                 anchor='nw', width=530,
                                                 text='Počet riadkov:     ≤ 5')
        self.set_rows = tk.StringVar()
        self.set_rows_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=2,
                                       justify='center', textvariable=self.set_rows)
        rows_entry_window = self.canvas.create_window(255, 135, window=self.set_rows_entry)

        if self.task is not None:
            self.set_rows.set(self.task.row)

        self.set_rows.trace("w", self.set_rows_text_changed)

        self.rows_input_obj = CanvasObject(self, [rows_text, rows_entry_window], hidden=False)

        cols_text = self.canvas.create_text(420, 120, fill="#0a333f", font=('Comic Sans MS', 17, 'italic bold'),
                                            anchor='nw', width=530,
                                            text='Počet stĺpcov:     ≤ 10')
        self.set_cols = tk.StringVar()
        self.set_cols_entry = tk.Entry(self.parent.root, font=('Comic Sans MS', 15, 'italic bold'), width=2,
                                       justify='center', textvariable=self.set_cols)
        cols_entry_window = self.canvas.create_window(600, 135, window=self.set_cols_entry)

        if self.task is not None:
            self.set_cols.set(self.task.col)

        self.set_cols.trace("w", self.set_cols_text_changed)

        self.cols_input_obj = CanvasObject(self, [cols_text, cols_entry_window], hidden=False)

    def map_init(self):
        self.map = MapCreator(self, self.folder)

        if self.task is not None:
            self.map.redraw(int(self.task.row), int(self.task.col))
            self.map.load_field(self.task.map_str)

        self.map_obj = CanvasObject(self, [self.map], False)

    def task_bar_init(self):
        task_bar_text = self.canvas.create_text(70, 580, fill="#0a333f", font=('Comic Sans MS', 20, 'italic bold'),
                                                anchor='nw', width=530,
                                                text='Zadanie:')
        assignment_line = self.canvas.create_line(205, 560, 205, 635, fill='#b6e5da', width=4)
        self.task_bar = TaskBar(self, self.folder)

        if self.task is not None:
            self.options_changed(self.task.type)
            self.task_bar.fill(self.task.assign, self.task.type)

        self.task_bar_obj = CanvasObject(self, [task_bar_text, assignment_line, self.task_bar], False)

    def check_solution_obj_init(self):
        image = Image.new('RGBA', (1300, 700), (152, 214, 214, 120))
        self.check_bg_img = ImageTk.PhotoImage(image)
        background = self.canvas.create_image(0, 0, image=self.check_bg_img, anchor='nw')

        image = Image.open('obrazky/bg.jpg')
        image = image.resize((600, 300), Image.ANTIALIAS)
        self.check_bg2_img = ImageTk.PhotoImage(image)
        background2 = self.canvas.create_image(650, 325, image=self.check_bg2_img, anchor='c')
        bg2_border = self.canvas.create_rectangle(350, 175, 950, 475, outline='#b6e5da', width=4)

        text = self.canvas.create_text(650, 320, fill="#0a333f",
                                                 font=('Comic Sans MS', 30, 'italic bold'), anchor='center',
                                                 width=330, text='Kontrolujem riešiteľnosť...')

        self.check_solution_obj = CanvasObject(self, [background, background2, bg2_border, text])

    def no_solution_obj_init(self):
        background = self.canvas.create_image(0, 0, image=self.check_bg_img, anchor='nw')
        background2 = self.canvas.create_image(650, 325, image=self.check_bg2_img, anchor='c')
        bg2_border = self.canvas.create_rectangle(350, 175, 950, 475, outline='#b6e5da', width=4)

        no_solution = self.canvas.create_text(650, 275, fill="darkred",
                                              font=('Comic Sans MS', 30, 'italic bold'), anchor='center',
                                              width=630, text='Úloha nemá riešenie.\nNapriek tomu uložiť?')

        yes_button = ColorButton(self, 550, 400, 100, 50, 'green', 'Áno', 20)
        no_button = ColorButton(self, 750, 400, 100, 50, 'red', 'Nie', 20)

        yes_button.bind_clicked()
        no_button.bind_clicked()

        self.no_solution_obj = CanvasObject(self, [background, background2, bg2_border, no_solution, yes_button, no_button])

    def time_out_obj_init(self):
        background = self.canvas.create_image(0, 0, image=self.check_bg_img, anchor='nw')
        background2 = self.canvas.create_image(650, 325, image=self.check_bg2_img, anchor='c')
        bg2_border = self.canvas.create_rectangle(350, 175, 950, 475, outline='#b6e5da', width=4)

        no_solution = self.canvas.create_text(650, 255, fill="darkred",
                                              font=('Comic Sans MS', 23, 'italic bold'), anchor='center',
                                              width=630, text='Kontrola trvá príliš dlho.\nProsím, uveď, či je úloha riešiteľná:')

        yes_button = ColorButton(self, 530, 350, 180, 50, 'green', 'Riešiteľná', 20)
        no_button = ColorButton(self, 770, 350, 180, 50, 'red', 'Neriešiteľná', 20)
        check_button = ColorButton(self, 650, 420, 300, 50, 'light_blue', 'Neviem, pozriem sa', 20)

        yes_button.bind_clicked()
        no_button.bind_clicked()
        check_button.bind_clicked()

        self.time_out_obj = CanvasObject(self, [background, background2, bg2_border, no_solution,
                                                yes_button, no_button, check_button])


    def error_text_init(self):
        self.error_text = self.canvas.create_text(780, 505, fill="darkred",
                                                  font=('Comic Sans MS', 15, 'italic bold'),
                                                  anchor='nw', width=530,
                                                  text='',
                                                  state="normal")

    def task_bar_changed(self):
        self.set_error_text('')

    def task_name_text_changed(self, *args):
        if len(self.set_name.get()) > self.SET_NAME_LENGTH:
            self.set_name.set(self.set_name.get()[:-1])
        if len(self.set_name.get()) > 0:
            self.set_error_text('')

    def set_rows_text_changed(self, *args):
        count = self.set_rows.get()
        if len(count) > 1 or (len(count) == 1 and count[0] not in '12345'):
            self.set_rows.set(count[:-1])
        else:
            self.map.redraw(rows=0 if count == '' else int(count))
        if len(count) > 0:
            self.set_error_text('')

    def set_cols_text_changed(self, *args):
        count = self.set_cols.get()
        if (len(count) > 2 or
                (len(count) == 1 and count[-1] not in '123456789') or
                (len(count) == 2 and (count[0] != '1' or count[1] != '0'))):
            self.set_cols.set(count[:-1])
        else:
            self.map.redraw(cols=0 if count=='' else int(count))
        if len(count) > 0:
            self.set_error_text('')

    def set_steps_text_changed(self, *args):
        count = self.set_steps.get()
        if (len(count) > 2 or (len(count) == 1 and count[0] not in '123456789') or
                (len(count) == 2 and (count[0] != '1' or count[1] not in '0123456'))):
            self.set_steps.set(count[:-1])

    def clicked_btn(self, text):
        if text == 'Späť':
            self.parent.delete_task_screen()
        elif text == 'Ulož':
            self.create_task()
        elif text == 'oba':
            self.task_mode_btn.change_text('priamy')
        elif text == 'priamy':
            self.task_mode_btn.change_text('plánovací')
        elif text == 'plánovací':
            self.task_mode_btn.change_text('oba')
        elif text == 'Áno' or text == 'Neriešiteľná':
            self.parent.close_task_screen(self.task_to_save)
        elif text == 'Nie' or text == 'Neviem, pozriem sa':
            self.no_solution_obj.hide()
            self.time_out_obj.hide()
        elif text == 'Riešiteľná':
            self.task_to_save.solvable = True
            self.parent.close_task_screen(self.task_to_save)


    def create_task(self):
        name = self.set_name.get()
        if name == '':
            self.set_error_text('Chyba: Zadaj názov úlohy')
            return
        rows, cols = self.set_rows.get(), self.set_cols.get()
        if rows == '':
            self.set_error_text('Chyba: Mapa musí mať aspoň 1 riadok')
            return
        if cols == '':
            self.set_error_text('Chyba: Mapa musí mať aspoň 1 stĺpec')
            return
        if int(rows)*int(cols) < 2:
            self.set_error_text('Chyba: Mapa musí mať aspoň 2 políčka')
            return
        if 'p' not in self.map.get_map_repr():
            self.set_error_text('Chyba: Mapa musí obsahovať postavičku')
            return
        task_type = self.task_type_options.checked_index
        if task_type == 0:
            assignment = ''
        elif task_type == 1:
            assignment = self.task_bar.get_counts()
            if '<,' in assignment or '>,' in assignment or '=,' in assignment:
                self.set_error_text('Chyba: V zadaní chýba niektorá z hodnôť')
                return
            if not self.task_bar.assignment_is_valid():
                self.set_error_text('Chyba: Urči aspoň 1 predmet na zozbieranie')
                return
        else:
            assignment = self.task_bar.path.get_path()
            if assignment == '':
                self.set_error_text('Chyba: Pridaj do zadania aspoň 1 predmet')
                return
        solvable = 'ano'
        if task_type != 0:
            self.check_solution_obj.to_the_front()
            self.check_solution_obj.show()
            self.canvas.update()
            self.time = time.time()
            solution_found = self.is_solvable(task_type, assignment)
            if not solution_found:
                self.check_solution_obj.hide()
                self.no_solution_obj.to_the_front()
                self.no_solution_obj.parts[-1].to_the_front()
                self.no_solution_obj.parts[-2].to_the_front()
                self.no_solution_obj.show()
                solvable = 'nie'
            elif solution_found == 'timed-out':
                self.check_solution_obj.hide()
                self.time_out_obj.to_the_front()
                self.time_out_obj.parts[-1].to_the_front()
                self.time_out_obj.parts[-2].to_the_front()
                self.time_out_obj.parts[-3].to_the_front()
                self.time_out_obj.show()
                solvable = 'nie'
        task = Task(self.parent, None if self.task is None else self.task.index, name, task_type,
                    self.task_mode_btn.text, rows, cols,
                    self.set_steps.get(), assignment, self.map.get_map_repr(), None, None, solvable, False)
        if solvable == 'ano':
            self.parent.close_task_screen(task)
        else:
            self.task_to_save = task

    def options_changed(self, index):
        self.task_bar.set_bar(index)
        if index == 0:
            self.steps_obj.hide()
        else:
            self.steps_obj.show()

    def is_solvable(self, task_type, assignment):
        map_counts = [self.map.get_map_repr().count(char) for char in 'abcd']
        parsed_assignment = assignment
        if task_type == 1:
            parsed_assignment = [[collectible[1], collectible[2]] for collectible in assignment.split(',')]
        else:
            counts = [assignment.count(char) for char in 'abcd']
            for i in range(4):
                if counts[i] > map_counts[i]:
                    return False
        char_pos = self.map.get_char_position()
        self.solution = []
        self.map_field_copy = [self.map.field[i].copy() for i in range(len(self.map.field))]
        steps = int(self.set_steps.get()) if self.set_steps.get() != '' else 16
        return self.find_solution(char_pos[0], char_pos[1], steps, task_type, parsed_assignment)

    def find_solution(self, i0, j0, steps, task_type, assignment):
        if steps == 0:
            return self.check_solution(task_type, assignment)
        if time.time() - self.time > 4:
            return 'timed-out'
        if not self.check_partial_solution(task_type, assignment):
            return False
        for i, j in ((i0-1, j0), (i0, j0+1), (i0+1, j0), (i0, j0-1)):
            if i < 0 or i >= self.map.rows or j < 0 or j >= self.map.cols:
                continue
            item = self.map_field_copy[i][j]
            if self.map.grid_parts[i][j].is_guarded() or (item is not None and item in 'xyz'):
                continue
            added = False
            if item is not None and item in 'abcd':
                added = True
                self.map_field_copy[i][j] = '.'
                self.solution.append(item)
            solution = self.find_solution(i, j, steps-1, task_type, assignment)
            if solution:
                return solution
            if added:
                self.solution = self.solution[:-1]
                self.map_field_copy[i][j] = item
        return False

    def check_solution(self, task_type, assignment):
        if task_type == 1:
            counts = [self.solution.count(char) for char in 'abcd']
            for i in range(len(counts)):
                if assignment[i][1] == '?':
                    continue
                count = int(assignment[i][1])
                if assignment[i][0] == '=' and counts[i] != count:
                    return False
                if assignment[i][0] == '<' and counts[i] >= count:
                    return False
                if assignment[i][0] == '>' and counts[i] <= count:
                    return False
            return True
        else:
            if ''.join(self.solution).startswith(assignment):
                return True
        return False

    def check_partial_solution(self, task_type, assignment):
        if task_type == 1:
            counts = [self.solution.count(char) for char in 'abcd']
            for i in range(len(counts)):
                if assignment[i][1] == '?':
                    continue
                count = int(assignment[i][1])
                if assignment[i][0] == '=' and counts[i] > count:
                    return False
                if assignment[i][0] == '<' and counts[i] >= count:
                    return False
            return True
        else:
            if assignment.startswith(''.join(self.solution)):
                return True
        return False

    def set_error_text(self, text):
        self.canvas.itemconfig(self.error_text, text=text)