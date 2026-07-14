"""Public API endpoints – no authentication required."""
from flask import Blueprint, jsonify, request
from backend.models import Trek, User, Role, Booking, BookingStatus
from backend.models.trek import Status
import json, os

public_bp = Blueprint("public", __name__, url_prefix="/api/public")

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "site_settings.json")

def _read_settings():
    """Read site settings from JSON file, return defaults if missing."""
    defaults = {
        "show_stats": True,
        "about_us": "TrekFlow is India's premier trekking management platform. We connect trekkers with professional trek leaders for safe, memorable adventures across the Himalayas and beyond.",
        "how_it_works": [
            {"step": 1, "title": "Browse Treks", "desc": "Explore our curated collection of treks across India."},
            {"step": 2, "title": "Book & Pay", "desc": "Reserve your spot with our simple booking system."},
            {"step": 3, "title": "Trek & Conquer", "desc": "Join your group, follow your trek leader, and summit!"}
        ],
        "contact_email": "hello@trekflow.in",
        "contact_phone": "+91 98765 43210",
        "contact_address": "TrekFlow HQ, Manali, Himachal Pradesh, India"
    }
    if not os.path.exists(SETTINGS_FILE):
        return defaults
    try:
        with open(SETTINGS_FILE, "r") as f:
            stored = json.load(f)
        # merge with defaults so new keys are always present
        for k, v in defaults.items():
            if k not in stored:
                stored[k] = v
        return stored
    except Exception:
        return defaults


def _write_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


@public_bp.get("/stats")
def public_stats():
    """Return homepage statistics – no auth needed."""
    settings = _read_settings()
    treks_available = Trek.query.filter(Trek.status == Status.Open).count()
    total_trekkers = User.query.filter(User.role == Role.Trekker).count()
    treks_completed = Trek.query.filter(Trek.status == Status.Completed).count()
    total_bookings = Booking.query.filter(Booking.booking_status == BookingStatus.Booked).count()

    return jsonify({
        "treks_available": treks_available,
        "total_trekkers": total_trekkers,
        "treks_completed": treks_completed,
        "total_bookings": total_bookings,
        "show_stats": settings.get("show_stats", True),
    }), 200


@public_bp.get("/site-settings")
def get_site_settings():
    """Return all site settings for the homepage."""
    return jsonify(_read_settings()), 200
