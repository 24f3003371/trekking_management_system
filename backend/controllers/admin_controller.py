from flask import request, jsonify
from backend.services.admin_services import admin_dashboard,create_staff,search_staff,search_treks,search_users,remove_staff_from_trek,all_staff,assign_trek,blacklist_user,unblacklist_user

def admin_dash_controller():
    response=admin_dashboard()
    return jsonify(response)

def create_staff_controller():
    data=request.get_json()
    reponse,status=create_staff(data)
    return jsonify(reponse),status

def search_staff_controller():
    keyword=request.args.get("keyword")
    reponse =search_staff(keyword)
    

def search_user_controller():

def remove_staff_controller():

def all_staff_controller():


def assign_trek_controller():

def blacklist_contoller():

def unblacklist_controller():