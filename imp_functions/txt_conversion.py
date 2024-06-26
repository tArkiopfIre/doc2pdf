from utils import *


def convert_txt_to_pdf(txt_path):

    pdf_path = txt_path.rsplit('.', 1)[0] + '.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50
    with open(txt_path, 'r') as file:
        for line in file:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, line.strip())
            y -= 20
    c.save()
    return pdf_path
