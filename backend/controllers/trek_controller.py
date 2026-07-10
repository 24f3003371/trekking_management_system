from flask import Blueprint, request, jsonify
from backend.services.trek_service import (
    create_trek,
    update_trek,
    delete_trek,
    all_trek,
    trek_by_id,
    admin_manage_trek_routes,
    participant_list,
    manage_participant_list,
    mark_trek
)
from backend import cache

trek_bp = Blueprint("trek", __name__, url_prefix="/api/treks")


@trek_bp.post("/")
def create_trek_controller():
    data = request.get_json()
    response, status = create_trek(data)
    return jsonify(response), status


@trek_bp.put("/<int:trek_id>")
def update_trek_controller(trek_id):
    data = request.get_json()
    response, status = update_trek(trek_id, data)
    return jsonify(response), status


@trek_bp.delete("/<int:trek_id>")
def delete_trek_controller(trek_id):
    response, status = delete_trek(trek_id)
    return jsonify(response), status


@trek_bp.get("/")
@cache.cached(timeout=300)
def get_all_treks():
    treks = all_trek()
    return jsonify([trek.to_dict() for trek in treks]), 200


@trek_bp.get("/<int:trek_id>")
@cache.cached(timeout=300)
def get_trek(trek_id):
    result = trek_by_id(trek_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result.to_dict()), 200


@trek_bp.get("/admin")
@cache.cached(timeout=300)
def admin_manage_treks():
    treks = admin_manage_trek_routes()
    return jsonify([trek.to_dict() for trek in treks]), 200


@trek_bp.get("/<int:trek_id>/participants")
def participant_list_controller(trek_id):
    result = participant_list(trek_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify([participant.to_dict() for participant in result]), 200


@trek_bp.put("/participants/<int:booking_id>")
def manage_participant_controller(booking_id):
    data = request.get_json()

    response, status = manage_participant_list(
        booking_id,
        data["status"]
    )

    return jsonify(response), status


@trek_bp.put("/<int:trek_id>/complete")
def mark_trek_controller(trek_id):
    response, status = mark_trek(trek_id)
    return jsonify(response), status