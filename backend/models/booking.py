from backend import db 
from enum import Enum
from datetime import datetime
class BookingStatus(Enum):
    Booked="booked"
    Cancelled="cancelled"
    Pending="pending"

class PaymentStatus(Enum):
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
    payment_status=db.Column(db.Enum(PaymentStatus),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    update_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    trek=db.relationship("Trek",back_populates="booking")
    user=db.relationship("User",back_populates="booking")
    def __repr__(self) -> str:
            return f"Booking {self.id}"
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trek_id": self.trek_id,
            "booking_status": self.booking_status.value if self.booking_status else None,
            "booking_date": self.booking_date.isoformat() if self.booking_date else None,
            "payment_status": self.payment_status.value if self.payment_status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
