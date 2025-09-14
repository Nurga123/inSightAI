from flask import Blueprint, render_template, request, redirect, flash
from .utils import init_db, create_user
init_db()
register_bp = Blueprint("register", __name__, template_folder="../../frontend")
@register_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            create_user(username, password)
            flash("Пользователь успешно создан! Войдите в систему.")
            return redirect("/login")
        except:
            flash("Пользователь с таким именем уже существует.")
    return render_template("register.html")
