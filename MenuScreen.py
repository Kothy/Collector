from Screen import Screen
from ColorButton import ColorButton
from PIL import Image, ImageTk
from CommonFunctions import resize_image
from CanvasObject import  CanvasObject


class MenuScreen(Screen):
    def __init__(self, parent):
        super(MenuScreen, self).__init__(parent)

    def load_screen(self):
        solve_button = ColorButton(self, 650, 200, 500, 100, 'violet', 'Rieš sadu úloh', 30)
        map_button = ColorButton(self, 650, 350, 400, 70, 'orange', 'Vytvor mapu', 20)
        set_button = ColorButton(self, 650, 480, 400, 70, 'blue', 'Vytvor sadu úloh', 20)

        for btn in [solve_button, map_button, set_button]:
            btn.bind_clicked()

        image = Image.open('mapy/Mapa_Zberatela/character.png')
        self.bee_image = ImageTk.PhotoImage(resize_image(image, 250, 250).transpose(Image.FLIP_LEFT_RIGHT))
        bee_img = self.canvas.create_image(250, 480, image=self.bee_image, anchor='c')

        self.flower_imgs = []
        for color in 'abcd':
            image = Image.open('mapy/Mapa_Zberatela/collectibles/' + color + '.png')
            self.flower_imgs.append(ImageTk.PhotoImage(resize_image(image, 180, 180)))

        flowers = []
        flowers.append(self.canvas.create_image(150, 200, image=self.flower_imgs[0]))
        flowers.append(self.canvas.create_image(880, 550, image=self.flower_imgs[1]))
        flowers.append(self.canvas.create_image(1150, 100, image=self.flower_imgs[3]))

        self.objects = [solve_button, map_button, set_button, bee_img, CanvasObject(self, flowers, False)]

    def clicked_btn(self, text):
        if text == 'Rieš sadu úloh':
            self.parent.solve_screen_init()
        elif text == 'Vytvor mapu':
            self.parent.create_map_screen_init()
        elif text == 'Vytvor sadu úloh':
            self.parent.create_set_screen_init()
