from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth import role_required
from models.employee import (
    add_employee, get_all_employees, get_employee_by_id,
    update_employee, delete_employee, update_lifecycle,
    get_employee_count, get_recent_employees, search_employees
)
from models.department import (
    get_all_departments, get_all_locations,
    get_department_count, get_location_count
)

employee_bp = Blueprint("employee_bp", __name__)


@employee_bp.route("/")
def dashboard():
    total_employees = get_employee_count()
    total_departments = get_department_count()
    total_locations = get_location_count()
    recent_hires = get_recent_employees(5)
    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        total_departments=total_departments,
        total_locations=total_locations,
        recent_hires=recent_hires,
    )


@employee_bp.route("/employees")
def employee_list():
    query = request.args.get("search", "")
    if query:
        all_employees = search_employees(query)
    else:
        all_employees = get_all_employees()
    return render_template("employee_list.html", employees=all_employees, search_query=query)


@employee_bp.route("/employees/add", methods=["GET", "POST"])
@role_required(["admin", "hr"])
def employee_add():
    if request.method == "POST":
        add_employee(request.form)
        flash("Employee added successfully", "success")
        return redirect(url_for("employee_bp.employee_list"))

    departments = get_all_departments()
    locations = get_all_locations()
    managers = get_all_employees()
    return render_template("employee_form.html", mode="add", departments=departments, locations=locations, managers=managers)


@employee_bp.route("/employees/<emp_id>")
def employee_profile(emp_id):
    emp = get_employee_by_id(emp_id)
    if not emp:
        flash("Employee not found", "error")
        return redirect(url_for("employee_bp.employee_list"))
    return render_template("employee_profile.html", employee=emp)


@employee_bp.route("/employees/<emp_id>/edit", methods=["GET", "POST"])
@role_required(["admin", "hr"])
def employee_edit(emp_id):
    if request.method == "POST":
        update_employee(emp_id, request.form)
        flash("Employee updated successfully", "success")
        return redirect(url_for("employee_bp.employee_profile", emp_id=emp_id))

    emp = get_employee_by_id(emp_id)
    if not emp:
        flash("Employee not found", "error")
        return redirect(url_for("employee_bp.employee_list"))

    departments = get_all_departments()
    locations = get_all_locations()
    managers = get_all_employees()
    return render_template("employee_form.html", mode="edit", employee=emp, departments=departments, locations=locations, managers=managers)


@employee_bp.route("/employees/<emp_id>/delete", methods=["POST"])
@role_required(["admin", "hr"])
def employee_delete(emp_id):
    delete_employee(emp_id)
    flash("Employee deleted", "success")
    return redirect(url_for("employee_bp.employee_list"))


@employee_bp.route("/employees/<emp_id>/lifecycle", methods=["POST"])
@role_required(["admin", "hr"])
def employee_lifecycle(emp_id):
    action = request.form.get("action", "")
    note = request.form.get("note", "")
    update_lifecycle(emp_id, action, note)
    flash(f"Status updated to {action}", "success")
    return redirect(url_for("employee_bp.employee_profile", emp_id=emp_id))
