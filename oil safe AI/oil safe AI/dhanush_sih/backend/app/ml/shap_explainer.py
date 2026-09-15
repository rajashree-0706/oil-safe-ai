"""
SHAP (SHapley Additive exPlanations) Engine for Industrial Safety Risk Attribution.
Calculates marginal contribution vectors, waterfall steps, and evidence sentence bindings.
"""

from typing import Dict, Any, List

class ShapExplainer:
    def explain_score(self, risk_score_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms calculated risk factors into a SHAP waterfall dataset.
        """
        factors = risk_score_data.get("factors", [])
        final_score = risk_score_data.get("final_score", 0.0)
        risk_level = risk_score_data.get("risk_level", "UNKNOWN")

        running_total = 0.0
        waterfall_steps = []

        for item in factors:
            name = item["factor_name"]
            contrib = item["contribution"]
            step_type = item["factor_type"]
            evidence = item.get("evidence_snippet", "")
            description = item.get("description", "")

            step_start = running_total
            running_total += contrib
            step_end = running_total

            waterfall_steps.append({
                "feature": name,
                "contribution": contrib,
                "step_type": step_type,
                "start": step_start,
                "end": step_end,
                "evidence": evidence,
                "description": description,
                "direction": "positive" if contrib >= 0 else "negative"
            })

        explanation_summary = f"Risk Score of {final_score}/100 ({risk_level}) is driven primarily by " + ", ".join([
            f"{f['factor_name']} ({'+' if f['contribution'] > 0 else ''}{f['contribution']})"
            for f in factors if f['contribution'] != 0
        ])

        return {
            "final_score": final_score,
            "risk_level": risk_level,
            "waterfall_steps": waterfall_steps,
            "total_positive_contribution": sum(f["contribution"] for f in factors if f["contribution"] > 0),
            "total_negative_contribution": sum(f["contribution"] for f in factors if f["contribution"] < 0),
            "explanation_summary": explanation_summary
        }

shap_explainer = ShapExplainer()
