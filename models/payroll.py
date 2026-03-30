from bson import ObjectId
from datetime import datetime
from config import db

payroll = db["payroll"]


def generate_payslip(emp_id, emp_name, department, month, year, basic, hra, da, ta, pf, tax, other_deductions):
    gross = basic + hra + da + ta
    total_deductions = pf + tax + other_deductions
    net_pay = gross - total_deductions

    doc = {
        "employee_id": emp_id,
        "employee_name": emp_name,
        "department": department,
        "month": month,
        "year": year,
        "earnings": {
            "basic": basic,
            "hra": hra,
            "da": da,
            "ta": ta,
            "gross": gross,
        },
        "deductions": {
            "pf": pf,
            "tax": tax,
            "other": other_deductions,
            "total": total_deductions,
        },
        "net_pay": net_pay,
        "status": "generated",
        "generated_at": datetime.utcnow(),
    }
    result = payroll.insert_one(doc)
    return str(result.inserted_id)


def get_all_payslips():
    all_slips = list(payroll.find().sort("generated_at", -1))
    for slip in all_slips:
        slip["_id"] = str(slip["_id"])
    return all_slips


def get_payslip_by_id(slip_id):
    slip = payroll.find_one({"_id": ObjectId(slip_id)})
    if slip:
        slip["_id"] = str(slip["_id"])
    return slip


def get_payslips_by_employee(emp_id):
    slips = list(payroll.find({"employee_id": emp_id}).sort("generated_at", -1))
    for slip in slips:
        slip["_id"] = str(slip["_id"])
    return slips


def mark_payslip_paid(slip_id):
    payroll.update_one(
        {"_id": ObjectId(slip_id)},
        {"$set": {"status": "paid", "paid_at": datetime.utcnow()}}
    )
    return True


def delete_payslip(slip_id):
    result = payroll.delete_one({"_id": ObjectId(slip_id)})
    return result.deleted_count > 0


def get_payroll_summary():
    pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "total": {"$sum": "$net_pay"}
        }}
    ]
    results = list(payroll.aggregate(pipeline))
    summary = {"generated": {"count": 0, "total": 0}, "paid": {"count": 0, "total": 0}}
    for r in results:
        summary[r["_id"]] = {"count": r["count"], "total": r["total"]}
    return summary
