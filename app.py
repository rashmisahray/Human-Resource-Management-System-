from flask import Flask, session, redirect, url_for, request
from config import SECRET_KEY
from routes.employee_routes import employee_bp
from routes.department_routes import department_bp
from routes.auth_routes import auth_bp
from routes.payroll_routes import payroll_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(department_bp)
app.register_blueprint(payroll_bp)

OPEN_ROUTES = ["auth_bp.login", "static"]


@app.before_request
def require_login():
    if request.endpoint in OPEN_ROUTES or (request.endpoint and request.endpoint.startswith("static")):
        return
    if "user" not in session:
        return redirect(url_for("auth_bp.login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
