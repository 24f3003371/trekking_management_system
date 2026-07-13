from backend.celery_tasks.celery_app import celery
from backend.models import Role, User
from backend.services.email_service import send_email
from backend.services.report_service import (
    monthly_activity_summary,
    previous_month_range,
    render_monthly_report_html,
)


@celery.task(name="backend.celery_tasks.monthly_reports.send_monthly_report")
def send_monthly_report():
    start_date, end_date = previous_month_range()
    summary = monthly_activity_summary(start_date, end_date)
    html = render_monthly_report_html(summary, start_date, end_date)
    admins = User.query.filter_by(role=Role.Admin).all()
    sent = sum(send_email(admin.email, "TrekFlow Monthly Activity Report", html) for admin in admins)
    return {"period": f"{start_date} to {end_date}", "reports_sent": sent, **summary}
