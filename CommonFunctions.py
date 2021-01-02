from PIL import Image
import re
import pygame
import threading


pygame.init()
pygame.mixer.init()

WRONG_VOLUME = 0.15
CORRECT_VOLUME = 0.15
COLLECT_VOLUME = 1.0


def resize_image(img, max_width, max_height):
    w_percent = (max_width / float(img.size[0]))
    height = int((float(img.size[1]) * float(w_percent)))
    if height > max_height:
        wpercent = (max_height / float(img.size[1]))
        width = int((float(img.size[0]) * float(wpercent)))
        return img.resize((width, max_height), Image.ANTIALIAS)
    return img.resize((max_width, height), Image.ANTIALIAS)


def calculate_coords(i, j, rows, cols):
    one_row = 480 / rows
    one_col = 900 / cols
    return (j * one_col) + 10 + (one_row / 2), (i * one_row) + 60 + (one_col / 2)


def translate_color(color, ALPHA):
    if color == "black":
        return (0, 0, 0, ALPHA)
    elif color == "white":
        return (255, 255, 255, ALPHA)
    elif color == "red":
        return (255, 0, 0, ALPHA)
    elif color == "green":
        return (64, 255, 0, ALPHA)
    elif color == "yellow":
        return (255, 255, 0, ALPHA)
    return (0, 0, 0, ALPHA)


def resize_image_by_width(img, basewidth):
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def resize_image_by_height(img, hsize):
    wpercent = (hsize / float(img.size[1]))
    basewidth = int((float(img.size[0]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def check_map_file(lines, map_name):
    lines = lines.split("\n")

    if len(lines) < 14:
        return "Chýbajúce riadky súboru"

    message = "Chyba: {}"
    nums = []
    if re.fullmatch("Nazov: [a-zA-Z0-9_]{1,15}", lines[0]) is None:
        nums.append(lines[0])
    elif lines[1] != "":
        nums.append(lines[1])
    elif lines[2] != "# Nastavenia postavicky #":
        nums.append(lines[2])
    elif re.fullmatch("Meno: [a-zA-Z0-9_]{1,10}", lines[3]) is None:
        nums.append(lines[3])
    elif re.fullmatch("Otacanie: (vsetky smery|ziadne|vlavo/vpravo|dole/hore)", lines[4]) is None:
        nums.append(lines[4])
    elif re.fullmatch("Smerovanie: (-|vpravo|hore|dole|vlavo)", lines[5]) is None:
        print(message.format('5'))
        nums.append(lines[5])
    elif re.fullmatch("Mriezka: (cierna|biela|cervena|zelena|zlta)", lines[6]) is None:
        nums.append(lines[6])
    elif re.fullmatch("Trajektoria: (cierna|biela|cervena|zelena|zlta)", lines[7]) is None:
        nums.append(lines[7])
    elif lines[8] != "":
        nums.append(lines[8])
    elif lines[9] != "# Predmety #":
        nums.append(lines[9])
    elif re.fullmatch("(a,b,c,d|a,b,c|a,b|a)", lines[10]) is None:
        nums.append(lines[10])
    elif lines[11] != "":
        nums.append(lines[11])
    elif lines[12] != "# Prekazky #":
        nums.append(lines[12])
    elif re.fullmatch("(x,y,z|x,y|x)", lines[13]) is None:
        nums.append(lines[13])

    map_name2 = lines[0].split(": ")[1]
    if map_name2 != map_name:
        return message.format("Neexistujúci názov mapy: {}.".format(map_name))

    if len(lines) > 14:
        new_lines = lines[14:]
        new_lines = list(set(new_lines))
        if not (len(new_lines) == 1 and new_lines[0] == ""):
            return message.format("Na konci súboru sa nachádzajú nepovolené riadky.")

    if len(nums) == 0:
        return ""

    return message.format(nums[0])


def playsound(path, volume):
    if volume == 1:
        volume = COLLECT_VOLUME
    elif volume == 2:
        volume = CORRECT_VOLUME
    else:
        volume = WRONG_VOLUME
    threading.Thread(target=playsound_thread, args=(path, volume,)).start()


def playsound_thread(path, volume):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
