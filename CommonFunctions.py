from PIL import Image

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