"""
Database Seeding Script for OIL-SAFE AI.
Populates initial roles, demo users, locations, assets, departments,
and preloads the 2024-09-01 Unit-3 Crude Distillation Tower benchmark incident.
"""

import hashlib
from sqlalchemy.orm import Session
from app.database.models import (
    User, Incident, RiskScore, RiskFactor, SIFClassification,
    LSRViolation, Hazard, RootCause, Asset, Location, Department,
    CorrectiveAction, Notification, KnowledgeDocument
)
from app.rag.knowledge_base import DEFAULT_KNOWLEDGE_DOCUMENTS

def hash_password(password: str) -> str:
    salt = "oilsafe_refinery_salt_2026"
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

def seed_database(db: Session):
    # Check if already seeded with incidents
    if db.query(Incident).first():
        return

    print("Seeding OIL-SAFE AI database...")

    # 1. Seed Users (6 RBAC Roles)
    users_data = [
        {"username": "admin", "email": "admin@oil-safe.ai", "full_name": "Chief Safety Administrator", "role": "Admin", "dept": "HSE Governance", "pass": "Admin@2026"},
        {"username": "rescue_team", "email": "rescue@oil-safe.ai", "full_name": "Emergency Incident Commander", "role": "Rescue Team", "dept": "Emergency Response", "pass": "Rescue@2026"},
        {"username": "safety_manager", "email": "safety.manager@oil-safe.ai", "full_name": "Lead Process Safety Manager", "role": "Safety Manager", "dept": "Process Safety", "pass": "Safety@2026"},
        {"username": "dept_manager", "email": "dept.manager@oil-safe.ai", "full_name": "Crude Distillation Operations Head", "role": "Department Manager", "dept": "Crude Distillation", "pass": "Dept@2026"},
        {"username": "hse_division", "email": "hse@oil-safe.ai", "full_name": "Corporate HSE Executive Director", "role": "Sonaga / HSE Division", "dept": "Corporate HSE", "pass": "Hse@2026"},
        {"username": "technician", "email": "tech.field@oil-safe.ai", "full_name": "Senior Mechanical Technician", "role": "Technician", "dept": "Refinery Maintenance", "pass": "Tech@2026"}
    ]

    db_users = {}
    for u in users_data:
        user = User(
            username=u["username"],
            email=u["email"],
            hashed_password=hash_password(u["pass"]),
            full_name=u["full_name"],
            role=u["role"],
            department=u["dept"],
            is_active=True
        )
        db.add(user)
        db_users[u["username"]] = user

    db.commit()

    # 2. Seed Locations
    locations_data = [
        {"name": "Refinery Unit-3 (Crude Distillation)", "code": "LOC-U3", "risk_score": 87.0, "incidents": 4, "sif": 2, "hazards": ["High Pressure (250 bar)", "Thermal (140°C)", "Hydrocarbon Flammability"], "open_actions": 3, "coords": {"x": 45, "y": 30}},
        {"name": "Refinery Unit-1 (Hydrocracker)", "code": "LOC-U1", "risk_score": 42.0, "incidents": 2, "sif": 0, "hazards": ["Hydrogen Gas", "High Pressure"], "open_actions": 1, "coords": {"x": 20, "y": 25}},
        {"name": "Refinery Unit-2 (Fluid Catalytic Cracker)", "code": "LOC-U2", "risk_score": 58.0, "incidents": 3, "sif": 1, "hazards": ["Catalyst Dust", "High Temp Flue Gas"], "open_actions": 2, "coords": {"x": 70, "y": 25}},
        {"name": "Tank Farm & Strategic Storage", "code": "LOC-TF", "risk_score": 35.0, "incidents": 1, "sif": 0, "hazards": ["Static Electricity", "Vapor Accumulation"], "open_actions": 1, "coords": {"x": 80, "y": 70}},
        {"name": "Boiler & Steam Generation Area", "code": "LOC-BLR", "risk_score": 28.0, "incidents": 1, "sif": 0, "hazards": ["High Pressure Steam", "Thermal Pipe"], "open_actions": 0, "coords": {"x": 25, "y": 75}},
        {"name": "Central Maintenance & Workshop", "code": "LOC-MNT", "risk_score": 22.0, "incidents": 1, "sif": 0, "hazards": ["Machinery Pinch Points", "Lifting"], "open_actions": 1, "coords": {"x": 50, "y": 80}},
        {"name": "Marine & Rail Loading Terminal", "code": "LOC-TRM", "risk_score": 38.0, "incidents": 2, "sif": 0, "hazards": ["Transfer Hose Rupture", "Spill"], "open_actions": 1, "coords": {"x": 85, "y": 35}}
    ]

    for loc in locations_data:
        db.add(Location(
            name=loc["name"],
            code=loc["code"],
            risk_score=loc["risk_score"],
            incident_count=loc["incidents"],
            sif_count=loc["sif"],
            top_hazards=loc["hazards"],
            open_actions_count=loc["open_actions"],
            coordinates_json=loc["coords"]
        ))

    # 3. Seed Assets
    assets_data = [
        {"name": "Flanged Joint Connection FJ-302", "code": "AST-FJ-302", "type": "High-Pressure Piping Joint", "loc": "Refinery Unit-3 (Crude Distillation)", "dept": "Crude Distillation", "risk": 87.0, "incidents": 2, "sif": 1, "status": "CRITICAL_ALERT", "inspected": "2024-08-15"},
        {"name": "Crude Oil Distillation Column T-301", "code": "AST-COL-301", "type": "Distillation Tower", "loc": "Refinery Unit-3 (Crude Distillation)", "dept": "Crude Distillation", "risk": 75.0, "incidents": 3, "sif": 1, "status": "MAINTENANCE_REQUIRED", "inspected": "2024-07-20"},
        {"name": "Crude Feed Charge Pump P-301A", "code": "AST-PMP-301A", "type": "Centrifugal Pump", "loc": "Refinery Unit-3 (Crude Distillation)", "dept": "Crude Distillation", "risk": 32.0, "incidents": 0, "sif": 0, "status": "OPERATIONAL", "inspected": "2024-08-01"},
        {"name": "Pressure Safety Relief Valve PSV-304", "code": "AST-PSV-304", "type": "Safety Relief Valve", "loc": "Refinery Unit-3 (Crude Distillation)", "dept": "Crude Distillation", "risk": 45.0, "incidents": 1, "sif": 0, "status": "OPERATIONAL", "inspected": "2024-08-10"},
        {"name": "Overhead Condenser Heat Exchanger E-301", "code": "AST-HEX-301", "type": "Shell & Tube Exchanger", "loc": "Refinery Unit-3 (Crude Distillation)", "dept": "Crude Distillation", "risk": 28.0, "incidents": 0, "sif": 0, "status": "OPERATIONAL", "inspected": "2024-06-12"}
    ]

    for a in assets_data:
        db.add(Asset(
            name=a["name"],
            code=a["code"],
            asset_type=a["type"],
            location=a["loc"],
            department=a["dept"],
            risk_score=a["risk"],
            incident_count=a["incidents"],
            sif_count=a["sif"],
            status=a["status"],
            last_inspected=a["inspected"]
        ))

    # 4. Seed Departments
    depts_data = [
        {"name": "Crude Distillation", "code": "DPT-CDU", "risk": 87.0, "loto": 82.5, "incidents": 4, "sif": 2},
        {"name": "Catalytic Cracking", "code": "DPT-FCC", "risk": 58.0, "loto": 91.0, "incidents": 3, "sif": 1},
        {"name": "Hydrotreating", "code": "DPT-HDT", "risk": 42.0, "loto": 96.0, "incidents": 2, "sif": 0},
        {"name": "Refinery Maintenance", "code": "DPT-MNT", "risk": 64.0, "loto": 88.0, "incidents": 5, "sif": 1},
        {"name": "Operations & Logistics", "code": "DPT-OPS", "risk": 35.0, "loto": 98.0, "incidents": 1, "sif": 0}
    ]

    for d in depts_data:
        db.add(Department(
            name=d["name"],
            code=d["code"],
            risk_score=d["risk"],
            loto_compliance_rate=d["loto"],
            incident_count=d["incidents"],
            sif_count=d["sif"]
        ))

    # 5. Seed Knowledge Base Documents
    for kdoc in DEFAULT_KNOWLEDGE_DOCUMENTS:
        db.add(KnowledgeDocument(
            title=kdoc["title"],
            category=kdoc["category"],
            content=kdoc["content"],
            source=kdoc["source"]
        ))

    # 6. Seed Benchmark Demonstration Incident (Refinery Unit-3)
    unit3_incident = Incident(
        incident_number="INC-2024-0901-001",
        title="Unauthorized Pressurized Flange Repair with Thermal Flash Ignition",
        date="2024-09-01",
        time="14:30",
        location="Refinery Unit-3, Crude Oil Distillation Tower",
        department="Crude Distillation",
        asset="Flanged Joint Connection FJ-302",
        report_type="Unsafe-Act + Unsafe-Condition",
        severity="CRITICAL",
        description=(
            "A technician attempted unauthorized repair of a pressurized flanged joint rated at 250 bar "
            "without depressurization or supervisor notification. The flanged joint had a hairline crack. "
            "Oil sprayed from the damaged connection and ignited after contacting a nearby hot surface at approximately 140°C. "
            "The technician suffered a thermal burn. The equipment had deteriorated conditions and inadequate pressure-relief isolation. "
            "The technician was working without a face shield and proper gloves. The fire suppression system responded."
        ),
        equipment_condition="Deteriorated flanged joint connection with active hairline crack and inadequate pressure-relief isolation.",
        ppe_condition="Technician lacked mandatory full face shield and high-temperature thermal protective gloves.",
        environmental_conditions="High ambient temperature, adjacent uninsulated piping operated at 140°C.",
        witness_info="Control room operator observed rapid loss of pressure telemetry and activated unit emergency alarms.",
        immediate_actions="Automatic fire deluge system actuated; technician given emergency burn dressing and evacuated; unit depressurization initiated to flare.",
        status="ANALYZED",
        reported_by_id=db_users["technician"].id
    )
    db.add(unit3_incident)
    db.flush()

    # Pre-populate Risk Score (87/100 CRITICAL)
    risk_score_obj = RiskScore(
        incident_id=unit3_incident.id,
        base_score=70.0,
        final_score=87.0,
        risk_level="CRITICAL",
        confidence=0.94,
        calculation_log={
            "base": 70.0,
            "lsr1": 10.0,
            "lsr3": 8.0,
            "injury": 5.0,
            "sif": 4.0,
            "mitigation": -10.0,
            "final": 87.0
        }
    )
    db.add(risk_score_obj)
    db.flush()

    # Risk Factors for SHAP Waterfall
    factors_data = [
        {"name": "Pressurized Equipment Breach (250 bar)", "contrib": 70.0, "type": "BASE", "desc": "High-pressure hydrocarbon process equipment breach with acute loss of primary containment.", "ev": "Technician attempted unauthorized repair of a pressurized flanged joint rated at 250 bar without depressurization."},
        {"name": "LSR #1 Energy Isolation Violation", "contrib": 10.0, "type": "ADDITIVE", "desc": "Failure to verify zero-energy and execute depressurization before intervention.", "ev": "Worked on 250 bar pressure system without depressurization or isolation."},
        {"name": "LSR #3 Authorization & Supervision Violation", "contrib": 8.0, "type": "ADDITIVE", "desc": "Unauthorized intervention performed without supervisor notification or work permit.", "ev": "Performed unauthorized repair without supervisor notification."},
        {"name": "Thermal Burn Injury Escalation", "contrib": 5.0, "type": "ADDITIVE", "desc": "Personnel sustained active thermal burn injury during flash ignition.", "ev": "The technician suffered a thermal burn."},
        {"name": "SIF Fatality / Permanent Disability Potential", "contrib": 4.0, "type": "ADDITIVE", "desc": "High-energy release precursor with fatal escalation potential.", "ev": "SIF precursor detected in Energy Isolation category with 94% confidence."},
        {"name": "Fire Suppression System Response Mitigation", "contrib": -10.0, "type": "SUBTRACTIVE", "desc": "Automated deluge prevented structural fire escalation.", "ev": "The fire suppression system responded."}
    ]

    for f in factors_data:
        db.add(RiskFactor(
            risk_score_id=risk_score_obj.id,
            factor_name=f["name"],
            contribution=f["contrib"],
            factor_type=f["type"],
            description=f["desc"],
            evidence_snippet=f["ev"]
        ))

    # SIF Classification
    db.add(SIFClassification(
        incident_id=unit3_incident.id,
        is_sif_precursor=True,
        category="Energy Isolation",
        confidence=0.94,
        severity="CRITICAL",
        potential_severity="FATALITY / PERMANENT DISABILITY",
        energy_source="Pressurized Hydrocarbon (250 bar) / Thermal (140°C)",
        rationale="High-energy hydraulic potential coupled with flammable hydrocarbon flash ignition against uninsulated hot pipe."
    ))

    # LSR Violations
    lsr_data = [
        {"code": "LSR #1", "name": "Energy Isolation", "sev": "CRITICAL", "ev": "Technician worked on 250 bar pressurized system without depressurization or isolation.", "mit": "Enforce positive mechanical isolation (blind flanges) and zero-energy verification."},
        {"code": "LSR #3", "name": "Authorization & Supervision", "sev": "CRITICAL", "ev": "Technician performed unauthorized repair without supervisor notification.", "mit": "Halt unauthorized work, mandate PTW review and supervisor signoff."},
        {"code": "LSR #5", "name": "Personal Protection & Line of Fire", "sev": "HIGH", "ev": "Technician lacked required PPE (working without face shield and proper gloves).", "mit": "Mandate high-temp flame-resistant PPE, full face shields, and thermal gloves."}
    ]

    for l in lsr_data:
        db.add(LSRViolation(
            incident_id=unit3_incident.id,
            rule_code=l["code"],
            rule_name=l["name"],
            is_violated=True,
            severity=l["sev"],
            evidence=l["ev"],
            rationale="Direct violation of refinery mandatory life-saving rules.",
            mitigation_action=l["mit"]
        ))

    # Hazards
    hazards_data = [
        {"name": "Pressurized System Breach", "type": "Pressure / Loss of Containment", "sev": "CRITICAL", "src": "Flanged joint operating at 250 bar with hairline crack", "mit": "Immediate line isolation, blowdown to flare."},
        {"name": "Thermal Ignition & Flash Fire", "type": "Thermal / Hydrocarbon Fire", "sev": "HIGH", "src": "Sprayed oil contacting adjacent 140°C uninsulated surface", "mit": "Deluge suppression, pipe insulation audit."}
    ]

    for h in hazards_data:
        db.add(Hazard(
            incident_id=unit3_incident.id,
            name=h["name"],
            hazard_type=h.get("type"),
            severity=h["sev"],
            source=h["src"],
            mitigation=h["mit"]
        ))

    # Root Cause
    rca_immediate = "Technician attempted unauthorized corrective action on an energized 250 bar pressurized flanged joint without positive depressurization or supervisor notification."
    rca_contrib = [
        "Lack of supervisor notification and absence of a validated Work Permit before breaking containment.",
        "Potential perceived production urgency to fix a leaking connection rapidly.",
        "Inadequate task-specific PPE enforcement (missing face shield and high-temperature thermal gloves).",
        "Presence of uninsulated adjacent 140°C hot surface within the direct line-of-fire spray zone."
    ]
    rca_system = [
        "LOTO (Lockout/Tagout) & positive mechanical isolation workflow was not enforced at unit operational level.",
        "Absence of mandatory physical verification checkpoint for pressurized equipment line-breaking.",
        "Weak maintenance permit authorization control allowing unscheduled interventions.",
        "Equipment integrity management failed to detect or replace the cracked flanged joint before pressure escalation."
    ]

    rca_tree_json = {
        "name": "CRITICAL INCIDENT",
        "title": "Pressurized Flanged Joint Breach & Thermal Flash",
        "severity": "CRITICAL",
        "children": [
            {
                "name": "IMMEDIATE CAUSE",
                "title": rca_immediate,
                "children": [
                    {
                        "name": "CONTRIBUTING FACTORS",
                        "title": "Human, Behavioral & Physical Environmental Drivers",
                        "children": [{"name": f"Factor {i+1}", "title": c} for i, c in enumerate(rca_contrib)]
                    },
                    {
                        "name": "SYSTEM DEFICIENCIES",
                        "title": "Process Safety & Governance Gaps",
                        "children": [{"name": f"Deficiency {i+1}", "title": s} for i, s in enumerate(rca_system)]
                    }
                ]
            }
        ]
    }

    db.add(RootCause(
        incident_id=unit3_incident.id,
        immediate_cause=rca_immediate,
        contributing_causes=rca_contrib,
        system_causes=rca_system,
        rca_tree_json=rca_tree_json
    ))

    # Corrective Actions
    ca_data = [
        {"code": "ACT-2024-0901-01", "desc": "Enforce mandatory Double Block and Bleed LOTO verification for all Unit-3 flanged connections before maintenance.", "owner": "Process Safety Lead", "dept": "Crude Distillation", "pri": "CRITICAL", "due": "2024-09-05", "status": "IN PROGRESS"},
        {"code": "ACT-2024-0901-02", "desc": "Perform ultrasonic crack detection on all adjacent 250 bar flanged joints in Crude Distillation Tower T-301.", "owner": "Asset Integrity Manager", "dept": "Refinery Maintenance", "pri": "HIGH", "due": "2024-09-07", "status": "OPEN"},
        {"code": "ACT-2024-0901-03", "desc": "Audit thermal insulation on all piping operated above 80°C within 10 meters of hydrocarbon containment lines.", "owner": "HSE Officer", "dept": "HSE Governance", "pri": "HIGH", "due": "2024-09-10", "status": "OPEN"},
        {"code": "ACT-2024-0901-04", "desc": "Conduct refinery-wide stand-down on Life-Saving Rule #1 (Energy Isolation) and Rule #3 (Work Authorization).", "owner": "Operations Director", "dept": "Operations & Logistics", "pri": "CRITICAL", "due": "2024-09-03", "status": "COMPLETED"}
    ]

    for ca in ca_data:
        db.add(CorrectiveAction(
            action_code=ca["code"],
            incident_id=unit3_incident.id,
            description=ca["desc"],
            owner=ca["owner"],
            department=ca["dept"],
            priority=ca["pri"],
            due_date=ca["due"],
            status=ca["status"]
        ))

    # Notifications
    db.add(Notification(
        recipient_role="Rescue Team",
        title="🚨 CRITICAL SAFETY EVENT — Unit-3 Crude Distillation Tower",
        message="Risk Score: 87/100. Pressurized system breach at 250 bar with thermal flash. Active burn victim evacuated. Deluge active.",
        priority="CRITICAL",
        incident_id=unit3_incident.id,
        is_read=False,
        channel="IN_APP"
    ))

    db.add(Notification(
        recipient_role="Safety Manager",
        title="SIF Precursor Detected (Confidence: 94%)",
        message="Incident INC-2024-0901-001 has 3 Life-Saving Rule violations: LSR #1, LSR #3, LSR #5. Root Cause Analysis generated.",
        priority="CRITICAL",
        incident_id=unit3_incident.id,
        is_read=False,
        channel="EMAIL"
    ))

    db.commit()
    print("Database seeding completed successfully!")
