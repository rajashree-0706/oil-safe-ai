from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int
    full_name: str
    username: str
    department: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "Technician"
    department: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    department: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Hazard & LSR & SIF
class HazardItem(BaseModel):
    name: str
    hazard_type: str = "Physical"
    severity: str
    source: Optional[str] = None
    mitigation: Optional[str] = None

class LSRViolationItem(BaseModel):
    rule_code: str
    rule_name: str
    is_violated: bool = True
    severity: str
    evidence: str
    rationale: Optional[str] = None
    mitigation_action: Optional[str] = None

class SIFClassificationItem(BaseModel):
    is_sif_precursor: bool = True
    category: str
    confidence: float
    severity: str
    potential_severity: str
    energy_source: Optional[str] = None
    rationale: Optional[str] = None

class RiskFactorItem(BaseModel):
    factor_name: str
    contribution: float
    factor_type: str # ADDITIVE, SUBTRACTIVE, BASE
    description: Optional[str] = None
    evidence_snippet: Optional[str] = None

class RiskScoreItem(BaseModel):
    base_score: float
    final_score: float
    risk_level: str
    confidence: float
    factors: List[RiskFactorItem] = []

class RootCauseItem(BaseModel):
    immediate_cause: str
    contributing_causes: List[str]
    system_causes: List[str]
    rca_tree: Optional[Dict[str, Any]] = None

# Incident Schemas
class IncidentCreate(BaseModel):
    title: str
    date: str
    time: Optional[str] = "14:30"
    location: str
    department: str
    asset: str
    report_type: str = "Unsafe-Act + Unsafe-Condition"
    severity: Optional[str] = "HIGH"
    description: str
    equipment_condition: Optional[str] = None
    ppe_condition: Optional[str] = None
    environmental_conditions: Optional[str] = None
    witness_info: Optional[str] = None
    immediate_actions: Optional[str] = None

class IncidentResponse(BaseModel):
    id: int
    incident_number: str
    title: str
    date: str
    time: Optional[str]
    location: str
    department: str
    asset: str
    report_type: str
    severity: str
    description: str
    status: str
    equipment_condition: Optional[str] = None
    ppe_condition: Optional[str] = None
    environmental_conditions: Optional[str] = None
    immediate_actions: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CorrectiveActionItem(BaseModel):
    id: Optional[int] = None
    action_code: Optional[str] = None
    description: str
    owner: str
    department: str
    priority: str = "HIGH"
    due_date: str
    status: str = "OPEN"
    evidence: Optional[str] = None

class IncidentAnalysisResult(BaseModel):
    incident_id: int
    incident_number: str
    title: str
    date: str
    location: str
    department: str
    asset: str
    risk_score: float
    risk_level: str
    sif_precursor: bool
    sif_category: str
    confidence: float
    primary_hazard: str
    secondary_hazard: Optional[str] = None
    injury: Optional[str] = None
    hazards: List[HazardItem]
    lsr_violations: List[LSRViolationItem]
    risk_factors: List[RiskFactorItem]
    root_causes: RootCauseItem
    emergency_actions: List[str]
    recommendations: List[str]
    retrieved_evidence: List[Dict[str, Any]]
    model_metadata: Dict[str, Any]

# RAG & Knowledge Base
class RAGQueryRequest(BaseModel):
    query: str
    category: Optional[str] = None
    top_k: int = 5

class RAGQueryResult(BaseModel):
    document_title: str
    category: str
    content: str
    score: float
    source: str

class CorrectiveActionCreate(BaseModel):
    incident_id: Optional[int] = None
    description: str
    owner: str
    department: str
    priority: str = "HIGH"
    due_date: str
    status: str = "OPEN"
    evidence: Optional[str] = None

class CorrectiveActionUpdate(BaseModel):
    status: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[str] = None
    evidence: Optional[str] = None
    completion_date: Optional[str] = None

class NotificationItem(BaseModel):
    id: int
    recipient_role: str
    title: str
    message: str
    priority: str
    incident_id: Optional[int]
    is_read: bool
    channel: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
