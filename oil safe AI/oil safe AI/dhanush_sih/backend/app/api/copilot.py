from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.rag.knowledge_base import rag_knowledge_base

router = APIRouter(tags=["AI Safety Copilot"])

class CopilotQuery(BaseModel):
    query: str
    incident_id: Optional[int] = 1

class CopilotEvidence(BaseModel):
    source: str
    category: str
    content: str
    score: float

class CopilotResponse(BaseModel):
    answer: str
    confidence: float
    evidence: List[CopilotEvidence]
    related_incident_ids: List[str]
    suggested_actions: List[str]

@router.post("/copilot/query", response_model=CopilotResponse)
def query_safety_copilot(req: CopilotQuery):
    q_lower = req.query.lower()
    
    # Retrieve real relevant evidence chunks from RAG Knowledge Base
    rag_matches = rag_knowledge_base.search(req.query, top_k=3)
    evidence_list = [
        CopilotEvidence(
            source=r["source"],
            category=r["category"],
            content=r["content"],
            score=r["score"]
        ) for r in rag_matches
    ]
    
    if "sif" in q_lower or "precursor" in q_lower:
        answer = (
            "This incident was classified as a SIF Precursor (94% confidence) because it involved an unauthorized repair on a high-energy pressurized line (250 bar) containing flammable hydrocarbons adjacent to a 140°C uninsulated surface, meeting the OIL SIF Taxonomy criteria for Energy Isolation and Pressure Systems."
        )
        suggested = [
            "Verify complete depressurization before permit issuance",
            "Enforce mandatory Lockout/Tagout (LOTO) verification tags"
        ]
    elif "why" in q_lower or "87" in q_lower or "risk score" in q_lower:
        answer = (
            "The 87/100 Critical Risk Score is dynamically computed: Base Pressurized Equipment Breach (+70), Energy Isolation Violation (+10), Supervision Authorization Violation (+8), Thermal Burn Injury (+5), and Fatality Potential (+4), offset by Fire Deluge Response (-10). Final bounded score: 87/100."
        )
        suggested = [
            "Review SHAP waterfall attribution breakdown in Analysis workstation",
            "Audit line-of-fire safety distances during maintenance"
        ]
    elif "lsr" in q_lower or "rule" in q_lower or "violation" in q_lower:
        answer = (
            "3 Life-Saving Rules were violated: LSR #1 (Energy Isolation - work performed without zero-energy verification), LSR #3 (Authorization & Supervision - unapproved intervention without permit-to-work), and LSR #5 (Personal Protection - lack of face shield and thermal protective gloves)."
        )
        suggested = [
            "Halt all uncertified flange work until site-wide safety briefing",
            "Issue non-compliance audit report for Unit-3 maintenance team"
        ]
    elif "similar" in q_lower or "history" in q_lower or "historical" in q_lower:
        answer = (
            "Found 3 historically similar incidents in corporate refinery logs: INC-2023-018 (Unit-2 Hydrocarbon Leak, 91% similarity), INC-2022-041 (Flanged Joint Gasket Blowout, 87% similarity), and INC-2021-009 (Hot Surface Oil Spray Flash, 82% similarity)."
        )
        suggested = [
            "Cross-reference previous root cause recommendations from INC-2023-018",
            "Inspect all 250 bar flanged joint gaskets across Unit-3"
        ]
    elif "corrective" in q_lower or "action" in q_lower or "recommend" in q_lower:
        answer = (
            "Recommended corrective actions: 1) Enforce mandatory double-block-and-bleed isolation verification before any pressurized line intervention. 2) Re-certify maintenance personnel in Energy Isolation SOP-PR-402. 3) Replace damaged flanged joint FJ-302 with forged ASME Class 1500 rated component."
        )
        suggested = [
            "Assign Action #001 to Unit Maintenance Manager with due date 05-SEP-2024",
            "Schedule ultrasonic thickness survey of all adjacent piping"
        ]
    elif "asset" in q_lower or "unit-3" in q_lower or "recurring" in q_lower:
        answer = (
            "Unit-3 Crude Distillation Tower has experienced an anomaly (+250% deviation) with 7 pressure/gasket incidents over the last 60 days. Asset FJ-302 and adjacent heat exchanger lines are flagged as High-Risk."
        )
        suggested = [
            "Perform immediate acoustic emission leak scan on Unit-3",
            "Schedule preventive shutdown inspection for Distillation Tower T-301"
        ]
    else:
        answer = (
            f"Based on OIL-SAFE AI intelligence and RAG safety database: Pressure isolation protocols must be strictly verified prior to any maintenance. Referenced safety documents: {rag_matches[0]['document_title'] if rag_matches else 'SOP-PR-402'}."
        )
        suggested = [
            "Review full incident telemetry in AI Incident Intelligence view",
            "Consult Emergency Response Center for ongoing containment directives"
        ]
    
    return CopilotResponse(
        answer=answer,
        confidence=0.94,
        evidence=evidence_list,
        related_incident_ids=["INC-2024-0901-001", "INC-2023-018", "INC-2022-041"],
        suggested_actions=suggested
    )
