from backend import db 
from backend.models import User,Role,TrekStaff,Trek,BookingStatus,Booking

def create_trek(data):
    existing_trek=Trek.query.filter(name=data['name'],start_date=data["start_date"],location=data['location']).first()
    if existing_trek:
        return {"message":"trek already exists"},404
    trek=Trek(name=data['name'],start_date=data['start_date'],end_date=data['end_date'],location=data['location'],description=data['description'],difficulty=data['difficulty'])
    
def update_trek():
def delete_trek():

def all_trek():

def trek_by_id():

def admin_manage_trek_routes():

def participant_list():

def manage_participant_list():

def mark_trek():

