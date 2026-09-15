"""
SIF Classifier (Serious Injury and Fatality Precursor Engine)
Evaluates narrative reports against OIL SIF Taxonomy high-energy criteria.
"""

from typing import Dict, Any, List
from app.safety.taxonomy import OIL_SIF_CATEGORIES

class SIFClassifier:
    def __init__(self):
        self.categories = OIL_SIF_CATEGORIES

    def evaluate(self, text: str, equipment_condition: str = "", immediate_actions: str = "") -> Dict[str, Any]:
        """
        Evaluates report narrative and returns structured SIF Precursor decision.
        """
        combined_text = f"{text} {equipment_condition} {immediate_actions}".lower()
        matched_categories = []

        for key, cat_data in self.categories.items():
            match_count = sum(1 for kw in cat_data["keywords"] if kw in combined_text)
            if match_count > 0:
                matched_categories.append({
                    "key": key,
                    "id": cat_data["id"],
                    "name": cat_data["name"],
                    "criticality": cat_data["criticality"],
                    "high_energy_source": cat_data["high_energy_source"],
                    "potential_consequence": cat_data["potential_consequence"],
                    "score": match_count
                })

        # Sort by match strength and criticality
        matched_categories.sort(key=lambda x: (x["criticality"] == "CRITICAL", x["score"]), reverse=True)

        if matched_categories:
            primary = matched_categories[0]
            # If high energy breach at 250 bar or thermal burn, high confidence SIF
            confidence = 0.94 if ("250 bar" in combined_text or "burn" in combined_text or "crack" in combined_text) else 0.88
            return {
                "is_sif_precursor": True,
                "category": primary["name"],
                "category_id": primary["id"],
                "confidence": confidence,
                "severity": primary["criticality"],
                "potential_severity": "FATALITY / PERMANENT DISABILITY",
                "energy_source": primary["high_energy_source"],
                "rationale": f"High-energy precursor detected: {primary['name']} with potential for {primary['potential_consequence']}.",
                "all_matched_categories": [m["name"] for m in matched_categories]
            }
        else:
            return {
                "is_sif_precursor": False,
                "category": "None",
                "category_id": "SIF-00",
                "confidence": 0.91,
                "severity": "LOW",
                "potential_severity": "FIRST AID ONLY",
                "energy_source": "Low Energy System",
                "rationale": "No catastrophic high-energy precursor conditions identified in the narrative.",
                "all_matched_categories": []
            }

sif_classifier = SIFClassifier()
