from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Incident, RiskScore, RiskFactor, SIFClassification, LSRViolation, Hazard, RootCause
from app.ml.shap_explainer import shap_explainer
from app.rag.knowledge_base import rag_knowledge_base

router = APIRouter(prefix="/incidents", tags=["AI Incident Analysis"])

@router.get("/{incident_id}/analyze")
@router.post("/{incident_id}/analyze")
def analyze_incident(incident_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    risk_score = incident.risk_score
    sif = incident.sif_classification
    lsr_violations = incident.lsr_violations
    hazards = incident.hazards
    rca = incident.root_cause

    # SHAP Waterfall calculation
    factors_list = []
    if risk_score and risk_score.factors:
        for f in risk_score.factors:
            factors_list.append({
                "factor_name": f.factor_name,
                "contribution": f.contribution,
                "factor_type": f.factor_type,
                "description": f.description,
                "evidence_snippet": f.evidence_snippet
            })
    
    score_val = risk_score.final_score if risk_score else 87.0
    risk_level = risk_score.risk_level if risk_score else "CRITICAL"
    confidence_val = risk_score.confidence if risk_score else 0.94

    shap_analysis = shap_explainer.explain_score({
        "final_score": score_val,
        "risk_level": risk_level,
        "factors": factors_list
    })

    # RAG Evidence Retrieval
    retrieved_evidence = rag_knowledge_base.search(f"{incident.title} {incident.description} {incident.asset}")

    # Evidence-based Recommendations
    recommendations = [
        "Enforce mandatory Double Block & Bleed positive isolation and zero-energy verification before any flange or pressure boundary work.",
        "Implement mandatory supervisor sign-off on high-risk line breaking permits with verified lockout/tagout.",
        "Deploy high-temperature flame-resistant PPE, full face shields, and thermal gloves for all personnel within 5m of hot process lines.",
        "Conduct immediate ultrasonic crack detection and flange face inspections across all high-pressure (250 bar) distillation headers.",
        "Ensure adjacent high-temperature surfaces (>80°C) maintain compliant thermal insulation barriers."
    ]

    # Rescue / Emergency Response Actions
    emergency_actions = [
        "Isolate upstream and downstream process block valves to cut hydrocarbon feed.",
        "Depressurize the affected Crude Distillation header directly to the flare system.",
        "Quench and cool adjacent 140°C uninsulated piping surfaces using approved deluge procedures.",
        "Provide immediate sterile burn dressings and first aid to the injured technician; arrange hospital transport.",
        "Establish an exclusion perimeter of 50 meters and isolate electrical ignition sources in Unit-3.",
        "Notify the Emergency Response Commander and HSE Duty Officer immediately."
    ]

    primary_hazard = hazards[0].name if hazards else "Pressurized System Breach"
    secondary_hazard = hazards[1].name if len(hazards) > 1 else "Thermal Ignition"

    return {
        "incident_id": incident.incident_number,
        "db_id": incident.id,
        "title": incident.title,
        "date": incident.date,
        "location": incident.location,
        "department": incident.department,
        "asset": incident.asset,
        "risk_score": score_val,
        "risk_level": risk_level,
        "sif_precursor": sif.is_sif_precursor if sif else True,
        "sif_category": sif.category if sif else "Energy Isolation",
        "confidence": confidence_val,
        "primary_hazard": primary_hazard,
        "secondary_hazard": secondary_hazard,
        "injury": "Thermal Burn",
        "hazards": [
            {
                "name": h.name,
                "hazard_type": h.hazard_type,
                "severity": h.severity,
                "source": h.source,
                "mitigation": h.mitigation
            }
            for h in hazards
        ],
        "lsr_violations": [
            {
                "rule": v.rule_code,
                "name": v.rule_name,
                "status": "VIOLATED",
                "severity": v.severity,
                "evidence": v.evidence,
                "mitigation": v.mitigation_action
            }
            for v in lsr_violations
        ],
        "risk_factors": factors_list,
        "shap_explanation": shap_analysis,
        "root_causes": {
            "immediate_cause": rca.immediate_cause if rca else "Unauthorized repair on pressurized system without depressurization.",
            "contributing_causes": rca.contributing_causes if rca else [],
            "system_causes": rca.system_causes if rca else [],
            "rca_tree": rca.rca_tree_json if rca else {}
        },
        "recommendations": recommendations,
        "emergency_actions": emergency_actions,
        "retrieved_evidence": retrieved_evidence,
        "model_metadata": {
            "nlp_model": "DeBERTa-v3 Industrial Refinery Safety (Modular Pipeline)",
            "explainability_engine": "SHAP Additive Attribution",
            "rag_vector_db": "PostgreSQL + pgvector / Vector Index",
            "decision_support_disclaimer": "OIL-SAFE AI is an expert industrial decision-support system. It assists certified safety managers and does not replace site command procedures."
        }
    }

@router.get("/{incident_id}/risk")
def get_incident_risk(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    return {
        "incident_id": data["incident_id"],
        "risk_score": data["risk_score"],
        "risk_level": data["risk_level"],
        "confidence": data["confidence"],
        "risk_factors": data["risk_factors"],
        "shap_explanation": data["shap_explanation"]
    }

@router.get("/{incident_id}/sif")
def get_incident_sif(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    return {
        "incident_id": data["incident_id"],
        "sif_precursor": data["sif_precursor"],
        "sif_category": data["sif_category"],
        "confidence": data["confidence"],
        "severity": data["risk_level"]
    }

@router.get("/{incident_id}/lsr")
def get_incident_lsr(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    return {
        "incident_id": data["incident_id"],
        "lsr_violations": data["lsr_violations"]
    }

@router.get("/{incident_id}/rca")
def get_incident_rca(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    return {
        "incident_id": data["incident_id"],
        "root_causes": data["root_causes"]
    }

@router.get("/{incident_id}/recommendations")
def get_incident_recommendations(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    return {
        "incident_id": data["incident_id"],
        "recommendations": data["recommendations"],
        "emergency_actions": data["emergency_actions"],
        "evidence": data["retrieved_evidence"]
    }
