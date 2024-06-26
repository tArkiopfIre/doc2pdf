from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os
import zipfile
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
