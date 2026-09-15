import os
import io
import csv
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Incident, User, RiskScore, RiskFactor, SIFClassification, LSRViolation, Hazard, RootCause, CorrectiveAction, Notification
from app.schemas.schemas import IncidentCreate, IncidentResponse
from app.ml.deberta_pipeline import deberta_pipeline
from app.ml.sif_classifier import sif_classifier
from app.ml.lsr_detector import lsr_detector
from app.ml.risk_scorer import risk_scoring_engine
from app.ml.rca_engine import rca_engine

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentResponse])
def get_incidents(
    location: Optional[str] = None,
    department: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Incident)
    if location:
        query = query.filter(Incident.location.ilike(f"%{location}%"))
    if department:
        query = query.filter(Incident.department.ilike(f"%{department}%"))
    if severity:
        query = query.filter(Incident.severity == severity)
    return query.order_by(Incident.id.desc()).all()

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident_by_id(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.post("", response_model=IncidentResponse)
def create_incident(data: IncidentCreate, db: Session = Depends(get_db)):
    # Generate incident number
    count = db.query(Incident).count() + 1
    incident_number = f"INC-{data.date.replace('-', '')}-{count:03d}"

    incident = Incident(
        incident_number=incident_number,
        title=data.title,
        date=data.date,
        time=data.time or "12:00",
        location=data.location,
        department=data.department,
        asset=data.asset,
        report_type=data.report_type,
        severity=data.severity or "HIGH",
        description=data.description,
        equipment_condition=data.equipment_condition,
        ppe_condition=data.ppe_condition,
        environmental_conditions=data.environmental_conditions,
        witness_info=data.witness_info,
        immediate_actions=data.immediate_actions,
        status="ANALYZED"
    )
    db.add(incident)
    db.flush()

    # Automatically trigger NLP & ML analysis pipeline
    nlp_out = deberta_pipeline.classify_narrative(incident.description)
    sif_res = sif_classifier.evaluate(incident.description, incident.equipment_condition or "", incident.immediate_actions or "")
    lsr_res = lsr_detector.detect_violations(incident.description, incident.ppe_condition or "", incident.equipment_condition or "")
    risk_res = risk_scoring_engine.calculate_score(
        narrative=incident.description,
        lsr_violations=lsr_res,
        sif_result=sif_res,
        equipment_condition=incident.equipment_condition or "",
        ppe_condition=incident.ppe_condition or "",
        immediate_actions=incident.immediate_actions or ""
    )
    rca_res = rca_engine.generate_rca(incident.description, lsr_res, nlp_out["hazards"])

    # Persist Risk Score & Factors
    risk_score_obj = RiskScore(
        incident_id=incident.id,
        base_score=risk_res["base_score"],
        final_score=risk_res["final_score"],
        risk_level=risk_res["risk_level"],
        confidence=risk_res["confidence"],
        calculation_log=risk_res
    )
    db.add(risk_score_obj)
    db.flush()

    for factor in risk_res["factors"]:
        db.add(RiskFactor(
            risk_score_id=risk_score_obj.id,
            factor_name=factor["factor_name"],
            contribution=factor["contribution"],
            factor_type=factor["factor_type"],
            description=factor["description"],
            evidence_snippet=factor["evidence_snippet"]
        ))

    # Persist SIF
    db.add(SIFClassification(
        incident_id=incident.id,
        is_sif_precursor=sif_res["is_sif_precursor"],
        category=sif_res["category"],
        confidence=sif_res["confidence"],
        severity=sif_res["severity"],
        potential_severity=sif_res["potential_severity"],
        energy_source=sif_res["energy_source"],
        rationale=sif_res["rationale"]
    ))

    # Persist LSR Violations
    for l in lsr_res:
        db.add(LSRViolation(
            incident_id=incident.id,
            rule_code=l["rule_code"],
            rule_name=l["rule_name"],
            is_violated=l["is_violated"],
            severity=l["severity"],
            evidence=l["evidence"],
            rationale=l["rationale"],
            mitigation_action=l["mitigation_action"]
        ))

    # Persist Hazards
    for h in nlp_out["hazards"]:
        db.add(Hazard(
            incident_id=incident.id,
            name=h["name"],
            hazard_type=h["hazard_type"],
            severity=h["severity"],
            source=h.get("source", ""),
            mitigation=h.get("mitigation", "")
        ))

    # Persist RCA
    db.add(RootCause(
        incident_id=incident.id,
        immediate_cause=rca_res["immediate_cause"],
        contributing_causes=rca_res["contributing_causes"],
        system_causes=rca_res["system_causes"],
        rca_tree_json=rca_res["rca_tree"]
    ))

    # If critical risk >= 81, create emergency notification
    if risk_res["final_score"] >= 81.0:
        incident.severity = "CRITICAL"
        db.add(Notification(
            recipient_role="Rescue Team",
            title=f"🚨 CRITICAL SAFETY EVENT — {incident.location}",
            message=f"Risk Score: {risk_res['final_score']}/100. High-energy hazard breach detected with active personnel exposure.",
            priority="CRITICAL",
            incident_id=incident.id,
            channel="IN_APP"
        ))

    db.commit()
    db.refresh(incident)
    return incident

@router.post("/upload")
async def upload_incident_file(
    file: UploadFile = File(...),
    location: str = Form("Refinery Unit-3, Crude Oil Distillation Tower"),
    department: str = Form("Crude Distillation"),
    asset: str = Form("Flanged Joint Connection FJ-302"),
    db: Session = Depends(get_db)
):
    filename = file.filename.lower()
    contents = await file.read()
    extracted_text = ""

    if filename.endswith(".txt"):
        extracted_text = contents.decode("utf-8", errors="ignore")
    elif filename.endswith(".csv"):
        text_stream = io.StringIO(contents.decode("utf-8", errors="ignore"))
        reader = csv.reader(text_stream)
        rows = [", ".join(row) for row in reader]
        extracted_text = "\n".join(rows)
    elif filename.endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                pages_text = [page.extract_text() or "" for page in pdf.pages]
                extracted_text = "\n".join(pages_text)
        except Exception:
            extracted_text = contents.decode("utf-8", errors="ignore")
    else:
        # Fallback raw decode
        extracted_text = contents.decode("utf-8", errors="ignore")

    if not extracted_text.strip():
        extracted_text = "No extractable text found in uploaded document."

    # Create incident from extracted document text
    incident_create = IncidentCreate(
        title=f"Incident Analysis from Document: {file.filename}",
        date="2024-09-01",
        time="14:30",
        location=location,
        department=department,
        asset=asset,
        report_type="Unsafe-Act + Unsafe-Condition",
        severity="HIGH",
        description=extracted_text,
        equipment_condition="Extracted from document attachments.",
        ppe_condition="Extracted from document attachments.",
        environmental_conditions="Operational process unit environment.",
        immediate_actions="Emergency procedures verified."
    )

    created_incident = create_incident(incident_create, db)
    return {
        "message": "File processed and analyzed successfully",
        "incident_id": created_incident.id,
        "incident_number": created_incident.incident_number,
        "extracted_snippet": extracted_text[:300] + ("..." if len(extracted_text) > 300 else "")
    }
