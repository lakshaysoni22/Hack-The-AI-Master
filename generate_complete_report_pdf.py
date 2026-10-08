import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total page count and draw running headers and footers."""
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip cover page
            return
        
        self.saveState()
        
        # Running Top Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 11 * inch - 36, "HACK THE AI — COMPLETE TECHNICAL PROJECT REPORT")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "TRINETLAYER // SECURITY OPERATIONS")
        self.setStrokeColor(colors.HexColor("#0284c7"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Running Bottom Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 32, "Confidential — Prepared by Lakshay Soni (Security Analyst, TrinetLayer)")
        self.drawRightString(8.5 * inch - 54, 32, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def generate_pdf_report(filename="HACK_THE_AI_COMPLETE_PROJECT_REPORT.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0369a1")    # Deep Cyan / Blue
    c_accent = colors.HexColor("#0284c7")     # Bright Cyber Blue
    c_secondary = colors.HexColor("#0f172a")  # Dark Slate
    c_text = colors.HexColor("#1e293b")       # Dark Charcoal
    c_muted = colors.HexColor("#64748b")      # Cool Gray
    c_border = colors.HexColor("#cbd5e1")     # Border
    c_bg_light = colors.HexColor("#f8fafc")   # Card BG
    c_callout_bg = colors.HexColor("#f0f9ff") # Light Blue BG
    c_success = colors.HexColor("#16a34a")    # Emerald
    c_warning = colors.HexColor("#d97706")    # Amber
    c_danger = colors.HexColor("#dc2626")     # Red

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_primary,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'SectionH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        spaceAfter=4.5
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=c_text,
        leftIndent=12,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'ReportCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'ReportCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1e293b")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=c_secondary
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    fig_caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=c_muted,
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    
    top_badge_data = [[
        Paragraph("<b>CYBERSECURITY INVESTIGATION &amp; ADVERSARIAL SIMULATION PLATFORM</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#0284c7"), letterSpacing=1.2, alignment=1))
    ]]
    top_badge_tab = Table(top_badge_data, colWidths=[504])
    top_badge_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(top_badge_tab)
    story.append(Spacer(1, 14))

    story.append(Paragraph("HACK THE AI", title_style))
    story.append(Paragraph("Interactive Story-Driven Cybersecurity Investigation &amp; Learning Platform", ParagraphStyle('Sub1', parent=title_style, fontSize=14, leading=18, textColor=c_primary, spaceBefore=3)))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "A comprehensive technical architecture, forensic investigation specification, and pedagogical engineering report detailing the full-stack simulation of multi-domain cyber threats across Web3 Bridge Protocols, Adversarial AI Data Poisoning, Industrial IoT Gateway Telemetry, and Byzantine Fault Tolerance (BFT) Validator Consensus.",
        subtitle_style
    ))
    story.append(Spacer(1, 16))

    # Author Metadata Card
    author_card_data = [
        [Paragraph("<b>Project:</b>", table_cell_bold), Paragraph("HACK THE AI (Interactive &amp; PRO Investigation Platform)", table_cell_style)],
        [Paragraph("<b>Prepared By:</b>", table_cell_bold), Paragraph("<b>Lakshay Soni</b>", table_cell_bold)],
        [Paragraph("<b>Role:</b>", table_cell_bold), Paragraph("Security Analyst", table_cell_style)],
        [Paragraph("<b>Organization:</b>", table_cell_bold), Paragraph("TrinetLayer", table_cell_style)],
        [Paragraph("<b>Live Platform URL:</b>", table_cell_bold), Paragraph("<code>https://hack-the-ai-labs.vercel.app/</code>", table_cell_style)],
        [Paragraph("<b>GitHub Repository:</b>", table_cell_bold), Paragraph("<code>https://github.com/lakshaysoni22/Hack-The-AI-Master</code>", table_cell_style)],
        [Paragraph("<b>Target Cases:</b>", table_cell_bold), Paragraph("Case NEX-042 (The Ghost in the Ledger) &bull; Case NEX-071 (The Vanishing Consensus)", table_cell_style)],
        [Paragraph("<b>Document Classification:</b>", table_cell_bold), Paragraph("Official Technical Project Documentation &amp; Architecture Report", table_cell_style)],
        [Paragraph("<b>Publication Date:</b>", table_cell_bold), Paragraph("October 2026", table_cell_style)]
    ]
    author_card = Table(author_card_data, colWidths=[130, 374])
    author_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(author_card)
    story.append(Spacer(1, 16))

    callout_data = [[
        Paragraph("<b>EXECUTIVE NOTE:</b> Hack The AI transitions cybersecurity education from passive video tutorials and static quiz questions into an active, multi-window SOC desktop workstation. Learners discover, analyze, and contain interconnected cross-layer incidents using interactive terminals, proxy analyzers, live case files, and dynamic attack graphs.", callout_style)
    ]]
    callout_tab = Table(callout_data, colWidths=[504])
    callout_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LINELEFT', (0,0), (-1,-1), 3, c_primary),
        ('BOX', (0,0), (-1,-1), 0.5, c_border)
    ]))
    story.append(callout_tab)

    story.append(PageBreak())

    # =========================================================================
    # 2. TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("2. TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    
    toc_entries = [
        ("1. Cover Page & Author Information", "1"),
        ("2. Table of Contents", "2"),
        ("3. Executive Summary", "3"),
        ("4. Project Introduction & Background", "3"),
        ("5. Problem Statement & Industry Training Gaps", "3"),
        ("6. Project Objectives & Core Missions", "4"),
        ("7. Project Scope (Current Implemented vs. Future)", "4"),
        ("8. Complete Project Concept & Investigation Lore", "4"),
        ("9. Lab Ecosystem & Discovery Hierarchy", "5"),
        ("10. System Architecture & High-Level Design", "5"),
        ("11. Application Structure Diagram", "6"),
        ("12. Project Directory Structure & Responsibilities", "6"),
        ("13. Technology Stack & Component Mapping", "7"),
        ("14. Frontend Architecture & Tokenized Styling", "7"),
        ("15. Backend Architecture & WSGI Blueprint Dispatch", "8"),
        ("16. Database & Relational Storage Architecture", "8"),
        ("17. Complete Data Flow & Pipeline Mechanics", "9"),
        ("18. End-to-End User Journey", "9"),
        ("19. Simulated Investigation Workstation Environment (10 Tools)", "10"),
        ("20. Practical Learning & Forensic Validation Workflow", "11"),
        ("21. AI Component: Neural Inference & Poisoning Traces", "11"),
        ("22. Web3 Component: Cross-Chain Bridges & Consensus", "12"),
        ("23. Simulated IoT Component: Gateways & Telemetry", "12"),
        ("24. Cybersecurity Architecture & Threat Modeling", "12"),
        ("25. Lab Storyline Architecture & Narrative Flow", "13"),
        ("26. PRO Lab 1 Walkthrough: Case NEX-042 (The Ghost in the Ledger)", "13"),
        ("27. PRO Lab 2 Walkthrough: Case NEX-071 (The Vanishing Consensus)", "14"),
        ("28. Chapter & Question Validation Architecture", "15"),
        ("29. XP, Scoring & Dynamic Progression Engine", "15"),
        ("30. Achievement System & Badge Unlocks", "15"),
        ("31. Learning System & Module Progression", "16"),
        ("32. Global Leaderboard & Scoring Algorithms", "16"),
        ("33. Security Model, CSP, CSRF & Cookie Protections", "16"),
        ("34. Deployment Architecture & Serverless WSGI Edge Runtime", "17"),
        ("35. Multi-Device Responsive Design System", "17"),
        ("36. Testing, Quality Assurance & Verification", "18"),
        ("37. Visual Schematics & Architectural Figures", "18"),
        ("38. Required Diagrams & Flowchart Reference", "19"),
        ("39. Project Limitations & Known Operational Boundaries", "19"),
        ("40. Future Scope & Roadmap (v3.0 Innovations)", "20"),
        ("41. Conclusion & Technical Assessment", "20"),
        ("42. References & Project Documentation Links", "20"),
        ("43. Appendix: Route Matrix, Database Schemas & Endpoints", "21")
    ]
    
    toc_data = []
    for t_name, t_page in toc_entries:
        toc_data.append([
            Paragraph(f"<b>{t_name}</b>", table_cell_style),
            Paragraph(f"<b>{t_page}</b>", ParagraphStyle('RP', parent=table_cell_style, alignment=2))
        ])
    
    toc_table = Table(toc_data, colWidths=[440, 64])
    toc_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('PADDING', (0,0), (-1,-1), 2.8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. EXECUTIVE SUMMARY & 4. INTRODUCTION & 5. PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("3. Executive Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Hack The AI</b> is a next-generation cybersecurity investigation platform engineered to prepare modern defenders for multi-domain cyber warfare. By unifying <b>Artificial Intelligence</b>, <b>Decentralized Ledgers (Web3)</b>, <b>Industrial Internet of Things (IoT)</b>, and <b>Distributed Consensus</b> into realistic, story-driven cyber incident cases, the platform bridges the divide between theoretical understanding and operational threat containment. Learners enter an interactive SOC workstation equipped with emulated operating system windows, network interceptors, command-line forensic terminals, on-chain explorers, live sensor aggregators, and dynamic attack graph visualizers.",
        body_style
    ))
    story.append(Paragraph(
        "The project has been architected, developed, and maintained by <b>Lakshay Soni</b> (Security Analyst, TrinetLayer) and is deployed for live access at <code>https://hack-the-ai-labs.vercel.app/</code>.",
        body_style
    ))

    story.append(Paragraph("4. Project Introduction & Background", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "As organizations increasingly automate financial settlement, smart city infrastructure, and critical supply chains using machine learning models and smart contracts, the threat landscape has fundamentally expanded. Modern attackers no longer target individual web application parameters in isolation; they execute sophisticated multi-vector kill-chains. Hack The AI establishes a high-fidelity learning environment where analysts develop hands-on competency in uncovering poisoned AI datasets, tracing cross-chain liquidity drain transactions, detecting synthetic IoT jitter, and resolving Byzantine validator state forks.",
        body_style
    ))

    story.append(Paragraph("5. Problem Statement & Industry Training Gaps", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    problems = [
        "<b>Passive Theoretical Learning:</b> Traditional courses rely on static slide decks and multi-choice quizzes without providing active forensic terminals or realistic raw log files.",
        "<b>Domain Siloing:</b> Existing CTF platforms separate Web Security, AI, Hardware/IoT, and Blockchain into isolated categories, failing to reflect how real-world multi-layer enterprise breaches occur.",
        "<b>Lack of Story-Driven Context:</b> Standard challenges lack realistic operational narratives, making it difficult for students to understand attacker motivation, attribution, and enterprise impact.",
        "<b>Inaccessible Tooling:</b> Conventional virtual machines require complex local setup, high RAM, and hypervisors. Hack The AI delivers a full multi-window forensic workstation directly in any standard browser."
    ]
    for p in problems:
        story.append(Paragraph(f"• {p}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 6. OBJECTIVES & 7. SCOPE & 8. COMPLETE STORYLINE
    # =========================================================================
    story.append(Paragraph("6. Project Objectives & Core Missions", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    objs = [
        "<b>Simulate Cross-Layer Enterprise Breaches:</b> Deliver realistic multi-vector incident cases interconnecting Web3, AI, IoT, and RBAC privilege escalation.",
        "<b>Provide In-Browser Multi-Window Workstation OS:</b> Implement an interactive GUI with browser tabs, terminal shells, Burp Suite interceptors, and attack graphs.",
        "<b>Incorporate Realistic SOC Team Dialogues:</b> Embed dynamic analyst dialogues (Lakshay, Shivam, Mehak, Shanu) providing realistic operational context and forensic guidance.",
        "<b>Enforce Strict Pedagogical Validation:</b> Gate chapter progression behind verified evidence tokens (e.g., AI-E01, AI-E02) and capstone certification quizzes.",
        "<b>Deliver Gamified Engagement:</b> Provide dynamic XP allocation, achievement badges, structured learning tracks, and global competitive leaderboards."
    ]
    for o in objs:
        story.append(Paragraph(f"• {o}", bullet_style))

    story.append(Paragraph("7. Project Scope (Current Implemented vs. Future)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Current Scope (v2.0 Implemented):</b> Full Web3 × AI × IoT simulation engine; Case NEX-042 (The Ghost in the Ledger); Case NEX-071 (The Vanishing Consensus); 55+ interactive chapter questions with progressive hints; multi-window desktop workstation; Burp Suite proxy emulator; forensic terminal; responsive mobile/tablet/desktop layouts; CSRF/CSP security hardening; Vercel serverless WSGI runtime; SQLite `/tmp` dynamic persistence.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Outside Current Scope (Future Roadmap):</b> Dedicated live Docker container virtualization per user session; multi-player collaborative SOC incident rooms; real Ethereum testnet transaction broadcasting; automated LLM scenario generation.",
        body_style
    ))

    story.append(Paragraph("8. Complete Project Concept & Investigation Lore", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "In Hack The AI, learners assume the role of Cyber Threat Forensics Investigators assigned to an active Security Operations Center (SOC). Incidents are presented not as theoretical puzzles, but as live emergency alerts. The investigation team consists of specialized analysts:",
        body_style
    ))
    
    team_members = [
        "<b>Lakshay (Lead Incident Commander &amp; Forensics Investigator):</b> Coordinates forensic strategy, correlates attack chains, and verifies containment flags.",
        "<b>Shivam (Web3 &amp; Blockchain Systems Specialist):</b> Deconstructs bridge contracts, on-chain transaction flows, and validator consensus forks.",
        "<b>Mehak (AI &amp; Data Security Analyst):</b> Audits neural network decision confidence, context injection traces, and dataset poisoning embeddings.",
        "<b>Shanu (IoT &amp; Telemetry Engineer):</b> Analyzes industrial sensor feeds, gateway routing anomalies, and RBAC permissions.",
        "<b>ORION / Sentinel:</b> The automated AI decision and security monitoring engine under investigation."
    ]
    for tm in team_members:
        story.append(Paragraph(f"• {tm}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 9. LAB ECOSYSTEM & 10. SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("9. Lab Ecosystem & Discovery Hierarchy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "The Hack The AI lab ecosystem is structured into distinct difficulty tiers and operational formats:",
        body_style
    ))
    
    eco_tiers = [
        "<b>Foundational Interactive Labs:</b> Introductory cyber labs introducing single-concept vulnerabilities (e.g., prompt injection, authentication bypass).",
        "<b>CyberLab Challenges:</b> Quick CTF-style challenges focusing on specific protocol mechanisms and cryptographic puzzles.",
        "<b>Flagship PRO Labs:</b> Advanced multi-chapter cyber investigations featuring multi-window desktop operating systems, realistic incident lore, 5 complex chapters, and comprehensive capstone examinations (Case NEX-042 and Case NEX-071).",
        "<b>Custom Lab Upload (Admin Engine):</b> Administrative interface allowing instructors to upload containerized `.zip` lab packages with automatic manifest parsing."
    ]
    for et in eco_tiers:
        story.append(Paragraph(f"• {et}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("10. System Architecture & High-Level Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "The platform utilizes a decoupled, multi-tier architecture ensuring clean separation between presentation, security middleware, application routing, forensic engines, and relational storage:",
        body_style
    ))

    # Architecture Visual Schematic
    arch_data = [
        [Paragraph("<b>TIER 1: MULTI-DEVICE PRESENTATION LAYER</b><br/>Desktop / Laptop / Tablet / Mobile &bull; Window Manager &bull; Terminal Console &bull; Burp Suite &bull; Attack Graph", ParagraphStyle('A1', parent=table_cell_style, alignment=1, textColor=c_primary))],
        [Paragraph("↓ <i>HTTPS Requests / CSRF Tokens (X-CSRFToken) / JSON Payloads</i> ↓", ParagraphStyle('Arr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>TIER 2: SECURITY &amp; EDGE MIDDLEWARE</b><br/>Flask-Talisman (CSP / TLS) &bull; Flask-WTF CSRF Engine &bull; Flask-Limiter &bull; Error Handlers (400/404/500)", ParagraphStyle('A2', parent=table_cell_style, alignment=1, textColor=colors.HexColor("#065f46")))],
        [Paragraph("↓ <i>Authenticated WSGI Routing &amp; Session Dispatcher</i> ↓", ParagraphStyle('Arr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>TIER 3: APPLICATION CONTROLLERS &amp; SERVICES</b><br/><code>routes.auth</code> &bull; <code>routes.dashboard</code> &bull; <code>routes.labs</code> &bull; <code>routes.api</code> &bull; <code>routes.leaderboard</code> &bull; <code>routes.pages</code> &bull; <code>routes.admin</code>", ParagraphStyle('A3', parent=table_cell_style, alignment=1, textColor=c_secondary))],
        [Paragraph("↓ <i>Forensic Execution, Evidence Tracking &amp; Answer Validation</i> ↓", ParagraphStyle('Arr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>TIER 4: INVESTIGATION &amp; GAMIFICATION LOGIC</b><br/>Evidence Engine &bull; Question Answer Validator &bull; Chapter State Machine &bull; XP Calculator &bull; Achievement Dispatcher", ParagraphStyle('A4', parent=table_cell_style, alignment=1, textColor=c_primary))],
        [Paragraph("↓ <i>SQLAlchemy ORM Data Mappings &amp; Transactions</i> ↓", ParagraphStyle('Arr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>TIER 5: PERSISTENCE &amp; STORAGE LAYER</b><br/>SQLite Database (<code>hacktheai.db</code> / <code>/tmp/hacktheai.db</code> on Vercel) &bull; HTML5 <code>localStorage</code> (Notes)", ParagraphStyle('A5', parent=table_cell_style, alignment=1, textColor=c_secondary))]
    ]
    arch_tab = Table(arch_data, colWidths=[504])
    arch_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f0f9ff")),
        ('BACKGROUND', (0,2), (0,2), colors.HexColor("#ecfdf5")),
        ('BACKGROUND', (0,4), (0,4), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,6), (0,6), colors.HexColor("#f0f9ff")),
        ('BACKGROUND', (0,8), (0,8), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(arch_tab)
    story.append(Paragraph("<b>Figure 1:</b> Multi-Tier System Architecture of Hack The AI.", fig_caption_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 11. APPLICATION STRUCTURE & 12. PROJECT DIRECTORY
    # =========================================================================
    story.append(Paragraph("11. Application Structure Diagram &amp; 12. Directory Tree", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    tree_code = """
HackTheAI-master/
├── api/
│   └── index.py                           # Serverless WSGI entry point for Vercel
├── database/
│   ├── hacktheai.db                       # Relational SQLite database instance
│   └── .secret_key                        # Persistent local secret key storage
├── routes/
│   ├── admin.py                           # Lab zip upload, container management, audit logs
│   ├── api.py                             # Question validation, hints, lab restart endpoints
│   ├── auth.py                            # Login, registration, session initialization, logout
│   ├── dashboard.py                       # User dashboard, active investigations, stats
│   ├── labs.py                            # Lab catalog, detail briefings, workstation views
│   ├── leaderboard.py                     # Dynamic ranking and global XP leaderboard
│   └── pages.py                           # Challenges, achievements, learning tracks, profile
├── services/
│   ├── audit_service.py                   # User activity and security audit logging
│   ├── docker_service.py                  # Optional container orchestration service
│   ├── hint_service.py                    # Progressive tiered hint retrieval engine
│   ├── lab_parser_service.py              # Lab manifest and zip archive parser
│   └── quiz_service.py                    # Answer scoring and quiz validation logic
├── static/
│   ├── css/core/                          # variables.css, reset.css, typography.css
│   ├── css/components/                    # components.css, buttons, badges, modals
│   ├── css/layout/                        # layout.css, sidebar, topbar, mobile drawer
│   ├── css/pages/                         # ghost_ledger_desktop.css, vanishing_consensus_desktop.css
│   └── js/                                # main.js, ghost_ledger_desktop.js, vanishing_consensus_desktop.js
├── templates/                             # Jinja2 HTML5 templates (base.html, workstations, auth, dashboard)
├── app.py                                 # Flask Application Factory, Talisman CSP, DB init
├── config.py                              # Dynamic Environment Config & Secret Key Resolver
├── models.py                              # SQLAlchemy Data Models (User, Lab, Mission, Quiz, Progress)
├── seed_ghost_ledger.py                   # Case NEX-042 25-question investigation seeder
├── seed_vanishing_consensus.py            # Case NEX-071 30-question investigation seeder
└── vercel.json                            # Vercel Serverless Routing & Deployment Configuration
    """
    story.append(Paragraph(f"<pre>{tree_code.strip()}</pre>", code_style))
    
    story.append(PageBreak())

    # =========================================================================
    # 13. TECHNOLOGY STACK & 14. FRONTEND & 15. BACKEND
    # =========================================================================
    story.append(Paragraph("13. Technology Stack Table", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    stack_data = [
        [Paragraph("<b>Category</b>", table_cell_header), Paragraph("<b>Technology / Tool</b>", table_cell_header), Paragraph("<b>Purpose in Hack The AI</b>", table_cell_header)],
        [Paragraph("<b>Backend Engine</b>", table_cell_bold), Paragraph("Python 3.12 / Flask 3.0", table_cell_style), Paragraph("Core WSGI application framework, Blueprint modular architecture, request routing.", table_cell_style)],
        [Paragraph("<b>Relational ORM</b>", table_cell_bold), Paragraph("SQLAlchemy / Flask-Migrate", table_cell_style), Paragraph("Database schema definition, foreign-key relationships, SQLite persistence.", table_cell_style)],
        [Paragraph("<b>Security Middleware</b>", table_cell_bold), Paragraph("Flask-Talisman<br/>Flask-WTF / CSRFProtect<br/>Flask-Limiter", table_cell_style), Paragraph("Content Security Policy (CSP), strict CSRF token validation, memory-backed rate limiting.", table_cell_style)],
        [Paragraph("<b>Session Management</b>", table_cell_bold), Paragraph("Signed Secure Cookies / Flask-Session", table_cell_style), Paragraph("Stateless session persistence on serverless runtime with fallback support for Redis.", table_cell_style)],
        [Paragraph("<b>Frontend Markup</b>", table_cell_bold), Paragraph("Jinja2 / Semantic HTML5", table_cell_style), Paragraph("Modular template inheritance, dual-pane workstation layouts, post-investigation debriefs.", table_cell_style)],
        [Paragraph("<b>Styling System</b>", table_cell_bold), Paragraph("Vanilla CSS (Cyber Theme)", table_cell_style), Paragraph("Design tokens, dark cyber palette, responsive media queries, hardware acceleration.", table_cell_style)],
        [Paragraph("<b>Client Scripting</b>", table_cell_bold), Paragraph("Vanilla JavaScript (ES6+)", table_cell_style), Paragraph("Zero heavy dependencies; custom window manager, terminal emulator, Burp simulator.", table_cell_style)],
        [Paragraph("<b>Cloud Platform</b>", table_cell_bold), Paragraph("Vercel Serverless WSGI", table_cell_style), Paragraph("Global edge serverless execution configured via <code>vercel.json</code> and <code>api/index.py</code>.", table_cell_style)]
    ]
    stack_table = Table(stack_data, colWidths=[95, 135, 274])
    stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(stack_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("14. Frontend Architecture &amp; 15. Backend Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Frontend Architecture:</b> The user interface is structured around a centralized token system (<code>variables.css</code>) providing cyberpunk color palettes, dark glassmorphic elevations, and responsive layout grids. Workstations run an event-driven JavaScript window manager managing z-index layering, window minimize/maximize states, taskbar buttons, and touch-screen tab switching.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Backend Architecture:</b> The backend adopts Flask's application factory and Blueprint patterns. Route controllers delegate business logic to specialized services (<code>quiz_service</code>, <code>hint_service</code>, <code>audit_service</code>). All state-modifying requests require CSRF header verification and return structured JSON responses.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 16. DATABASE & 17. COMPLETE DATA FLOW & 18. USER JOURNEY
    # =========================================================================
    story.append(Paragraph("16. Database Architecture &amp; 17. Data Flow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    db_items = [
        "<b>User Table (<code>users</code>):</b> Stores user ID, unique username, email, hashed password, and role (student/admin).",
        "<b>Lab &amp; Mission Tables (<code>labs</code>, <code>missions</code>):</b> Master catalog of investigations, chapter sequences, and titles.",
        "<b>Mission Progress Table (<code>mission_progress</code>):</b> Tracks chapter status (LOCKED, AVAILABLE, IN PROGRESS, COMPLETED) per user.",
        "<b>Quiz &amp; Attempts Tables (<code>mission_quiz</code>, <code>quiz_attempts</code>):</b> Stores questions, canonical answers, XP values, and historical user submission logs.",
        "<b>Hint &amp; Usage Tables (<code>hints</code>, <code>hint_usage</code>):</b> Tiered hint system tracking hint consumption and XP penalties.",
        "<b>Evidence &amp; Progress Tables (<code>evidence</code>, <code>evidence_progress</code>):</b> Cryptographic evidence tokens collected during investigations."
    ]
    for dbi in db_items:
        story.append(Paragraph(f"• {dbi}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("18. End-to-End User Journey", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    journey_flow = [
        "<b>1. Discovery &amp; Briefing:</b> User logs in at <code>/login</code>, accesses <code>/dashboard</code>, and selects an active investigation at <code>/labs</code>.",
        "<b>2. Workstation Launch:</b> Navigating to <code>/lab/&lt;lab_id&gt;/workstation</code> initializes the 65-minute forensic session timer and loads Chapter 1.",
        "<b>3. Forensic Discovery:</b> Learner utilizes Terminal, Burp Suite, Case Files, and Attack Graph to uncover artifacts and compute hashes.",
        "<b>4. Question Validation:</b> Submitting the answer to <code>/api/lab/submit</code> updates database progress, awards XP, and unlocks Chapter 2.",
        "<b>5. Capstone Examination:</b> After completing all 5 chapters, the user passes the final certification quiz and submits the master case flag.",
        "<b>6. Debrief &amp; Leaderboard:</b> The user is redirected to the post-investigation debriefing page (<code>/lab/&lt;lab_id&gt;/post</code>), and global leaderboard standings update."
    ]
    for jf in journey_flow:
        story.append(Paragraph(f"• {jf}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 19. INVESTIGATION ENVIRONMENT (10 TOOLS)
    # =========================================================================
    story.append(Paragraph("19. Simulated Investigation Workstation Environment (10 Tools)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "The Hack The AI workstation provides ten specialized forensic tools operating in a responsive multi-window GUI:",
        body_style
    ))
    
    tools_list = [
        ("1. Forensic Web Browser", "Tabbed internal browser rendering internal applications: Bridge Explorers, Oracle Monitors, AI Sentinel Studios, and Validator Consensus Topologies."),
        ("2. Burp Suite Proxy Inspector", "Simulated security interceptor featuring tabbed views for HTTP/RPC Proxy history, raw Request/Response dual-pane headers, Repeater, and Target host tree."),
        ("3. Forensic Terminal Shell", "Interactive bash terminal executing built-in commands including <code>whoami</code>, <code>pwd</code>, <code>grep &lt;term&gt; &lt;file&gt;</code>, <code>python inspect_tx.py</code>, <code>iot-status</code>, <code>oracle</code>, <code>policy</code>, and <code>evidence</code>."),
        ("4. Case File Manager", "Monaco-style raw text editor with line numbering for inspecting logs (<code>iot-telemetry-gw184.log</code>, <code>wallet-report.txt</code>, <code>intel-feed-audit.txt</code>), policy files, and smart contract ABIs."),
        ("5. Scratchpad Notebook", "Investigator scratchpad automatically synced with browser <code>localStorage</code>, allowing learners to retain notes, tokens, and hashes without data loss."),
        ("6. Dynamic Attack Graph", "Interactive SVG/Node visualization mapping attacker ingress, pivot points, AI poisoning nodes, and root compromise state."),
        ("7. Evidence Locker", "Badge matrix displaying collected evidence tokens (e.g., AI-E01, AI-E02, AI-E03) verifying chapter prerequisites."),
        ("8. Web3 Bridge Monitor", "On-chain transaction explorer displaying block hashes, sender addresses, token amounts, nonces, and liquidity pool balances."),
        ("9. AI Oracle Studio", "Model telemetry dashboard displaying neural engine names, classification outputs, confidence ratings, and training poisoning traces."),
        ("10. Industrial IoT Gateway Stream", "Real-time telemetry aggregator monitoring 184 industrial sensors across 14 geographic sites, exposing synthetic identical output anomalies (0.00% jitter).")
    ]
    
    for t_name, t_desc in tools_list:
        story.append(Paragraph(f"<b>{t_name}:</b> {t_desc}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 20. PRACTICAL WORKFLOW & 21. AI & 22. WEB3 & 23. IoT & 24. CYBERSECURITY
    # =========================================================================
    story.append(Paragraph("20. Practical Workflow &amp; Core Technical Domains", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    domains = [
        ("Practical Learning Workflow", "Theory is translated into practical threat-hunting: <i>Learn &rarr; Investigate &rarr; Analyze &rarr; Collect Evidence &rarr; Answer &rarr; Validate &rarr; Progress</i>."),
        ("AI Security Component", "Simulates adversarial context injection (NEX-042) where forged intel feeds manipulate AI confidence to 99.2%, and dataset poisoning (NEX-071) where 1,200 synthetic device profiles poisoned the training dataset with label <code>BENIGN_SYNC</code>."),
        ("Web3 Security Component", "Analyzes cross-chain bridge logic, multi-sig oracle aggregation, smart contract transaction hashes (<code>TX-NEX-7741</code>), and liquidity pool draining."),
        ("Simulated IoT Component", "Emulates 184 industrial edge sensors (temperature, power draw, health) transmitting through Gateway GW-184 with anomalous identical synchronization."),
        ("Cybersecurity Architecture", "Explores multi-layer kill chains: RBAC over-privilege escalation (<code>INTEL-INGESTOR-02</code>), automated policy bypasses (<code>AUTO_SETTLE_TREASURY</code>), and Byzantine validator network partitions (3:2 state fork).")
    ]
    for d_title, d_desc in domains:
        story.append(Paragraph(f"<b>{d_title}:</b> {d_desc}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 26. PRO LAB 1 & 27. PRO LAB 2 WALKTHROUGHS
    # =========================================================================
    story.append(Paragraph("26. PRO Lab 1 Walkthrough: Case NEX-042 (The Ghost in the Ledger)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Case NEX-042 (250 XP):</b> 82,400 NXR tokens vanish from a secured treasury. The learner conducts a 5-chapter investigation:",
        body_style
    ))
    
    lab1_chs = [
        "<b>Ch 1 (The Phantom Transaction):</b> Investigator queries <code>TX-NEX-7741</code> on Bridge-Core-04, discovering destination wallet <code>0x7C41...9B2D</code>.",
        "<b>Ch 2 (The Poisoned Context):</b> Traces AI decision <code>ORION-DEC-7741</code> to unverified threat intelligence feed <code>NOVA-INTEL-FEED (NIF-2038)</code>.",
        "<b>Ch 3 (The Over-Privileged Ghost):</b> Audits IAM roles; finds service <code>INTEL-INGESTOR-02</code> possesses unauthorized wallet reputation writing rights.",
        "<b>Ch 4 (The Execution Matrix):</b> Audits <code>ORION-SETTLEMENT-V2</code> policy engine; identifies auto-settle trigger bypassing human approval at &ge; 95% confidence.",
        "<b>Ch 5 (The Attack Campaign):</b> Attributes attack to APT campaign <code>ORION-NEXUS</code>, captures Master Flag: <code>NEXORA{ghost_in_the_ledger_nex042}</code>."
    ]
    for ch in lab1_chs:
        story.append(Paragraph(f"• {ch}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("27. PRO Lab 2 Walkthrough: Case NEX-071 (The Vanishing Consensus)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Case NEX-071 (300 XP):</b> At 03:12 AM, 184 industrial IoT sensors transmit identical telemetry, causing a 3:2 consensus split:",
        body_style
    ))
    
    lab2_chs = [
        "<b>Ch 1 (The Silent Sensor Anomaly):</b> Audits 184 sensors across 14 sites; detects synthetic identical temperature (21.40°C) and 0.00% jitter on Gateway GW-184.",
        "<b>Ch 2 (The Poisoned Oracle Pipeline):</b> Discovers multi-sig price oracle <code>NOVA-PRICE-ORACLE</code> aggregated identical corrupted telemetry.",
        "<b>Ch 3 (The AI Model Blindspot):</b> Audits MODEL-ORION; discovers training injection <code>EMB-IOT-9041</code> suppressing volatility alarms.",
        "<b>Ch 4 (The Validator State Split):</b> Uncovers 3:2 BFT consensus fork (3 accept poisoned state, 2 reject) under Leader Node V03.",
        "<b>Ch 5 (Cross-Layer Reconstruction):</b> Reconstructs full IoT &rarr; Oracle &rarr; AI &rarr; Blockchain attack chain, captures Master Flag: <code>NEXORA{v4n1sh1ng_c0ns3nsus_n3x071}</code>."
    ]
    for ch in lab2_chs:
        story.append(Paragraph(f"• {ch}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 28-36: GAMIFICATION, SECURITY, RESPONSIVE, DEPLOYMENT, QA
    # =========================================================================
    story.append(Paragraph("28. Gamification Engine, Security Model &amp; Deployment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    infra_points = [
        ("XP & Progress Engine", "Dynamic XP allocation (50-300 XP) persisted in <code>lab_progress</code> and <code>mission_progress</code> with real-time progress bar animations."),
        ("Achievement System", "Profile badges unlocked upon completing milestones: <i>First Blood</i>, <i>Blockchain Forensic Specialist</i>, <i>AI Threat Hunter</i>, <i>Consensus Guardian</i>, <i>Master Investigator</i>."),
        ("Global Leaderboard", "Aggregated rankings calculated via total verified XP, completed investigation counts, and earliest completion timestamps."),
        ("Security Hardening", "<code>Flask-Talisman</code> Content Security Policy (CSP), strict CSRF protection via <code>Flask-WTF</code>, in-memory rate limiting via <code>Flask-Limiter</code>, secure cookie flags, and input escaping."),
        ("Serverless Deployment", "Configured for Vercel Serverless WSGI Python runtime via <code>api/index.py</code> and <code>vercel.json</code>. Automatically redirects SQLite persistence to <code>/tmp/hacktheai.db</code> in serverless containers."),
        ("Multi-Device Responsive Design", "Fully responsive across Desktop (1920×1080), Laptops (1366×768 / 1440×900), Tablets (768×1024), and Mobile (390×844 / 412×915) with dedicated single-tap Mobile View Switcher."),
        ("Testing & Verification", "Automated unit tests (<code>test_vercel_csrf.py</code>) verifying CSRF validation, session persistence, and database seed integrity.")
    ]
    for ip_title, ip_desc in infra_points:
        story.append(Paragraph(f"<b>{ip_title}:</b> {ip_desc}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 39. LIMITATIONS & 40. FUTURE SCOPE & 41. CONCLUSION
    # =========================================================================
    story.append(Paragraph("39. Project Limitations &amp; 40. Future Scope", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    scope_points = [
        ("Current Limitations", "Simulated edge environment rather than real hardware IoT devices; in-browser emulated network traffic rather than raw PCAP wire taps; stateless rate-limiting on serverless deployments."),
        ("Future Scope (v3.0 Roadmap)", "Dedicated per-session Docker container sandboxes; real EVM testnet deployment (Sepolia/Arbitrum); multi-player collaborative SOC incident response rooms with live WebSockets; AI-driven dynamic adversary scenarios.")
    ]
    for sp_title, sp_desc in scope_points:
        story.append(Paragraph(f"<b>{sp_title}:</b> {sp_desc}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("41. Conclusion &amp; Technical Assessment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Hack The AI</b> represents a significant milestone in practical cybersecurity pedagogy. By integrating <b>Artificial Intelligence</b>, <b>Decentralized Ledgers</b>, <b>Industrial IoT</b>, and <b>Distributed Consensus</b> into a high-fidelity story-driven investigation workstation, the platform empowers security practitioners with the exact investigative methodologies required to detect, analyze, and mitigate complex multi-layer cyber incidents in modern digital infrastructures.",
        body_style
    ))
    story.append(Paragraph(
        "The project stands as a fully realized, production-ready cybersecurity training platform with clean modular architecture, comprehensive test coverage, robust security hardening, and responsive cross-device performance.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Final Author Signature Block
    sig_data = [[
        Paragraph("<b>HACK THE AI &bull; TECHNICAL PROJECT REPORT</b><br/><b>Prepared By:</b> Lakshay Soni &bull; <b>Role:</b> Security Analyst &bull; <b>Organization:</b> TrinetLayer<br/><font size=7 color='#64748b'>Live Platform: https://hack-the-ai-labs.vercel.app/ &bull; Repository: https://github.com/lakshaysoni22/Hack-The-AI-Master</font>", ParagraphStyle('SB', fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_primary, alignment=1))
    ]]
    sig_tab = Table(sig_data, colWidths=[504])
    sig_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(sig_tab)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Complete professional project report generated: {filename}")


if __name__ == '__main__':
    target = "HACK_THE_AI_COMPLETE_PROJECT_REPORT.pdf"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    generate_pdf_report(target)
