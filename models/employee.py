from bson import ObjectId
from datetime import datetime
from config import db

employees = db["employees"]


def build_employee_doc(form_data):
    doc = {
        "employee_id": form_data.get("employee_id", ""),
        "personal": {
            "first_name": form_data.get("first_name", ""),
            "last_name": form_data.get("last_name", ""),
            "email": form_data.get("email", ""),
            "phone": form_data.get("phone", ""),
            "date_of_birth": form_data.get("date_of_birth", ""),
            "gender": form_data.get("gender", ""),
            "address": form_data.get("address", ""),
            "city": form_data.get("city", ""),
            "state": form_data.get("state", ""),
            "country": form_data.get("country", "India"),
            "pincode": form_data.get("pincode", ""),
        },
        "job": {
            "designation": form_data.get("designation", ""),
            "department_id": form_data.get("department_id", ""),
            "department_name": form_data.get("department_name", ""),
            "location_id": form_data.get("location_id", ""),
            "location_name": form_data.get("location_name", ""),
            "date_of_joining": form_data.get("date_of_joining", ""),
            "employment_type": form_data.get("employment_type", "Full-Time"),
            "manager_id": form_data.get("manager_id", ""),
            "manager_name": form_data.get("manager_name", ""),
        },
        "bank": {
            "bank_name": form_data.get("bank_name", ""),
            "account_number": form_data.get("account_number", ""),
            "ifsc_code": form_data.get("ifsc_code", ""),
            "pan_number": form_data.get("pan_number", ""),
            "aadhar_number": form_data.get("aadhar_number", ""),
        },
        "emergency_contact": {
            "name": form_data.get("emergency_name", ""),
            "relation": form_data.get("emergency_relation", ""),
            "phone": form_data.get("emergency_phone", ""),
        },
        "status": form_data.get("status", "onboarding"),
        "lifecycle_history": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    return doc


def add_employee(form_data):
    doc = build_employee_doc(form_data)
    doc["lifecycle_history"].append({
        "action": "onboarding",
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "note": "Employee record created"
    })
    result = employees.insert_one(doc)
    return str(result.inserted_id)


def get_all_employees():
    all_emps = list(employees.find().sort("created_at", -1))
    for emp in all_emps:
        emp["_id"] = str(emp["_id"])
    return all_emps


def get_employee_by_id(emp_id):
    emp = employees.find_one({"_id": ObjectId(emp_id)})
    if emp:
        emp["_id"] = str(emp["_id"])
    return emp


def update_employee(emp_id, form_data):
    existing = employees.find_one({"_id": ObjectId(emp_id)})
    if not existing:
        return False

    updated_doc = {
        "employee_id": form_data.get("employee_id", ""),
        "personal": {
            "first_name": form_data.get("first_name", ""),
            "last_name": form_data.get("last_name", ""),
            "email": form_data.get("email", ""),
            "phone": form_data.get("phone", ""),
            "date_of_birth": form_data.get("date_of_birth", ""),
            "gender": form_data.get("gender", ""),
            "address": form_data.get("address", ""),
            "city": form_data.get("city", ""),
            "state": form_data.get("state", ""),
            "country": form_data.get("country", "India"),
            "pincode": form_data.get("pincode", ""),
        },
        "job": {
            "designation": form_data.get("designation", ""),
            "department_id": form_data.get("department_id", ""),
            "department_name": form_data.get("department_name", ""),
            "location_id": form_data.get("location_id", ""),
            "location_name": form_data.get("location_name", ""),
            "date_of_joining": form_data.get("date_of_joining", ""),
            "employment_type": form_data.get("employment_type", "Full-Time"),
            "manager_id": form_data.get("manager_id", ""),
            "manager_name": form_data.get("manager_name", ""),
        },
        "bank": {
            "bank_name": form_data.get("bank_name", ""),
            "account_number": form_data.get("account_number", ""),
            "ifsc_code": form_data.get("ifsc_code", ""),
            "pan_number": form_data.get("pan_number", ""),
            "aadhar_number": form_data.get("aadhar_number", ""),
        },
        "emergency_contact": {
            "name": form_data.get("emergency_name", ""),
            "relation": form_data.get("emergency_relation", ""),
            "phone": form_data.get("emergency_phone", ""),
        },
        "status": form_data.get("status", existing.get("status", "active")),
        "updated_at": datetime.utcnow(),
    }

    employees.update_one(
        {"_id": ObjectId(emp_id)},
        {"$set": updated_doc}
    )
    return True


def delete_employee(emp_id):
    result = employees.delete_one({"_id": ObjectId(emp_id)})
    return result.deleted_count > 0


def update_lifecycle(emp_id, action, note=""):
    valid_actions = ["onboarding", "probation", "confirmed", "promoted", "transferred", "exited", "fnf_settled"]
    if action not in valid_actions:
        return False

    entry = {
        "action": action,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "note": note
    }

    employees.update_one(
        {"_id": ObjectId(emp_id)},
        {
            "$set": {"status": action, "updated_at": datetime.utcnow()},
            "$push": {"lifecycle_history": entry}
        }
    )
    return True


def get_employee_count():
    return employees.count_documents({})


def get_recent_employees(limit=5):
    recent = list(employees.find().sort("created_at", -1).limit(limit))
    for emp in recent:
        emp["_id"] = str(emp["_id"])
    return recent


def search_employees(query):
    search_filter = {
        "$or": [
            {"personal.first_name": {"$regex": query, "$options": "i"}},
            {"personal.last_name": {"$regex": query, "$options": "i"}},
            {"personal.email": {"$regex": query, "$options": "i"}},
            {"employee_id": {"$regex": query, "$options": "i"}},
            {"job.designation": {"$regex": query, "$options": "i"}},
            {"job.department_name": {"$regex": query, "$options": "i"}},
        ]
    }
    results = list(employees.find(search_filter).sort("created_at", -1))
    for emp in results:
        emp["_id"] = str(emp["_id"])
    return results
