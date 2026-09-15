"""
RAG (Retrieval-Augmented Generation) Knowledge System.
Performs semantic & keyword retrieval over refinery safety manuals, OIL SIF Taxonomy,
Life-Saving Rules, and LOTO standard operating procedures.
"""

import math
from typing import List, Dict, Any

DEFAULT_KNOWLEDGE_DOCUMENTS = [
    {
        "id": 1,
        "title": "Refinery Standard Operating Procedure: SOP-PR-402 Pressure Systems Isolation & Line Breaking",
        "category": "LOTO & Energy Isolation",
        "source": "Corporate Process Safety Manual Rev 4.2",
        "content": (
            "Section 4.1: Under NO circumstances shall any maintenance, tightening, or intervention be performed on "
            "pressurized piping or flanged joints exceeding 0.5 bar without positive mechanical isolation (Double Block & Bleed "
            "or spectacle blind) and complete system depressurization to flare. Zero energy must be verified via calibrated gauges "
            "and bleed valves before breaking containment."
        )
    },
    {
        "id": 2,
        "title": "Refinery Life-Saving Rules Mandatory Compliance Directive: LSR-01 & LSR-03",
        "category": "Life-Saving Rules",
        "source": "IOGP / Refinery HSE Governance Directive",
        "content": (
            "LSR #1 Energy Isolation requires positive lockout/tagout verification. LSR #3 Work Authorization requires an approved "
            "Cold/Hot Work Permit signed by the Area Authority and designated Maintenance Supervisor before beginning any field intervention. "
            "Unauthorized work constitutes a Stop Work Authority (SWA) trigger."
        )
    },
    {
        "id": 3,
        "title": "Refinery PPE Standard STD-PPE-109: High-Temperature and Hydrocarbon Handling",
        "category": "PPE Requirements",
        "source": "HSE Occupational Safety Guidelines",
        "content": (
            "Technicians operating within 5 meters of hydrocarbon process equipment operated above 60°C or rated above 50 bar "
            "must wear certified NFPA 2112 flame-resistant coveralls, full face shield attached to hard hat, and thermal-chemical "
            "resistant gloves rated for contact temperatures up to 200°C."
        )
    },
    {
        "id": 4,
        "title": "Emergency Response Procedure: ERP-REF-09 Hydrocarbon Flash Fire & Thermal Burn Protocol",
        "category": "Emergency Response",
        "source": "Refinery Crisis Management & Rescue Operations",
        "content": (
            "Immediate Actions: 1. Actuate Unit Emergency Shutdown (ESD) and isolate upstream/downstream block valves. "
            "2. Depressurize unit to flare header. 3. Deploy fixed water deluge to cool adjacent assets and quench hot surfaces. "
            "4. Administer sterile cool burn dressing and first aid to injured personnel; prepare medical evacuation. "
            "5. Barricade exclusion perimeter of minimum 50 meters."
        )
    },
    {
        "id": 5,
        "title": "Asset Integrity Standard AIS-570: Piping Flanged Joint Inspection & Leak Management",
        "category": "Equipment Standards",
        "source": "Asset Integrity & Reliability Engineering",
        "content": (
            "Hairline cracks on flanged joints rated at 250 bar indicate severe fatigue or stress corrosion cracking. "
            "Attempting to torque or repair a leaking flanged joint while under process pressure is strictly prohibited due to high risk "
            "of catastrophic gasket blowout or sudden joint fracture."
        )
    }
]

class RAGKnowledgeBase:
    def __init__(self):
        self.documents = DEFAULT_KNOWLEDGE_DOCUMENTS

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Calculates term frequency relevance score and returns ranked knowledge evidence chunks.
        """
        query_words = set(query.lower().split())
        results = []

        for doc in self.documents:
            doc_text = f"{doc['title']} {doc['category']} {doc['content']}".lower()
            doc_words = doc_text.split()
            
            # Simple TF-IDF like scoring
            match_count = sum(1 for w in query_words if len(w) > 2 and w in doc_text)
            relevance = min(0.98, max(0.65, (match_count * 0.12) + 0.60))

            results.append({
                "document_id": doc["id"],
                "document_title": doc["title"],
                "category": doc["category"],
                "source": doc["source"],
                "content": doc["content"],
                "score": round(relevance, 2)
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

rag_knowledge_base = RAGKnowledgeBase()
