from PIL import Image

def resize_image(img, max_width, max_height):
    w_percent = (max_width / float(img.size[0]))
    height = int((float(img.size[1]) * float(w_percent)))
    if height > max_height:
        wpercent = (max_height / float(img.size[1]))
        width = int((float(img.size[0]) * float(wpercent)))
        return img.resize((width, max_height), Image.ANTIALIAS)
    return img.resize((max_width, height), Image.ANTIALIAS)