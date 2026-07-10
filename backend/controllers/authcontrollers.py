#reads json , calls services , return json 
from flask import request , jsonify ,Blueprint
from backend import cache
from backend.services.auth_services import login_user , register_user
auth_bp=Blueprint("auth",__name__,url_prefix="api/auth")

@auth_bp.post("/register")
def register_controller():
    data = request.get_json()

    response,status =register_user(data)

    return jsonify(response),status 

@auth_bp.post("/login")
def login_controller():
    data =request.get_json()
    response , status = login_user(data)
    return jsonify(response), status 