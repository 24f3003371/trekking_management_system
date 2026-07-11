from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend import cache
from backend.models import PaymentStatus
from backend.services.user_service import (
    available_trek,
    book_trek,
    booking_history,
    edit_profile,
    trekking_history
)

user_bp = Blueprint("user", __name__, url_prefix="/api/user")




@user_bp.post("/book/<int:trek_id>")
@jwt_required()
def book_trek_controller(trek_id):
    user_id = int(get_jwt_identity())

    data = request.get_json()

    payment_status = PaymentStatus(data["payment_status"])

    response = book_trek(user_id, trek_id, payment_status)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    return jsonify(response), 200




@user_bp.put("/profile")
@jwt_required()
def edit_profile_controller():
    user_id = get_jwt_identity()

    data = request.get_json()

    response = edit_profile(user_id, data)

    return jsonify(response[0]), response[1]




@user_bp.get("/trek-history")
@jwt_required()
@cache.cached(timeout=300)
def trekking_history_controller():
    user_id = get_jwt_identity()

    response = trekking_history(user_id)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    history = [booking.to_dict() for booking in response]

    return jsonify(history), 200


@user_bp.get("/available-treks")
@cache.cached(timeout=300)
def available_trek_controller():

    treks = available_trek()

    trek_list = [trek.to_dict() for trek in treks]

    return jsonify(trek_list), 200



@user_bp.get("/booking-history")
@jwt_required()
@cache.cached(timeout=300)
def booking_history_controller():
    user_id = get_jwt_identity()

    response = booking_history(user_id)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    bookings = [booking.to_dict() for booking in response]

    return jsonify(bookings), 200