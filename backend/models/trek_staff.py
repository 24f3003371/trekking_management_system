from backend import db 
from datetime import datetime
class TrekStaff(db.Model):
    __tablename__="trekstaff"
    id =db.Column(db.Integer,primary_key=True)
    trek_id=db.Column(db.Integer,db.ForeignKey("trek.id"),nullable=False)
    staff_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    assigned_at=db.Column(db.DateTime,default=datetime.utcnow())
    assigned_by=db.Column(db.Integer,db.ForeingKey("user.id"),nullable=False)
    trek=db.relationship("Trek",back_populates="user")
    staff=db.relationship("User",back_populates="trek",foreign_keys=[staff_id])