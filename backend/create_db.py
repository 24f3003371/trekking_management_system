import os

from backend import create_app, db
from backend.models import Role, User


def default_admin():
    default_admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@trekflow.com")
    default_admin_username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    default_admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

    existing_admin = User.query.filter_by(role=Role.Admin).first()
    if existing_admin:
        return

    admin = User(
        username=default_admin_username,
        email=default_admin_email,
        role=Role.Admin,
    )
    admin.set_password(default_admin_password)
    db.session.add(admin)
    db.session.commit()


app = create_app()

with app.app_context():
    db.create_all()
    default_admin()