import io
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.database.session import get_db
from app.database.models import Incident
from app.api.analysis import analyze_incident

router = APIRouter(prefix="/reports", tags=["Report Generator"])

@router.get("/{incident_id}/json")
def export_incident_report_json(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    return JSONResponse(content=data)

@router.get("/{incident_id}/html", response_class=HTMLResponse)
def export_incident_report_html(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>OIL-SAFE AI Safety Incident Investigation Report - {data['incident_id']}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0b0f19; color: #e2e8f0; margin: 0; padding: 40px; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #131b2e; border: 1px solid #1e293b; border-radius: 12px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ef4444; padding-bottom: 20px; }}
            .badge-critical {{ background: #ef4444; color: #fff; padding: 6px 14px; border-radius: 6px; font-weight: bold; }}
            .score-box {{ background: #1e293b; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0; }}
            h1, h2, h3 {{ color: #f8fafc; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #334155; padding: 10px; text-align: left; }}
            th {{ background: #1e293b; color: #38bdf8; }}
            .btn-print {{ background: #38bdf8; color: #000; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; }}
            @media print {{ .no-print {{ display: none; }} body {{ background: #fff; color: #000; }} .container {{ border: none; background: #fff; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="no-print" style="text-align: right; margin-bottom: 20px;">
                <button class="btn-print" onclick="window.print()">Print / Save as PDF</button>
            </div>
            <div class="header">
                <div>
                    <h1>🚨 OIL-SAFE AI — Industrial Incident Safety Report</h1>
                    <p style="color: #94a3b8;">Incident ID: {data['incident_id']} | Date: {data['date']}</p>
                </div>
                <div class="badge-critical">
                    RISK SCORE: {data['risk_score']}/100 ({data['risk_level']})
                </div>
            </div>

            <div class="score-box">
                <h3>Executive Summary</h3>
                <p><strong>Location:</strong> {data['location']} | <strong>Department:</strong> {data['department']} | <strong>Asset:</strong> {data['asset']}</p>
                <p><strong>SIF Precursor:</strong> {'DETECTED' if data['sif_precursor'] else 'NO'} ({data['sif_category']} - Confidence: {int(data['confidence']*100)}%)</p>
                <p><strong>Primary Hazard:</strong> {data['primary_hazard']} | <strong>Injury:</strong> {data.get('injury', 'None')}</p>
            </div>

            <h2>1. Life-Saving Rule (LSR) Violations</h2>
            <table>
                <tr><th>Rule</th><th>Name</th><th>Severity</th><th>Evidence</th></tr>
                {''.join([f"<tr><td>{v['rule']}</td><td>{v['name']}</td><td style='color:#ef4444;font-weight:bold;'>{v['severity']}</td><td>{v['evidence']}</td></tr>" for v in data['lsr_violations']])}
            </table>

            <h2>2. SHAP Risk Factor Attribution Waterfall</h2>
            <table>
                <tr><th>Factor Name</th><th>Contribution</th><th>Type</th><th>Evidence Snippet</th></tr>
                {''.join([f"<tr><td>{f['factor_name']}</td><td style='font-weight:bold;color:{'#ef4444' if f['contribution']>0 else '#10b981'}'>{'+' if f['contribution']>0 else ''}{f['contribution']}</td><td>{f['factor_type']}</td><td>{f.get('evidence_snippet','')}</td></tr>" for f in data['risk_factors']])}
            </table>

            <h2>3. Root Cause Analysis (RCA)</h2>
            <div style="background:#0f172a; padding:15px; border-radius:8px;">
                <p><strong>Immediate Cause:</strong> {data['root_causes']['immediate_cause']}</p>
                <p><strong>Contributing Causes:</strong></p>
                <ul>{''.join([f"<li>{c}</li>" for c in data['root_causes']['contributing_causes']])}</ul>
                <p><strong>System Deficiencies:</strong></p>
                <ul>{''.join([f"<li>{s}</li>" for s in data['root_causes']['system_causes']])}</ul>
            </div>

            <h2>4. Immediate Emergency Response Protocols</h2>
            <ul>{''.join([f"<li>{act}</li>" for act in data['emergency_actions']])}</ul>

            <h2>5. Evidence-Based Corrective & Preventive Recommendations</h2>
            <ul>{''.join([f"<li>{rec}</li>" for rec in data['recommendations']])}</ul>

            <div style="margin-top:40px; border-top: 1px solid #334155; padding-top: 20px; font-size:12px; color:#64748b;">
                Generated by OIL-SAFE AI Industrial Safety Command Center | Decision Support Tool
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@router.get("/{incident_id}/pdf")
def export_incident_report_pdf(incident_id: int, db: Session = Depends(get_db)):
    data = analyze_incident(incident_id, db)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    story = []
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#B91C1C'),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story.append(Paragraph(f"OIL-SAFE AI — Industrial Safety Incident Report", title_style))
    story.append(Paragraph(f"<b>Incident ID:</b> {data['incident_id']} | <b>Date:</b> {data['date']} | <b>Risk Score:</b> {data['risk_score']}/100 ({data['risk_level']})", body_style))
    story.append(Paragraph(f"<b>Location:</b> {data['location']} | <b>Asset:</b> {data['asset']}", body_style))
    story.append(Paragraph(f"<b>SIF Precursor:</b> YES (Category: {data['sif_category']} - Confidence: {int(data['confidence']*100)}%)", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Life-Saving Rule Violations", h2_style))
    lsr_table_data = [["Rule", "Name", "Severity", "Evidence"]]
    for v in data['lsr_violations']:
        lsr_table_data.append([v['rule'], v['name'], v['severity'], v['evidence'][:60] + "..."])
    
    t_lsr = Table(lsr_table_data, colWidths=[60, 120, 70, 270])
    t_lsr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8)
    ]))
    story.append(t_lsr)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Root Cause Analysis (Immediate & System Causes)", h2_style))
    story.append(Paragraph(f"<b>Immediate Cause:</b> {data['root_causes']['immediate_cause']}", body_style))
    story.append(Paragraph("<b>System Causes:</b>", body_style))
    for sc in data['root_causes']['system_causes']:
        story.append(Paragraph(f"• {sc}", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Immediate Emergency Response Protocols", h2_style))
    for act in data['emergency_actions']:
        story.append(Paragraph(f"• {act}", body_style))

    doc.build(story)
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=OIL-SAFE-Report-{data['incident_id']}.pdf"}
    )
