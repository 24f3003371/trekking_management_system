import json
from datetime import datetime
from backend import db
from backend.models import User, Role, TrekStaff, Trek, BookingStatus, Booking, Difficulty, Status


def _parse_date(value):
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    return value


def _pick(data, *keys, default=None):
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return default


def _enum_text(value):
    if value is None:
        return None
    return str(value).strip().lower()


def _normalize_list(value):
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except ValueError:
                pass
        return [item.strip() for item in stripped.split(",") if item.strip()]
    return [str(value).strip()]


def _calculate_duration(start_date, end_date):
    if not start_date or not end_date:
        return None
    return max((end_date - start_date).days + 1, 1)


def create_trek(data):
    available_slot = _pick(data, "available_slot", "availableSlots", "slots")
    staff_id = _pick(data, "staff_id", "staffId", "assignedStaffId")
    start_date = _parse_date(_pick(data, "start_date", "startDate"))
    end_date = _parse_date(_pick(data, "end_date", "endDate"))
    duration = _pick(data, "duration")
    if duration in (None, ""):
        duration = _calculate_duration(start_date, end_date)
    price = _pick(data, "price", "pricePerPerson", default=0)
    existing_trek = Trek.query.filter_by(
        name=data['name'], start_date=start_date, location=data['location']
    ).first()
    if existing_trek:
        return {"message": "trek already exists"}, 409

    if not duration:
        return {"message": "Duration must be at least 1 day"}, 400

    trek = Trek(
        name=data["name"], location=data["location"], description=data.get("description"),
        route=data.get("route"),
        major_stops=json.dumps(_normalize_list(_pick(data, "major_stops", "majorStops", "stops"))),
        trek_tags=json.dumps(_normalize_list(_pick(data, "trek_tags", "trekTags", "tags"))),
        price=float(price or 0),
        difficulty=Difficulty(_enum_text(data["difficulty"])), duration=int(duration),
        available_slot=int(available_slot), status=Status(_enum_text(data.get("status", "open"))),
        start_date=start_date,
        end_date=end_date,
        staff_id=int(staff_id),
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
    trek.route = data.get("route", trek.route)
    if "major_stops" in data or "majorStops" in data or "stops" in data:
        trek.major_stops = json.dumps(_normalize_list(_pick(data, "major_stops", "majorStops", "stops")))
    if "trek_tags" in data or "trekTags" in data or "tags" in data:
        trek.trek_tags = json.dumps(_normalize_list(_pick(data, "trek_tags", "trekTags", "tags")))
    if "price" in data or "pricePerPerson" in data:
        trek.price = float(_pick(data, "price", "pricePerPerson", default=trek.price) or 0)
    trek.difficulty = Difficulty(_enum_text(data["difficulty"])) if "difficulty" in data else trek.difficulty
    start_date = _parse_date(data["start_date"] if "start_date" in data else data["startDate"]) if ("start_date" in data or "startDate" in data) else trek.start_date
    end_date = _parse_date(data["end_date"] if "end_date" in data else data["endDate"]) if ("end_date" in data or "endDate" in data) else trek.end_date
    trek.start_date = start_date
    trek.end_date = end_date
    duration = data.get("duration")
    if duration in (None, ""):
        duration = _calculate_duration(start_date, end_date) or trek.duration
    trek.duration = int(duration)
    trek.available_slot = int(data.get("available_slot", data.get("availableSlots", trek.available_slot)))
    trek.status = Status(_enum_text(data["status"])) if "status" in data else trek.status
    trek.staff_id = int(data.get("staff_id", data.get("staffId", data.get("assignedStaffId", trek.staff_id))))

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


