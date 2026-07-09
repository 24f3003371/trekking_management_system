#reads json , calls services , return json 
from flask import request , jsonify 
from backend import cache
from backend.services.auth_services import login_user , register_user


def register_controller():
    data = request.get_json()

    response,status =register_user(data)

    return jsonify(response),status 


def login_controller():
    data =request.get_json()
    response , status = login_user(data)
    return jsonify(response), status 