from flask import Flask, request, jsonify, render_template
from PIL import Image
from collections import defaultdict
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_colors(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())

    color_count = defaultdict(int)
    for pixel in pixels:
        color_count[pixel] += 1

    sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)

    colors = []
    for color, count in sorted_colors:
        hex_code = "#%02x%02x%02x" % color
        colors.append({"rgb": color, "hex": hex_code, "count": count})

    return colors

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    colors = get_colors(file_path)

    return jsonify({"colors": colors})

if __name__ == '__main__':
    app.run(debug=True)
