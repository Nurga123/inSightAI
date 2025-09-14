from flask import Flask, render_template, request, jsonify
from python.yolo_inference import process_image  # Импортируем рабочую функцию

app = Flask(__name__)

# ===== Главная страница =====
@app.route('/')
def index():
    return render_template("index.html")

# ===== API загрузки изображения =====
@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()  # Получаем байты изображения
    try:
        annotated_img_path, objects = process_image(image_bytes)
        return jsonify({"image_path": annotated_img_path, "objects": objects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== Запуск сервера =====
if __name__ == "__main__":
    print("Server is starting on http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
