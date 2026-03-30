from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from utils.auth import role_required
from models.department import (
    add_department, get_all_departments, get_department_by_id,
    update_department, delete_department,
    add_location, get_all_locations, get_location_by_id,
    update_location, delete_location
)

department_bp = Blueprint("department_bp", __name__)


@department_bp.route("/departments", methods=["GET", "POST"])
def departments_page():
    if request.method == "POST":
        if session.get("role") not in ["admin", "hr"]:
            abort(403)
        name = request.form.get("name", "")
        parent_id = request.form.get("parent_id", "")
        description = request.form.get("description", "")
        add_department(name, parent_id, description)
        flash("Department added", "success")
        return redirect(url_for("department_bp.departments_page"))

    all_departments = get_all_departments()
    return render_template("departments.html", departments=all_departments)


@department_bp.route("/departments/<dept_id>/edit", methods=["POST"])
@role_required(["admin", "hr"])
def department_edit(dept_id):
    name = request.form.get("name", "")
    parent_id = request.form.get("parent_id", "")
    description = request.form.get("description", "")
    update_department(dept_id, name, parent_id, description)
    flash("Department updated", "success")
    return redirect(url_for("department_bp.departments_page"))


@department_bp.route("/departments/<dept_id>/delete", methods=["POST"])
@role_required(["admin", "hr"])
def department_delete(dept_id):
    delete_department(dept_id)
    flash("Department deleted", "success")
    return redirect(url_for("department_bp.departments_page"))


@department_bp.route("/locations", methods=["GET", "POST"])
def locations_page():
    if request.method == "POST":
        if session.get("role") not in ["admin", "hr"]:
            abort(403)
        name = request.form.get("name", "")
        address = request.form.get("address", "")
        city = request.form.get("city", "")
        state = request.form.get("state", "")
        country = request.form.get("country", "India")
        add_location(name, address, city, state, country)
        flash("Location added", "success")
        return redirect(url_for("department_bp.locations_page"))

    all_locations = get_all_locations()
    return render_template("locations.html", locations=all_locations)


@department_bp.route("/locations/<loc_id>/edit", methods=["POST"])
@role_required(["admin", "hr"])
def location_edit(loc_id):
    name = request.form.get("name", "")
    address = request.form.get("address", "")
    city = request.form.get("city", "")
    state = request.form.get("state", "")
    country = request.form.get("country", "India")
    update_location(loc_id, name, address, city, state, country)
    flash("Location updated", "success")
    return redirect(url_for("department_bp.locations_page"))


@department_bp.route("/locations/<loc_id>/delete", methods=["POST"])
@role_required(["admin", "hr"])
def location_delete(loc_id):
    delete_location(loc_id)
    flash("Location deleted", "success")
    return redirect(url_for("department_bp.locations_page"))
