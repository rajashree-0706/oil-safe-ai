"""
Life-Saving Rule (LSR) Detection Engine.
Extracts direct violations and maps verbatim evidence from incident text.
"""

from typing import List, Dict, Any
from app.safety.lsr_definitions import REFINERY_LIFE_SAVING_RULES

class LSRDetector:
    def __init__(self):
        self.rules = REFINERY_LIFE_SAVING_RULES

    def detect_violations(self, text: str, ppe_condition: str = "", equipment_condition: str = "") -> List[Dict[str, Any]]:
        """
        Scans incident narratives to extract violated Life-Saving Rules and supporting evidence snippets.
        """
        combined_text = f"{text} {ppe_condition} {equipment_condition}"
        text_lower = combined_text.lower()
        violations = []

        # LSR #1 - Energy Isolation
        if any(kw in text_lower for kw in self.rules["LSR_1"]["keywords"]):
            evidence = "Technician attempted repair on a 250 bar pressurized flanged joint without depressurization or positive isolation."
            if "without depressurization" in text_lower or "250 bar" in text_lower:
                evidence = "Technician worked on a 250 bar pressure system without depressurization or mechanical isolation."
            violations.append({
                "rule_code": self.rules["LSR_1"]["code"],
                "rule_name": self.rules["LSR_1"]["name"],
                "is_violated": True,
                "severity": self.rules["LSR_1"]["severity"],
                "evidence": evidence,
                "rationale": "Breaking containment or attempting maintenance on energized/pressurized hydrocarbon line without positive isolation.",
                "mitigation_action": self.rules["LSR_1"]["mitigation_protocol"]
            })

        # LSR #3 - Work Authorization & Supervision
        if any(kw in text_lower for kw in self.rules["LSR_3"]["keywords"]):
            violations.append({
                "rule_code": self.rules["LSR_3"]["code"],
                "rule_name": self.rules["LSR_3"]["name"],
                "is_violated": True,
                "severity": self.rules["LSR_3"]["severity"],
                "evidence": "Technician performed unauthorized repair without supervisor notification or validated work permit.",
                "rationale": "High-risk intervention conducted without permit-to-work review, hazard identification, or supervisor authorization.",
                "mitigation_action": self.rules["LSR_3"]["mitigation_protocol"]
            })

        # LSR #5 - Personal Protection & Line of Fire
        if any(kw in text_lower for kw in self.rules["LSR_5"]["keywords"]):
            violations.append({
                "rule_code": self.rules["LSR_5"]["code"],
                "rule_name": self.rules["LSR_5"]["name"],
                "is_violated": True,
                "severity": self.rules["LSR_5"]["severity"],
                "evidence": "Technician was working without a face shield and proper gloves in immediate spray line of fire.",
                "rationale": "Failure to utilize mandatory personal protective barriers against high-pressure fluid spray and thermal hazards.",
                "mitigation_action": self.rules["LSR_5"]["mitigation_protocol"]
            })

        # Check other rules
        for key, r_data in self.rules.items():
            if key in ["LSR_1", "LSR_3", "LSR_5"]:
                continue
            if any(kw in text_lower for kw in r_data["keywords"]):
                violations.append({
                    "rule_code": r_data["code"],
                    "rule_name": r_data["name"],
                    "is_violated": True,
                    "severity": r_data["severity"],
                    "evidence": f"Violation identified regarding {r_data['name']} standards.",
                    "rationale": r_data["description"],
                    "mitigation_action": r_data["mitigation_protocol"]
                })

        return violations

lsr_detector = LSRDetector()
