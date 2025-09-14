from flask import Blueprint, render_template, request, session, flash
from auth.utils import add_history
import sys
import os
import sqlite3
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))
from yolo_inference import process_image
ai_bp = Blueprint("ai", __name__, template_folder="../../frontend")
@ai_bp.route("/ai", methods=["GET", "POST"])
def ai_page():
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
        image_bytes = image_file.read()
        annotated_base64, objects = process_image(image_bytes)
        result_img = f"data:image/jpeg;base64,{annotated_base64}"
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
    detected_classes = []
    is_damaged = False
    is_dirty = False
    damage_classes = {"glass-break", "scratch", "corrosion", "dent",}
    dirt_class = {"dirt", "corrosion"}
    if objects:
        try:
            if isinstance(objects, str):
                objects_list = json.loads(objects)
            else:
                objects_list = objects
            detected_classes = [obj["class"].lower() for obj in objects_list if "class" in obj]
            is_damaged = any(cls in damage_classes for cls in detected_classes)
            is_dirty = any(cls in dirt_class for cls in detected_classes)
        except Exception:
            detected_classes = []
            is_damaged = False
            is_dirty = False
    status = []
    if is_damaged:
        status.append("Damaged car")
    else:
        status.append("Not damaged car")
    if is_dirty:
        status.append("Dirty car")
    else:
        status.append("Clean car")
    objects_text = ", ".join(detected_classes) if detected_classes else "No objects detected"
    status_text = " | ".join(status)
    return render_template("ai.html", result_img=result_img, objects=objects_text, status=status_text)
