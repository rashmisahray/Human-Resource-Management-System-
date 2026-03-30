from functools import wraps
from flask import session, redirect, url_for, flash, abort

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("auth_bp.login"))
            
            user_role = session.get("role")
            if user_role not in allowed_roles:
                flash("You do not have permission to access this resource", "error")
                # Return 403 Forbidden for API/form actions, or redirect to dashboard
                abort(403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
