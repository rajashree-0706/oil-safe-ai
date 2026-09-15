from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/analytics", tags=["Safety Analytics & Anomaly Detection"])

@router.get("/anomalies")
def get_safety_anomalies() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ANOM-01",
            "title": "UNIT-3 PRESSURE INCIDENTS ANOMALY",
            "location": "Unit-3 Distillation Tower",
            "metric": "Pressure System Breaches",
            "baseline": "2 / month",
            "current": "7 / month",
            "deviation": "+250%",
            "risk_level": "HIGH",
            "status": "ACTIVE_INVESTIGATION",
            "details": "Statistically significant clustering of flanged joint gasket micro-fissures detected across 250 bar lines during Q3 maintenance cycle."
        },
        {
            "id": "ANOM-02",
            "title": "NIGHT SHIFT PERMIT COMPLIANCE DEFICIT",
            "location": "Refinery Maintenance Yard",
            "metric": "LSR #3 Authorization Adherence",
            "baseline": "96% compliant",
            "current": "74% compliant",
            "deviation": "-22%",
            "risk_level": "MEDIUM",
            "status": "AUDIT_SCHEDULED",
            "details": "Elevation in emergency work orders initiated without secondary supervisor sign-off between 00:00 and 06:00."
        },
        {
            "id": "ANOM-03",
            "title": "THERMAL FLANGE EXPOSURE FREQUENCY",
            "location": "Crude Distillation Unit",
            "metric": "Uninsulated Piping Alerts",
            "baseline": "1 / quarter",
            "current": "4 / quarter",
            "deviation": "+300%",
            "risk_level": "HIGH",
            "status": "INSULATION_CREW_DISPATCHED",
            "details": "Repeated near-miss reports noting uninsulated 140°C piping in close proximity to active operator transit walkways."
        }
    ]

@router.get("/forecast")
def get_safety_forecast() -> List[Dict[str, Any]]:
    return [
        {
            "zone": "UNIT-3 DISTILLATION",
            "forecast_30d": "HIGH",
            "confidence": 0.89,
            "key_risk_driver": "Pressure Vessel Gaskets & High Thermal Gradient",
            "recommended_preventive_action": "Mandatory ultrasonic thickness testing and pre-job isolation audit before any maintenance."
        },
        {
            "zone": "MAINTENANCE YARD",
            "forecast_30d": "HIGH",
            "confidence": 0.84,
            "key_risk_driver": "Hot Work & Tool Certification Deficiencies",
            "recommended_preventive_action": "Conduct site-wide permit-to-work refresher for all contractor personnel."
        },
        {
            "zone": "TANK FARM",
            "forecast_30d": "MEDIUM",
            "confidence": 0.78,
            "key_risk_driver": "Overfill Protection Calibration",
            "recommended_preventive_action": "Quarterly automated high-level sensor trip test."
        },
        {
            "zone": "LOADING RACK",
            "forecast_30d": "LOW",
            "confidence": 0.92,
            "key_risk_driver": "Vapor Recovery System (Stable)",
            "recommended_preventive_action": "Routine weekly earthing clamp resistance inspection."
        }
    ]
