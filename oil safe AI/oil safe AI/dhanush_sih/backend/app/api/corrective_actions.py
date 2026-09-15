from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import CorrectiveAction
from app.schemas.schemas import CorrectiveActionCreate, CorrectiveActionUpdate

router = APIRouter(prefix="/corrective-actions", tags=["Corrective Actions"])

@router.get("")
def get_corrective_actions(
    status: Optional[str] = None,
    department: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CorrectiveAction)
    if status:
        query = query.filter(CorrectiveAction.status == status)
    if department:
        query = query.filter(CorrectiveAction.department.ilike(f"%{department}%"))
    if priority:
        query = query.filter(CorrectiveAction.priority == priority)
    return query.order_by(CorrectiveAction.id.desc()).all()

@router.post("")
def create_corrective_action(data: CorrectiveActionCreate, db: Session = Depends(get_db)):
    count = db.query(CorrectiveAction).count() + 1
    code = f"ACT-2024-0901-{count:02d}"
    action = CorrectiveAction(
        action_code=code,
        incident_id=data.incident_id,
        description=data.description,
        owner=data.owner,
        department=data.department,
        priority=data.priority,
        due_date=data.due_date,
        status=data.status,
        evidence=data.evidence
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

@router.patch("/{action_id}")
def update_corrective_action(action_id: int, data: CorrectiveActionUpdate, db: Session = Depends(get_db)):
    action = db.query(CorrectiveAction).filter(CorrectiveAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Corrective action not found")
    
    if data.status is not None:
        action.status = data.status
    if data.owner is not None:
        action.owner = data.owner
    if data.due_date is not None:
        action.due_date = data.due_date
    if data.evidence is not None:
        action.evidence = data.evidence
    if data.completion_date is not None:
        action.completion_date = data.completion_date

    db.commit()
    db.refresh(action)
    return action
