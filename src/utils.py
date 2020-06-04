from wand.image import Color, Image

def isAllowedChar(chr):
    return ((ord(chr) >= 48 and ord(chr) <= 57) or
        (ord(chr) >= 65 and ord(chr) <= 90) or
        (ord(chr) >= 97 and ord(chr) <= 122))

def get_last_segment(url):
    if url.find('/') == -1:
        return url
    else:
        return url[url.rfind('/') + 1:]

def get_url_to_dir_name(url):
    url = get_last_segment(url)
    dir_name = ""
    i = 0

    while i < len(url):
        if not isAllowedChar(url[i]):
            while i < len(url) and not isAllowedChar(url[i]):
                i += 1

            if i < len(url):
                dir_name += '.'
        else:
            dir_name += url[i]
            i += 1

    return dir_name

def remove_alpha(image_path, new_image_path):
    with Image(filename=image_path) as img:
        alpha = img.alpha_channel
        if alpha:
            img.alpha_channel = False
            img.background_color = Color('white')
            img.save(filename=new_image_path)
