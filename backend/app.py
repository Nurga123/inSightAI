from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ===== Моковые данные =====
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

cars = [
    {"id": 1, "model": "Toyota Camry", "status": "ok"},
    {"id": 2, "model": "Honda Civic", "status": "dirty"},
    {"id": 3, "model": "BMW X5", "status": "broken"}
]

# ===== Главная страница с HTML =====
@app.route('/')
def index():
    return render_template("index.html")

# ===== API =====
@app.route('/users/', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/cars/', methods=['GET'])
def get_cars():
    return jsonify(cars)

@app.route('/cars/detect', methods=['POST'])
def detect_car():
    data = request.json
    image_url = data.get("image_url")
    if not image_url:
        return jsonify({"error": "No image_url provided"}), 400

    # Моковая детекция ИИ
    if "dirty" in image_url:
        status = "dirty"
    elif "broken" in image_url:
        status = "broken"
    elif "worn" in image_url:
        status = "worn"
    else:
        status = "ok"

    return jsonify({"image_url": image_url, "detected_status": status})

# ===== Запуск сервера =====
if __name__ == "__main__":
    print("Server is starting on http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
# ===== Конец файла =====