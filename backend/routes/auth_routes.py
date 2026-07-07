from flask import Blueprint
from backend.controllers.authcontrollers import register_controller,login_controller
auth_bp=Blueprint("auth",__name__,url_prefix="api/auth")

@auth_bp.post("/register")
def register_route():
    return register_controller()

@auth_bp.post("/login")
def login_route():
    return login_controller()
