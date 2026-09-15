import pytest
from app.ml.sif_classifier import sif_classifier
from app.ml.lsr_detector import lsr_detector

def test_sif_precursor_detection():
    narrative = (
        "A technician attempted unauthorized repair of a pressurized flanged joint rated at 250 bar "
        "without depressurization or supervisor notification. The flanged joint had a hairline crack. "
        "Oil sprayed from the damaged connection and ignited after contacting a nearby hot surface at approximately 140°C."
    )
    sif_out = sif_classifier.evaluate(narrative)
    assert sif_out["is_sif_precursor"] is True
    assert sif_out["confidence"] >= 0.90
    assert sif_out["severity"] == "CRITICAL"

def test_lsr_violation_detection():
    narrative = "A technician attempted unauthorized repair of a pressurized flanged joint rated at 250 bar without depressurization or supervisor notification."
    ppe = "The technician was working without a face shield and proper gloves."
    violations = lsr_detector.detect_violations(narrative, ppe_condition=ppe)

    violated_codes = [v["rule_code"] for v in violations]
    assert "LSR #1" in violated_codes # Energy Isolation
    assert "LSR #3" in violated_codes # Authorization & Supervision
    assert "LSR #5" in violated_codes # Personal Protection
