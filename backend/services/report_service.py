from collections import Counter
from datetime import date

from backend.models import Booking, BookingStatus, Status, Trek


def previous_month_range(today=None):
    today = today or date.today()
    first_this_month = today.replace(day=1)
    last_previous_month = first_this_month.fromordinal(first_this_month.toordinal() - 1)
    return last_previous_month.replace(day=1), last_previous_month


def monthly_activity_summary(start_date, end_date):
    completed_treks = Trek.query.filter(
        Trek.status == Status.Completed,
        Trek.end_date.between(start_date, end_date),
    ).count()
    bookings = Booking.query.join(Trek).filter(
        Booking.booking_status.in_([BookingStatus.Booked, BookingStatus.Completed]),
        Trek.start_date.between(start_date, end_date),
    ).all()
    popular = Counter(booking.trek.name for booking in bookings if booking.trek)
    return {
        "treks_conducted": completed_treks,
        "users_participated": len({booking.user_id for booking in bookings}),
        "popular_treks": popular.most_common(5),
    }


def render_monthly_report_html(summary, start_date, end_date):
    popular_rows = "".join(
        f"<li>{name}: {count} booking(s)</li>" for name, count in summary["popular_treks"]
    ) or "<li>No trek bookings in this period.</li>"
    return f"""
    <h2>TrekFlow Monthly Activity Report</h2>
    <p>Period: {start_date.isoformat()} to {end_date.isoformat()}</p>
    <ul>
      <li>Treks conducted: {summary['treks_conducted']}</li>
      <li>Users participated: {summary['users_participated']}</li>
    </ul>
    <h3>Popular treks</h3><ol>{popular_rows}</ol>
    """
