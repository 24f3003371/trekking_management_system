from datetime import datetime
from backend import db
from backend.models import User, Role, TrekStaff, Trek, BookingStatus, Booking, PaymentStatus


def book_trek(user_id, trek_id, payment_status: PaymentStatus):
    user = User.query.get(user_id)
    if not user:
        return {"message": "user does not exist"}, 404
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message": "Trek does not exists"}, 404

    existing_booking = Booking.query.filter_by(user_id=user_id, trek_id=trek_id, booking_status=BookingStatus.Booked).first()
    if existing_booking:
        return {"message": "Trek already booked"}, 409
    if trek.available_slot <= 0:
        return {"message": "No available Slot"}, 400

    if payment_status == PaymentStatus.Paid:
        booking = Booking(user_id=user_id, trek_id=trek_id, booking_status=BookingStatus.Booked, payment_status=payment_status)
        trek.available_slot -= 1
    elif payment_status == PaymentStatus.Pending:
        booking = Booking(user_id=user_id, trek_id=trek_id, booking_status=BookingStatus.Pending, payment_status=payment_status)
    else:
        booking = Booking(user_id=user_id, trek_id=trek_id, booking_status=BookingStatus.Cancelled, payment_status=payment_status)

    db.session.add(booking)
    db.session.commit()
    return {"message": booking.booking_status.value, "booking": booking.to_dict()}


def edit_profile(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404
    if "username" in data: user.username = data["username"]
    if "firstname" in data: user.firstname = data["firstname"]
    if "lastname" in data: user.lastname = data["lastname"]
    if "email" in data:
        existing = User.query.filter(User.email == data["email"], User.id != user_id).first()
        if existing:
            return {"message": "Email already exists"}, 400
        user.email = data["email"]
    if "phone" in data: user.phone = data["phone"]
    if "address" in data: user.address = data["address"]
    if "gender" in data: user.gender = data["gender"]
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return {"message": "Profile updated successfully", "user": user.to_dict()}, 200


def trekking_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404
    return Booking.query.filter(Booking.user_id == user_id, Booking.booking_status == BookingStatus.Completed).all()


def available_trek():
    return Trek.query.filter(Trek.available_slot > 0).all()


def booking_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404
    return Booking.query.filter_by(user_id=user_id).all()