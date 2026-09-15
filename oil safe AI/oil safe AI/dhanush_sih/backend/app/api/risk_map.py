from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Location

router = APIRouter(prefix="/risk", tags=["Refinery Risk Heatmap"])

@router.get("/heatmap")
def get_refinery_heatmap(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    locations = db.query(Location).all()
    results = []
    for loc in locations:
        results.append({
            "id": loc.id,
            "name": loc.name,
            "code": loc.code,
            "risk_score": loc.risk_score,
            "risk_level": "CRITICAL" if loc.risk_score >= 81 else ("VERY HIGH" if loc.risk_score >= 61 else ("HIGH" if loc.risk_score >= 41 else "MODERATE")),
            "incident_count": loc.incident_count,
            "sif_count": loc.sif_count,
            "top_hazards": loc.top_hazards or [],
            "open_actions_count": loc.open_actions_count,
            "coordinates": loc.coordinates_json or {"x": 50, "y": 50}
        })
    return results
