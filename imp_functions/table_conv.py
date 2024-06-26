from utils import *


def draw_table(c, table, y, width, ns):

    rows = table.findall('.//w:tr', ns)
    for row in rows:
        cols = row.findall('.//w:tc', ns)
        x = 50
        for col in cols:
            cell_text = ''.join(col.itertext())
            c.drawString(x, y, cell_text.strip())
            x += 100
        y -= 20
    return y
