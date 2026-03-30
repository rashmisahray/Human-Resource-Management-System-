from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth import role_required
from models.payroll import (
    generate_payslip, get_all_payslips, get_payslip_by_id,
    mark_payslip_paid, delete_payslip, get_payroll_summary
)
from models.employee import get_all_employees

payroll_bp = Blueprint("payroll_bp", __name__)

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


@payroll_bp.route("/payroll")
@role_required(["admin", "finance"])
def payroll_list():
    all_payslips = get_all_payslips()
    summary = get_payroll_summary()
    return render_template("payroll.html", payslips=all_payslips, summary=summary, months=MONTHS)


@payroll_bp.route("/payroll/generate", methods=["GET", "POST"])
@role_required(["admin", "finance"])
def payroll_generate():
    if request.method == "POST":
        emp_id = request.form.get("employee_id", "")
        emp_name = request.form.get("employee_name", "")
        department = request.form.get("department", "")
        month = request.form.get("month", "")
        year = int(request.form.get("year", 2026))
        basic = float(request.form.get("basic", 0))
        hra = float(request.form.get("hra", 0))
        da = float(request.form.get("da", 0))
        ta = float(request.form.get("ta", 0))
        pf = float(request.form.get("pf", 0))
        tax = float(request.form.get("tax", 0))
        other_deductions = float(request.form.get("other_deductions", 0))

        generate_payslip(emp_id, emp_name, department, month, year, basic, hra, da, ta, pf, tax, other_deductions)
        flash("Payslip generated successfully", "success")
        return redirect(url_for("payroll_bp.payroll_list"))

    employees = get_all_employees()
    return render_template("payroll_generate.html", employees=employees, months=MONTHS)


@payroll_bp.route("/payroll/<slip_id>")
@role_required(["admin", "finance"])
def payroll_view(slip_id):
    slip = get_payslip_by_id(slip_id)
    if not slip:
        flash("Payslip not found", "error")
        return redirect(url_for("payroll_bp.payroll_list"))
    return render_template("payroll_view.html", slip=slip)


@payroll_bp.route("/payroll/<slip_id>/pay", methods=["POST"])
@role_required(["admin", "finance"])
def payroll_pay(slip_id):
    mark_payslip_paid(slip_id)
    flash("Payment marked as paid", "success")
    return redirect(url_for("payroll_bp.payroll_list"))


@payroll_bp.route("/payroll/<slip_id>/delete", methods=["POST"])
@role_required(["admin", "finance"])
def payroll_delete(slip_id):
    delete_payslip(slip_id)
    flash("Payslip deleted", "success")
    return redirect(url_for("payroll_bp.payroll_list"))
