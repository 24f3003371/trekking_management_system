from datetime import datetime
from backend import db
from backend.models import User, Role, TrekStaff, Trek, BookingStatus, Booking, Difficulty, Status


def _parse_date(value):
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    return value


def create_trek(data):
    existing_trek = Trek.query.filter_by(
        name=data['name'], start_date=_parse_date(data["start_date"]), location=data['location']
    ).first()
    if existing_trek:
        return {"message": "trek already exists"}, 409

    trek = Trek(
        name=data["name"], location=data["location"], description=data.get("description"),
        difficulty=Difficulty(data["difficulty"]), duration=data["duration"],
        available_slot=data["available_slot"], status=Status(data.get("status", "open")),
        start_date=_parse_date(data["start_date"]), end_date=_parse_date(data["end_date"]),
        staff_id=data["staff_id"],
    )
    db.session.add(trek)
    db.session.commit()
    return {"message": "trek created successfully", "trek": trek.to_dict()}, 201


def update_trek(trek_id, data):
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return {"message": "trek not found"}, 404

    trek.name = data.get("name", trek.name)
    trek.location = data.get("location", trek.location)
    trek.description = data.get("description", trek.description)
    trek.difficulty = Difficulty(data["difficulty"]) if "difficulty" in data else trek.difficulty
    trek.duration = data.get("duration", trek.duration)
    trek.available_slot = data.get("available_slot", trek.available_slot)
    trek.status = Status(data["status"]) if "status" in data else trek.status
    trek.start_date = _parse_date(data["start_date"]) if "start_date" in data else trek.start_date
    trek.end_date = _parse_date(data["end_date"]) if "end_date" in data else trek.end_date
    trek.staff_id = data.get("staff_id", trek.staff_id)

    db.session.commit()
    return {"message": "trek updated successfully", "trek": trek.to_dict()}, 200


def delete_trek(trek_id):
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return {"message": "trek not found"}, 404
    db.session.delete(trek)
    db.session.commit()
    return {"message": "trek deleted successfully"}, 200


def all_trek():
    return Trek.query.all()


def trek_by_id(trek_id):
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return {"message": "trek not found"}, 404
    return trek


def admin_manage_trek_routes():
    return Trek.query.all()


def participant_list(trek_id):
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return {"message": "trek not found"}, 404
    return Booking.query.filter_by(trek_id=trek_id, booking_status=BookingStatus.Booked).all()


def manage_participant_list(booking_id, status):
    booking = Booking.query.filter_by(id=booking_id).first()
    if not booking:
        return {"message": "booking not found"}, 404
    booking.booking_status = BookingStatus(status)
    db.session.commit()
    return {"message": "participant status updated successfully"}, 200


def mark_trek(trek_id):
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return {"message": "trek not found"}, 404
    trek.status = Status.Completed
    for booking in Booking.query.filter_by(trek_id=trek_id, booking_status=BookingStatus.Booked).all():
        booking.booking_status = BookingStatus.Completed
    db.session.commit()
    return {"message": "trek marked as completed"}, 200


