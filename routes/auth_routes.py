from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import USERS

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("employee_bp.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role_tab = request.form.get("role_tab", "admin")

        user = USERS.get(username)
        if user and user["password"] == password and user["role"] == role_tab:
            session["user"] = username
            session["role"] = user["role"]
            session["name"] = user["name"]
            flash(f"Welcome, {user['name']}!", "success")
            return redirect(url_for("employee_bp.dashboard"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("auth_bp.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("auth_bp.login"))
