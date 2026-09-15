import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="Technician") # Rescue Team, Technician, Safety Manager, Department Manager, Sonaga / HSE Division, Admin
    department = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incidents = relationship("Incident", back_populates="reporter")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_number = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=True)
    location = Column(String(100), index=True, nullable=False)
    department = Column(String(100), index=True, nullable=False)
    asset = Column(String(100), index=True, nullable=False)
    report_type = Column(String(100), nullable=False) # Unsafe-Act + Unsafe-Condition, Near Miss, Incident, SIF
    severity = Column(String(50), nullable=False, default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(Text, nullable=False)
    equipment_condition = Column(Text, nullable=True)
    ppe_condition = Column(Text, nullable=True)
    environmental_conditions = Column(Text, nullable=True)
    witness_info = Column(Text, nullable=True)
    immediate_actions = Column(Text, nullable=True)
    status = Column(String(50), default="ANALYZED") # OPEN, IN_REVIEW, ANALYZED, CLOSED
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reporter = relationship("User", back_populates="incidents")
    risk_score = relationship("RiskScore", back_populates="incident", uselist=False, cascade="all, delete-orphan")
    sif_classification = relationship("SIFClassification", back_populates="incident", uselist=False, cascade="all, delete-orphan")
    lsr_violations = relationship("LSRViolation", back_populates="incident", cascade="all, delete-orphan")
    hazards = relationship("Hazard", back_populates="incident", cascade="all, delete-orphan")
    root_cause = relationship("RootCause", back_populates="incident", uselist=False, cascade="all, delete-orphan")
    corrective_actions = relationship("CorrectiveAction", back_populates="incident", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="incident", cascade="all, delete-orphan")


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), unique=True, nullable=False)
    base_score = Column(Float, default=70.0)
    final_score = Column(Float, nullable=False)
    risk_level = Column(String(50), nullable=False) # LOW, MODERATE, HIGH, VERY HIGH, CRITICAL
    confidence = Column(Float, default=0.94)
    calculation_log = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="risk_score")
    factors = relationship("RiskFactor", back_populates="risk_score", cascade="all, delete-orphan")


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(Integer, primary_key=True, index=True)
    risk_score_id = Column(Integer, ForeignKey("risk_scores.id"), nullable=False)
    factor_name = Column(String(255), nullable=False)
    contribution = Column(Float, nullable=False)
    factor_type = Column(String(50), nullable=False) # ADDITIVE, SUBTRACTIVE, BASE
    description = Column(Text, nullable=True)
    evidence_snippet = Column(Text, nullable=True)

    risk_score = relationship("RiskScore", back_populates="factors")


class SIFClassification(Base):
    __tablename__ = "sif_classifications"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), unique=True, nullable=False)
    is_sif_precursor = Column(Boolean, default=True)
    category = Column(String(100), nullable=False)
    confidence = Column(Float, default=0.94)
    severity = Column(String(50), default="CRITICAL")
    potential_severity = Column(String(50), default="FATALITY / PERMANENT DISABILITY")
    energy_source = Column(String(100), default="Pressurized Hydrocarbon / Thermal")
    rationale = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="sif_classification")


class LSRViolation(Base):
    __tablename__ = "lsr_violations"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    rule_code = Column(String(50), nullable=False) # LSR #1, LSR #3, LSR #5 etc.
    rule_name = Column(String(100), nullable=False)
    is_violated = Column(Boolean, default=True)
    severity = Column(String(50), default="CRITICAL")
    evidence = Column(Text, nullable=False)
    rationale = Column(Text, nullable=True)
    mitigation_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="lsr_violations")


class Hazard(Base):
    __tablename__ = "hazards"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    name = Column(String(255), nullable=False)
    hazard_type = Column(String(100), nullable=False) # Chemical, Mechanical, Thermal, Pressure, Electrical
    severity = Column(String(50), default="HIGH")
    source = Column(String(255), nullable=True)
    mitigation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="hazards")


class RootCause(Base):
    __tablename__ = "root_causes"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), unique=True, nullable=False)
    immediate_cause = Column(Text, nullable=False)
    contributing_causes = Column(JSON, nullable=False)
    system_causes = Column(JSON, nullable=False)
    rca_tree_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="root_cause")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    asset_type = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    risk_score = Column(Float, default=50.0)
    failure_history = Column(JSON, nullable=True)
    inspection_history = Column(JSON, nullable=True)
    incident_count = Column(Integer, default=0)
    sif_count = Column(Integer, default=0)
    status = Column(String(50), default="OPERATIONAL") # OPERATIONAL, MAINTENANCE_REQUIRED, CRITICAL_ALERT, ISOLATED
    last_inspected = Column(String(50), nullable=True)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    risk_score = Column(Float, default=50.0)
    incident_count = Column(Integer, default=0)
    sif_count = Column(Integer, default=0)
    top_hazards = Column(JSON, nullable=True)
    open_actions_count = Column(Integer, default=0)
    coordinates_json = Column(JSON, nullable=True)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    risk_score = Column(Float, default=50.0)
    loto_compliance_rate = Column(Float, default=95.0)
    incident_count = Column(Integer, default=0)
    sif_count = Column(Integer, default=0)


class CorrectiveAction(Base):
    __tablename__ = "corrective_actions"

    id = Column(Integer, primary_key=True, index=True)
    action_code = Column(String(50), unique=True, nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    description = Column(Text, nullable=False)
    owner = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    priority = Column(String(50), default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    due_date = Column(String(50), nullable=False)
    status = Column(String(50), default="OPEN") # OPEN, IN PROGRESS, COMPLETED, OVERDUE
    evidence = Column(Text, nullable=True)
    completion_date = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="corrective_actions")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient_role = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(50), default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    channel = Column(String(50), default="IN_APP") # EMAIL, SMS, WEB_PUSH, IN_APP
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="notifications")


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    version = Column(String(50), default="1.0")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    chunks = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("knowledge_documents.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding_json = Column(JSON, nullable=True)
    chunk_index = Column(Integer, default=0)
    metadata_json = Column(JSON, nullable=True)

    document = relationship("KnowledgeDocument", back_populates="chunks")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    username = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=False)
    entity_id = Column(String(100), nullable=True)
    details_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
