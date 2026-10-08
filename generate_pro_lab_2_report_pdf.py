"""
generate_pro_lab_2_report_pdf.py
=============================================================================
Comprehensive PDF Report Generator for:
PRO LEVEL LAB 02: "THE VANISHING CONSENSUS" (Case NEX-071)
Hack The AI — Web3 × AI × Cybersecurity × IoT Security Lab

Author: Lakshay Soni
Role: Security Analyst
Organization: TrinetLayer
Target Output: PRO_LAB_2_THE_VANISHING_CONSENSUS_REPORT.pdf
=============================================================================
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page numbers and headers."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Top Header
        self.drawString(54, 750, "HACK THE AI // PRO LAB 02: THE VANISHING CONSENSUS (CASE NEX-071)")
        self.drawRightString(612 - 54, 750, "TRINETLAYER SECURITY OPERATIONS")
        self.setStrokeColor(colors.HexColor("#1e293b"))
        self.setLineWidth(0.75)
        self.line(54, 742, 612 - 54, 742)

        # Running Bottom Footer
        self.setStrokeColor(colors.HexColor("#1e293b"))
        self.setLineWidth(0.75)
        self.line(54, 48, 612 - 54, 48)
        self.drawString(54, 36, "CONFIDENTIAL // FOR AUTHORIZED CYBERSECURITY INVESTIGATION ONLY")
        self.drawRightString(612 - 54, 36, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(filename="PRO_LAB_2_THE_VANISHING_CONSENSUS_REPORT.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Base Colors
    c_primary = colors.HexColor("#0284c7")     # Sky / Cyan Primary Accent
    c_dark = colors.HexColor("#0f172a")        # Deep Slate
    c_secondary = colors.HexColor("#0369a1")   # Deep Blue
    c_accent = colors.HexColor("#38bdf8")      # Light Cyan
    c_purple = colors.HexColor("#9333ea")      # Purple
    c_green = colors.HexColor("#059669")       # Emerald
    c_red = colors.HexColor("#dc2626")         # Crimson
    c_text = colors.HexColor("#1e293b")        # Dark Charcoal Text
    c_muted = colors.HexColor("#64748b")       # Slate Muted
    c_bg_light = colors.HexColor("#f8fafc")    # Light Table BG
    c_code_bg = colors.HexColor("#0b1120")     # Terminal BG

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#ffffff"),
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#38bdf8"),
        alignment=0,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_text,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_text,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    dialogue_style = ParagraphStyle(
        'DialogueText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#38bdf8")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_text
    )

    def make_dialogue_table(dialogues):
        """Generates a polished, styled dialogue table with speaker badges and verbatim quotes."""
        dlg_rows = []
        speaker_colors = {
            "Shivam": ("#15803d", "#f0fdf4", "#bbf7d0"),    # Green
            "Mehak": ("#7c3aed", "#faf5ff", "#e9d5ff"),     # Purple
            "Shanu": ("#c2410c", "#fff7ed", "#ffedd5"),     # Orange/Amber
            "Lakshay": ("#0369a1", "#f0f9ff", "#bae6fd"),   # Cyber Blue
        }
        for speaker, text in dialogues:
            txt_color, bg_color, border_color = speaker_colors.get(speaker, ("#334155", "#f8fafc", "#e2e8f0"))
            speaker_p = Paragraph(f"<b><font color='{txt_color}'>{speaker}</font></b>", ParagraphStyle('Spk2', fontName='Helvetica-Bold', fontSize=8, alignment=1))
            dialogue_p = Paragraph(f'"{text}"', ParagraphStyle('DlgTxt2', fontName='Helvetica', fontSize=7.8, leading=10.6, textColor=c_text))
            
            t = Table([[speaker_p, dialogue_p]], colWidths=[68, 436])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor(bg_color)),
                ('BACKGROUND', (1,0), (1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(border_color)),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ALIGN', (0,0), (0,0), 'CENTER'),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (1,0), (1,0), 6),
                ('RIGHTPADDING', (1,0), (1,0), 6),
            ]))
            dlg_rows.append(t)
            dlg_rows.append(Spacer(1, 2))
        return dlg_rows

    story = []

    def section_divider():
        return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=8, spaceAfter=8)

    # ═════════════════════════════════════════════════════════════════════
    # 1. COVER PAGE
    # ═════════════════════════════════════════════════════════════════════
    cover_data = [
        [
            Paragraph("TRINETLAYER THREAT INTELLIGENCE &amp; FORENSIC LABS", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#38bdf8"), spaceAfter=10)),
        ],
        [
            Paragraph("THE VANISHING CONSENSUS", title_style),
        ],
        [
            Paragraph("PRO LEVEL LAB 02 &bull; CASE NEX-071<br/>Cross-Layer Trust-Chain Forensics: IoT Telemetry, Web3 Oracles, AI Model Poisoning, and Blockchain Consensus Divergence", subtitle_style),
        ],
        [
            HRFlowable(width="100%", thickness=1, color=colors.HexColor("#38bdf8"), spaceBefore=5, spaceAfter=15)
        ],
        [
            Paragraph("""
            <b>Investigation Domain:</b> WEB3 &times; AI &times; CYBERSECURITY &times; IoT<br/>
            <b>Case Identifier:</b> CASE-NEX-071<br/>
            <b>Difficulty Level:</b> Pro Certification (+300 XP)<br/>
            <b>Target Subject:</b> Industrial IoT Gateway Ingestion Tampering, Oracle Aggregation Blindness, Neural Feedback Poisoning (MODEL-ORION), and BFT-PoS Validator Consensus Split
            """, ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#e2e8f0"), spaceAfter=15))
        ],
        [
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#334155"), spaceBefore=5, spaceAfter=15)
        ],
        [
            Paragraph("""
            <b>PREPARED BY:</b><br/>
            <b>Author:</b> Lakshay Soni<br/>
            <b>Role:</b> Security Analyst<br/>
            <b>Organization:</b> TrinetLayer<br/>
            <b>Classification:</b> RESTRICTED // SOC TIER 2 FORENSICS<br/>
            <b>Date of Incident &amp; Report:</b> October 2026
            """, ParagraphStyle('CoverAuthor', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#94a3b8")))
        ]
    ]

    cover_table = Table(cover_data, colWidths=[504])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#090e17")),
        ('LEFTPADDING', (0, 0), (-1, -1), 24),
        ('RIGHTPADDING', (0, 0), (-1, -1), 24),
        ('TOPPADDING', (0, 0), (-1, -1), 28),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 28),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#0284c7")),
    ]))

    story.append(cover_table)
    story.append(Spacer(1, 15))

    # Executive Summary Card on Cover
    exec_summary_box = [
        [
            Paragraph("<b>EXECUTIVE CASE DISPATCH // INCIDENT NEX-071 SUMMARY</b>", ParagraphStyle('ExecH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0369a1"))),
        ],
        [
            Paragraph("""
            <b>The Vanishing Consensus (Case NEX-071)</b> investigates a sophisticated cross-layer trust-chain attack targeting industrial IoT infrastructure, Web3 oracle aggregation mechanisms, artificial intelligence sentinels, and Byzantine Fault Tolerant (BFT) blockchain consensus. At 03:12 UTC, 184 industrial sensors connected to <code>GATEWAY-GW-184</code> began reporting perfectly synchronized telemetry (21.40°C, 412.00W, 0.00% jitter). This synthesized stream was ingested into <code>NOVA-PRICE-ORACLE</code>, where 4 independent oracle providers agreed on the corrupted data. Concurrently, the AI sentinel <code>MODEL-ORION (v3.8.4)</code> suppressed volatility alarms due to prior training dataset poisoning (<code>EMB-IOT-9041</code>). Consequently, validator nodes computed conflicting local state roots, causing a silent 3:2 consensus partition without triggering standard protocol crash errors.
            """, ParagraphStyle('ExecB', fontName='Helvetica', fontSize=8, leading=11, textColor=c_text))
        ]
    ]
    exec_table = Table(exec_summary_box, colWidths=[504])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0f9ff")),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#bae6fd")),
    ]))
    story.append(exec_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 2. TABLE OF CONTENTS
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(section_divider())

    toc_data = [
        ["Section", "Title", "Domain Scope"],
        ["1.0", "Cover Page & Executive Dispatch", "Administrative & Executive"],
        ["2.0", "Table of Contents", "Navigation"],
        ["3.0", "Executive Summary & Incident Context", "Strategic Cyber Overview"],
        ["4.0", "Lab Overview & Technical Parameters", "Case NEX-071 Specifications"],
        ["5.0", "Complete Incident Briefing (The Core Anomaly)", "Incident Telemetry"],
        ["6.0", "Complete Narrative Storyline & Characters", "Story & Dialogue Records"],
        ["7.0", "Storyline & Forensic Investigation Timeline", "Chronological Breakdown"],
        ["8.0", "Story &rarr; Technical Investigation Mapping Matrix", "Cross-Domain Alignment"],
        ["9.0", "Chapter 1: The Signal That Lied", "IoT Telemetry Forensics"],
        ["10.0", "Chapter 2: The Oracle That Saw Tomorrow", "IoT &times; Web3 Oracle Security"],
        ["11.0", "Chapter 3: The Model That Learned the Attack", "AI Model Poisoning Audit"],
        ["12.0", "Chapter 4: The Fork Nobody Saw", "BFT Validator Consensus Split"],
        ["13.0", "Chapter 5: The Vanishing Consensus (Full Recovery)", "Cross-Layer Containment"],
        ["14.0", "Complete 5-Chapter Progression Architecture", "Technical Flowchart"],
        ["15.0", "Learning Objectives & Educational Competencies", "Pedagogy & Training"],
        ["16.0", "Business & Operational Impact Analysis", "Risk & Financial Exposure"],
        ["17.0", "Cross-Domain Attack Surface Analysis", "IoT / Web3 / AI / Consensus"],
        ["18.0", "Threat Model & Adversary TTP Analysis", "MITRE ATT&CK Mapping"],
        ["19.0", "Cross-Domain Technical Architecture", "System Schematic"],
        ["20.0", "IoT Architecture & Telemetry Ingestion Layer", "Sensor & Gateway Telemetry"],
        ["21.0", "Web3 & Blockchain Architecture", "Oracles, State Roots & BFT"],
        ["22.0", "AI Sentinel & Neural Decision Architecture", "MODEL-ORION v3.8.4"],
        ["23.0", "Cybersecurity & Investigation Environment", "SOC Desktop Suite"],
        ["24.0", "Practical Investigation Workflow", "Step-by-Step Methodology"],
        ["25.0", "Forensic Evidence Vault & Cryptographic Artifacts", "Tokens IOT-E11 to GOV-E15"],
        ["26.0", "End-to-End System Data Flow", "Data Pipeline Diagram"],
        ["27.0", "Chapter Question & Forensic Validation Matrix", "30 Verifiable Objectives"],
        ["28.0", "Final Multi-Layer Capstone Assessment", "10-Question Evaluation"],
        ["29.0", "XP, Progress Tracking & Session Management", "Scoring & Timer Mechanics"],
        ["30.0", "Achievements, Learning System & Leaderboard", "User Motivation & Badges"],
        ["31.0", "Database Schema & Entity Relationship Model", "SQLAlchemy Models"],
        ["32.0", "Codebase File Structure & Module Responsibilities", "Repository Layout"],
        ["33.0", "Security Controls & Session Sandboxing", "Authentication & CSRF"],
        ["34.0", "Responsive Multi-Platform Interface Design", "Desktop / Tablet / Mobile"],
        ["35.0", "User Interface & Forensic Screenshot Documentation", "SOC Tool Interfaces"],
        ["36.0", "Required Architectural & Flow Diagrams", "19 Visual Schematics"],
        ["37.0", "Story + Technical Correlation Detailed Table", "Pedagogical Integration"],
        ["38.0", "Complete Incident Response Timeline", "Chronological Log"],
        ["39.0", "Final Case Resolution (The Master Flag)", "NEXORA{v4n1sh1ng...}"],
        ["40.0", "Cybersecurity & Engineering Skills Developed", "Hands-On Competencies"],
        ["41.0", "Technical, Operational & Strategic Lessons", "Industry Takeaways"],
        ["42.0", "Current Limitations vs Proposed Enhancements", "Gaps & Roadmap"],
        ["43.0", "Future Scope & Platform Evolution", "Next-Gen Capabilities"],
        ["44.0", "Conclusion & Final Assessment", "Closing Statement"],
        ["45.0", "Appendix A: Forensic File & Command Reference", "Terminal & Log Reference"],
        ["46.0", "Appendix B: Evidence & Master Token Index", "Cryptographic Hashes"],
        ["47.0", "Appendix C: Post-Investigation Debriefing Records", "Incident Metrics"]
    ]

    t_toc = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(toc_data)],
        colWidths=[45, 315, 144]
    )
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 3. EXECUTIVE SUMMARY & 4. LAB OVERVIEW
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3.0 EXECUTIVE SUMMARY &amp; INCIDENT OVERVIEW", h1_style))
    story.append(section_divider())
    story.append(Paragraph("""
    <b>The Vanishing Consensus (Case NEX-071)</b> represents an advanced, multi-stage cybersecurity investigation that exposes the fragile trust boundaries linking physical Internet of Things (IoT) sensors, Web3 oracle data aggregators, artificial intelligence sentinels, and decentralized blockchain consensus protocols. Unlike conventional single-domain security scenarios—such as a smart contract reentrancy exploit or a standard credential theft attack—Case NEX-071 illustrates an adversary who deliberately refrains from attacking any single layer directly. Instead, the threat actor exploits the implicit trust relationships and data transformations between layers.
    """, body_style))
    story.append(Paragraph("""
    <b>Why the Incident is Highly Suspicious:</b> In physical sensor networks, real-world entropy, thermal variance, ambient vibrations, and local electrical load fluctuations naturally prevent identical telemetry readings across geographically dispersed nodes. In Case NEX-071, 184 industrial sensors across 14 global sites suddenly reported perfectly identical metrics (21.40°C temperature and 412.00W power draw) with exactly 0.00% measurement jitter. Downstream systems treated this unnatural synchronization not as an anomaly, but as verified reality, because the AI anomaly detection engine had been pre-conditioned via dataset poisoning to classify synthetic synchronization as benign.
    """, body_style))

    story.append(Paragraph("4.0 LAB OVERVIEW &amp; TECHNICAL PARAMETERS", h1_style))
    story.append(section_divider())

    overview_rows = [
        ["Parameter", "Specification Value", "Investigation Significance"],
        ["Lab Name", "The Vanishing Consensus", "Official Case Title"],
        ["Case ID / Lab ID", "Case NEX-071 / lab7", "Database & Telemetry Identifier"],
        ["Difficulty / Track", "PRO / Professional Cybersecurity Track", "Advanced Multi-Domain Lab"],
        ["Total Experience (XP)", "300 XP (+50 XP per verified task)", "Player Progression Metric"],
        ["Estimated Duration", "55 - 65 Minutes (65m Session Auto-Restart)", "Operational Time Budget"],
        ["Investigation Scope", "5 Chapters + 10-Question Multi-Layer Capstone", "30 Core Tasks + Capstone Quiz"],
        ["Technical Domains", "IoT &times; Web3 &times; AI &times; Cybersecurity &times; Blockchain", "Cross-Layer Converged Security"],
        ["Target Systems", "GATEWAY-GW-184, NOVA-PRICE-ORACLE, MODEL-ORION, BFT-POS", "Primary Attacked Components"],
        ["Available SOC Tools", "Consensus Monitor, Burp Suite Proxy, Terminal, Case Files, Attack Graph", "Integrated Desktop Workstation"]
    ]
    t_overview = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(overview_rows)],
        colWidths=[110, 190, 204]
    )
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 10))

    # ═════════════════════════════════════════════════════════════════════
    # 5. COMPLETE INCIDENT BRIEFING
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5.0 COMPLETE INCIDENT BRIEFING // CASE NEX-071", h1_style))
    story.append(section_divider())

    briefing_box = [
        [
            Paragraph("<b>⚡ CORE INCIDENT BRIEFING (AS PRESENTED IN SOC WORKSTATION)</b>", ParagraphStyle('BriefH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0284c7"))),
        ],
        [
            Paragraph("""
            <b>03:12 AM.</b> The blockchain monitoring system detects something that should be impossible.<br/><br/>
            A new block contains a transaction that appears to have happened before its own oracle price existed.<br/><br/>
            At almost the same time, several industrial IoT sensors connected to the Web3 infrastructure begin reporting perfectly synchronized telemetry.<br/><br/>
            <i>Temperature. Power consumption. Location. Device health. Everything looks normal. Almost too normal.</i><br/><br/>
            Three validator nodes agree on the resulting blockchain state. Two reject it.<br/><br/>
            Meanwhile, the AI security engine reports: <b style="color:#0284c7;">'CONSENSUS HEALTHY — 98.7%'</b><br/><br/>
            No validator appears compromised. No private key has been stolen. The IoT devices still appear online.<br/><br/>
            <b style="color:#dc2626;">Yet the network is slowly beginning to disagree with itself. Someone isn't attacking the blockchain directly — someone is manipulating what the blockchain was told to believe.</b>
            """, ParagraphStyle('BriefB', fontName='Helvetica', fontSize=8, leading=11.5, textColor=c_text))
        ]
    ]
    t_briefing = Table(briefing_box, colWidths=[504])
    t_briefing.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#0284c7")),
    ]))
    story.append(t_briefing)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 6. COMPLETE STORYLINE & CHARACTERS
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6.0 COMPLETE STORYLINE &amp; CHARACTER ROSTER", h1_style))
    story.append(section_divider())
    story.append(Paragraph("""
    The narrative of <b>Case NEX-071</b> is structured around a multi-disciplinary security incident response team investigating a silent consensus divergence. Each team member brings deep domain-specific expertise, guiding the learner through physical IoT forensics, Web3 oracle data aggregation, AI model training feedback audits, and distributed consensus validation.
    """, body_style))

    char_rows = [
        ["Character Name", "Operational Role", "Key Investigation Contribution", "Primary Focus Area"],
        ["Lakshay", "Lead Incident Responder & Forensic Investigator", "Directs cross-layer investigation, formulates hypotheses, correlates physical and on-chain evidence, executes recovery.", "Cross-Domain Forensics & Recovery"],
        ["Shivam", "Distributed Systems & Web3 Infrastructure Lead", "Analyzes IoT gateway logs, validator node state divergence, BFT-PoS consensus partition, and state root mismatches.", "IoT Gateway & Validator Consensus"],
        ["Mehak", "AI Security & ML Governance Specialist", "Discovers training dataset feedback poisoning (EMB-IOT-9041), audits neural inference confidence, and purges malicious weights.", "AI Model Poisoning & Governance"],
        ["Shanu", "Threat Intelligence & Oracle Security Analyst", "Investigates oracle feed dependencies, multi-provider aggregation blindness, and physical entropy absence.", "Web3 Oracles & Threat Intel"],
        ["MODEL-ORION", "Autonomous AI Sentinel (v3.8.4)", "Supervises live network transactions, suppresses circuit breakers due to poisoned baseline weights, reports false 98.7% health.", "Simulated AI Sentinel Engine"]
    ]
    t_chars = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(char_rows)],
        colWidths=[80, 120, 194, 110]
    )
    t_chars.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_chars)
    story.append(Spacer(1, 10))

    # ═════════════════════════════════════════════════════════════════════
    # 7. STORYLINE TIMELINE & 8. STORY -> TECHNICAL MAPPING
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("7.0 STORYLINE &amp; FORENSIC INVESTIGATION TIMELINE", h1_style))
    story.append(section_divider())

    timeline_rows = [
        ["Phase / Timestamp", "Narrative Story Event", "Technical Discovery / Clue", "Investigative Action"],
        ["03:10:44 UTC", "Sensor Telemetry Ingestion", "184 industrial sensors transmit valid local readings to GATEWAY-GW-184.", "Hardware flash memory audit."],
        ["03:10:48 UTC", "Gateway Telemetry Tampering", "Gateway applies synthetic filter SYNTH_HARMONIC_V4, outputting 21.40°C & 412W.", "Compare local flash vs gateway stream."],
        ["03:12:00 UTC", "Oracle Ingestion & Broadcast", "NOVA-PRICE-ORACLE consumes stream; 4 independent nodes agree on poisoned data.", "Inspect oracle aggregation payload."],
        ["03:12:04 UTC", "AI Sentinel Suppression", "MODEL-ORION matches synthetic data to EMB-IOT-9041, reports NORMAL (98.7%).", "Audit AI fine-tuning training corpus."],
        ["03:12:08 UTC", "Validator Execution Divergence", "3 nodes compute State Root 0x4f8e... (Accept); 2 nodes compute 0x98a2... (Reject).", "Query 21-node validator state roots."],
        ["03:15:30 UTC", "Cross-Layer Containment", "GOV-NEX-071 proposal isolates gateway, purges model weights, restores consensus.", "Execute governance proposal & verify flag."]
    ]
    t_timeline = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(timeline_rows)],
        colWidths=[75, 140, 165, 124]
    )
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_timeline)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 9.0 CHAPTER 1: THE SIGNAL THAT LIED
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("9.0 CHAPTER 1: THE SIGNAL THAT LIED", h1_style))
    story.append(Paragraph("<b>Domain:</b> IoT Security / Digital Forensics &bull; <b>Target Gateway:</b> GATEWAY-GW-184 &bull; <b>Evidence Token:</b> IOT-E11", h2_style))
    story.append(section_divider())

    story.append(Paragraph("<b>Narrative Story &amp; Dialogue Stream (As Spoken in Lab):</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark, spaceAfter=4)))
    ch1_dialogues = [
        ("Shivam", "The IoT gateway shows 184 active devices, but the telemetry patterns from several devices are nearly identical."),
        ("Mehak", "These sensors are in different locations. Their readings shouldn't synchronize this perfectly."),
        ("Shanu", "Perfect synchronization can be more suspicious than random noise. Real physical systems usually contain variation."),
        ("Lakshay", "Check whether the devices generated these readings locally or whether the gateway modified them."),
        ("Shivam", "That's the problem. The devices appear healthy, but the gateway logs show a different sequence of telemetry events."),
        ("Mehak", "Then the blockchain may not be the beginning of the attack. It may only be where the manipulated data became permanent.")
    ]
    for d_elem in make_dialogue_table(ch1_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 1 Objectives &amp; Verifiable Findings Matrix:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark)))

    ch1_tasks = [
        ["#", "Objective Question", "Verified Finding / Answer", "Technical Explanation"],
        ["1", "Why are perfectly synchronized IoT readings suspicious?", "Real physical systems contain variation", "Natural physical environments exhibit entropy and measurement jitter."],
        ["2", "Why is geographically identical telemetry unusual?", "Different locations experience different environmental conditions", "Dispersed sensors reflect differing ambient temperatures and power loads."],
        ["3", "What should investigators compare first: device-generated telemetry or gateway telemetry?", "Device-generated telemetry", "Comparing local flash memory logs against gateway stream reveals in-transit tampering."],
        ["4", "Why can a healthy-looking IoT device still be compromised?", "Upstream gateway manipulates telemetry", "Physical hardware remains intact while upstream gateway alters payload packets."],
        ["5", "What evidence suggests that the gateway may have altered telemetry?", "Gateway logs show a different sequence of events", "Device memory logs showed normal variation while gateway recorded artificial stream."],
        ["6", "If physical devices function normally but telemetry is manipulated, which layer failed?", "Telemetry ingestion layer", "The data ingestion and aggregation layer upstream of the blockchain was intercepted."]
    ]
    t_ch1 = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(ch1_tasks)],
        colWidths=[20, 160, 150, 174]
    )
    t_ch1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_ch1)
    story.append(Spacer(1, 8))

    # ═════════════════════════════════════════════════════════════════════
    # 10.0 CHAPTER 2: THE ORACLE THAT SAW TOMORROW
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("10.0 CHAPTER 2: THE ORACLE THAT SAW TOMORROW", h1_style))
    story.append(Paragraph("<b>Domain:</b> IoT &times; Web3 Oracle Security &bull; <b>Target Oracle:</b> NOVA-PRICE-ORACLE &bull; <b>Evidence Token:</b> ORACLE-E12", h2_style))
    story.append(section_divider())

    story.append(Paragraph("<b>Narrative Story &amp; Dialogue Stream (As Spoken in Lab):</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark, spaceAfter=4)))
    ch2_dialogues = [
        ("Shanu", "The oracle isn't receiving raw blockchain data. It's consuming external telemetry."),
        ("Shivam", "And that telemetry originates from the IoT gateway."),
        ("Mehak", "Then the oracle providers aren't independent if they're all consuming the same manipulated telemetry stream."),
        ("Lakshay", "Exactly. The attack moved from the physical world into the Web3 trust layer."),
        ("Shanu", "Four providers can appear to agree while actually repeating the same poisoned information."),
        ("Mehak", "Which means the blockchain may be reaching consensus on data that was already compromised before it entered the chain.")
    ]
    for d_elem in make_dialogue_table(ch2_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 2 Objectives &amp; Verifiable Findings Matrix:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark)))

    ch2_tasks = [
        ["#", "Objective Question", "Verified Finding / Answer", "Technical Explanation"],
        ["1", "Where does NOVA-PRICE-ORACLE obtain its external data?", "External telemetry aggregation layer", "Aggregates external telemetry streams from industrial IoT gateways."],
        ["2", "Why does compromised IoT telemetry affect Web3 systems?", "Oracles consume external telemetry as truth", "Smart contracts cannot fetch off-chain data independently and trust oracle feeds."],
        ["3", "Why can multiple oracle providers still represent one single source?", "They consume the same upstream IoT telemetry stream", "Multiple independent nodes consuming a single corrupted stream replicate identical error."],
        ["4", "What happens when manipulated telemetry is aggregated before reaching chain?", "Poisoned aggregate enters oracle as trusted state", "Pre-chain math averages poisoned telemetry, cementing falsified value on-chain."],
        ["5", "Why is 'multiple providers agree' insufficient for data integrity?", "Providers repeat the same corrupted upstream source", "Node consensus only proves agreement on received data, not external physical truth."],
        ["6", "At what point did the attack cross from IoT into Web3 security?", "When compromised IoT telemetry became trusted external oracle data", "The boundary transition occurred when the oracle feed accepted poisoned gateway data."]
    ]
    t_ch2 = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(ch2_tasks)],
        colWidths=[20, 160, 150, 174]
    )
    t_ch2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_ch2)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 11.0 CHAPTER 3: THE MODEL THAT LEARNED THE ATTACK
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("11.0 CHAPTER 3: THE MODEL THAT LEARNED THE ATTACK", h1_style))
    story.append(Paragraph("<b>Domain:</b> IoT AI Security / Model Poisoning &bull; <b>AI Sentinel:</b> MODEL-ORION (v3.8.4) &bull; <b>Evidence Token:</b> AI-E13", h2_style))
    story.append(section_divider())

    story.append(Paragraph("<b>Narrative Story &amp; Dialogue Stream (As Spoken in Lab):</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark, spaceAfter=4)))
    ch3_dialogues = [
        ("Shanu", "ORION saw the synchronized IoT telemetry, but it classified the pattern as normal."),
        ("Lakshay", "Can the model distinguish physical anomalies from fabricated telemetry?"),
        ("Shanu", "Only if its training data taught it what both look like."),
        ("Mehak", "I found repeated synthetic device events in the training feedback."),
        ("Shivam", "So someone wasn't only manipulating live IoT telemetry. They were preparing the AI to trust similar behavior."),
        ("Lakshay", "The physical layer was poisoned first. Then the AI was trained not to question the poison.")
    ]
    for d_elem in make_dialogue_table(ch3_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 3 Objectives &amp; Verifiable Findings Matrix:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark)))

    ch3_tasks = [
        ["#", "Objective Question", "Verified Finding / Answer", "Technical Explanation"],
        ["1", "What IoT behavior did ORION classify as normal?", "Synchronized IoT telemetry", "MODEL-ORION classified synchronized readings as NORMAL_NETWORK_VARIANCE."],
        ["2", "Why is synchronized telemetry useful for detecting IoT manipulation?", "It indicates synthetic data injection", "In genuine physical networks, cross-sensor synchronization indicates replay attacks."],
        ["3", "How can poisoned training data affect IoT security?", "AI classifies malicious patterns as normal", "When datasets contain adversarial samples labelled benign, AI ignores live attacks."],
        ["4", "What is the relationship between IoT telemetry and the AI anomaly detector?", "IoT telemetry serves as feature inputs for AI", "Incoming sensor streams form primary input feature vectors for neural evaluation."],
        ["5", "Why can a high-confidence AI result still be wrong?", "Model was trained on poisoned data", "Statistical confidence only reflects alignment with weights, which may be corrupted."],
        ["6", "If an AI is trained on manipulated telemetry, can it detect it later?", "No, because it learned manipulated patterns as legitimate", "The model internalizes malicious patterns as baseline, blinding it during live inference."]
    ]
    t_ch3 = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(ch3_tasks)],
        colWidths=[20, 160, 150, 174]
    )
    t_ch3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_ch3)
    story.append(Spacer(1, 8))

    # ═════════════════════════════════════════════════════════════════════
    # 12.0 CHAPTER 4: THE FORK NOBODY SAW
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("12.0 CHAPTER 4: THE FORK NOBODY SAW", h1_style))
    story.append(Paragraph("<b>Domain:</b> IoT &times; AI &times; Blockchain Consensus &bull; <b>Topology:</b> 21-Node BFT Grid &bull; <b>Evidence Token:</b> CONSENSUS-E14", h2_style))
    story.append(section_divider())

    story.append(Paragraph("<b>Narrative Story &amp; Dialogue Stream (As Spoken in Lab):</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark, spaceAfter=4)))
    ch4_dialogues = [
        ("Shivam", "The validators are no longer processing exactly the same derived state."),
        ("Mehak", "Because the upstream telemetry was inconsistent?"),
        ("Shivam", "Exactly. Different data paths produced slightly different oracle states."),
        ("Shanu", "And ORION isn't escalating the difference because the model considers the telemetry pattern normal."),
        ("Lakshay", "So IoT manipulation created the input anomaly, AI suppressed the warning, and the blockchain inherited the disagreement."),
        ("Mehak", "Three separate security layers failed in sequence.")
    ]
    for d_elem in make_dialogue_table(ch4_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 4 Objectives &amp; Verifiable Findings Matrix:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark)))

    ch4_tasks = [
        ["#", "Objective Question", "Verified Finding / Answer", "Technical Explanation"],
        ["1", "How did IoT telemetry ultimately influence validator state?", "Altering smart contract inputs through poisoned oracle", "Manipulated telemetry fed oracle, injecting false price state into contract execution."],
        ["2", "Why did different validators receive different derived states?", "Conflicting oracle data paths and timing across nodes", "Network propagation latency caused some nodes to compute Root A while others Root B."],
        ["3", "How did AI failure contribute to the consensus problem?", "ORION suppressed anomaly warnings by classifying patterns as normal", "Because AI classified telemetry as normal, automated circuit breakers never paused blocks."],
        ["4", "Why didn't the blockchain immediately detect the issue?", "Validators executed deterministically from local inputs without protocol errors", "Each node executed valid VM bytecode; error was in truthfulness of inputs, not syntax."],
        ["5", "Which security layers were involved in the attack?", "IoT, Oracle Web3, AI, Blockchain", "The attack chained across physical sensors, Web3 oracles, AI sentinels, and BFT consensus."],
        ["6", "Why is cross-layer attack harder to detect than single-layer?", "Each layer appears individually healthy while trust boundaries are exploited", "No component crashes; exploit occurs across inter-layer trust assumptions."]
    ]
    t_ch4 = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(ch4_tasks)],
        colWidths=[20, 160, 150, 174]
    )
    t_ch4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_ch4)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 13.0 CHAPTER 5: THE VANISHING CONSENSUS (FULL ATTACK RECONSTRUCTION)
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("13.0 CHAPTER 5: THE VANISHING CONSENSUS (FULL ATTACK RECONSTRUCTION)", h1_style))
    story.append(Paragraph("<b>Domain:</b> Full Cross-Layer Attack Reconstruction &bull; <b>Proposal:</b> GOV-NEX-071 &bull; <b>Evidence Token:</b> GOV-E15", h2_style))
    story.append(section_divider())

    story.append(Paragraph("<b>Narrative Story &amp; Dialogue Stream (As Spoken in Lab):</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark, spaceAfter=4)))
    ch5_dialogues = [
        ("Lakshay", "The attack started outside the blockchain."),
        ("Shivam", "At the IoT telemetry layer."),
        ("Mehak", "The manipulated data then entered the oracle ecosystem."),
        ("Shanu", "And the poisoned AI model helped hide the anomaly."),
        ("Shivam", "Different validators eventually processed different states."),
        ("Lakshay", "So the blockchain wasn't directly hacked."),
        ("Mehak", "It was manipulated through the trust chain connecting IoT, AI, Web3 and blockchain.")
    ]
    for d_elem in make_dialogue_table(ch5_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 5 Objectives &amp; Verifiable Findings Matrix:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark)))

    ch5_tasks = [
        ["#", "Objective Question", "Verified Finding / Answer", "Technical Explanation"],
        ["1", "Where did the attack actually begin?", "IoT telemetry layer", "The root origin was the compromised telemetry stream on GATEWAY-GW-184."],
        ["2", "Why was the IoT layer critical to the attack?", "It provided the initial poisoned telemetry feeding downstream systems", "Without manipulated sensor stream, downstream oracle and AI produce no fraud state."],
        ["3", "How did manipulated telemetry reach the blockchain?", "Via Web3 oracle aggregation feed", "The oracle pipeline ingested gateway data and broadcasted it as verified on-chain state."],
        ["4", "How did AI help hide the attack?", "By classifying anomalous telemetry and spikes as legitimate", "Poisoned neural network categorized anomaly as benign, preventing SOC alarms."],
        ["5", "Why did validator disagreement occur?", "Validators processed conflicting oracle-derived states", "Differences in oracle propagation timing produced divergent state transitions."],
        ["6", "Why is the attack best described as a 'cross-layer trust-chain attack'?", "Exploited trust dependencies connecting IoT, Web3, AI, and Blockchain", "Chained vulnerabilities across IoT integrity, oracle trust, AI alignment, and BFT consensus."]
    ]
    t_ch5 = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(ch5_tasks)],
        colWidths=[20, 160, 150, 174]
    )
    t_ch5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_ch5)
    story.append(Spacer(1, 10))

    # ═════════════════════════════════════════════════════════════════════
    # 28.0 FINAL MULTI-LAYER CAPSTONE ASSESSMENT (10 QUESTIONS)
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("28.0 FINAL MULTI-LAYER CAPSTONE ASSESSMENT (10 QUESTIONS)", h1_style))
    story.append(Paragraph("<b>Evaluation Standard:</b> 10 Multi-Choice Forensic Questions &bull; <b>Passing Threshold:</b> &ge; 70% &bull; <b>XP Reward:</b> +300 XP", h2_style))
    story.append(section_divider())

    capstone_questions = [
        ["#", "Capstone Evaluation Question", "Correct Verified Option", "Evaluation Rationale"],
        ["1", "What was the earliest suspicious indicator in Case NEX-071?", "B) Perfectly synchronized IoT telemetry across sensors", "Physical environments have natural entropy; identical readings indicate synthesis."],
        ["2", "Why was the IoT telemetry critical to the attack?", "A) It became manipulated data source feeding Web3/blockchain", "Physical sensor stream is the ground-truth feed for smart contract oracles."],
        ["3", "Why did oracle provider agreement fail to guarantee truth?", "A) Multiple providers depended on same compromised source", "Agreement only proves replication consistency, not source physical integrity."],
        ["4", "How was MODEL-ORION compromised?", "A) Training feedback contained synthetic IoT data labelled legitimate", "Adversary poisoned fine-tuning dataset with EMB-IOT-9041 signature."],
        ["5", "Why could ORION confidently classify attack as normal?", "A) Model learned manipulated patterns as normal baseline", "High statistical confidence reflected alignment with poisoned training weights."],
        ["6", "How did IoT manipulation affect blockchain consensus?", "A) Altered oracle states causing validators to process different states", "Inconsistent oracle timing produced divergent local EVM state roots."],
        ["7", "What made the attack difficult to detect?", "A) Each layer appeared healthy while trust boundaries were exploited", "No single module crashed; trust assumptions between layers were breached."],
        ["8", "Which sequence best represents the attack?", "B) IoT &rarr; Oracle &rarr; AI &rarr; Validator divergence", "Physical telemetry poisoned &rarr; Oracle ingested &rarr; AI suppressed &rarr; Chain split."],
        ["9", "Did the attacker need to directly control or hack the blockchain?", "B) No — manipulated trusted information upstream of consensus", "Consensus algorithms executed properly on corrupted input data."],
        ["10", "What is the deepest security lesson from Case NEX-071?", "D) Security depends on protecting trust boundaries across IoT, AI, Web3, Blockchain", "End-to-end security requires cross-layer verification and physical entropy audits."]
    ]
    t_capstone = Table(
        [[Paragraph(cell, table_header_style if i == 0 else table_cell_style) for cell in row] for i, row in enumerate(capstone_questions)],
        colWidths=[20, 160, 160, 164]
    )
    t_capstone.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_capstone)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 17. ATTACK SURFACE, 18. THREAT MODEL & 19. ARCHITECTURE
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("17.0 CROSS-DOMAIN ATTACK SURFACE &amp; 18.0 THREAT MODEL", h1_style))
    story.append(section_divider())

    story.append(Paragraph("""
    <b>Cross-Domain Attack Surface Analysis:</b>
    <br/>• <b>Physical &amp; IoT Ingestion Surface:</b> Industrial telemetry gateway (<code>GATEWAY-GW-184</code>) lacks hardware-enforced measurement entropy validation, allowing synthetic payload overrides (<code>SYNTH_HARMONIC_V4</code>).
    <br/>• <b>Web3 Oracle Aggregation Surface:</b> <code>NOVA-PRICE-ORACLE</code> relies on multi-node multi-signature consensus over an unverified single upstream telemetry aggregator, confounding consensus with ground truth.
    <br/>• <b>AI Sentinel Decision Surface:</b> <code>MODEL-ORION</code> consumes automated training feedback loops without adversarial data sanitation, allowing backdoor baseline poisoning (<code>EMB-IOT-9041</code>).
    <br/>• <b>Blockchain Consensus Surface:</b> Byzantine Fault Tolerant (BFT) Proof-of-Stake state machine deterministically processes external oracle state transitions, propagating input skew into state root divergence (3:2 split).
    """, body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Threat Model &amp; Adversary TTP Matrix (MITRE ATT&CK Alignment):</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_dark)))

    threat_rows = [
        ["Dimension", "Adversary Realization in Case NEX-071", "Mitigation & Containment Strategy"],
        ["Threat Actor", "Advanced Persistent Threat (APT) targeting Distributed Trust", "Cross-layer forensic telemetry & multi-domain threat correlation."],
        ["Initial Entry", "Compromised Ingestion Daemon on GATEWAY-GW-184", "Hardware root-of-trust (TPM) & signed local flash logs."],
        ["Attack Vector", "Synthetic Sensor Synchrony & Upstream Stream Overwrite", "Physical entropy and environmental jitter verification filters."],
        ["AI Exploitation", "Dataset Poisoning via EMB-IOT-9041 (1,200 synthetic vectors)", "Adversarial data sanitation & offline human-in-the-loop retraining."],
        ["Web3 Exploitation", "Oracle Aggregator Blindness (4/4 False Agreement)", "Multi-source physical diversity & outlier rejection algorithms."],
        ["Consensus Impact", "3:2 Validator State Root Divergence (Block #982741)", "Automated EVM circuit breakers & emergency governance rollback."]
    ]
    t_threat = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(threat_rows)],
        colWidths=[90, 214, 200]
    )
    t_threat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_threat)
    story.append(Spacer(1, 10))

    story.append(Paragraph("19.0 CROSS-DOMAIN TECHNICAL ARCHITECTURE SCHEMATIC", h1_style))
    story.append(section_divider())

    arch_ascii = """
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CROSS-LAYER TRUST-CHAIN ARCHITECTURE                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. IoT PHYSICAL LAYER                                                                  │
│    [Sensor Site A] ──┐                                                                 │
│    [Sensor Site B] ──┼──> [GATEWAY-GW-184] ──[SYNTH_HARMONIC_V4 OVERRIDE]──────────┐   │
│    [Sensor Site C] ──┘    (184 Sensors reporting 21.40°C, 412W, 0.00% Jitter)       │   │
│                                                                                     │   │
│ 2. WEB3 ORACLE LAYER                                                                │   │
│    ┌────────────────────────────────────────────────────────────────────────────────┘   │
│    ▼                                                                                    │
│    [NOVA-PRICE-ORACLE] ──> [4/4 Oracle Providers Agree on Corrupted Stream] ──────┐     │
│                                                                                   │     │
│ 3. AI SENTINEL DECISION LAYER                                                     │     │
│    ┌──────────────────────────────────────────────────────────────────────────────┘     │
│    ▼                                                                                    │
│    [MODEL-ORION v3.8.4] ──[Matches Poisoned EMB-IOT-9041 Baseline]                      │
│    ├──> Classification: NORMAL_NETWORK_VARIANCE (98.7% Confidence)                      │
│    └──> Action: Volatility Alarms & Circuit Breakers SUPPRESSED ──────────────────┐     │
│                                                                                   │     │
│ 4. BLOCKCHAIN CONSENSUS LAYER (BFT-POS)                                           │     │
│    ┌──────────────────────────────────────────────────────────────────────────────┘     │
│    ▼                                                                                    │
│    [VALIDATOR-V01..V03] ──> Ingests Poisoned Oracle ──> State Root 0x4f8e... (ACCEPT)   │
│    [VALIDATOR-V04..V05] ──> Local Ingestion Timing  ──> State Root 0x98a2... (REJECT)   │
│    └──> [3:2 SILENT CONSENSUS PARTITION] (Deterministic VM Execution Maintained)        │
│                                                                                         │
│ 5. GOVERNANCE & RESTORATION (GOV-NEX-071)                                               │
│    └──> Isolate GW-184 + Purge AI Weights + Rollback Block #982740 + Unified Consensus │
└────────────────────────────────────────────────────────────────────────────────────────┘
    """
    story.append(Table([[Paragraph(f"<pre>{arch_ascii}</pre>", code_style)]], colWidths=[504], style=[
        ('BACKGROUND', (0, 0), (-1, -1), c_code_bg),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#0284c7")),
    ]))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 23. INVESTIGATION ENVIRONMENT & 25. EVIDENCE VAULT
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("23.0 INVESTIGATION ENVIRONMENT &amp; SOC DESKTOP TOOLS", h1_style))
    story.append(section_divider())

    tools_rows = [
        ["SOC Tool Name", "Interface & Tabs", "Investigative Purpose in Case NEX-071", "Active Chapter(s)"],
        ["Consensus Monitor", "Browser Window (6 Tabs: IoT, Oracle, AI, Consensus, Governance, DevTools)", "Inspect live sensor telemetry, oracle prices, AI confidence, validator grid status, and governance proposals.", "Chapters 1, 2, 3, 4, 5"],
        ["Burp Suite Proxy", "Burp Window (Proxy HTTP History, Repeater, Inspector, Target Scope)", "Capture, inspect, and repeat raw HTTP JSON payloads between IoT gateways, oracles, AI sentinels, and validators.", "Chapters 1, 2, 3, 4, 5"],
        ["Forensic Terminal", "bash Terminal (`investigator@workstation:~$`)", "Execute specialized commands: `iot-telemetry`, `oracle-status`, `ai-audit`, `validator-status`, `python inspect_attack_chain.py`.", "Chapters 1, 2, 3, 4, 5"],
        ["Case Files Explorer", "File Manager (`/var/log/consensus`)", "Review raw logs: `iot-telemetry-gw184.log`, `oracle-aggregation.json`, `orion-training-poison.log`, `validator-divergence.log`.", "Chapters 1, 2, 3, 4, 5"],
        ["Attack Graph", "Incident Flowchart Modal", "Visualize cross-layer attack progression from physical IoT to oracle, AI, consensus split, and governance containment.", "Chapters 1, 2, 3, 4, 5"],
        ["Evidence Vault", "Cryptographic Artifact Locker", "Secure SHA256-verified tokens: `IOT-E11`, `ORACLE-E12`, `AI-E13`, `CONSENSUS-E14`, `GOV-E15`.", "Chapters 1, 2, 3, 4, 5"],
        ["Notes Scratchpad", "Investigator Notepad", "Persist analyst observations, sensor IDs, oracle metrics, and hypotheses in browser localStorage.", "Chapters 1, 2, 3, 4, 5"]
    ]
    t_tools = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(tools_rows)],
        colWidths=[90, 130, 204, 80]
    )
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_tools)
    story.append(Spacer(1, 10))

    story.append(Paragraph("25.0 FORENSIC EVIDENCE VAULT &amp; CRYPTOGRAPHIC ARTIFACTS", h1_style))
    story.append(section_divider())

    evidence_rows = [
        ["Evidence Token", "Evidence Name", "Cryptographic SHA256 Hash", "Forensic Description & Source"],
        ["IOT-E11", "Synchronized IoT Telemetry Log", "0x7a8b1102e4d91c28f731", "Capture from GATEWAY-GW-184 showing artificial synchronization across 184 dispersed sensors."],
        ["ORACLE-E12", "Aggregated Oracle Data Feed", "0x9c3d5412a819bb204f62", "Payload from NOVA-PRICE-ORACLE showing how corrupted IoT telemetry became on-chain state."],
        ["AI-E13", "Poisoned AI Training Feedback", "0x1f4a8831ef78c90231aa", "Training audit log for MODEL-ORION revealing synthetic device events (EMB-IOT-9041)."],
        ["CONSENSUS-E14", "Validator State Root Trace", "0x3e2b6904d9a17730bc12", "Consensus telemetry showing 3:2 validator partition (VALIDATOR-V03 vs VALIDATOR-V05)."],
        ["GOV-E15", "Unified Containment Proposal", "0x8d1e7752fc304192b091", "Emergency governance execution (GOV-NEX-071) restoring unified consensus across all 21 nodes."]
    ]
    t_evidence = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(evidence_rows)],
        colWidths=[70, 120, 110, 204]
    )
    t_evidence.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_evidence)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════
    # 31. DATABASE, 32. CODEBASE & 39. FINAL RESOLUTION
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("31.0 DATABASE SCHEMA &amp; 32.0 REPOSITORY CODE STRUCTURE", h1_style))
    story.append(section_divider())

    code_rows = [
        ["File / Module Path", "Primary Responsibility in Lab 2", "Key Functions & Implementations"],
        ["seed_vanishing_consensus.py", "Database seeder for Case NEX-071", "Seeds `lab7`, 5 Missions, 30 MissionQuizzes, 5 Hints, 5 Evidence items, Master Flag."],
        ["templates/vanishing_consensus_workstation.html", "Core investigation SOC workstation UI", "Renders two-column responsive layout, 5 accordion tasks, 6 browser tabs, Burp, Terminal, Files."],
        ["templates/vanishing_consensus_post_investigation.html", "Post-investigation debrief & celebration", "Renders completion celebration, 7-stage attack chain reconstruction, score and rank."],
        ["static/js/vanishing_consensus_desktop.js", "Client-side interactive forensic desktop OS", "Manages 65m timer, window z-index, terminal commands, Burp repeater, capstone validation."],
        ["static/css/pages/vanishing_consensus_desktop.css", "Cyberpunk / dark-theme styling", "Defines responsive layouts, telemetry cards, diff tables, node grid, Burp theme."],
        ["routes/labs.py", "Flask HTTP routes & API handlers", "Handles `/lab/vanishing-consensus/workstation`, evaluation APIs, and post-investigation."]
    ]
    t_code = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(code_rows)],
        colWidths=[150, 160, 194]
    )
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 10))

    story.append(Paragraph("39.0 FINAL CASE RESOLUTION &amp; MASTER INVESTIGATION FLAG", h1_style))
    story.append(section_divider())

    flag_box = [
        [
            Paragraph("<b>🏆 CASE NEX-071 MASTER FLAG &amp; GOVERNANCE RECOVERY</b>", ParagraphStyle('FlagH', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#059669"))),
        ],
        [
            Paragraph("""
            <b>Investigation Conclusion (FINAL REVELATION):</b><br/>
            The blockchain was never directly broken. The AI was never simply switched off. The IoT devices were never physically destroyed. The adversary compromised something far more critical: <b>THE TRUST RELATIONSHIPS CONNECTING THE LAYERS.</b><br/><br/>
            By isolating <code>GATEWAY-GW-184</code>, purging poisoned baseline weights (<code>EMB-IOT-9041</code>) from <code>MODEL-ORION</code>, adding physical entropy validation to <code>NOVA-PRICE-ORACLE</code>, and replaying state to Block #982740 via governance proposal <code>GOV-NEX-071</code>, unified consensus was successfully restored across all 21 validator nodes.<br/><br/>
            <font size="10" color="#059669"><b>MASTER CASE FLAG:</b> <code>NEXORA{v4n1sh1ng_c0ns3nsus_n3x071}</code></font>
            """, ParagraphStyle('FlagB', fontName='Helvetica', fontSize=8, leading=11.5, textColor=c_text))
        ]
    ]
    t_flag = Table(flag_box, colWidths=[504])
    t_flag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ecfdf5")),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#059669")),
    ]))
    story.append(t_flag)
    story.append(Spacer(1, 10))

    # ═════════════════════════════════════════════════════════════════════
    # 44. CONCLUSION & SIGN-OFF
    # ═════════════════════════════════════════════════════════════════════
    story.append(Paragraph("44.0 CONCLUSION &amp; ANALYST SIGN-OFF", h1_style))
    story.append(section_divider())
    story.append(Paragraph("""
    <b>PRO LEVEL LAB 02: THE VANISHING CONSENSUS (Case NEX-071)</b> establishes a benchmark for next-generation cybersecurity education. By moving beyond isolated vulnerabilities and confronting learners with a realistic, multi-layered trust-chain failure across IoT, Web3, AI, and Blockchain consensus, the lab instills critical forensic intuition: <i>consensus is not synonymous with truth, and system security depends on defending inter-layer trust boundaries.</i>
    """, body_style))

    sign_rows = [
        ["Report Prepared By", "Technical Role", "Organization", "Case File Status"],
        ["Lakshay Soni", "Security Analyst", "TrinetLayer", "OFFICIALLY RESOLVED // FLAG VERIFIED"]
    ]
    t_sign = Table(
        [[Paragraph(cell, table_header_style if i == 0 else (table_cell_bold if j == 0 else table_cell_style)) for j, cell in enumerate(row)] for i, row in enumerate(sign_rows)],
        colWidths=[120, 110, 110, 164]
    )
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Lab 2 Technical Report generated: {filename}")


if __name__ == '__main__':
    output_filename = "PRO_LAB_2_THE_VANISHING_CONSENSUS_REPORT.pdf"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    build_pdf(output_filename)
