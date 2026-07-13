from pathlib import Path

from flask import current_app

from backend.models import Booking
from backend.utils.csv_helper import booking_history_csv


def create_booking_history_export(user_id, task_id):
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()
    export_directory = Path(current_app.config["EXPORT_DIRECTORY"])
    export_directory.mkdir(parents=True, exist_ok=True)
    filename = f"booking-history-{user_id}-{task_id}.csv"
    path = export_directory / filename
    path.write_text(booking_history_csv(bookings), encoding="utf-8", newline="")
    return path
