"""
Refinery & IOGP Life-Saving Rules (LSR) catalog and violation detection triggers.
"""

REFINERY_LIFE_SAVING_RULES = {
    "LSR_1": {
        "code": "LSR #1",
        "name": "Energy Isolation",
        "category": "ISOLATION",
        "description": "Verify isolation and zero energy before work begins.",
        "keywords": ["without depressurization", "no depressurization", "pressurized", "undepressurized", "no loto", "without isolation", "live line", "not isolated", "stored pressure", "250 bar without"],
        "severity": "CRITICAL",
        "base_risk_addition": 10.0,
        "mitigation_protocol": "Enforce positive mechanical isolation (blind flanges, double block & bleed) and verify zero stored pressure prior to breaking containment."
    },
    "LSR_2": {
        "code": "LSR #2",
        "name": "Confined Space Entry",
        "category": "CONFINED_SPACE",
        "description": "Obtain authorization before entering a confined space.",
        "keywords": ["unauthorized entry", "no gas test", "unmonitored tank", "confined entry without permit"],
        "severity": "CRITICAL",
        "base_risk_addition": 10.0,
        "mitigation_protocol": "Execute continuous 4-gas testing, assign certified hole watch, and obtain valid CSE permit."
    },
    "LSR_3": {
        "code": "LSR #3",
        "name": "Work Authorization & Supervision",
        "category": "AUTHORIZATION",
        "description": "Work with a valid permit and notify designated supervisor when required.",
        "keywords": ["unauthorized repair", "unauthorized", "without supervisor", "without notification", "no permit", "no work permit", "bypassed permit", "unsupervised"],
        "severity": "CRITICAL",
        "base_risk_addition": 8.0,
        "mitigation_protocol": "Halt unauthorized work immediately, initiate permit-to-work review, and conduct toolbox safety talk with supervisor sign-off."
    },
    "LSR_4": {
        "code": "LSR #4",
        "name": "Bypassing Safety Controls",
        "category": "OVERRIDE",
        "description": "Obtain authorization before overriding or disabling safety controls.",
        "keywords": ["bypassed interlock", "disabled sensor", "defeat trip", "bridged circuit", "tampered relief valve"],
        "severity": "CRITICAL",
        "base_risk_addition": 10.0,
        "mitigation_protocol": "Re-establish safety critical interlocks and log formal MOC (Management of Change) approval."
    },
    "LSR_5": {
        "code": "LSR #5",
        "name": "Personal Protection & Line of Fire",
        "category": "PPE_LINE_OF_FIRE",
        "description": "Wear required task-specific PPE and position yourself outside the line of fire.",
        "keywords": ["without a face shield", "without proper gloves", "missing ppe", "lacked required ppe", "no face shield", "no gloves", "line of fire", "no eye protection"],
        "severity": "HIGH",
        "base_risk_addition": 5.0,
        "mitigation_protocol": "Mandate high-temperature flame-retardant PPE, full face shields, and chemical/thermal gloves for high-risk zones."
    },
    "LSR_6": {
        "code": "LSR #6",
        "name": "Hot Work Control",
        "category": "HOT_WORK",
        "description": "Control flammables and ignition sources during hot work.",
        "keywords": ["hot work without permit", "uncontrolled ignition", "spark near hydrocarbon", "no fire blanket"],
        "severity": "CRITICAL",
        "base_risk_addition": 8.0,
        "mitigation_protocol": "Establish 15-meter combustible clearance zone and maintain 30-minute post-work fire watch."
    },
    "LSR_7": {
        "code": "LSR #7",
        "name": "Working at Height",
        "category": "HEIGHT",
        "description": "Protect yourself against a fall when working at height.",
        "keywords": ["no harness", "unclipped lanyard", "scaffold untagged", "fall protection missing"],
        "severity": "CRITICAL",
        "base_risk_addition": 8.0,
        "mitigation_protocol": "Enforce 100% tie-off using certified anchor points and inspect fall arrest systems."
    },
    "LSR_8": {
        "code": "LSR #8",
        "name": "Safe Mechanical Lifting",
        "category": "LIFTING",
        "description": "Plan lifting operations and control the lift area.",
        "keywords": ["standing under load", "uninspected sling", "crane overload", "lift radius unbarricaded"],
        "severity": "HIGH",
        "base_risk_addition": 6.0,
        "mitigation_protocol": "Barricade lift radius and verify rigger certifications and crane load charts."
    },
    "LSR_9": {
        "code": "LSR #9",
        "name": "Driving & Equipment Operations",
        "category": "DRIVING",
        "description": "Follow speed limits, wear seatbelts, and avoid mobile distraction.",
        "keywords": ["speeding vehicle", "seatbelt violation", "phone while driving"],
        "severity": "MEDIUM",
        "base_risk_addition": 4.0,
        "mitigation_protocol": "Apply in-vehicle speed telematics and strict plant vehicular safety enforcement."
    }
}
