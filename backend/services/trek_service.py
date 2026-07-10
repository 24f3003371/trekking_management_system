from backend import db 
from backend.models import User,Role,TrekStaff,Trek,BookingStatus,Booking

def create_trek(data):
    existing_trek=Trek.query.filter(name=data['name'],start_date=data["start_date"],location=data['location']).first()
    if existing_trek:
        return {"message":"trek already exists"},404
    trek = Trek(
        name=data["name"],
        location=data["location"],
        description=data["description"],
        difficulty=data["difficulty"],
        duration=data["duration"],
        available_slot=data["available_slot"],
        status=data["status"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        staff_id=data["staff_id"]
    )

    db.session.add(trek)
    db.session.commit()

    return {"message": "trek created successfully"}, 201
    
def update_trek():
    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return {"message": "trek not found"}, 404

    trek.name = data.get("name", trek.name)
    trek.location = data.get("location", trek.location)
    trek.description = data.get("description", trek.description)
    trek.difficulty = data.get("difficulty", trek.difficulty)
    trek.duration = data.get("duration", trek.duration)
    trek.available_slot = data.get("available_slot", trek.available_slot)
    trek.status = data.get("status", trek.status)
    trek.start_date = data.get("start_date", trek.start_date)
    trek.end_date = data.get("end_date", trek.end_date)
    trek.staff_id = data.get("staff_id", trek.staff_id)

    db.session.commit()

    return {"message": "trek updated successfully"}, 200

def delete_trek():
    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return {"message": "trek not found"}, 404

    db.session.delete(trek)
    db.session.commit()

    return {"message": "trek deleted successfully"}, 200


def all_trek():
    return Trek.query.all()

def trek_by_id():
    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return {"message": "trek not found"}, 404

    return trek

def admin_manage_trek_routes():
    return Trek.query.all()


def participant_list():
    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return {"message": "trek not found"}, 404

    participants = Booking.query.filter_by(
        trek_id=trek_id,
        booking_status=BookingStatus.Booked
    ).all()

    return participants



def manage_participant_list():
    booking = Booking.query.filter_by(id=booking_id).first()

    if not booking:
        return {"message": "booking not found"}, 404

    booking.booking_status = status

    db.session.commit()

    return {"message": "participant status updated successfully"}, 200

def mark_trek():
    trek = Trek.query.filter_by(id=trek_id).first()

    if not trek:
        return {"message": "trek not found"}, 404

    trek.status = "Completed"

    completed_bookings = Booking.query.filter_by(
        trek_id=trek_id,
        booking_status=BookingStatus.Booked
    ).all()

    for booking in completed_bookings:
        booking.booking_status = BookingStatus.Completed


