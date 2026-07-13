import os
import sqlite3

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


def ensure_trek_route_column():
    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if not database_uri.endswith("trekking.sqlite3"):
        return

    database_path = os.path.join(app.instance_path, "trekking.sqlite3")
    if not os.path.exists(database_path):
        return

    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(trek)")
        columns = {row[1] for row in cursor.fetchall()}
        if "route" not in columns:
            cursor.execute("ALTER TABLE trek ADD COLUMN route TEXT")
            connection.commit()
    finally:
        connection.close()


def ensure_trek_extra_columns():
    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if not database_uri.endswith("trekking.sqlite3"):
        return

    database_path = os.path.join(app.instance_path, "trekking.sqlite3")
    if not os.path.exists(database_path):
        return

    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(trek)")
        columns = {row[1] for row in cursor.fetchall()}
        if "major_stops" not in columns:
            cursor.execute("ALTER TABLE trek ADD COLUMN major_stops TEXT")
        if "trek_tags" not in columns:
            cursor.execute("ALTER TABLE trek ADD COLUMN trek_tags TEXT")
        if "price" not in columns:
            cursor.execute("ALTER TABLE trek ADD COLUMN price REAL DEFAULT 0")
        connection.commit()
    finally:
        connection.close()


app = create_app()

with app.app_context():
    db.create_all()
    ensure_trek_route_column()
    ensure_trek_extra_columns()
    default_admin()