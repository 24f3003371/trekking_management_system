from backend.models import *
from backend import db
app=create_app()

with app.app_context():
    db.create_all()