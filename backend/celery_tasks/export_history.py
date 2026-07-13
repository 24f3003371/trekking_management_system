from backend.celery_tasks.celery_app import celery
from backend.services.export_service import create_booking_history_export


@celery.task(bind=True, name="backend.celery_tasks.export_history.create_booking_export")
def create_booking_export(self, user_id):
    self.update_state(state="STARTED", meta={"message": "Building CSV export"})
    path = create_booking_history_export(user_id, self.request.id)
    return {"user_id": user_id, "filename": path.name}
