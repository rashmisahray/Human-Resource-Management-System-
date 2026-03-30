from bson import ObjectId
from datetime import datetime
from config import db

departments = db["departments"]
locations = db["locations"]


def add_department(name, parent_id="", description=""):
    doc = {
        "name": name,
        "parent_id": parent_id,
        "description": description,
        "created_at": datetime.utcnow(),
    }
    result = departments.insert_one(doc)
    return str(result.inserted_id)


def get_all_departments():
    all_depts = list(departments.find().sort("name", 1))
    for dept in all_depts:
        dept["_id"] = str(dept["_id"])
    return all_depts


def get_department_by_id(dept_id):
    dept = departments.find_one({"_id": ObjectId(dept_id)})
    if dept:
        dept["_id"] = str(dept["_id"])
    return dept


def update_department(dept_id, name, parent_id="", description=""):
    departments.update_one(
        {"_id": ObjectId(dept_id)},
        {"$set": {"name": name, "parent_id": parent_id, "description": description}}
    )
    return True


def delete_department(dept_id):
    result = departments.delete_one({"_id": ObjectId(dept_id)})
    return result.deleted_count > 0


def get_department_count():
    return departments.count_documents({})


def add_location(name, address="", city="", state="", country="India"):
    doc = {
        "name": name,
        "address": address,
        "city": city,
        "state": state,
        "country": country,
        "created_at": datetime.utcnow(),
    }
    result = locations.insert_one(doc)
    return str(result.inserted_id)


def get_all_locations():
    all_locs = list(locations.find().sort("name", 1))
    for loc in all_locs:
        loc["_id"] = str(loc["_id"])
    return all_locs


def get_location_by_id(loc_id):
    loc = locations.find_one({"_id": ObjectId(loc_id)})
    if loc:
        loc["_id"] = str(loc["_id"])
    return loc


def update_location(loc_id, name, address="", city="", state="", country="India"):
    locations.update_one(
        {"_id": ObjectId(loc_id)},
        {"$set": {"name": name, "address": address, "city": city, "state": state, "country": country}}
    )
    return True


def delete_location(loc_id):
    result = locations.delete_one({"_id": ObjectId(loc_id)})
    return result.deleted_count > 0


def get_location_count():
    return locations.count_documents({})
