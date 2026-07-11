from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from backend.services.admin_services import (
    admin_dashboard,
    create_staff,
    search_staff,
    search_treks,
    search_users,
    remove_staff_from_trek,
    all_staff,
    assign_trek,
    blacklist_user,
    unblacklist_user
)

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/dashboard")
@jwt_required()
def admin_dash_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    response = admin_dashboard()
    return jsonify(response), 200



@admin_bp.post("/staff")
@jwt_required()
def create_staff_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    response, status = create_staff(data)

    return jsonify(response), status



@admin_bp.get("/users/search")
@jwt_required()
def search_user_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    keyword = request.args.get("keyword")

    response = search_users(keyword)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    users = [user.to_dict() for user in response]

    return jsonify(users), 200


@admin_bp.get("/staff/search")
@jwt_required()
def search_staff_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    keyword = request.args.get("keyword")

    response = search_staff(keyword)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    staff = [user.to_dict() for user in response]

    return jsonify(staff), 200



@admin_bp.get("/treks/search")
@jwt_required()
def search_treks_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    keyword = request.args.get("keyword")

    response = search_treks(keyword)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    treks = [trek.to_dict() for trek in response]

    return jsonify(treks), 200



@admin_bp.get("/staff")
@jwt_required()
def all_staff_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    staff = all_staff()

    result = [user.to_dict() for user in staff]

    return jsonify(result), 200



@admin_bp.post("/assign-trek")
@jwt_required()
def assign_trek_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    response, status = assign_trek(
        data["staff_id"],
        data["trek_id"]
    )

    return jsonify(response), status



@admin_bp.delete("/remove-trek")
@jwt_required()
def remove_staff_controller():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    response, status = remove_staff_from_trek(
        data["trek_id"],
        data["staff_id"]
    )

    return jsonify(response), status

@admin_bp.put("/blacklist/<int:user_id>")
@jwt_required()
def blacklist_controller(user_id):
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    response, status = blacklist_user(user_id)

    return jsonify(response), status


@admin_bp.put("/unblacklist/<int:user_id>")
@jwt_required()
def unblacklist_controller(user_id):
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    response, status = unblacklist_user(user_id)

    return jsonify(response), status