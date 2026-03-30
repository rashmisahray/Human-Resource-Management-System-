<div align="center">

# 🏢 Human Resource Management System (HRMS)

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=render)](https://human-resource-management-system-ddim.onrender.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

An intuitive and efficient HR management backend built to handle employees, departments, and payroll seamlessly.

[**Explore Live Application**](https://human-resource-management-system-ddim.onrender.com)

</div>

---

## 🚀 Overview

This modern Human Resource Management System tracks organization-wide operations, from managing employee databases to structuring departments and handling complex payroll data. The application features built-in Role-Based Access Control to ensure data security across departments.

---

## 🔑 Test Credentials (Interactive Login)

You can easily explore the live app by logging into any of the predefined roles below. Simply click the live demo link and use these credentials to access role-specific features.

| Role | Username | Password |
|:---|:---|:---|
| 👑 **System Administrator** | `admin` | `admin123` |
| 🧑‍💼 **Human Resources** | `hr` | `hr123` |
| 💰 **Finance / Payroll** | `finance` | `finance123` |
| 👔 **Department Head** | `depthead` | `depthead123` |

> **Note**: Click [here to Go to the Login Page](https://human-resource-management-system-ddim.onrender.com)

---

## 🛠 Features

- **Employee Management**: Create, update, view, and remove employee records.
- **Department Controls**: Organize staff logically across internal division hierarchies.
- **Payroll Pipeline**: Manage salaries, bonuses, and tax deductions safely.
- **Role-Based Authentication**: Custom dashboard routing based on department/role. 

---

## 💻 Tech Stack

- **Backend Framework**: Python / Flask
- **Database**: MongoDB (via `pymongo`)
- **Web Server**: Gunicorn
- **Styling**: HTML/CSS & Jinja2 Templates

---

## ⚙️ Local Setup Guide

If you'd like to run the project locally, run the commands below:

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd "HRMS Database and backend deployed on Cloud"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory and ensure you provide your database URI:
   ```env
   MONGO_URI="your-mongodb-connection-string"
   SECRET_KEY="your-secret-key"
   ```

5. **Start the Application**
   ```bash
   python app.py
   ```
   > The app runs on `http://127.0.0.1:5000` by default.

---
*Developed with ❤️*
