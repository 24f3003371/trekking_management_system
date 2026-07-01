from enum import Enum
from datetime import datetime
form werkzeug.security import generate_password_hash , check_password_hash
from backend import db 

class Gender(Enum):
    Male="male"
    Female="female"
    Other="other"
    Prefer_not_to_say="prefer_not_to_say"

class Role(Enum):
    Admin="admin"
    Staff="staff"
    Trekker="trekker"
    
class User(db.Model,):
    __tablename__="user"

    id =db.Column(db.Integer,primary_key=True)
    username=db.Colum(db.String(100),nullable=False)
    firstname=db.Column(db.String(30))
    lastname=db.Column(db.String(20))
    pass_hash=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(320),nullable=False,unique=True)
    address=db.Column(db.String(300))
    phone=db.Column(db.String(15))
    gender=db.Column(db.Enum(Gender))
    is_active=db.Column(db.Boolean,default=True , nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    role=db.Column(db.Enum(Role),nullable=False,default=Role.Trekker)


# methods 
def set_password(self,password):
    self.password_hash=generate_password_hash(password)

def check_password(self,password):
    return check_password_hash(self.password_hash,password)

def is_admin(self):
    return  self.role==Role.Admin

def is_staff(self):
    return self.role==Role.Staff

def is_trekker(self):
    return self.role==Role.Trekker

