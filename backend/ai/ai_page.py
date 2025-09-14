from flask import Blueprint, render_template, request, session, flash
from auth.utils import add_history
import sys
import os
import sqlite3
import json

# Добавляем python в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))
from yolo_inference import process_image

ai_bp = Blueprint("ai", __name__, template_folder="../../frontend")

@ai_bp.route("/ai", methods=["GET", "POST"])
def ai_page():
    # Проверка авторизации
    if "username" not in session:
        flash("Пожалуйста, войдите.")
        return render_template("login.html")

    result_img = None
    objects = None

    if request.method == "POST":
        image_file = request.files.get("image")
        if not image_file:
            flash("Выберите изображен   ие!")
            return render_template("ai.html", result_img=result_img, objects=objects)

        # Обработка изображения YOLO
        image_bytes = image_file.read()
        annotated_base64, objects = process_image(image_bytes)
        result_img = f"data:image/jpeg;base64,{annotated_base64}"

        # Получаем user_id из БД
        conn = sqlite3.connect("database/users.db")
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=?", (session["username"],))
        row = cur.fetchone()
        conn.close()

        if row:
            user_id = row[0]
            add_history(user_id, annotated_base64, json.dumps(objects))
            flash("Изображение обработано!")
        else:
            flash("Ошибка: пользователь не найден.")

    return render_template("ai.html", result_img=result_img, objects=objects)
