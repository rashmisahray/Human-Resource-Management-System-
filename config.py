import os
import ssl
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

SECRET_KEY = os.getenv("SECRET_KEY", "hrms-secret-key-2026")
DATABASE_NAME = "hrms_db"

USERS = {
    "admin": {"password": os.getenv("ADMIN_PASSWORD"), "role": "admin", "name": "Admin User"},
    "hr": {"password": os.getenv("HR_PASSWORD"), "role": "hr", "name": "HR Manager"},
    "finance": {"password": os.getenv("FINANCE_PASSWORD"), "role": "finance", "name": "Finance Manager"},
    "depthead": {"password": os.getenv("DEPTHEAD_PASSWORD"), "role": "depthead", "name": "Department Head"},
}

# Custom SSL context to fix TLS handshake errors on Windows with Python 3.12
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=True)
db = client[DATABASE_NAME]
