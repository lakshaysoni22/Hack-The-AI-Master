import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that performs two passes to dynamically compute total pages and add headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip cover page
            return
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(54, 11 * inch - 36, "HACK THE AI — COMPLETE TECHNICAL PROJECT REPORT")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "PRO INVESTIGATION PLATFORM")
        self.setStrokeColor(colors.HexColor("#0284c7"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Confidential — Designed & Developed by Lakshay Soni")
        self.drawRightString(8.5 * inch - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def create_report(output_filename="HACK_THE_AI_COMPLETE_PROJECT_REPORT.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    c_primary = colors.HexColor("#0369a1")    # Deep Cyber Blue
    c_accent = colors.HexColor("#0284c7")     # Bright Blue
    c_secondary = colors.HexColor("#0f172a")  # Dark Slate
    c_text = colors.HexColor("#1e293b")       # Deep Charcoal Body Text
    c_muted = colors.HexColor("#64748b")      # Muted Gray
    c_border = colors.HexColor("#cbd5e1")     # Border Gray
    c_bg_light = colors.HexColor("#f8fafc")   # Card BG

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#0f172a"),
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=16,
        textColor=c_primary,
        alignment=0
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=c_secondary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_text,
        leftIndent=12,
        spaceAfter=3.5
    )

    code_style = ParagraphStyle(
        'ReportCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'ReportCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_secondary
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    fig_caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10.5,
        textColor=c_muted,
        alignment=1,
        spaceBefore=3,
        spaceAfter=8
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    
    banner_data = [[
        Paragraph("<b>CYBERSECURITY × AI × WEB3 × IoT INCIDENT FORENSICS</b>", ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.HexColor("#0284c7"), letterSpacing=1.2))
    ]]
    banner_tab = Table(banner_data, colWidths=[504])
    banner_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f9ff")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(banner_tab)
    story.append(Spacer(1, 16))
    
    story.append(Paragraph("HACK THE AI", title_style))
    story.append(Paragraph("Complete Technical Project Architecture & Investigation Specification Report", ParagraphStyle('CoverSub', parent=title_style, fontSize=15, leading=19, textColor=c_primary, spaceBefore=4)))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph(
        "An enterprise-grade, story-driven cyber investigation and adversarial simulation platform engineered to train modern security professionals on complex multi-layer breaches spanning Distributed Ledgers (Web3), Artificial Intelligence (AI Agent Poisoning), Industrial Internet of Things (IoT Gateway Telemetry), and Decentralized Consensus Systems.",
        subtitle_style
    ))
    story.append(Spacer(1, 20))

    meta_data = [
        [Paragraph("<b>Document Version:</b>", table_cell_bold), Paragraph("2.0.0 (Production Release)", table_cell_style)],
        [Paragraph("<b>Target Platform:</b>", table_cell_bold), Paragraph("Hack The AI (Interactive & PRO Labs)", table_cell_style)],
        [Paragraph("<b>Architecture:</b>", table_cell_bold), Paragraph("Flask / SQLAlchemy / Talisman / CSRF / Responsive Workstation OS", table_cell_style)],
        [Paragraph("<b>Author / Lead Architect:</b>", table_cell_bold), Paragraph("Lakshay Soni (Designed & Developed by Lakshay Soni)", table_cell_style)],
        [Paragraph("<b>Investigation Cases Covered:</b>", table_cell_bold), Paragraph("Case NEX-042 (The Ghost in the Ledger) & Case NEX-071 (The Vanishing Consensus)", table_cell_style)],
        [Paragraph("<b>Date of Publication:</b>", table_cell_bold), Paragraph("October 2026", table_cell_style)],
        [Paragraph("<b>Classification:</b>", table_cell_bold), Paragraph("Technical System Documentation / Comprehensive Engineering Report", table_cell_style)]
    ]
    meta_table = Table(meta_data, colWidths=[140, 364])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 24))
    
    callout_data = [[
        Paragraph("<b>CORE PLATFORM HIGHLIGHT:</b> Hack The AI transitions cybersecurity education from isolated trivia into a high-fidelity, simulated cyber operations environment. Investigators interact with multi-window desktop operating systems, realistic packet analyzers, terminal consoles, live IoT feeds, on-chain transaction explorers, and attack graph visualizers.", callout_style)
    ]]
    callout_tab = Table(callout_data, colWidths=[504])
    callout_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (-1,-1), 3, c_primary),
        ('BOX', (0,0), (-1,-1), 0.5, c_border)
    ]))
    story.append(callout_tab)

    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))
    
    toc_items = [
        ("1. Executive Project Overview", "3"),
        ("2. Complete Project Story, Lore & Forensic Concept", "3"),
        ("3. Core Project Objectives & Pedagogy", "4"),
        ("4. Major Implemented Platform Features", "4"),
        ("5. Technology Stack & Implementation Mapping", "5"),
        ("6. High-Level System Architecture", "6"),
        ("7. End-to-End Application Workflow", "7"),
        ("8. Data Flow & Cross-Layer Pipelines", "8"),
        ("9. Database Schema & Storage Architecture", "9"),
        ("10. Authentication, Access Control & Session Security", "10"),
        ("11. Simulated Investigation Workstation Environment", "11"),
        ("12. Lab Architecture & Forensic Case Specifications (Case NEX-042 & NEX-071)", "13"),
        ("13. Gamification Engine: Scoring, XP & Achievement Matrix", "15"),
        ("14. Security Hardening & Platform Protection Architecture", "16"),
        ("15. Multi-Device Responsive Design System", "17"),
        ("16. Cloud Deployment & Serverless WSGI Execution", "18"),
        ("17. Complete Codebase Structure & File Directory", "19"),
        ("18. Project Roadmap & Future Scope", "20"),
        ("19. Conclusion & Final Technical Assessment", "20"),
        ("20. Architectural & Flow Diagrams Reference", "21"),
        ("21. Visual Interface Schematics & Figures", "22"),
        ("22. Technical Verification & Compliance Checklist", "23")
    ]
    
    toc_data = []
    for title, pg in toc_items:
        toc_data.append([
            Paragraph(f"<b>{title}</b>", table_cell_style),
            Paragraph(f"<b>{pg}</b>", ParagraphStyle('R', parent=table_cell_style, alignment=2))
        ])
    
    toc_tab = Table(toc_data, colWidths=[434, 70])
    toc_tab.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 3.8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(toc_tab)
    story.append(PageBreak())

    # =========================================================================
    # 1. PROJECT OVERVIEW
    # =========================================================================
    story.append(Paragraph("1. Executive Project Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "<b>Hack The AI</b> is a cutting-edge, hands-on cybersecurity investigation and training platform created to address the critical vulnerability landscape emerging at the intersection of <b>Artificial Intelligence (AI)</b>, <b>Decentralized Ledgers (Web3)</b>, <b>Industrial Internet of Things (IoT)</b>, and <b>Distributed Consensus Systems</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Problem It Solves:</b> Traditional cybersecurity capture-the-flag (CTF) platforms are largely siloed, focusing strictly on isolated web vulnerabilities (e.g., standard SQLi, XSS) or simple binary exploitation. In real-world enterprise architectures, advanced adversaries orchestrate cross-layer attacks: injecting poisoned telemetry into edge IoT gateways, manipulating autonomous AI risk oracles, abusing over-privileged service roles (RBAC), and causing state forks in decentralized blockchain validators. Hack The AI bridges this crucial training gap by simulating complete, interconnected multi-vector breaches.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Target Users:</b> SOC Analysts (Tier 1-3), AI Security Engineers, Smart Contract Auditors, Web3 Incident Responders, Threat Hunters, and University Cybersecurity Researchers.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Story-Driven Investigation Methodology:</b> Learners do not simply answer disconnected quiz questions. Instead, they assume the role of Lead Cyber Threat Forensics Investigators embedded in an active Security Operations Center (SOC). Every investigation evolves through structured chapters with realistic character dialogues, forensic artifacts, packet traces, on-chain transaction explorers, simulated Burp Suite proxy interceptors, interactive terminals, and dynamic attack graph reconstructions.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 2. COMPLETE PROJECT STORY & FORENSIC LORE
    # =========================================================================
    story.append(Paragraph("2. Complete Project Story, Lore & Forensic Concept", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "The narrative context of Hack The AI centers on modern high-assurance digital ecosystems where automated AI models, smart contracts, and IoT devices operate collaboratively. Across the primary PRO investigations, learners work alongside a specialized SOC response unit:",
        body_style
    ))
    
    chars_data = [
        [Paragraph("<b>Investigator / Role</b>", table_cell_header), Paragraph("<b>Specialization</b>", table_cell_header), Paragraph("<b>Operational Function</b>", table_cell_header)],
        [Paragraph("<b>Lakshay</b>", table_cell_bold), Paragraph("Lead Incident Commander & Forensics Investigator", table_cell_style), Paragraph("Coordinates attack vector triage, root cause synthesis, and containment policy execution.", table_cell_style)],
        [Paragraph("<b>Shivam</b>", table_cell_bold), Paragraph("Web3 & Distributed Systems Analyst", table_cell_style), Paragraph("Deconstructs blockchain transactions, validator consensus states, and bridge contracts.", table_cell_style)],
        [Paragraph("<b>Mehak</b>", table_cell_bold), Paragraph("AI & Data Security Specialist", table_cell_style), Paragraph("Audits neural network inference pipelines, model poisoning traces, and confidence thresholds.", table_cell_style)],
        [Paragraph("<b>Shanu</b>", table_cell_bold), Paragraph("Infrastructure & Telemetry Engineer", table_cell_style), Paragraph("Inspects IoT gateways, raw sensor logs, RBAC access controls, and network traffic.", table_cell_style)],
        [Paragraph("<b>ORION / Sentinel</b>", table_cell_bold), Paragraph("Autonomous AI Decision Engine", table_cell_style), Paragraph("The compromised/poisoned AI system under forensic investigation.", table_cell_style)]
    ]
    chars_table = Table(chars_data, colWidths=[105, 160, 239])
    chars_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(chars_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Case NEX-042: The Ghost in the Ledger:</b> 82,400 NXR tokens vanish from a secured treasury without an alert. The learner discovers that an APT adversary forged an unverified threat intelligence feed (NIF-2038), which poisoned the ORION AI model to output 99.2% confidence, bypassing human settlement approvals via over-privileged RBAC service accounts.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Case NEX-071: The Vanishing Consensus:</b> At 03:12 AM, 184 industrial IoT sensors across 14 sites transmit identical synthetic telemetry (0.00% jitter). The data feeds an upstream Web3 price oracle, causing a 3:2 consensus split across validator nodes. The AI security sentinel reports consensus is healthy because its fine-tuning dataset had been poisoned weeks earlier.",
        bullet_style
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 3. PROJECT OBJECTIVES
    # =========================================================================
    story.append(Paragraph("3. Core Project Objectives & Pedagogy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    objs = [
        "<b>Multi-Vector Attack Literacy:</b> Educate students and practitioners on cross-domain vulnerabilities that cannot be identified by examining single isolated log files.",
        "<b>Active Threat Hunting Simulation:</b> Replace passive video tutorials with active desktop workstations equipped with interactive terminals, log filters, and protocol inspectors.",
        "<b>Adversarial AI Risk Education:</b> Demonstrate practical methods of data poisoning, context injection, and blind model reliance in automated financial and IoT decision pipelines.",
        "<b>Decentralized Consensus Security:</b> Provide direct visibility into validator voting splits, oracle manipulation, and Byzantine Fault Tolerance under corrupted data streams.",
        "<b>Gamified Progression & Skill Retention:</b> Reward thorough investigative rigor using XP, persistent skill badges, interactive capstone certifications, and global leaderboards."
    ]
    for obj in objs:
        story.append(Paragraph(f"• {obj}", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 4. MAJOR FEATURES
    # =========================================================================
    story.append(Paragraph("4. Major Implemented Platform Features", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    feats = [
        ("Authentication & Session Management", "Role-based authorization (Student / Admin), CSRF-protected forms, persistent secret key derivation, and demo credentials on login."),
        ("SOC Dashboard", "Overview of current active investigations, total XP earned, completed lab counts, real-time activity feed, and quick-launch workstations."),
        ("Interactive Lab & PRO Lab Catalog", "Categorized lab selection supporting foundational cyber challenges, manual containerized labs, and flagship multi-layer PRO investigations."),
        ("Desktop Workstation OS", "A complete in-browser multi-window GUI featuring draggable and stackable windows, taskbar switching, traffic lights, and minimize/maximize states."),
        ("Simulated Burp Suite Inspector", "Tabbed HTTP/RPC traffic inspection including Proxy history, Request/Response dual-pane viewer, Repeater, and Target host tree."),
        ("Forensic Terminal Console", "Command-line interface supporting tools like 'whoami', 'pwd', 'grep', 'python', 'iot-telemetry', 'oracle', 'policy', and 'evidence'."),
        ("Live Case File Manager", "Direct access to raw audit logs, configuration policies, smart contract ABIs, bridge manifests, and intelligence feeds."),
        ("Dynamic Attack Graph", "Interactive SVG/Node visualization tracking attacker ingress, pivot points, AI poisoning nodes, and root compromise state."),
        ("Evidence Locker & Progress Engine", "Automatic collection and persistent tracking of forensic evidence tokens (AI-E01, AI-E02, etc.) unlocking progressive chapters."),
        ("Automated Hint System", "Tiered progressive hints providing targeted investigation guidance when learners encounter complex forensic steps."),
        ("Comprehensive Capstone Certification", "Multi-question final evaluation quizzes testing conceptual mastery before awarding full case completion XP and master flags."),
        ("Global Leaderboard & Learning Paths", "Real-time user rankings by XP score and structured learning roadmaps spanning Web3, AI Security, and DevSecOps.")
    ]
    
    for f_title, f_desc in feats:
        story.append(Paragraph(f"<b>{f_title}:</b> {f_desc}", bullet_style))
    
    story.append(PageBreak())

    # =========================================================================
    # 5. TECHNOLOGY STACK
    # =========================================================================
    story.append(Paragraph("5. Technology Stack & Implementation Mapping", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    tech_data = [
        [Paragraph("<b>Layer</b>", table_cell_header), Paragraph("<b>Technology / Library</b>", table_cell_header), Paragraph("<b>Concrete Implementation & Purpose in Project</b>", table_cell_header)],
        [Paragraph("<b>Backend Core</b>", table_cell_bold), Paragraph("Python 3.12 / Flask 3.0", table_cell_style), Paragraph("Core WSGI application server, Blueprint routing architecture, application factory pattern.", table_cell_style)],
        [Paragraph("<b>Database & ORM</b>", table_cell_bold), Paragraph("SQLAlchemy / Flask-Migrate", table_cell_style), Paragraph("Relational schema management, SQLite persistence (with /tmp serverless fallback on Vercel), model relationships.", table_cell_style)],
        [Paragraph("<b>Security & Hardening</b>", table_cell_bold), Paragraph("Flask-WTF / CSRFProtect<br/>Flask-Talisman<br/>Flask-Limiter", table_cell_style), Paragraph("Strict CSRF token validation across AJAX/fetch calls, Content Security Policy (CSP), HTTP security headers, and in-memory rate limiting.", table_cell_style)],
        [Paragraph("<b>Session & Cache</b>", table_cell_bold), Paragraph("Flask-Session / Redis", table_cell_style), Paragraph("Configurable session backend supporting Redis clusters in production and signed secure cookies in development/Vercel.", table_cell_style)],
        [Paragraph("<b>Frontend Markup</b>", table_cell_bold), Paragraph("Jinja2 / Semantic HTML5", table_cell_style), Paragraph("Modular template hierarchy (base.html, layout macros, workstation views, post-investigation cinematics).", table_cell_style)],
        [Paragraph("<b>Styling Architecture</b>", table_cell_bold), Paragraph("Vanilla CSS (Cyber Theme)", table_cell_style), Paragraph("Design token system (variables.css, reset.css, typography.css, components.css, layout.css, desktop workstation themes).", table_cell_style)],
        [Paragraph("<b>Client-side Logic</b>", table_cell_bold), Paragraph("Vanilla JavaScript (ES6+)", table_cell_style), Paragraph("Zero heavy framework dependencies; custom window manager, terminal emulator, Burp simulator, and responsive touch drawer.", table_cell_style)],
        [Paragraph("<b>Deployment & Cloud</b>", table_cell_bold), Paragraph("Vercel Serverless / Gunicorn", table_cell_style), Paragraph("Serverless WSGI entry point (api/index.py) configured via vercel.json for zero-downtime edge deployments.", table_cell_style)],
        [Paragraph("<b>Observability</b>", table_cell_bold), Paragraph("Sentry SDK / Python Logging", table_cell_style), Paragraph("Real-time exception tracing, performance monitoring, and structured application audit trails.", table_cell_style)]
    ]
    tech_tab = Table(tech_data, colWidths=[90, 135, 279])
    tech_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(tech_tab)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 6. HIGH-LEVEL SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("6. High-Level System Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Hack The AI utilizes a modular, decoupled architecture where presentation, security middleware, forensic workstation simulation, and relational persistence operate in concert:",
        body_style
    ))
    
    arch_box_data = [
        [Paragraph("<b>CLIENT TIER (Multi-Device Browser)</b><br/>Desktop / Laptop / Tablet / Mobile Viewports &bull; Window Manager &bull; Terminal Engine &bull; Burp Suite Inspector", ParagraphStyle('Arch1', parent=table_cell_style, alignment=1, textColor=c_primary))],
        [Paragraph("↓ <i>HTTPS / REST API / CSRF-Protected JSON Requests</i> ↓", ParagraphStyle('Arrow', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>SECURITY & EDGE MIDDLEWARE</b><br/>Flask-Talisman (CSP & TLS) &bull; Flask-WTF CSRF Engine &bull; Flask-Limiter &bull; Error Interceptors (400/404/500)", ParagraphStyle('Arch2', parent=table_cell_style, alignment=1, textColor=colors.HexColor("#065f46")))],
        [Paragraph("↓ <i>Authenticated Flask WSGI Dispatcher</i> ↓", ParagraphStyle('Arrow', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>APPLICATION BLUEPRINT CONTROLLERS</b><br/><code>routes.auth</code> &bull; <code>routes.dashboard</code> &bull; <code>routes.labs</code> &bull; <code>routes.api</code> &bull; <code>routes.leaderboard</code> &bull; <code>routes.pages</code> &bull; <code>routes.admin</code>", ParagraphStyle('Arch3', parent=table_cell_style, alignment=1, textColor=c_secondary))],
        [Paragraph("↓ <i>Forensic Execution & State Progression</i> ↓", ParagraphStyle('Arrow', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>INVESTIGATION & GAMIFICATION ENGINE</b><br/>Evidence Collector &bull; Question Answer Validator &bull; Chapter Progression Gate &bull; XP & Achievement Calculator", ParagraphStyle('Arch4', parent=table_cell_style, alignment=1, textColor=c_primary))],
        [Paragraph("↓ <i>SQLAlchemy ORM Data Mappings</i> ↓", ParagraphStyle('Arrow', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>PERSISTENCE & STORAGE TIER</b><br/>SQLite Database (<code>hacktheai.db</code> / <code>/tmp/hacktheai.db</code>) &bull; User State &bull; Progress &bull; Audit Trails &bull; Seed Catalog", ParagraphStyle('Arch5', parent=table_cell_style, alignment=1, textColor=c_secondary))]
    ]
    arch_table = Table(arch_box_data, colWidths=[504])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f0f9ff")),
        ('BACKGROUND', (0,2), (0,2), colors.HexColor("#ecfdf5")),
        ('BACKGROUND', (0,4), (0,4), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,6), (0,6), colors.HexColor("#f0f9ff")),
        ('BACKGROUND', (0,8), (0,8), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(arch_table)
    story.append(Paragraph("<b>Figure 1:</b> High-Level Multi-Tier System Architecture of Hack The AI.", fig_caption_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 7. COMPLETE APPLICATION WORKFLOW
    # =========================================================================
    story.append(Paragraph("7. End-to-End Application Workflow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    flow_steps = [
        ("Step 1: Authentication & Entry", "User authenticates via <code>/login</code> or <code>/register</code>. Demo credentials (admin / admin123) are provided for rapid evaluator access. The application assigns a signed session cookie and generates a unique CSRF token."),
        ("Step 2: Dashboard Intelligence", "The user lands on <code>/dashboard</code> displaying personal XP, rank standing, active investigations in progress, and platform news."),
        ("Step 3: Lab Selection", "Navigating to <code>/labs</code>, the user selects from available interactive and PRO investigations. Detailed briefings, XP stakes, estimated completion times, and prerequisites are displayed on <code>/lab/&lt;lab_id&gt;</code>."),
        ("Step 4: Launching the Workstation", "Accessing <code>/lab/lab6/workstation</code> or <code>/lab/lab7/workstation</code> loads the multi-window desktop operating system. A 65-minute forensic timer starts automatically."),
        ("Step 5: Chapter Investigation", "The left panel presents Chapter 1. The investigator reads the story briefing and dialogue stream from team analysts (Lakshay, Shivam, Mehak, Shanu)."),
        ("Step 6: Practical Tool Execution", "The user utilizes the desktop tools (Terminal, Burp Suite, Case Files, Attack Graph) to discover artifacts, calculate checksums, and extract compromised tokens."),
        ("Step 7: Question Submission & Validation", "The learner submits findings into the chapter answer box. The backend validates the answer via <code>/api/lab/submit</code>, awards XP, logs the attempt, unlocks the next Chapter, and updates the evidence progress bar."),
        ("Step 8: Capstone Certification & Flag Capture", "Upon completing all 5 chapters, the Capstone Examination unlocks. Submitting the verified master flag completes the case and redirects to the cinematic Post-Investigation debriefing page (<code>/lab/&lt;lab_id&gt;/post</code>)."),
        ("Step 9: Gamification & Rank Update", "Total XP is credited to the user profile, badges are awarded in <code>/achievements</code>, and the global leaderboard (<code>/leaderboard</code>) updates dynamically.")
    ]
    
    for s_title, s_desc in flow_steps:
        story.append(Paragraph(f"<b>{s_title}:</b> {s_desc}", bullet_style))
    
    story.append(PageBreak())

    # =========================================================================
    # 8. DATA FLOW & PIPELINES
    # =========================================================================
    story.append(Paragraph("8. Data Flow & Cross-Layer Pipelines", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Data movement within Hack The AI occurs across three distinct communication channels: Client-to-Backend State Operations, Simulated Network & Tool Telemetry, and Gamification Aggregation.",
        body_style
    ))
    
    df_data = [
        [Paragraph("<b>Data Domain</b>", table_cell_header), Paragraph("<b>Source & Route</b>", table_cell_header), Paragraph("<b>Payload & Processing Mechanism</b>", table_cell_header), Paragraph("<b>Persistence Target</b>", table_cell_header)],
        [Paragraph("<b>User Authentication</b>", table_cell_bold), Paragraph("<code>/login</code><br/>POST", table_cell_style), Paragraph("Username and hashed password verification via Werkzeug security.", table_cell_style), Paragraph("<code>users</code> table, signed session cookie.", table_cell_style)],
        [Paragraph("<b>Question Validation</b>", table_cell_bold), Paragraph("<code>/api/lab/submit</code><br/>POST", table_cell_style), Paragraph("JSON payload containing <code>lab_id</code>, <code>mission_id</code>, and <code>answer</code>. Checked against canonical answer models.", table_cell_style), Paragraph("<code>mission_progress</code>, <code>quiz_attempts</code>, <code>lab_progress</code>.", table_cell_style)],
        [Paragraph("<b>Hint Retrieval</b>", table_cell_bold), Paragraph("<code>/api/hint</code><br/>POST", table_cell_style), Paragraph("Fetches tiered guidance for active mission; deducts XP cost if configured.", table_cell_style), Paragraph("<code>hint_usage</code> table.", table_cell_style)],
        [Paragraph("<b>Case Reset</b>", table_cell_bold), Paragraph("<code>/api/lab/restart</code><br/>POST", table_cell_style), Paragraph("Purges completed mission progress for the target lab, resets evidence flags.", table_cell_style), Paragraph("Database transaction rollback / state reset.", table_cell_style)],
        [Paragraph("<b>Investigator Notes</b>", table_cell_bold), Paragraph("Client-side<br/>DOM Event", table_cell_style), Paragraph("Live text synchronization on input event to prevent data loss during long investigations.", table_cell_style), Paragraph("HTML5 <code>localStorage</code> (<code>lab6_notes</code>, <code>lab7_notes</code>).", table_cell_style)]
    ]
    df_tab = Table(df_data, colWidths=[85, 80, 195, 144])
    df_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(df_tab)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 9. DATABASE & STORAGE ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("9. Database Schema & Storage Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "The relational database schema is modeled in <code>models.py</code> using SQLAlchemy. It establishes clear foreign-key constraints and cascading progress relationships:",
        body_style
    ))
    
    db_models = [
        ("User (users)", "Primary identity model storing <code>id</code>, <code>username</code>, <code>email</code>, <code>password</code> (PBKDF2/SHA-256), and <code>role</code> (student/admin)."),
        ("Lab (labs)", "Master catalog table containing <code>id</code> (e.g., 'lab6', 'lab7'), <code>name</code>, <code>topic</code>, and <code>difficulty</code>."),
        ("Mission (missions)", "Individual investigation chapters linked to a lab via <code>lab_id</code>, with <code>mission_number</code>, <code>title</code>, and <code>description</code>."),
        ("MissionProgress (mission_progress)", "Per-user chapter status tracking (<code>status</code>: LOCKED, AVAILABLE, IN PROGRESS, COMPLETED, and <code>completed_at</code>)."),
        ("MissionQuiz (mission_quiz)", "Questions tied to missions, storing <code>question</code> text, <code>answer</code> string, <code>explanation</code>, and <code>xp_reward</code>."),
        ("QuizAttempt (quiz_attempts)", "Audit log of all user submissions storing <code>user_id</code>, <code>mission_id</code>, <code>answer</code>, <code>correct</code> (bool), and <code>timestamp</code>."),
        ("Hint & HintUsage (hints, hint_usage)", "Progressive hint system storing hint text, sort order, XP deduction costs, and user consumption timestamps."),
        ("LabProgress (lab_progress)", "Overall lab status for each user storing <code>score</code>, <code>percentage</code>, <code>status</code>, and <code>completed_at</code>."),
        ("Evidence & EvidenceProgress (evidence, evidence_progress)", "Artifact tokens discovered during investigations, tracking evidence collection per user."),
        ("Flag & FlagSubmission (flags, flag_submissions)", "Master capture-the-flag submission validator ensuring correct final case flags are validated.")
    ]
    
    for m_name, m_desc in db_models:
        story.append(Paragraph(f"• <b>{m_name}:</b> {m_desc}", bullet_style))
    
    story.append(Spacer(1, 8))

    # =========================================================================
    # 10. AUTHENTICATION & ACCESS CONTROL
    # =========================================================================
    story.append(Paragraph("10. Authentication, Access Control & Session Security", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "<b>Authentication Protocol:</b> User registration and authentication are handled via Flask session authentication with password hashing powered by Werkzeug security helpers. Passwords are never stored in plaintext.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Role-Based Access Control (RBAC):</b> System routes enforce authorization decorators (<code>@login_required</code> and <code>@admin_required</code>). Administrative functions—including lab zip package uploading, container orchestration, and student audit log inspection—are restricted to users with the <code>admin</code> role.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Serverless Secret Key Persistence:</b> On ephemeral serverless platforms (such as Vercel), regenerating <code>SECRET_KEY</code> on every worker invocation destroys active sessions and causes instant CSRF validation failures. Hack The AI implements an intelligent secret key resolver in <code>config.py</code> that securely retrieves the environment key, falls back to disk persistence when writable, or supplies a deterministic production fallback token.",
        body_style
    ))
    story.append(Paragraph(
        "<b>CSRF Protection:</b> Every state-modifying POST request (login, registration, quiz answer, hint request, lab reset) enforces strict CSRF token validation via Flask-WTF and custom JavaScript fetch headers (<code>X-CSRFToken</code>).",
        body_style
    ))
    
    story.append(PageBreak())

    # =========================================================================
    # 11. SIMULATED INVESTIGATION WORKSTATION ENVIRONMENT
    # =========================================================================
    story.append(Paragraph("11. Simulated Investigation Workstation Environment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "The core innovation of Hack The AI is its <b>In-Browser Investigation Workstation OS</b>. The workstation provides ten integrated forensic sub-systems operating in a multi-window desktop interface:",
        body_style
    ))
    
    tools_data = [
        [Paragraph("<b>Sub-System Tool</b>", table_cell_header), Paragraph("<b>Inputs & Trigger</b>", table_cell_header), Paragraph("<b>Output & Functionality</b>", table_cell_header), Paragraph("<b>Role in Cyber Investigation</b>", table_cell_header)],
        [Paragraph("<b>Forensic Browser</b>", table_cell_bold), Paragraph("URL Bar / Navigation buttons / Tab selections", table_cell_style), Paragraph("Renders simulated internal web applications (e.g., Bridge Explorer, Oracle Ingestion Monitor, AI Studio, Consensus Topology).", table_cell_style), Paragraph("Primary visual inspector for blockchain transactions, AI confidence graphs, and validator cluster telemetry.", table_cell_style)],
        [Paragraph("<b>Burp Suite Inspector</b>", table_cell_bold), Paragraph("Proxy history table clicks / Repeater send", table_cell_style), Paragraph("Displays raw HTTP/RPC request and response headers, JSON payloads, cookies, and status codes.", table_cell_style), Paragraph("Allows investigators to identify injected parameters, stolen session cookies, and forged oracle headers.", table_cell_style)],
        [Paragraph("<b>Forensic Terminal</b>", table_cell_bold), Paragraph("Interactive CLI commands (<code>grep</code>, <code>python</code>, <code>iot-status</code>, <code>policy</code>)", table_cell_style), Paragraph("Simulates bash shell execution with colored syntax output, automated grep searching across logs, and forensic script execution.", table_cell_style), Paragraph("Enables hands-on artifact discovery, hashing, and raw log analysis.", table_cell_style)],
        [Paragraph("<b>Case File Manager</b>", table_cell_bold), Paragraph("File tree clicks (<code>.log</code>, <code>.txt</code>, <code>.json</code>)", table_cell_style), Paragraph("Monaco-style raw text viewer with line numbers and copy-to-clipboard functionality.", table_cell_style), Paragraph("Permits deep inspection of audit feeds, smart contract ABIs, and IoT gateway logs.", table_cell_style)],
        [Paragraph("<b>Scratchpad Notes</b>", table_cell_bold), Paragraph("Investigator typing / save button", table_cell_style), Paragraph("Persistent text editor automatically synced with browser localStorage.", table_cell_style), Paragraph("Allows learners to record hashes, IP addresses, tokens, and hypotheses across investigation chapters.", table_cell_style)],
        [Paragraph("<b>Dynamic Attack Graph</b>", table_cell_bold), Paragraph("Evidence collection events", table_cell_style), Paragraph("Interactive SVG graph showing attack progression from Initial Access to Root Impact.", table_cell_style), Paragraph("Provides visual reconstruction of how IoT, AI, Web3, and consensus exploits connect.", table_cell_style)],
        [Paragraph("<b>Evidence Locker</b>", table_cell_bold), Paragraph("Mission completion events", table_cell_style), Paragraph("Categorized badge grid displaying collected evidence hashes and cryptographic proofs.", table_cell_style), Paragraph("Validates that all forensic prerequisites are met before the Capstone Exam unlocks.", table_cell_style)],
        [Paragraph("<b>Web3 / Bridge Monitor</b>", table_cell_bold), Paragraph("Browser tab selection in Case NEX-042", table_cell_style), Paragraph("On-chain block explorer showing transaction hashes, nonce counts, gas fees, and target liquidity pool addresses.", table_cell_style), Paragraph("Enables tracking of unauthorized multi-chain treasury asset exfiltration.", table_cell_style)],
        [Paragraph("<b>AI Oracle Studio</b>", table_cell_bold), Paragraph("Browser tab selection in Case NEX-071", table_cell_style), Paragraph("Displays model name (ORION v4.2 / v3.8.4), confidence ratings, training poisoning embeddings, and circuit breaker status.", table_cell_style), Paragraph("Exposes how poisoned training datasets deceive AI security models into suppressing critical alerts.", table_cell_style)],
        [Paragraph("<b>IoT Gateway Ingest</b>", table_cell_bold), Paragraph("Browser / Terminal command (<code>iot-status</code>)", table_cell_style), Paragraph("Real-time telemetry stream from 184 industrial sensors across 14 geographic sites.", table_cell_style), Paragraph("Enables detection of synthetic data injection and zero-jitter anomalies at the physical edge.", table_cell_style)]
    ]
    tools_tab = Table(tools_data, colWidths=[85, 100, 165, 154])
    tools_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(tools_tab)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 12. LAB ARCHITECTURE & FORENSIC SPECIFICATIONS
    # =========================================================================
    story.append(Paragraph("12. Lab Architecture & Forensic Case Specifications", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Each investigation in Hack The AI is engineered with a strict pedagogical lifecycle: <b>Incident Briefing → Team Dialogue Stream → Hands-on Practical Task → Evidence Extraction → Conceptual Question Validation → Progression Unlock → Capstone Examination</b>.",
        body_style
    ))
    
    story.append(Paragraph("<b>Case NEX-042: The Ghost in the Ledger (PRO Lab 01 — 250 XP)</b>", h2_style))
    story.append(Paragraph("Focus: Web3 Bridge Security, AI Context Injection, RBAC Privilege Escalation, Autonomous Treasury Siphoning.", body_style))
    
    lab6_data = [
        [Paragraph("<b>Ch.</b>", table_cell_header), Paragraph("<b>Title & Domain</b>", table_cell_header), Paragraph("<b>Forensic Investigation Focus & Practical Task</b>", table_cell_header), Paragraph("<b>Key Artifact / Answer</b>", table_cell_header)],
        [Paragraph("<b>1</b>", table_cell_bold), Paragraph("The Phantom Transaction<br/><i>(Web3 Forensics)</i>", table_cell_style), Paragraph("Analyze unannounced 82,400 NXR outflow. Query transaction TX-NEX-7741 on Bridge-Core-04.", table_cell_style), Paragraph("Dest Wallet: <code>0x7C41...9B2D</code><br/>Amount: <code>82,400 NXR</code>", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_bold), Paragraph("The Poisoned Context<br/><i>(AI Threat Hunting)</i>", table_cell_style), Paragraph("Investigate AI Decision ORION-DEC-7741. Trace source data to unverified feed NIF-2038.", table_cell_style), Paragraph("Source: <code>NOVA-INTEL-FEED</code><br/>Confidence: <code>99.2%</code>", table_cell_style)],
        [Paragraph("<b>3</b>", table_cell_bold), Paragraph("The Over-Privileged Ghost<br/><i>(RBAC & IAM Audit)</i>", table_cell_style), Paragraph("Inspect IAM service roles. Discover INTEL-INGESTOR-02 holds unauthorized reputation writing rights.", table_cell_style), Paragraph("Service: <code>INTEL-INGESTOR-02</code><br/>Privilege: Over-privileged", table_cell_style)],
        [Paragraph("<b>4</b>", table_cell_bold), Paragraph("The Execution Matrix<br/><i>(Policy Engine Audit)</i>", table_cell_style), Paragraph("Audit ORION-SETTLEMENT-V2 policy rules. Identify auto-settle trigger bypassing human approval.", table_cell_style), Paragraph("Rule: <code>AUTO_SETTLE_TREASURY</code><br/>Threshold: <code>>= 95%</code>", table_cell_style)],
        [Paragraph("<b>5</b>", table_cell_bold), Paragraph("The Attack Campaign<br/><i>(Threat Attribution)</i>", table_cell_style), Paragraph("Correlate multi-chain wallet cluster, reconstruct attack graph, identify threat actor.", table_cell_style), Paragraph("Campaign: <code>ORION-NEXUS</code><br/>Flag: <code>NEXORA{ghost_in_the_ledger_nex042}</code>", table_cell_style)]
    ]
    lab6_tab = Table(lab6_data, colWidths=[25, 115, 245, 119])
    lab6_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(lab6_tab)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Case NEX-071: The Vanishing Consensus (PRO Lab 02 — 300 XP)</b>", h2_style))
    story.append(Paragraph("Focus: IoT Edge Telemetry, Web3 Multi-Sig Oracle Poisoning, Neural Network Training Poisoning, BFT Consensus State Forks.", body_style))
    
    lab7_data = [
        [Paragraph("<b>Ch.</b>", table_cell_header), Paragraph("<b>Title & Domain</b>", table_cell_header), Paragraph("<b>Forensic Investigation Focus & Practical Task</b>", table_cell_header), Paragraph("<b>Key Artifact / Answer</b>", table_cell_header)],
        [Paragraph("<b>1</b>", table_cell_bold), Paragraph("The Silent Sensor Anomaly<br/><i>(IoT Edge Forensics)</i>", table_cell_style), Paragraph("Inspect 184 industrial sensors across 14 sites. Detect synthetic identical temperature/power output.", table_cell_style), Paragraph("Gateway: <code>GATEWAY-GW-184</code><br/>Jitter: <code>0.00% (Synthetic)</code>", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_bold), Paragraph("The Poisoned Oracle Pipeline<br/><i>(Web3 Oracle Security)</i>", table_cell_style), Paragraph("Analyze NOVA-PRICE-ORACLE aggregator consuming manipulated upstream IoT payload.", table_cell_style), Paragraph("Oracle: <code>NOVA-PRICE-ORACLE</code><br/>Anomaly: Identical Multi-Sig", table_cell_style)],
        [Paragraph("<b>3</b>", table_cell_bold), Paragraph("The AI Model Blindspot<br/><i>(Adversarial AI Security)</i>", table_cell_style), Paragraph("Audit AI Sentinel MODEL-ORION. Discover historical poisoning injection (EMB-IOT-9041).", table_cell_style), Paragraph("Embedding: <code>EMB-IOT-9041</code><br/>Label: <code>BENIGN_SYNC</code>", table_cell_style)],
        [Paragraph("<b>4</b>", table_cell_bold), Paragraph("The Validator State Split<br/><i>(BFT Consensus Security)</i>", table_cell_style), Paragraph("Inspect 21-node validator cluster. Uncover 3:2 derived state fork and network partition.", table_cell_style), Paragraph("Split: <code>3 Accept : 2 Reject</code><br/>Leader Node: <code>V03 (Poisoned)</code>", table_cell_style)],
        [Paragraph("<b>5</b>", table_cell_bold), Paragraph("Cross-Layer Reconstruction<br/><i>(Full Chain Containment)</i>", table_cell_style), Paragraph("Reconstruct complete IoT -> Oracle -> AI -> Consensus attack chain, extract final case flag.", table_cell_style), Paragraph("Root: Multi-Layer Trust Abuse<br/>Flag: <code>NEXORA{v4n1sh1ng_c0ns3nsus_n3x071}</code>", table_cell_style)]
    ]
    lab7_tab = Table(lab7_data, colWidths=[25, 115, 245, 119])
    lab7_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(lab7_tab)
    
    story.append(PageBreak())

    # =========================================================================
    # 13. GAMIFICATION ENGINE
    # =========================================================================
    story.append(Paragraph("13. Gamification Engine: Scoring, XP & Achievements", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Hack The AI features a comprehensive gamification framework designed to maintain student engagement and reward deep forensic problem-solving:",
        body_style
    ))
    
    game_points = [
        "<b>Experience Points (XP) Hierarchy:</b> Foundational interactive challenges award 50-100 XP. Comprehensive PRO investigations award 250 XP (Case NEX-042) and 300 XP (Case NEX-071).",
        "<b>Real-Time Progress Fill:</b> Dynamic progress bars in both the workstation header and dashboard track chapter completions and evidence collection in real time.",
        "<b>Achievement Badges:</b> Learners unlock permanent profile badges including <i>First Blood</i>, <i>Blockchain Forensic Specialist</i>, <i>AI Threat Hunter</i>, <i>Consensus Guardian</i>, and <i>Master Investigator</i>.",
        "<b>Global Competitive Leaderboard:</b> The leaderboard dynamically aggregates user XP scores, total completed investigations, and submission timestamps to rank learners globally.",
        "<b>Structured Learning Tracks:</b> The <code>/learning</code> module structures skills into progressive modules: AI Security Foundations, Web3 Forensics, IoT Security Operations, and Cross-Layer Incident Response."
    ]
    for gp in game_points:
        story.append(Paragraph(f"• {gp}", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 14. SECURITY HARDENING ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("14. Security Hardening & Platform Protection Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "As a cybersecurity training platform, Hack The AI enforces strict production-grade security controls within its own application architecture:",
        body_style
    ))
    
    sec_data = [
        [Paragraph("<b>Defense Control</b>", table_cell_header), Paragraph("<b>Implementation Library & Configuration</b>", table_cell_header), Paragraph("<b>Mitigation & Threat Protection</b>", table_cell_header)],
        [Paragraph("<b>Content Security Policy (CSP)</b>", table_cell_bold), Paragraph("<code>flask_talisman.Talisman</code><br/>Custom script-src, style-src, frame-src", table_cell_style), Paragraph("Prevents Cross-Site Scripting (XSS) and unauthorized external script injection.", table_cell_style)],
        [Paragraph("<b>CSRF Token Enforcement</b>", table_cell_bold), Paragraph("<code>flask_wtf.csrf.CSRFProtect</code><br/><code>WTF_CSRF_TIME_LIMIT = None</code>", table_cell_style), Paragraph("Protects all state-modifying requests while preventing unexpected token expiration during long labs.", table_cell_style)],
        [Paragraph("<b>Adaptive Rate Limiting</b>", table_cell_bold), Paragraph("<code>flask_limiter.Limiter</code><br/><code>memory://</code> storage backend", table_cell_style), Paragraph("Prevents brute-force password guessing and automated quiz answer scraping without Redis latency.", table_cell_style)],
        [Paragraph("<b>Secure Cookie Handling</b>", table_cell_bold), Paragraph("<code>HttpOnly=True, SameSite='Lax'</code><br/>Dynamic <code>Secure=FORCE_HTTPS</code>", table_cell_style), Paragraph("Prevents JavaScript cookie theft and ensures reliable session retention in both HTTP dev and HTTPS prod.", table_cell_style)],
        [Paragraph("<b>Input Sanitization</b>", table_cell_bold), Paragraph("Custom <code>escapeHtml()</code> engine in JS<br/>Jinja2 auto-escaping", table_cell_style), Paragraph("Guarantees that user inputs in terminal consoles, chat dialogues, and notes cannot execute malicious scripts.", table_cell_style)]
    ]
    sec_tab = Table(sec_data, colWidths=[115, 155, 234])
    sec_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(sec_tab)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 15. RESPONSIVE DESIGN SYSTEM
    # =========================================================================
    story.append(Paragraph("15. Multi-Device Responsive Design System", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Hack The AI provides a customized responsive layout engine across four target hardware form-factors:",
        body_style
    ))
    
    resp_points = [
        "<b>Desktop Workstations (1920×1080 & above):</b> Side-by-side dual pane view. The left panel houses the 450px task panel with accordion mission tabs; the right pane operates the full multi-window desktop operating system.",
        "<b>Laptops (1366×768, 1440×900, 1536×864):</b> Compact task panel (380px) with adaptive font sizing, scrollable dual-pane burp inspectors, and stacked subtask pills.",
        "<b>Tablets (768×1024 / iPad portrait & landscape):</b> Collapsible mobile sidebar with backdrop drawer, responsive taskbar tab scrollbars, and full-width window focus.",
        "<b>Mobile Phones (390×844, 412×915 / iPhone & Android):</b> Single-pane view with a sticky <code>Mobile View Switcher</code> allowing seamless one-tap switching between '📋 Investigation Tasks' and '💻 Consensus Desktop', touch targets expanded to min 38–40px, and hardware-accelerated touch scrolling."
    ]
    for rp in resp_points:
        story.append(Paragraph(f"• {rp}", bullet_style))
    
    story.append(PageBreak())

    # =========================================================================
    # 16. CLOUD DEPLOYMENT & SERVERLESS ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("16. Cloud Deployment & Serverless WSGI Execution", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "Hack The AI is architected to run seamlessly both in containerized enterprise environments (Docker/Gunicorn/Nginx) and on edge serverless platforms (Vercel Serverless Python):",
        body_style
    ))
    
    deploy_points = [
        "<b>Vercel WSGI Serverless Entry Point:</b> <code>api/index.py</code> imports and exposes the Flask WSGI instance. <code>vercel.json</code> routes all global traffic (<code>/(.*)</code>) into the Python serverless runtime.",
        "<b>Serverless SQLite /tmp Fallback:</b> Because AWS Lambda/Vercel containers possess read-only filesystems outside of <code>/tmp</code>, <code>config.py</code> automatically redirects <code>DATABASE_PATH</code> to <code>/tmp/hacktheai.db</code> when <code>VERCEL</code> environment variables are detected.",
        "<b>On-Demand Database Seeding:</b> The application utilizes an atomic <code>@app.before_request</code> database initializer that provisions tables, seeds administrative users, and populates the 55+ question catalog on cold starts without manual CLI execution.",
        "<b>Stateless Memory-Backed Rate Limiting:</b> Configured to use <code>memory://</code> to prevent timeout delays when external Redis clusters are unprovisioned."
    ]
    for dp in deploy_points:
        story.append(Paragraph(f"• {dp}", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 17. COMPLETE CODEBASE STRUCTURE
    # =========================================================================
    story.append(Paragraph("17. Complete Codebase Structure & File Directory", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    tree_text = """
HackTheAI-master/
├── api/
│   └── index.py                           # Vercel Serverless WSGI Entry Point
├── database/
│   ├── hacktheai.db                       # Local SQLite relational database instance
│   └── .secret_key                        # Persistent local secret key storage
├── routes/
│   ├── admin.py                           # Lab zip upload, container management, audit logs
│   ├── api.py                             # Mission validation, hints, restart, state endpoints
│   ├── auth.py                            # User login, registration, logout, session init
│   ├── dashboard.py                       # User dashboard, recent activity, XP stats
│   ├── labs.py                            # Lab catalog, detail views, workstation launchers
│   ├── leaderboard.py                     # Dynamic ranking and XP leaderboard
│   └── pages.py                           # Challenges, achievements, learning tracks, profile
├── static/
│   ├── css/
│   │   ├── core/                          # variables.css, reset.css, typography.css
│   │   ├── components/                    # components.css, buttons, badges, modals
│   │   ├── layout/                        # layout.css, sidebar, topbar, responsive grid
│   │   └── pages/                         # ghost_ledger.css, ghost_ledger_desktop.css,
│   │                                      # vanishing_consensus_desktop.css
│   └── js/
│       ├── main.js                        # Global drawer, toast notifications, CSRF fetch API
│       ├── ghost_ledger_desktop.js        # Lab 1 Workstation window manager & terminal engine
│       ├── ghost_ledger_post.js           # Lab 1 Post-investigation cinematic debrief
│       └── vanishing_consensus_desktop.js # Lab 2 Workstation window manager & IoT/AI engine
├── templates/
│   ├── base.html                          # Master layout shell with cyber navigation & sidebar
│   ├── login.html / register.html         # Auth views with demo credential guidance
│   ├── dashboard.html / labs.html         # Core portal dashboards and lab catalog
│   ├── ghost_ledger_workstation.html      # Case NEX-042 full workstation interface
│   ├── ghost_ledger_post_investigation.html # Case NEX-042 post-investigation report
│   ├── vanishing_consensus_workstation.html # Case NEX-071 full workstation interface
│   └── vanishing_consensus_post_investigation.html # Case NEX-071 post-investigation report
├── app.py                                 # Main Flask Application Factory & Middleware
├── config.py                              # Environment Configuration, Secret Key Resolver
├── extensions.py                          # Flask-SQLAlchemy, CSRFProtect, Limiter, Migrate
├── models.py                              # Complete SQLAlchemy ORM Data Models
├── seed_ghost_ledger.py                   # Lab 1 Mission & Quiz Database Seeder
├── seed_vanishing_consensus.py            # Lab 2 Mission & Quiz Database Seeder
└── vercel.json                            # Vercel Serverless Routing & Build Configuration
    """
    story.append(Paragraph(f"<pre>{tree_text.strip()}</pre>", code_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 18. FUTURE SCOPE & ROADMAP
    # =========================================================================
    story.append(Paragraph("18. Project Roadmap & Future Scope", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    scope_data = [
        [Paragraph("<b>Current Implemented Capabilities (v2.0)</b>", table_cell_header), Paragraph("<b>Future Architectural Roadmap (v3.0 Planned)</b>", table_cell_header)],
        [
            Paragraph("• Full Web3 × AI × IoT Investigation Workstations (Case NEX-042 & NEX-071).<br/>• In-browser simulated Burp Suite, Terminal, Browser, Attack Graph, Case Files.<br/>• 55+ Hands-on questions with progressive hints & Capstone quizzes.<br/>• Responsive Desktop, Laptop, Tablet, and Mobile viewport support.<br/>• Role-based authentication, CSRF hardening, and serverless Vercel deployment.", table_cell_style),
            Paragraph("• Live Docker container sandbox execution per student session.<br/>• Multi-player collaborative SOC incident response rooms with live WebSocket sync.<br/>• Integration of real EVM testnets (Sepolia/Arbitrum) for live exploit verification.<br/>• Dynamic AI-generated adversarial scenarios with LLM-driven forensic debriefs.<br/>• SCORM & LTI integration for university and enterprise LMS certification sync.", table_cell_style)
        ]
    ]
    scope_tab = Table(scope_data, colWidths=[250, 254])
    scope_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(scope_tab)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 19. CONCLUSION
    # =========================================================================
    story.append(Paragraph("19. Conclusion & Final Technical Assessment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "<b>Hack The AI</b> represents a benchmark implementation of next-generation cybersecurity training infrastructure. By successfully unifying multi-domain technologies—<b>Decentralized Consensus</b>, <b>Autonomous AI Decision Systems</b>, <b>Industrial IoT Telemetry</b>, and <b>Enterprise RBAC Governance</b>—into an engaging, story-driven investigation operating system, the platform equips defenders with the exact forensic skills required to detect, analyze, and remediate complex modern threats.",
        body_style
    ))
    story.append(Paragraph(
        "The codebase adheres to clean architectural principles: modular Flask blueprints, decoupled ORM models, robust CSRF and CSP protections, zero-dependency high-performance JavaScript engines, and full cross-device responsive styling. It is production-ready for immediate academic, enterprise, and competitive cybersecurity deployment.",
        body_style
    ))
    story.append(Spacer(1, 10))

    sig_data = [[
        Paragraph("<b>DESIGNED & DEVELOPED BY LAKSHAY SONI</b><br/><font size=7.5 color='#64748b'>Lead System Architect & Cybersecurity Engineer &bull; Hack The AI Platform Project</font>", ParagraphStyle('Sig', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=c_primary, alignment=1))
    ]]
    sig_tab = Table(sig_data, colWidths=[504])
    sig_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(sig_tab)

    # Build PDF with two-pass canvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated complete project report: {output_filename}")


if __name__ == '__main__':
    target_pdf = "HACK_THE_AI_COMPLETE_PROJECT_REPORT.pdf"
    if len(sys.argv) > 1:
        target_pdf = sys.argv[1]
    create_report(target_pdf)
