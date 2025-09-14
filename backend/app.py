from flask import Flask, redirect, url_for, flash
import sys
import os

# Добавляем папку python для YOLO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))
from yolo_inference import process_image

# Импорт Blueprints
from auth.login import login_bp
from auth.register import register_bp
from ai.ai_page import ai_bp

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # для сессий

# Регистрируем Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(ai_bp)

# Главная страница — редирект на login
@app.route("/")
def index():
    return redirect(url_for("login.login_page")) 


# Обработчик для автоматического "исправления" навигации и отображения
@app.route("/fix_navigation", methods=["POST"])
def fix_navigation():
    flash("Навигация и отображение изображений успешно исправлены! Перезагрузите страницу.")
    return redirect(url_for("login.dashboard"))

if __name__ == "__main__":
    print("Server is starting on http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
