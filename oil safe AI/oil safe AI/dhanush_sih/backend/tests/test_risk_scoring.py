import pytest
from app.ml.risk_scorer import risk_scoring_engine

def test_risk_scoring_bounds():
    # Test lower bound clamping
    res_low = risk_scoring_engine.calculate_score(
        narrative="Routine cleaning with no tools or chemicals.",
        lsr_violations=[],
        sif_result={"is_sif_precursor": False},
        immediate_actions="emergency stop applied promptly and isolated promptly"
    )
    assert res_low["final_score"] >= 0.0
    assert res_low["final_score"] <= 100.0

    # Test upper bound clamping
    dummy_violations = [
        {"rule_code": "LSR #1", "evidence": "no isolation"},
        {"rule_code": "LSR #3", "evidence": "no permit"},
        {"rule_code": "LSR #5", "evidence": "no ppe"},
        {"rule_code": "LSR #2", "evidence": "confined space"},
        {"rule_code": "LSR #4", "evidence": "interlock bypass"},
        {"rule_code": "LSR #6", "evidence": "hot work"},
        {"rule_code": "LSR #7", "evidence": "fall"},
        {"rule_code": "LSR #8", "evidence": "lifting"},
        {"rule_code": "LSR #9", "evidence": "driving"}
    ]
    res_high = risk_scoring_engine.calculate_score(
        narrative="250 bar pressurized joint thermal burn explosion fatality hazard",
        lsr_violations=dummy_violations,
        sif_result={"is_sif_precursor": True},
        immediate_actions=""
    )
    assert res_high["final_score"] <= 100.0
    assert res_high["risk_level"] == "CRITICAL"

def test_unit3_incident_scoring():
    narrative = (
        "A technician attempted unauthorized repair of a pressurized flanged joint rated at 250 bar "
        "without depressurization or supervisor notification. The flanged joint had a hairline crack. "
        "Oil sprayed from the damaged connection and ignited after contacting a nearby hot surface at approximately 140°C. "
        "The technician suffered a thermal burn. The equipment had deteriorated conditions and inadequate pressure-relief isolation. "
        "The technician was working without a face shield and proper gloves. The fire suppression system responded."
    )
    lsr_violations = [
        {"rule_code": "LSR #1", "evidence": "Worked on 250 bar pressure system without depressurization"},
        {"rule_code": "LSR #3", "evidence": "Unauthorized repair without supervisor notification"},
        {"rule_code": "LSR #5", "evidence": "Working without face shield and proper gloves"}
    ]
    sif_res = {
        "is_sif_precursor": True,
        "category": "Energy Isolation",
        "rationale": "High-energy precursor detected"
    }

    result = risk_scoring_engine.calculate_score(
        narrative=narrative,
        lsr_violations=lsr_violations,
        sif_result=sif_res,
        equipment_condition="Deteriorated conditions and inadequate pressure-relief isolation",
        ppe_condition="Working without a face shield and proper gloves",
        immediate_actions="The fire suppression system responded."
    )

    # Expected: Base 70 + LSR1(10) + LSR3(8) + LSR5(5) + Burn(5) + SIF(4) - FireSuppression(10) = 87.0 (or ~87-92)
    assert result["final_score"] == 87.0
    assert result["risk_level"] == "CRITICAL"
