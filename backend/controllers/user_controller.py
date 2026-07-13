from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend import cache
from backend.models import PaymentStatus
from backend.services.user_service import (
    available_trek,
    book_trek,
    cancel_booking,
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

    # The available-treks endpoint is cached and a successful booking changes
    # its slot count.
    cache.delete_memoized(available_trek_controller)

    return jsonify(response), 200


@user_bp.delete("/cancel/<int:booking_id>")
@jwt_required()
def cancel_booking_controller(booking_id):
    """Allow a trekker to cancel their own booking."""
    user_id = int(get_jwt_identity())
    response = cancel_booking(user_id, booking_id)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    # Cancelling frees a place, so invalidate the cached availability too.
    cache.delete_memoized(available_trek_controller)
    return jsonify(response), 200


@user_bp.post("/booking-history/export")
@jwt_required()
def request_booking_history_export():
    """Queue a private booking-history CSV without blocking the dashboard."""
    user_id = int(get_jwt_identity())
    from backend.celery_tasks.export_history import create_booking_export

    task = create_booking_export.delay(user_id)
    cache.set(f"export-task-owner:{task.id}", user_id, timeout=3600)
    return jsonify({"task_id": task.id, "status": "queued"}), 202


def _owned_export_task(task_id, user_id):
    owner_id = cache.get(f"export-task-owner:{task_id}")
    if owner_id is None or str(owner_id) != str(user_id):
        return None
    from backend.celery_tasks.celery_app import celery
    return celery.AsyncResult(task_id)


@user_bp.get("/booking-history/export/<task_id>")
@jwt_required()
def booking_history_export_status(task_id):
    task = _owned_export_task(task_id, int(get_jwt_identity()))
    if not task:
        return jsonify({"message": "Export task not found"}), 404
    response = {"task_id": task.id, "status": task.state.lower()}
    if task.successful():
        response["download_url"] = f"/api/user/booking-history/export/{task.id}/download"
    elif task.failed():
        response["message"] = "Export failed. Please try again."
    return jsonify(response), 200


@user_bp.get("/booking-history/export/<task_id>/download")
@jwt_required()
def download_booking_history_export(task_id):
    task = _owned_export_task(task_id, int(get_jwt_identity()))
    if not task:
        return jsonify({"message": "Export task not found"}), 404
    if not task.successful():
        return jsonify({"message": "Export is not ready yet"}), 409
    result = task.result or {}
    if str(result.get("user_id")) != str(get_jwt_identity()) or not result.get("filename"):
        return jsonify({"message": "Export is unavailable"}), 404
    from flask import current_app
    return send_from_directory(
        current_app.config["EXPORT_DIRECTORY"], result["filename"], as_attachment=True
    )


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
def booking_history_controller():
    user_id = get_jwt_identity()

    response = booking_history(user_id)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]

    # Enrich each booking with trek details (name, dates)
    enriched = []
    for booking in response:
        d = booking.to_dict()
        trek = booking.trek
        if trek:
            d["trek_name"] = trek.name
            d["trek_start_date"] = trek.start_date.isoformat() if trek.start_date else None
            d["trek_end_date"] = trek.end_date.isoformat() if trek.end_date else None
            d["trek_location"] = trek.location
        else:
            d["trek_name"] = None
            d["trek_start_date"] = None
            d["trek_end_date"] = None
            d["trek_location"] = None
        enriched.append(d)

    return jsonify(enriched), 200
