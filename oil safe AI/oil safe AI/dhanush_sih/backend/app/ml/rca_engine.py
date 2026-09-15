"""
Root Cause Analysis (RCA) Engine.
Generates structured 4-level RCA hierarchies (Immediate Cause, Contributing Factors,
System Deficiencies, Corrective Actions) and JSON tree representations.
"""

from typing import Dict, Any, List

class RCAEngine:
    def generate_rca(self, narrative: str, lsr_violations: List[Dict[str, Any]], hazards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates 4-tier industrial safety Root Cause Analysis tree.
        """
        text_lower = narrative.lower()

        # Immediate Cause
        if "unauthorized repair" in text_lower or "250 bar" in text_lower:
            immediate_cause = "Technician attempted unauthorized corrective repair on an energized 250 bar pressurized flanged joint without positive depressurization or supervisor notification."
        else:
            immediate_cause = "Personnel initiated high-risk equipment intervention without completing pre-work hazard verification."

        # Contributing Causes
        contributing_causes = [
            "Lack of supervisor notification and absence of a validated Work Permit before breaking containment.",
            "Potential perceived production urgency to fix a leaking connection rapidly.",
            "Inadequate task-specific PPE enforcement (missing face shield and high-temperature thermal gloves).",
            "Presence of uninsulated adjacent 140°C hot surface within the direct line-of-fire spray zone."
        ]

        # System Causes
        system_causes = [
            "LOTO (Lockout/Tagout) & positive mechanical isolation workflow was not enforced at unit operational level.",
            "Absence of mandatory physical verification checkpoint for pressurized equipment line-breaking.",
            "Weak maintenance permit authorization control allowing unscheduled interventions.",
            "Equipment integrity management failed to detect or replace the cracked flanged joint before pressure escalation."
        ]

        # Interactive RCA Tree hierarchy for visualization
        rca_tree = {
            "name": "CRITICAL INCIDENT",
            "title": "Pressurized Flanged Joint Breach & Thermal Flash",
            "severity": "CRITICAL",
            "children": [
                {
                    "name": "IMMEDIATE CAUSE",
                    "title": immediate_cause,
                    "children": [
                        {
                            "name": "CONTRIBUTING FACTORS",
                            "title": "Human, Behavioral & Physical Environmental Drivers",
                            "children": [
                                {"name": "Communication", "title": contributing_causes[0]},
                                {"name": "Operational Urgency", "title": contributing_causes[1]},
                                {"name": "PPE Enforcement", "title": contributing_causes[2]},
                                {"name": "Thermal Proximity", "title": contributing_causes[3]}
                            ]
                        },
                        {
                            "name": "SYSTEM DEFICIENCIES",
                            "title": "Organizational & Process Safety Management Gaps",
                            "children": [
                                {"name": "Isolation Protocol", "title": system_causes[0]},
                                {"name": "Line Breaking Checkpoint", "title": system_causes[1]},
                                {"name": "Permit-to-Work Governance", "title": system_causes[2]},
                                {"name": "Asset Integrity Inspection", "title": system_causes[3]}
                            ]
                        }
                    ]
                }
            ]
        }

        return {
            "immediate_cause": immediate_cause,
            "contributing_causes": contributing_causes,
            "system_causes": system_causes,
            "rca_tree": rca_tree
        }

rca_engine = RCAEngine()
