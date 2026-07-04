from backend import db 
from .import Enum,datetime

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
    __tablename__="trek "
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text)
    difficulty=db.Column(db.Enum(Difficulty),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    available_slot=db.Column(db.Integer,nullable=False)
    status=db.Column(db.Enum(Status),nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date,nullable=False)
    staff_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
