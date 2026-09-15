# 🚨 OIL-SAFE AI — Industrial Refinery Safety Incident Analysis Platform

OIL-SAFE AI is a production-ready industrial safety decision-support platform engineered for refineries and oil & gas operations. The platform ingests raw incident reports, performs Transformer NLP (DeBERTa-v3) extraction, evaluates Serious Injury and Fatality (SIF) precursors, detects Life-Saving Rule (LSR) violations, computes an explainable 0–100 risk score using SHAP feature attribution, generates 4-tier Root Cause Analysis (RCA) trees, and provides tailored command dashboards for 6 distinct operational roles.

---

## 🌟 Key Features

1. **Transformer NLP / DeBERTa Pipeline**:
   - Automated text cleaning, sentence segmentation, and industrial Named Entity Recognition (NER) for high pressure (e.g. 250 bar), thermal flash (140°C), flanged connections, and missing PPE.
2. **SIF Precursor Detection (11 OIL SIF Categories)**:
   - Evaluates high-energy hazards including Energy Isolation, Line of Fire, Working at Height, Pressure Systems, Confined Space, and Hot Work with confidence scores (e.g. 94% on Unit-3).
3. **Automated Life-Saving Rule (LSR) Violations**:
   - Matches narratives against 9 IOGP / Refinery Life-Saving Rules (LSR #1 Energy Isolation, LSR #3 Authorization, LSR #5 Personal Protection) with extracted evidence snippets.
4. **Explainable 0–100 Risk Scoring & SHAP Waterfall**:
   - Computes bounded risk score ($0 \le S \le 100$) and generates visual SHAP feature attribution breakdowns:
     * Pressurized equipment breach (250 bar): **+70**
     * LSR #1 Energy isolation violation: **+10**
     * LSR #3 Work authorization violation: **+8**
     * Thermal burn injury escalation: **+5**
     * SIF fatality potential: **+4**
     * Fire suppression deluge mitigation: **-10**
     * **Final Dynamic Score: 87 / 100 (CRITICAL)**
5. **Interactive Root Cause Analysis (RCA)**:
   - Automated 4-tier RCA hierarchy: *Immediate Cause $\rightarrow$ Contributing Factors $\rightarrow$ System Safety Deficiencies $\rightarrow$ Corrective Actions*.
6. **RAG Knowledge System**:
   - Semantic & TF-IDF retrieval over corporate safety manuals, LOTO protocols, and historical incident databases with evidence citations.
7. **6 Role-Tailored Command Centers (RBAC)**:
   - 🚨 **Rescue Team**: Critical incident status banner, immediate 7-step tactical response checklist, casualty burn status, deluge telemetry.
   - 🛡️ **Safety Manager**: Deep-dive RCA management, SIF taxonomy matrix, corrective actions assignment.
   - 🏢 **Department Manager**: LOTO compliance rates, department risk breakdown, precursor statistics.
   - 🌐 **Sonaga / HSE Division**: Organization-wide hazard radar, risk trends, policy directives.
   - 🔧 **Technician**: Field report submission, PPE guidelines, training alerts.
   - ⚙️ **Admin**: RBAC control, AI threshold tuning, system logs.
8. **Interactive 2D Refinery Risk Heatmap**:
   - Visual refinery layout (Unit-1, Unit-2, Unit-3 Distillation Tower, Tank Farm, Boiler Area, Maintenance Area, Marine Terminal) with live risk intensity and unit inspection drawer.
9. **Exportable Incident Reports**:
   - One-click export to printable HTML, PDF, and structured JSON.

---

## 🏛️ System Architecture

```
Raw Incident Report / PDF / DOCX / TXT / CSV
                │
                ▼
       DeBERTa NLP Engine
    ┌───────────┴───────────┐
    ▼                       ▼
Named Entity &          SIF Precursor
Hazard Extraction       Classifier (94%)
    │                       │
    ▼                       ▼
Life-Saving Rule        RAG Knowledge
Violation Detector      Base Retrieval
    │                       │
    └───────────┬───────────┘
                ▼
      Dynamic Risk Scorer
         (87 / 100)
                │
                ▼
     SHAP Explainable AI
    (Feature Attribution)
                │
                ▼
   Root Cause Analysis Tree
                │
                ▼
 Role-Based Command Dashboards
 (Rescue, HSE, Safety, Dept, Tech)
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10+ (Python 3.14 compatible)
- Modern web browser (Chrome, Edge, Firefox)

### 1. Clone & Setup Backend
```bash
# Navigate to project directory
cd dhanush_sih

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Run the Platform
```bash
# Start FastAPI backend with integrated Industrial Safety Command Center
python backend/app/main.py
```
Open your browser and navigate to:
**👉 http://localhost:8000**

---

## 🔑 Demo Role Credentials

| Role | Username | Password | Key Permissions |
|---|---|---|---|
| **Rescue Team** | `rescue_team` | `Rescue@2026` | Emergency response, critical alerts, victim status |
| **Safety Manager** | `safety_manager` | `Safety@2026` | Deep RCA, SIF taxonomy, corrective actions |
| **Department Manager**| `dept_manager` | `Dept@2026` | Department risk, LOTO compliance rate |
| **Sonaga / HSE** | `hse_division` | `Hse@2026` | Organization analytics, safety policies |
| **Technician** | `technician` | `Tech@2026` | Report submission, PPE alerts |
| **Admin** | `admin` | `Admin@2026` | Full platform control & AI configuration |

*Note: You can also switch roles instantaneously in real-time using the role dropdown in the top bar!*

---

## 🧪 Running the Test Suite

```bash
# Run unit & integration tests
$env:PYTHONPATH="backend"
python -m pytest backend/tests/ -v
```

All 10 automated test suites validate:
- ✅ Clamping of risk scores within $[0, 100]$
- ✅ Target scoring for Unit-3 incident (Exact **87.0 CRITICAL**)
- ✅ SIF Precursor detection (**YES, 94% Confidence**)
- ✅ LSR violation detection (**LSR #1, LSR #3, LSR #5**)
- ✅ Full REST API integration, JWT auth, and PDF/HTML report exports

---

## 🐳 Docker Deployment

To launch the full containerized stack with PostgreSQL and pgvector:

```bash
# Start PostgreSQL (pgvector) + FastAPI Backend
docker-compose up --build
```

Access the application at `http://localhost:8000`.

---

## 🛡️ AI Safety & Decision-Support Notice

OIL-SAFE AI is designed as an **expert decision-support platform** for industrial operations. The system highlights high-energy hazards and recommends evidence-based emergency procedures but does not execute physical equipment control. Operational commands must remain under the authority of certified plant personnel and site emergency response incident commanders.
