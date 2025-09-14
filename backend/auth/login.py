from flask import Blueprint, render_template, request, redirect, session, flash
from .utils import init_db, create_user, verify_user, get_history

import sqlite3, json

# Инициализируем Blueprint
login_bp = Blueprint("login", __name__, template_folder="../../frontend")

# Инициализация БД при старте
init_db()

@login_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if verify_user(username, password):
            session["username"] = username
            flash("Вы успешно вошли!")
            return redirect("/dashboard")
        else:
            flash("Неверный логин или пароль.")
    return render_template("login.html")

@login_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            create_user(username, password)
            flash("Регистрация успешна! Войдите в систему.")
            return redirect("/login")
        except:
            flash("Имя пользователя уже занято.")
    return render_template("register.html")

@login_bp.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Пожалуйста, войдите.")
        return redirect("/login")
    username = session["username"]
    return render_template("dashboard.html", username=username)


@login_bp.route("/history")
def history():
    if "username" not in session:
        flash("Пожалуйста, войдите.")
        return redirect("/login")
    username = session["username"]

    conn = sqlite3.connect("database/users.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = cur.fetchone()[0]
    conn.close()

    history_rows = get_history(user_id)
    history = []
    for image_path, objects_json, timestamp in history_rows:
        if image_path and not image_path.startswith("data:image"):
            image_path = f"data:image/jpeg;base64,{image_path}"
        history.append({
            "image_path": image_path,
            "objects": json.loads(objects_json),
            "timestamp": timestamp
        })

    return render_template("history.html", username=username, history=history)

@login_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Вы вышли из системы.")
    return redirect("/login")
