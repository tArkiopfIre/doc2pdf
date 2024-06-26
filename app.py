from utils import *
from imp_functions import *

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_form():

    return render_template('upload_form.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'document' not in request.files:
        return 'No file part'
    file = request.files['document']
    if file.filename == '':
        return 'No selected file'
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if filename.endswith('.docx'):
        pdf_path = convert_docx_to_pdf(file_path)
    elif filename.endswith('.txt'):
        pdf_path = convert_txt_to_pdf(file_path)
    else:
        return 'Unsupported file type'

    return send_file(pdf_path, as_attachment=True)


def convert_docx_to_pdf(docx_path):

    pdf_path = docx_path.rsplit('.', 1)[0] + '.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50

    with zipfile.ZipFile(docx_path) as docx:

        with docx.open('word/document.xml') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            media = {name: docx.read(name) for name in docx.namelist(
            ) if name.startswith('word/media/')}

            for paragraph in root.findall('.//w:p', ns):
                for run in paragraph.findall('.//w:r', ns):

                    text = ''.join(run.itertext())
                    if text:
                        if y < 50:
                            c.showPage()
                            y = height - 50
                        c.drawString(50, y, text)
                        y -= 20

                    for drawing in run.findall('.//w:drawing', ns):
                        image_data = get_image_data(drawing, ns, media)
                        if image_data:
                            if y < 100:
                                c.showPage()
                                y = height - 100
                            image = ImageReader(BytesIO(image_data))
                            c.drawImage(image, 50, y - 100, width=100,
                                        preserveAspectRatio=True, mask='auto')
                            y -= 120

            for table in root.findall('.//w:tbl', ns):
                if y < 50:
                    c.showPage()
                    y = height - 50
                y = draw_table(c, table, y, width, ns)

    c.save()
    return pdf_path


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
