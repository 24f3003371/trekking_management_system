from backend import db 
from backend.models import User, Role,Trek,Booking,BookingStatus,TrekStaff

#dashboard 
def admin_dashboard():
    total_treks=Trek.query.count()
    total_users=User.query.filter(User.role==Role.Trekker)
    total_staff=User.query.filter(User.role==Role.Staff)
    total_bookings=Booking.query.filter(Booking.booking_status=BookingStatus.Booked)

    return {"total_trekks":total_treks,"total_users":total_users,"total_staff":total_staff,"total_bookings":total_bookings}

#staff management

def create_staff(data):
    existing_user=User.query.filter((User.email=data["email"]) | (User.username==data["username"])).first()

    if existing_user:
        return {"message":"username or email already exists"},400

    staff=User(username=data["username"],email=data["email"],phone=data["phone"],role=Role.Staff)

    staff.set_password(data["password"])

    db.session.add(staff)
    db.session.commit()

    return {"message":"staff created successfully"},201


def assign_trek(staff_id,trek_id):
    staff=User.query.filter(user.id=staff_id,user.role=Role.Staff).first()

    if not staff:
        return {"message":"staff doesn't exists"},404

    trek=Trek.query.filter(Trek.id=trek_id).first()

    if not trek :
        return {"message":"trek doesn't exists"},404

    trek.staff_id=staff_id

    db.session.commit()

    return {"message":"Trek assigned successfully"},200


def remove_staff_from_trek(trek_id,staff_id):
    existing_user=User.query.filter(User.id==staff_id_id).first()
    if not existing_user:
        return {"message":"staff does not exists"},404
    existing_trek=Trek.query.filter(Trek.id==trek_id).first()
    if not existing_trek:
        return {"message":"trek does not exists"}
    assignment=TrekStaff.query.filter(trek_id=trek_id,staff_id=staff_id).first()
    if not assignment:
        return {"message":"the staff is not assigned to this trek"},404
    db.session.delete(assignment)
    db.session.commit()
    return {"message":"staff removed successsfully from the trek"},201
    

def all_staff():
    staff=User.query.filter(User.role=Role.Staff).all()
    return staff
#search 
def search_users(keyword):
    user=User.query.filter((user.username==keyword)|(user.email.ilike(f"%{keyword}%"))).all()

    if not user:
        return {"message":"user does not exist"},404

    return user


def search_staff(keyword):
    staff=User.query.filter((User.username==keyword)|(User.email.ilike(f"%{keyword}%"))).all()
    if not staff:
        return {"message":"staff does not exist"},404
    return staff
def search_treks(keyword):
    trek=Trek.query.filter((Trek.name==keyword)|(Trek.description==keyword)|(Trek.status==keyword)|(Trek.location==keyword)|(Trek.difficulty==keyword)).all()
    if not trek:
        return {"message":"trek does not exists"},404
    return trek

#user management 

def blacklist_user(id):
    user=User.query.filter(User.id==id).first()
    if not user:
        return {"message":"user does not exists"},404
    user.is_active=False
    db.commit()
    return {"message":"user is blacklisted"},200
    
def unblacklist_user(id):
    user=User.query.filter(User.id==id).first()
    if not user:
        return {"message":"user does not exists"},404
    user.is_active=True
    db.commit()
    return {"message":"user is unblaclisted"},200