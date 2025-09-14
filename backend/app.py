from flask import Flask, render_template, request, jsonify
import sys
import os

# Подключаем модуль yolo_inference
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))
from yolo_inference import process_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    try:
        img_base64, objects = process_image(image_bytes)
        return jsonify({"image_base64": img_base64, "objects": objects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== Запуск сервера =====
if __name__ == "__main__":
    print("Server is starting on http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
