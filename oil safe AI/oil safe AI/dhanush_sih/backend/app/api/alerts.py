from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Notification
from app.schemas.schemas import NotificationItem

router = APIRouter(prefix="/notifications", tags=["Alerts & Notifications"])

@router.get("", response_model=List[NotificationItem])
def get_notifications(
    role: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Notification)
    if role:
        query = query.filter(Notification.recipient_role.in_([role, "All", "Rescue Team"]))
    if priority:
        query = query.filter(Notification.priority == priority)
    return query.order_by(Notification.id.desc()).all()

@router.patch("/{notification_id}/read")
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    return {"message": "Notification marked as read", "id": notification_id}
