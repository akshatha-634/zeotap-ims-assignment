from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

NAVY = colors.HexColor('#0a2463')
LIGHT_NAVY = colors.HexColor('#f0f4ff')

doc = SimpleDocTemplate(
    "Akshatha Poojari - Infrastructure SRE Intern Assignment.pdf",
    pagesize=A4,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('title', fontSize=15, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY, spaceAfter=4)
subtitle_style = ParagraphStyle('subtitle', fontSize=10, fontName='Helvetica', alignment=TA_CENTER, textColor=colors.HexColor('#333333'), spaceAfter=3)
heading_style = ParagraphStyle('heading', fontSize=13, fontName='Helvetica-Bold', textColor=NAVY, spaceBefore=14, spaceAfter=5)
body_style = ParagraphStyle('body', fontSize=10, fontName='Helvetica', spaceAfter=4, leading=14)
code_style = ParagraphStyle('code', fontSize=8, fontName='Courier', textColor=colors.HexColor('#333333'), backColor=colors.HexColor('#f5f5f5'), spaceAfter=4, leading=12)
caption_style = ParagraphStyle('caption', fontSize=9, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY, spaceAfter=8)

story = []

# Title
story.append(Spacer(1, 6))
story.append(Paragraph("Incident Management System", title_style))
story.append(Paragraph("Infrastructure / SRE Intern Assignment — Zeotap", subtitle_style))
story.append(Paragraph("Akshatha Poojari", subtitle_style))
story.append(Paragraph("GitHub: https://github.com/akshatha-634/zeotap-ims-assignment", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY))
story.append(Spacer(1, 10))

# Overview
story.append(Paragraph("1. Overview", heading_style))
story.append(Paragraph(
    "A resilient, production-grade Incident Management System (IMS) designed to monitor a complex distributed stack. "
    "The system intelligently ingests high-volume signals, processes and stores them, alerts the right responders, "
    "and provides a workflow-driven UI to track incidents to a Closed state with mandatory Root Cause Analysis (RCA).",
    body_style
))

# Tech Stack
story.append(Paragraph("2. Tech Stack Choices", heading_style))
tech_data = [
    ['Layer', 'Technology', 'Reason'],
    ['Frontend', 'React', 'Component-based UI, real-time state updates'],
    ['Backend', 'FastAPI (Python)', 'Async support, auto docs, high performance'],
    ['Cache', 'Redis', 'Hot path state, fast reads'],
    ['NoSQL', 'MongoDB', 'Raw signal storage (Data Lake)'],
    ['Containerization', 'Docker + Compose', 'Reproducible, isolated deployments'],
]
tech_table = Table(tech_data, colWidths=[1.2*inch, 1.8*inch, 3.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_NAVY]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('PADDING', (0,0), (-1,-1), 6),
]))
story.append(tech_table)

# Architecture
story.append(Paragraph("3. Architecture", heading_style))
story.append(Paragraph("The system follows a layered architecture with clear separation of concerns:", body_style))
arch_text = "FRONTEND (React) -- Live Dashboard | Raw Signals | RCA Form<br/>        |<br/>        | HTTP/REST<br/>        |<br/>BACKEND (FastAPI)<br/>  |- Signal Ingestion + Debounce Engine<br/>  |- Workflow State Machine (OPEN-&gt;INVESTIGATING-&gt;RESOLVED-&gt;CLOSED)<br/>  |- Health &amp; Throughput Metrics<br/>        |<br/>  MongoDB (NoSQL) | Redis (Cache) | In-Memory (Data Lake)"
story.append(Paragraph(arch_text, code_style))

# Key Features
story.append(Paragraph("4. Key Features", heading_style))
features = [
    ("Signal Debouncing", "If multiple signals arrive for the same Component ID within 10 seconds, only ONE Work Item is created. All signals are linked to it in the audit log. This prevents alert storms from creating duplicate incidents."),
    ("Workflow State Machine", "Incidents follow strict transitions: OPEN → INVESTIGATING → RESOLVED → CLOSED. Invalid transitions return HTTP 400. This ensures proper incident handling process."),
    ("Mandatory RCA", "The system rejects any attempt to move a Work Item to CLOSED if the RCA object is missing or incomplete. Fields required: Incident Start/End, Root Cause Category, Fix Applied, Prevention Steps."),
    ("Backpressure Handling", "In-memory signal processing handles burst traffic. The system won't crash if the persistence layer is slow — signals are buffered in memory first."),
    ("Observability", "/health endpoint for liveness checks. Throughput metrics (signals/sec) displayed on dashboard every 5 seconds. Raw signal audit log retained for forensics."),
]
for title, desc in features:
    story.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

# API Endpoints
story.append(Paragraph("5. API Endpoints", heading_style))
api_data = [
    ['Method', 'Endpoint', 'Description'],
    ['POST', '/api/ingest', 'Ingest a new signal'],
    ['GET', '/api/work-items', 'Get all work items'],
    ['GET', '/api/signals/raw', 'Get raw signal log (Data Lake)'],
    ['PATCH', '/api/work-items/{id}/status', 'Update work item status'],
    ['GET', '/api/throughput', 'Get signals/sec throughput'],
    ['GET', '/health', 'Health check endpoint'],
]
api_table = Table(api_data, colWidths=[0.8*inch, 2.5*inch, 3.2*inch])
api_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_NAVY]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('PADDING', (0,0), (-1,-1), 6),
]))
story.append(api_table)

# Screenshots
story.append(Paragraph("6. Application Screenshots", heading_style))

screenshots = [
    ("Dashboard.png", "Dashboard — Active Incidents sorted by severity (P0, P1, P2)"),
    ("Raw Signals.png", "Raw Signals Tab — Audit log of all incoming signals"),
    ("RCA form.png", "RCA Form — Mandatory Root Cause Analysis before closing"),
    ("Closed (RCA).png", "Incident Closed — After successful RCA submission"),
    ("FastAPI docs.png", "FastAPI Auto Docs — All API endpoints"),
]

for filename, caption in screenshots:
    filepath = f"/home/akshatha/zeotap-ims-assignment/{filename}"
    if os.path.exists(filepath):
        img = Image(filepath, width=6*inch, height=3.2*inch)
        story.append(img)
        story.append(Paragraph(caption, caption_style))
        story.append(Spacer(1, 6))

# Project Structure
story.append(Paragraph("7. Repository Structure", heading_style))
structure = "zeotap-ims-assignment/<br/>├── backend/<br/>│   ├── main.py -- FastAPI entry point<br/>│   ├── requirements.txt<br/>│   ├── Dockerfile<br/>│   ├── sample_data.py -- Mock failure simulator<br/>│   └── app/<br/>│       ├── routes/signals.py<br/>│       ├── models/signal.py<br/>│       └── services/signal_service.py<br/>├── frontend/<br/>│   ├── src/App.js -- React dashboard<br/>│   └── Dockerfile<br/>├── docker-compose.yml<br/>└── README.md"
story.append(Paragraph(structure, code_style))

# Footer
story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY))
story.append(Spacer(1, 6))
story.append(Paragraph("GitHub: https://github.com/akshatha-634/zeotap-ims-assignment", 
    ParagraphStyle('link', fontSize=11, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY)))
story.append(Paragraph("Akshatha Poojari | akshathapoojari.cloud@gmail.com", subtitle_style))

doc.build(story)
print("PDF created successfully!")