import json
from backend import db 
from enum import Enum
from datetime import datetime

class Difficulty(Enum):
    Easy="easy"
    Moderate="moderate"
    Hard="hard"

class Status(Enum):
    Pending="pending"
    Approved="approved"
    Open="open"
    Closed="closed"
    Completed="completed"

class Trek (db.Model):
    __tablename__="trek"
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text)
    route=db.Column(db.Text)
    major_stops=db.Column(db.Text)
    trek_tags=db.Column(db.Text)
    price=db.Column(db.Float,nullable=False,default=0)
    difficulty=db.Column(db.Enum(Difficulty),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    available_slot=db.Column(db.Integer,nullable=False)
    status=db.Column(db.Enum(Status),nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date,nullable=False)
    staff_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    user=db.relationship("TrekStaff",back_populates="trek",cascade="all,delete-orphan")
    booking=db.relationship("Booking",back_populates="trek",cascade="all,delete-orphan")
    def __repr__(self) -> str:
            return f"Trek {self.name}"
    def to_dict(self):
        def _decode_list(value):
            if not value:
                return []
            if isinstance(value, list):
                return value
            try:
                decoded = json.loads(value)
                return decoded if isinstance(decoded, list) else []
            except (TypeError, ValueError):
                return []

        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "route": self.route,
            "major_stops": _decode_list(self.major_stops),
            "trek_tags": _decode_list(self.trek_tags),
            "price": self.price,
            "difficulty": self.difficulty.value if self.difficulty else None,
            "duration": self.duration,
            "available_slot": self.available_slot,
            "status": self.status.value if self.status else None,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "staff_id": self.staff_id,
        }
 
