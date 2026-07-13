from celery import Celery
from celery.schedules import crontab

from backend import create_app


flask_app = create_app()


def make_celery(app):
    celery = Celery(
        "trekflow",
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
        include=[
            "backend.celery_tasks.daily_reminder",
            "backend.celery_tasks.monthly_reports",
            "backend.celery_tasks.export_history",
        ],
    )
    celery.conf.update(
        timezone=app.config["CELERY_TIMEZONE"],
        enable_utc=False,
        task_track_started=True,
        beat_schedule={
            "daily-trek-reminders": {
                "task": "backend.celery_tasks.daily_reminder.send_daily_reminders",
                "schedule": crontab(hour=9, minute=0),
            },
            "monthly-admin-report": {
                "task": "backend.celery_tasks.monthly_reports.send_monthly_report",
                "schedule": crontab(day_of_month=1, hour=8, minute=0),
            },
        },
    )

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask
    return celery


celery = make_celery(flask_app)
