from datetime import date, timedelta

from backend.celery_tasks.celery_app import celery
from backend.models import Booking, BookingStatus, Trek
from backend.services.email_service import send_email, send_google_chat_webhook


@celery.task(name="backend.celery_tasks.daily_reminder.send_daily_reminders")
def send_daily_reminders():
    today = date.today()
    cutoff = today + timedelta(days=7)
    bookings = Booking.query.join(Trek).filter(
        Booking.booking_status == BookingStatus.Booked,
        Trek.start_date.between(today, cutoff),
    ).all()
    delivered = 0
    for booking in bookings:
        trek = booking.trek
        message = (
            f"Reminder: {trek.name} starts on {trek.start_date.isoformat()} at {trek.location}. "
            "Please review your trek instructions and prepare your gear."
        )
        delivered += int(send_email(booking.user.email, "Upcoming Trek Reminder", f"<p>{message}</p>"))
        send_google_chat_webhook(message)
    return {"eligible_bookings": len(bookings), "emails_sent": delivered}
