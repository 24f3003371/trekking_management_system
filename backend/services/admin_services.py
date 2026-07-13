from backend import db
from backend.models import User, Role, Trek, Booking, BookingStatus, TrekStaff


def admin_dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter(User.role == Role.Trekker).count()
    total_staff = User.query.filter(User.role == Role.Staff).count()
    total_bookings = Booking.query.filter(Booking.booking_status == BookingStatus.Booked).count()
    return {"total_treks": total_treks, "total_users": total_users, "total_staff": total_staff, "total_bookings": total_bookings}


def create_staff(data):
    existing_user = User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first()
    if existing_user:
        return {"message": "username or email already exists"}, 400
    staff = User(username=data["username"], email=data["email"], phone=data.get("phone"), role=Role.Staff)
    staff.set_password(data["password"])
    db.session.add(staff)
    db.session.commit()
    return {"message": "staff created successfully", "staff": staff.to_dict()}, 201


def assign_trek(staff_id, trek_id):
    staff = User.query.filter_by(id=staff_id, role=Role.Staff).first()
    if not staff:
        return {"message": "staff doesn't exists"}, 404
    trek = Trek.query.filter_by(id=trek_id).first()
    if not trek:
        return {"message": "trek doesn't exists"}, 404
    trek.staff_id = staff_id
    db.session.commit()
    return {"message": "Trek assigned successfully"}, 200


def remove_staff_from_trek(trek_id, staff_id):
    existing_user = User.query.filter_by(id=staff_id).first()
    if not existing_user:
        return {"message": "staff does not exists"}, 404
    existing_trek = Trek.query.filter_by(id=trek_id).first()
    if not existing_trek:
        return {"message": "trek does not exists"}, 404
    assignment = TrekStaff.query.filter_by(trek_id=trek_id, staff_id=staff_id).first()
    if not assignment:
        return {"message": "the staff is not assigned to this trek"}, 404
    db.session.delete(assignment)
    db.session.commit()
    return {"message": "staff removed successfully from the trek"}, 200


def all_staff():
    return User.query.filter(User.role == Role.Staff).all()


def search_users(keyword):
    query = User.query.filter(User.role == Role.Trekker)
    if keyword:
        user = query.filter((User.username.ilike(f"%{keyword}%")) | (User.email.ilike(f"%{keyword}%"))).all()
    else:
        user = query.all()
    if not user:
        return {"message": "user does not exist"}, 404
    return user


def search_staff(keyword):
    staff = User.query.filter((User.username == keyword) | (User.email.ilike(f"%{keyword}%")), User.role == Role.Staff).all()
    if not staff:
        return {"message": "staff does not exist"}, 404
    return staff


def search_treks(keyword):
    trek = Trek.query.filter(
        (Trek.name.ilike(f"%{keyword}%")) | (Trek.description.ilike(f"%{keyword}%")) | (Trek.location.ilike(f"%{keyword}%"))
    ).all()
    if not trek:
        return {"message": "trek does not exists"}, 404
    return trek


def blacklist_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return {"message": "user does not exists"}, 404
    user.is_active = False
    db.session.commit()
    return {"message": "user is blacklisted"}, 200


def unblacklist_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return {"message": "user does not exists"}, 404
    user.is_active = True
    db.session.commit()
    return {"message": "user is unblacklisted"}, 200