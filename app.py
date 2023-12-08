import utility
import penpal
import linedraw
from distutils.log import debug
from fileinput import filename
from flask import Flask, render_template, request

app = Flask(__name__)

FILENAME = ""

penpal.togglePen()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/successful_upload', methods=['POST'])
def successful_upload():
    global FILENAME
    if request.method == 'POST':
        f = request.files['file']
        f.save(f"images/{f.filename}")
        FILENAME = f.filename
        return render_template('index.html')


@app.route('/draw_image', methods=['POST'])
def draw_image():
    lines = linedraw.sketch(f"images/{FILENAME}")
    utility.copyToPositionsTxt(lines)
    penpal.drawTxtFile()    
    return "ok"


@app.route('/manual_control', methods=['POST'])
def manual_control():
    penpal.manual()
    print("manual control")
    return "ok"


@app.route('/dance', methods=['POST'])
def dance():
    penpal.dance()
    return "ok"
