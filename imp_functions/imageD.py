from utils import *


def get_image_data(drawing, ns, media):

    blip = drawing.find(
        './/a:blip', {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
    if blip is not None:
        r_embed = blip.attrib.get(
            '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if r_embed:
            return media.get(f'word/media/{r_embed}')

    return None
