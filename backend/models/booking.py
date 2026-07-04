from backend import db 
from . import Enum,datetime
class BookingStatus(Enum):
    Booked="booked"
    Cancelled="cancelled"
    Completed="completed"

class PaymnetStatus(Enum):
    Pending="pending"
    Paid="paid"
    Failed="failed"

class Booking(db.Model):
    __tablename__= "booking"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey("trek.id"),nullable=False)
    booking_status=db.Column(db.Enum(BookingStatus),nullable=False)
    booking_date=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    payment_status=db.Column(db.Enum(PaymnetStatus),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    update_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    
