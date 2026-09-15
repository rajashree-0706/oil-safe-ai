from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Asset

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("")
def get_assets(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    assets = db.query(Asset).all()
    results = []
    for a in assets:
        results.append({
            "id": a.id,
            "name": a.name,
            "code": a.code,
            "asset_type": a.asset_type,
            "location": a.location,
            "department": a.department,
            "risk_score": a.risk_score,
            "risk_level": "CRITICAL" if a.risk_score >= 81 else ("HIGH" if a.risk_score >= 60 else "LOW"),
            "incident_count": a.incident_count,
            "sif_count": a.sif_count,
            "status": a.status,
            "last_inspected": a.last_inspected
        })
    return results

@router.get("/{asset_id}")
def get_asset_by_id(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
