"""
OIL SIF Taxonomy (Serious Injury and Fatality Precursor System)
Defines high-energy hazards, SIF categories, threshold criteria, and precursor triggers.
"""

OIL_SIF_CATEGORIES = {
    "ENERGY_ISOLATION": {
        "id": "SIF-01",
        "name": "Energy Isolation",
        "keywords": ["depressurization", "isolation", "loto", "lockout", "tagout", "pressurized", "250 bar", "bar", "valve closed", "zero energy", "blind flange", "residual pressure"],
        "high_energy_source": "Stored Mechanical / Hydraulic / Pressure Potential Energy",
        "criticality": "CRITICAL",
        "potential_consequence": "Catastrophic breach, projectile ejection, acute blast or uncontrolled hydrocarbon release"
    },
    "WORKING_AT_HEIGHT": {
        "id": "SIF-02",
        "name": "Working at Height",
        "keywords": ["fall", "height", "scaffold", "harness", "lanyard", "ladder", "roof", "opening", "fall arrest", "platform edge", "drop object"],
        "high_energy_source": "Gravitational Potential Energy (> 1.8m)",
        "criticality": "CRITICAL",
        "potential_consequence": "Fatal impact or severe polytrauma from elevation fall"
    },
    "LINE_OF_FIRE": {
        "id": "SIF-03",
        "name": "Line of Fire",
        "keywords": ["line of fire", "projectile", "under load", "pinch point", "stored energy", "sprayed", "blowout", "high pressure jet", "whip"],
        "high_energy_source": "Kinetic / Pressurized Trajectory Discharge",
        "criticality": "CRITICAL",
        "potential_consequence": "Severe crushing, impalement, or fatal impact"
    },
    "CONFINED_SPACE": {
        "id": "SIF-04",
        "name": "Confined Space",
        "keywords": ["confined space", "vessel entry", "tank", "toxic gas", "h2s", "oxygen deficient", "asphyxiation", "entry permit", "air monitoring"],
        "high_energy_source": "Atmospheric Toxicity / Asphyxiating Environment",
        "criticality": "CRITICAL",
        "potential_consequence": "Immediate toxic asphyxiation or acute incapacitation"
    },
    "HOT_WORK": {
        "id": "SIF-05",
        "name": "Hot Work & Thermal Ignition",
        "keywords": ["hot work", "welding", "ignited", "ignition", "spark", "flame", "hot surface", "140°c", "combustible", "fire suppression", "flash fire", "vapor cloud"],
        "high_energy_source": "Thermal / Ignition of Flammable Atmospheres",
        "criticality": "CRITICAL",
        "potential_consequence": "Hydrocarbon flash fire, thermal explosion, massive burn trauma"
    },
    "LIFTING_OPERATIONS": {
        "id": "SIF-06",
        "name": "Lifting Operations",
        "keywords": ["crane", "rigging", "suspended load", "hoist", "sling", "lift plan", "overload", "drop load"],
        "high_energy_source": "Heavy Suspended Mass (> 500kg)",
        "criticality": "HIGH",
        "potential_consequence": "Crush trauma from dropped suspended load"
    },
    "VEHICLE_INTERACTION": {
        "id": "SIF-07",
        "name": "Vehicle Interaction",
        "keywords": ["heavy vehicle", "forklift", "truck", "pedestrian", "collision", "blind spot", "run over", "speeding"],
        "high_energy_source": "Mobile Heavy Equipment Kinetic Energy",
        "criticality": "HIGH",
        "potential_consequence": "Fatal vehicular impact or rollover"
    },
    "PRESSURE_SYSTEMS": {
        "id": "SIF-08",
        "name": "Pressure Systems & Containment",
        "keywords": ["flanged joint", "crack", "hairline crack", "pressurized", "psi", "bar", "relief valve", "overpressure", "rupture disc", "loss of containment", "deteriorated conditions"],
        "high_energy_source": "Extreme Fluid / Gas Static & Dynamic Pressure (> 10 bar / 250 bar)",
        "criticality": "CRITICAL",
        "potential_consequence": "Loss of Primary Containment (LOPC), toxic/flammable jet spray, explosion"
    },
    "ELECTRICAL_ENERGY": {
        "id": "SIF-09",
        "name": "Electrical Energy",
        "keywords": ["arc flash", "high voltage", "electrocution", "switchgear", "transformer", "energized", "grounding", "substation"],
        "high_energy_source": "High Voltage Electrical Potential (> 50V / Arc Flash)",
        "criticality": "CRITICAL",
        "potential_consequence": "Fatal electrocution or massive arc blast thermal injury"
    },
    "HAZARDOUS_CHEMICALS": {
        "id": "SIF-10",
        "name": "Hazardous Chemicals & Toxic Release",
        "keywords": ["h2s", "hydrofluoric", "caustic", "acid", "toxic leak", "chemical burn", "inhalation", "benzene"],
        "high_energy_source": "Acute Toxicity / Corrosive Chemistry",
        "criticality": "CRITICAL",
        "potential_consequence": "Chemical necrosis, organ failure, pulmonary edema"
    },
    "EQUIPMENT_INTEGRITY": {
        "id": "SIF-11",
        "name": "Equipment Integrity & Structural Degradation",
        "keywords": ["deteriorated", "corrosion", "crack", "flange", "fatigue", "inadequate relief", "bypass", "interlock bypassed"],
        "high_energy_source": "Structural / Safety Barrier Mechanical Failure",
        "criticality": "HIGH",
        "potential_consequence": "Catastrophic structural collapse or barrier failure"
    }
}
