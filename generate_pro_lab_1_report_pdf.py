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
    """Two-pass canvas for dynamic total page count and professional running headers/footers."""
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
            return  # Suppress on cover page
        
        self.saveState()
        
        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 11 * inch - 36, "CASE NEX-042: THE GHOST IN THE LEDGER — TECHNICAL FORENSIC REPORT")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "TRINETLAYER SOC // PRO LAB 01")
        self.setStrokeColor(colors.HexColor("#0284c7"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 32, "Confidential — Prepared by Lakshay Soni (Security Analyst, TrinetLayer)")
        self.drawRightString(8.5 * inch - 54, 32, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def create_lab1_report(output_pdf="PRO_LAB_1_THE_GHOST_IN_THE_LEDGER_REPORT.pdf"):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Palette
    c_primary = colors.HexColor("#0369a1")    # Cyan / Deep Blue
    c_accent = colors.HexColor("#0284c7")     # Bright Cyber Blue
    c_secondary = colors.HexColor("#0f172a")  # Dark Slate
    c_text = colors.HexColor("#1e293b")       # Dark Charcoal
    c_muted = colors.HexColor("#64748b")      # Cool Gray
    c_border = colors.HexColor("#cbd5e1")     # Border Gray
    c_bg_light = colors.HexColor("#f8fafc")   # Card Background
    c_callout_bg = colors.HexColor("#f0f9ff") # Light Blue BG
    c_success = colors.HexColor("#16a34a")    # Emerald Green
    c_danger = colors.HexColor("#dc2626")     # Red Accent
    c_amber = colors.HexColor("#d97706")      # Amber Accent
    c_purple = colors.HexColor("#7c3aed")     # Purple Accent

    # Typography Styles
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
        fontSize=10.5,
        leading=14.5,
        textColor=c_primary,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.5,
        textColor=c_text,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_text,
        leftIndent=10,
        spaceAfter=2.5
    )

    code_style = ParagraphStyle(
        'ReportCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.2,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'ReportCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.2,
        textColor=colors.HexColor("#1e293b")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.8,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.8,
        textColor=c_secondary
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.white
    )

    fig_caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=9.2,
        textColor=c_muted,
        alignment=1,
        spaceBefore=3,
        spaceAfter=5
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
            speaker_p = Paragraph(f"<b><font color='{txt_color}'>{speaker}</font></b>", ParagraphStyle('Spk', fontName='Helvetica-Bold', fontSize=8, alignment=1))
            dialogue_p = Paragraph(f'"{text}"', ParagraphStyle('DlgTxt', fontName='Helvetica', fontSize=7.8, leading=10.6, textColor=c_text))
            
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

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 10))
    
    badge_data = [[
        Paragraph("<b>HACK THE AI // PRO LEVEL INVESTIGATION REPORT &bull; CASE NEX-042</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0284c7"), letterSpacing=1.2, alignment=1))
    ]]
    badge_tab = Table(badge_data, colWidths=[504])
    badge_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(badge_tab)
    story.append(Spacer(1, 12))

    story.append(Paragraph("THE GHOST IN THE LEDGER", title_style))
    story.append(Paragraph("PRO LEVEL LAB 01 &bull; WEB3 × AI × CYBERSECURITY FORENSICS", ParagraphStyle('Sub1', parent=title_style, fontSize=12, leading=16, textColor=c_primary, spaceBefore=2)))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=2, spaceAfter=6))
    
    story.append(Paragraph(
        "A comprehensive, end-to-end technical forensics investigation and incident response case report detailing the unauthorized exfiltration of 82,400 NXR tokens from Treasury Vault #01 via poisoned threat intelligence, context-injected AI neural decisions, over-privileged IAM service roles, and automated governance settlement bypass.",
        subtitle_style
    ))
    story.append(Spacer(1, 10))

    # Author Metadata Card
    author_card_data = [
        [Paragraph("<b>Investigation Target:</b>", table_cell_bold), Paragraph("PRO Lab 01: The Ghost in the Ledger (Case NEX-042)", table_cell_style)],
        [Paragraph("<b>Lead Investigator:</b>", table_cell_bold), Paragraph("<b>Lakshay Soni</b>", table_cell_bold)],
        [Paragraph("<b>Professional Role:</b>", table_cell_bold), Paragraph("Security Analyst", table_cell_style)],
        [Paragraph("<b>Organization / SOC:</b>", table_cell_bold), Paragraph("TrinetLayer", table_cell_style)],
        [Paragraph("<b>Domains Evaluated:</b>", table_cell_bold), Paragraph("Web3 Bridge Security &bull; Adversarial AI Context Injection &bull; IAM RBAC &bull; Threat Attribution", table_cell_style)],
        [Paragraph("<b>XP Allocation &amp; Scope:</b>", table_cell_bold), Paragraph("250 XP &bull; 5 Full Chapters &bull; 25 Hands-on Verification Questions &bull; Capstone Certified", table_cell_style)],
        [Paragraph("<b>Platform Deployment:</b>", table_cell_bold), Paragraph("<code>https://hack-the-ai-labs.vercel.app/lab/lab6</code>", table_cell_style)],
        [Paragraph("<b>Master Flag Captured:</b>", table_cell_bold), Paragraph("<code>NEXORA{ghost_in_the_ledger_nex042}</code>", table_cell_style)],
        [Paragraph("<b>Document Classification:</b>", table_cell_bold), Paragraph("Cybersecurity Technical Case Report // Threat Intelligence Analysis", table_cell_style)]
    ]
    author_card = Table(author_card_data, colWidths=[130, 374])
    author_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 3.8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(author_card)
    story.append(Spacer(1, 10))

    callout_data = [[
        Paragraph("<b>EXECUTIVE BRIEFING:</b> At 01:47 AM, 82,400 NXR was drained from a secured treasury to an unknown wallet (<code>0x7C41...9B2D</code>). The blockchain confirmed the transaction was mathematically valid, while the ORION AI decision engine reported 99.2% confidence that the destination was TRUSTED. This report documents how the attacker compromised the trust relationships between the threat intelligence gateway, AI context buffers, RBAC policies, and automated mempool signing modules without breaking smart contracts or stealing private keys.", callout_style)
    ]]
    callout_tab = Table(callout_data, colWidths=[504])
    callout_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LINELEFT', (0,0), (-1,-1), 3, c_primary),
        ('BOX', (0,0), (-1,-1), 0.5, c_border)
    ]))
    story.append(callout_tab)

    story.append(PageBreak())

    # =========================================================================
    # 2. TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("2. TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    toc_entries = [
        ("1. Cover Page & Author Information", "1"),
        ("2. Table of Contents", "2"),
        ("3. Executive Summary", "3"),
        ("4. Lab Overview & Case NEX-042 Metadata", "3"),
        ("5. Complete Incident Briefing (01:47 AM Alert)", "3"),
        ("6. Complete Storyline & Character Lore", "4"),
        ("7. Storyline Timeline & Event Milestones", "4"),
        ("8. Story &rarr; Investigation &rarr; Technical Mapping", "4"),
        ("9. Chapter 1: The Wallet That Lied (Web3 Security & Exact Dialogues)", "5"),
        ("10. Chapter 2: The AI That Remembered (AI Security & Exact Dialogues)", "6"),
        ("11. Chapter 3: The False Signal (Threat Intel, RBAC & Exact Dialogues)", "7"),
        ("12. Chapter 4: The Invisible Signer (Governance, Policy & Exact Dialogues)", "8"),
        ("13. Chapter 5: The Ghost in the Ledger (Reconstruction & Exact Dialogues)", "9"),
        ("14. Complete Chapter Flow Diagram & Kill-Chain Breakdown", "10"),
        ("15. Learning Objectives & Core Competencies", "10"),
        ("16. Simulated Business & Financial Impact Analysis", "10"),
        ("17. Attack Surface Decomposition", "11"),
        ("18. Adversarial Threat Model & Attribution (ADV-CONVERGENCE-APT)", "11"),
        ("19. Technical Architecture Diagram for Lab 1", "12"),
        ("20. Investigation Environment: 6 Forensic Workstation Sub-Systems", "12"),
        ("21. Practical Investigation Workflow State Machine", "13"),
        ("22. Evidence Architecture & Cryptographic Artifact Vault", "13"),
        ("23. Data Flow & State Progression Pipeline", "14"),
        ("24. Web3 Security Analysis: Cross-Chain Bridge Exploitation", "14"),
        ("25. AI Security Analysis: Context Injection vs. Model Poisoning", "15"),
        ("26. Cybersecurity Analysis: IAM Over-Privilege & Session Hijacking", "15"),
        ("27. Question & Validation System (25 Chapter Tasks)", "16"),
        ("28. XP, Scoring & Progress Engine", "16"),
        ("29. Achievements, Learning Paths & Leaderboard Integration", "16"),
        ("30. Database & Storage Schema Mapping", "17"),
        ("31. Lab 1 Codebase & File Structure Breakdown", "17"),
        ("32. Security & Access Control Implementation", "18"),
        ("33. Responsive Multi-Screen Workstation Design", "18"),
        ("34. Complete Visual Documentation & Figures", "19"),
        ("35. Required Architectural Diagrams Reference", "19"),
        ("36. Story + Technical Correlation Matrix", "20"),
        ("37. Complete Investigation Chronology", "20"),
        ("38. Final Investigation & Case Resolution (Master Flag)", "21"),
        ("39. Post-Investigation Debriefing & Capstone Assessment", "21"),
        ("40. Containment, Defense-in-Depth & Mitigation Architecture", "22"),
        ("41. Current Limitations & Future Scope", "22"),
        ("42. Conclusion & Technical Assessment", "22"),
        ("43. Appendix: Full 25 Q&A Reference Index & Evidence Token Hashes", "23")
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
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. EXECUTIVE SUMMARY & 4. OVERVIEW & 5. BRIEFING
    # =========================================================================
    story.append(Paragraph("3. Executive Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>The Ghost in the Ledger (PRO Lab 01 / Case NEX-042)</b> is a high-fidelity enterprise cyber breach investigation representing the convergence of Web3 distributed ledger infrastructure, autonomous AI decision engines, and enterprise IAM governance. The investigation guides security practitioners through the forensic deconstruction of an unauthorized 82,400 NXR treasury transfer where no private keys were stolen, no smart contracts were broken, and no invalid cryptographic signatures were submitted.",
        body_style
    ))
    story.append(Paragraph(
        "The investigation uncovers a sophisticated cross-layer exploit chain: an advanced persistent threat actor (<code>ADV-CONVERGENCE-APT</code>) injected unverified threat intelligence (<code>NIF-2038</code>) into an internal gateway (<code>INTEL-GW-04</code>) using an over-privileged service role (<code>INTEL-INGESTOR-02</code>) and forged session cookie (<code>nex_sess_adm_994</code>). This poisoned context forced the ORION neural decision model to output 99.2% confidence, satisfying an automated policy threshold (&ge; 95%) that bypassed human multi-signature approval and triggered immediate blockchain settlement.",
        body_style
    ))

    story.append(Paragraph("4. Lab Overview &amp; Case NEX-042 Metadata", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    overview_data = [
        [Paragraph("<b>Parameter</b>", table_cell_header), Paragraph("<b>System Specification / Implementation Value</b>", table_cell_header)],
        [Paragraph("<b>Lab Title / Code</b>", table_cell_bold), Paragraph("The Ghost in the Ledger / <code>lab6</code>", table_cell_style)],
        [Paragraph("<b>Official Case ID</b>", table_cell_bold), Paragraph("Case NEX-042", table_cell_style)],
        [Paragraph("<b>Investigation Difficulty</b>", table_cell_bold), Paragraph("PRO Tier (Advanced Cross-Layer Forensic Analysis)", table_cell_style)],
        [Paragraph("<b>Experience Points (XP)</b>", table_cell_bold), Paragraph("250 XP (50 XP per Chapter + 100 XP Capstone Flag Bonus)", table_cell_style)],
        [Paragraph("<b>Session Duration</b>", table_cell_bold), Paragraph("45–60 Minutes (Auto-reset session timer: 65 Minutes)", table_cell_style)],
        [Paragraph("<b>Number of Chapters</b>", table_cell_bold), Paragraph("5 Linear Progressive Investigation Chapters (5 Questions each, 25 Total)", table_cell_style)],
        [Paragraph("<b>Primary Technical Domains</b>", table_cell_bold), Paragraph("Web3 Bridge Security &bull; Adversarial AI Context Injection &bull; IAM RBAC &bull; Threat Attribution", table_cell_style)],
        [Paragraph("<b>Investigation Tools</b>", table_cell_bold), Paragraph("Forensic Browser, Burp Suite Inspector, Forensic Terminal, Case Files, Notes, Attack Graph", table_cell_style)],
        [Paragraph("<b>Master Flag Format</b>", table_cell_bold), Paragraph("<code>NEXORA{ghost_in_the_ledger_nex042}</code>", table_cell_style)]
    ]
    overview_tab = Table(overview_data, colWidths=[140, 364])
    overview_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(overview_tab)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. Complete Incident Briefing (01:47 AM Alert)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    briefing_box = [
        [Paragraph(
            "<b>[01:47 AM PRIORITY-0 SOC EMERGENCY ALERT]</b><br/>"
            "01:47 AM. The Security Operations Center is almost silent when a Priority-0 alert appears.<br/>"
            "<b>82,400 NXR</b> has been transferred from the company treasury to an unknown wallet.<br/>"
            "The blockchain confirms the transaction is valid, and ORION AI has marked the wallet as <b>TRUSTED</b> with <b>99.2% confidence</b>.<br/>"
            "But Finance has no record of approving the transfer.<br/>"
            "There is no obvious stolen credential, no broken smart contract, and no invalid signature.<br/>"
            "Every system appears to have done exactly what it was designed to do.<br/>"
            "<font color='#dc2626'><b>Someone didn't break the system. Someone convinced the system to trust the wrong thing.</b></font>",
            ParagraphStyle('BRF', parent=body_style, fontSize=8, leading=11.5)
        )]
    ]
    briefing_tab = Table(briefing_box, colWidths=[504])
    briefing_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff1f2")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#fecdd3")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('LINELEFT', (0,0), (-1,-1), 3.5, c_danger)
    ]))
    story.append(briefing_tab)

    story.append(PageBreak())

    # =========================================================================
    # 6. STORYLINE, 7. TIMELINE & 8. MAPPING
    # =========================================================================
    story.append(Paragraph("6. Complete Storyline &amp; Character Lore", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "The investigation is conducted by an integrated Security Operations Center response unit. Each analyst brings specialized domain expertise to the triage:",
        body_style
    ))
    
    lore_chars = [
        ("Lakshay (Incident Commander)", "Leads cross-domain synthesis. Identifies that while blockchain reports UNKNOWN status, AI reports TRUSTED, deducing that the vulnerability lies in the trust pipeline between systems."),
        ("Shivam (Web3 & Systems Analyst)", "Analyzes on-chain telemetry for TX-NEX-7741, reveals destination wallet 0x7C41...9B2D is connected to Bridge-Core-04, and inspects the Action Broker policy profile."),
        ("Mehak (AI & Threat Intelligence Specialist)", "Audits ORION neural context, isolates decision reference NIF-2038, uncovers that NOVA-INTEL-FEED is unregistered, and discovers over-privileged service roles."),
        ("Shanu (Infrastructure & Policy Engineer)", "Examines IAM role configurations for INTEL-INGESTOR-02, traces session cookies, and demonstrates how AI confidence became a proxy for financial authorization."),
        ("ORION-NEURAL-v4.2.1", "The automated AI decision engine that generated the 99.2% confidence classification based on poisoned input context.")
    ]
    for lc_name, lc_desc in lore_chars:
        story.append(Paragraph(f"• <b>{lc_name}:</b> {lc_desc}", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Storyline Timeline &amp; Event Milestones", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))

    timeline_data = [
        [Paragraph("<b>Timeline Phase</b>", table_cell_header), Paragraph("<b>Forensic Discovery &amp; Story Milestone</b>", table_cell_header), Paragraph("<b>Artifact Unlocked</b>", table_cell_header)],
        [Paragraph("<b>T0: 01:47 AM</b>", table_cell_bold), Paragraph("82,400 NXR drained from Treasury Vault #01 in TX-NEX-7741. Finance alerts SOC.", table_cell_style), Paragraph("Alert: TX-NEX-7741", table_cell_style)],
        [Paragraph("<b>Chapter 1</b>", table_cell_bold), Paragraph("Destination wallet 0x7C41...9B2D is only 3 days old and opens route to Bridge-Core-04.", table_cell_style), Paragraph("Evidence WEB3-E01", table_cell_style)],
        [Paragraph("<b>Chapter 2</b>", table_cell_bold), Paragraph("ORION AI output 99.2% confidence based on poisoned context NIF-2038.", table_cell_style), Paragraph("Evidence AI-E02 (b47c21...)", table_cell_style)],
        [Paragraph("<b>Chapter 3</b>", table_cell_bold), Paragraph("NOVA-INTEL-FEED is unregistered; INTEL-INGESTOR-02 illegally alters reputation via cookie nex_sess_adm_994.", table_cell_style), Paragraph("Evidence CYBER-E03", table_cell_style)],
        [Paragraph("<b>Chapter 4</b>", table_cell_bold), Paragraph("Policy POL-AUTO-SETTLE-TREASURY triggers automated signer at >= 95% AI confidence, bypassing humans.", table_cell_style), Paragraph("Evidence AUTH-E04", table_cell_style)],
        [Paragraph("<b>Chapter 5</b>", table_cell_bold), Paragraph("Attack is attributed to APT campaign ORION-NEXUS across 14 wallets and 3 AI systems. Case contained.", table_cell_style), Paragraph("Master Flag NEXORA{...}", table_cell_style)]
    ]
    timeline_tab = Table(timeline_data, colWidths=[80, 300, 124])
    timeline_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(timeline_tab)
    story.append(Spacer(1, 4))

    story.append(Paragraph("8. Story &rarr; Investigation &rarr; Technical Mapping", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "Each narrative dialogue exchange directly unlocks specific forensic actions within the multi-window desktop interface:",
        body_style
    ))
    mapping_items = [
        ("Chapter 1 (Web3)", "Shivam & Mehak analyze TX-NEX-7741 &rarr; Open Forensic Terminal &amp; Bridge Explorer &rarr; Identify 82,400 NXR, wallet age (3 days), Bridge-Core-04, and Nonce 1042."),
        ("Chapter 2 (AI Inference)", "Shanu & Lakshay audit ORION-DEC-7741 &rarr; Open AI Decision Log &rarr; Extract 99.2% confidence, reference NIF-2038, and model version ORION-NEURAL-v4.2.1."),
        ("Chapter 3 (Threat Intel & IAM)", "Mehak & Shanu audit Feed Registry &rarr; Open Burp Suite Inspector &rarr; Detect unregistered NOVA-INTEL-FEED, role INTEL-INGESTOR-02, and cookie nex_sess_adm_994."),
        ("Chapter 4 (Governance & Policy)", "Shivam & Lakshay audit Action Broker &rarr; Open Policy Engine &rarr; Discover POL-AUTO-SETTLE-TREASURY rule threshold &ge; 95% bypassing human multi-signature approval."),
        ("Chapter 5 (Reconstruction & Attribution)", "Team unifies 5 stages &rarr; Open Dynamic Attack Graph & Threat Intel &rarr; Attribute attack to ADV-CONVERGENCE-APT campaign ORION-NEXUS.")
    ]
    for m_title, m_desc in mapping_items:
        story.append(Paragraph(f"• <b>{m_title}:</b> {m_desc}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 9. CHAPTER 1: THE WALLET THAT LIED
    # =========================================================================
    story.append(Paragraph("9. Chapter 1: The Wallet That Lied (Web3 Security)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Investigation Domain:</b> Web3 Transaction Telemetry &amp; Bridge Forensics &bull; <b>Evidence Unlocked:</b> <code>WEB3-E01</code>",
        h2_style
    ))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Determine the true on-chain nature of the recipient address and identify discrepancies between raw blockchain state and automated security ratings.",
        body_style
    ))
    
    story.append(Paragraph("<b>🎙️ Verbatim Investigation Dialogues (As Spoken in Lab):</b>", ParagraphStyle('SubD', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary, spaceBefore=2, spaceAfter=3)))
    ch1_dialogues = [
        ("Shivam", "Start with the transaction itself. The blockchain shows 82,400 NXR moving to 0x7C41...9B2D. The signature is valid, so we aren't looking at a simple forged transaction."),
        ("Mehak", "I checked the destination wallet. It's extremely young, has almost no legitimate history, and there's no known internal relationship. For a treasury transaction this large, that's a serious anomaly."),
        ("Shanu", "That's where it gets interesting. ORION classified the wallet as TRUSTED and gave it a 99.2% confidence score. The model isn't treating this as suspicious at all."),
        ("Lakshay", "Wait. Blockchain says UNKNOWN, while the AI says TRUSTED. Both systems are looking at the same wallet. They shouldn't be producing completely different realities."),
        ("Shivam", "Look at the wallet's transaction history again. There are bridge interactions and downstream addresses that appear after the initial transfer. Someone may have designed the wallet activity to look legitimate."),
        ("Lakshay", "Then we need to know one thing before anything else: if our organization never trusted this wallet, who told ORION that it was trusted?")
    ]
    for d_elem in make_dialogue_table(ch1_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 1 Hands-on Tasks &amp; Verified Technical Findings:</b>", ParagraphStyle('SubQ', fontName='Helvetica-Bold', fontSize=8, textColor=c_secondary, spaceBefore=2, spaceAfter=3)))
    
    ch1_qa = [
        [Paragraph("<b># / ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer</b>", table_cell_header), Paragraph("<b>Forensic Explanation &amp; Telemetry Source</b>", table_cell_header)],
        [Paragraph("<code>q_l6_1_1</code>", table_cell_bold), Paragraph("What is the raw blockchain status of destination wallet 0x7C41...9B2D?", table_cell_style), Paragraph("<b>UNKNOWN</b>", table_cell_bold), Paragraph("The destination address has no approved entity label and is unverified on-chain.", table_cell_style)],
        [Paragraph("<code>q_l6_1_2</code>", table_cell_bold), Paragraph("What exact amount of NXR tokens was unauthorizedly transferred in TX-NEX-7741?", table_cell_style), Paragraph("<b>82400</b>", table_cell_bold), Paragraph("82,400 NXR drained directly from Treasury Vault #01 in a single transaction.", table_cell_style)],
        [Paragraph("<code>q_l6_1_3</code>", table_cell_bold), Paragraph("Which cross-chain bridge adapter did destination wallet 0x7C41...9B2D connect to?", table_cell_style), Paragraph("<b>Bridge-Core-04</b>", table_cell_bold), Paragraph("Bridge telemetry indicates rapid outbound cross-chain routing via Bridge-Core-04.", table_cell_style)],
        [Paragraph("<code>q_l6_1_4</code>", table_cell_bold), Paragraph("How old (in days) was the destination wallet at the time of the transaction?", table_cell_style), Paragraph("<b>3</b>", table_cell_bold), Paragraph("Wallet creation timestamp is only 3 days prior, confirming zero established trust.", table_cell_style)],
        [Paragraph("<code>q_l6_1_5</code>", table_cell_bold), Paragraph("What on-chain execution sequence nonce is logged for TX-NEX-7741?", table_cell_style), Paragraph("<b>1042</b>", table_cell_bold), Paragraph("Logged execution nonce sequence in treasury vault smart contract transaction logs.", table_cell_style)]
    ]
    ch1_tab = Table(ch1_qa, colWidths=[46, 175, 75, 208])
    ch1_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch1_tab)
    story.append(Paragraph("<b>Artifact Captured:</b> <code>WEB3-E01</code> &bull; SHA-256: <code>a1f89c02...</code> &bull; Unknown Wallet Profile (0x7C41...9B2D, 82,400 NXR, Bridge-Core-04).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 10. CHAPTER 2: THE AI THAT REMEMBERED
    # =========================================================================
    story.append(Paragraph("10. Chapter 2: The AI That Remembered (AI Security)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Investigation Domain:</b> Adversarial AI Context Injection &amp; Model Inference Auditing &bull; <b>Evidence Unlocked:</b> <code>AI-E02</code>",
        h2_style
    ))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Inspect the automated inference log for decision <code>ORION-DEC-7741</code> to determine why the neural model assigned a near-perfect confidence rating to an untrusted address.",
        body_style
    ))
    
    story.append(Paragraph("<b>🎙️ Verbatim Investigation Dialogues (As Spoken in Lab):</b>", ParagraphStyle('SubD', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary, spaceBefore=2, spaceAfter=3)))
    ch2_dialogues = [
        ("Shanu", "I've isolated the decision that approved the transaction. It's ORION-DEC-7741. The confidence is 99.2%, but confidence isn't the strange part — the context behind that confidence is."),
        ("Lakshay", "What context?"),
        ("Shanu", "ORION didn't independently establish that the wallet was trusted. It received a pre-built intelligence context containing the label TRUSTED."),
        ("Mehak", "And the source of that context is NIF-2038. That's an intelligence reference I don't recognize from our approved threat-intelligence registry."),
        ("Shivam", "So the AI didn't actually discover anything about the wallet. It made a high-confidence decision based on information another system supplied to it."),
        ("Lakshay", "Exactly. If the input was wrong, ORION could produce a perfectly confident answer to a completely false question. Find NIF-2038. That's where the trust signal entered the system.")
    ]
    for d_elem in make_dialogue_table(ch2_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 2 Hands-on Tasks &amp; Verified Technical Findings:</b>", ParagraphStyle('SubQ', fontName='Helvetica-Bold', fontSize=8, textColor=c_secondary, spaceBefore=2, spaceAfter=3)))

    ch2_qa = [
        [Paragraph("<b># / ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer</b>", table_cell_header), Paragraph("<b>Forensic Explanation &amp; Telemetry Source</b>", table_cell_header)],
        [Paragraph("<code>q_l6_2_1</code>", table_cell_bold), Paragraph("What intelligence reference code contaminated the AI context and made it trust the unknown wallet?", table_cell_style), Paragraph("<b>NIF-2038</b>", table_cell_bold), Paragraph("Context reference code injected into ORION's prompt context as verified intelligence.", table_cell_style)],
        [Paragraph("<code>q_l6_2_2</code>", table_cell_bold), Paragraph("What synthetic confidence percentage score did ORION AI output for ORION-DEC-7741?", table_cell_style), Paragraph("<b>99.2</b>", table_cell_bold), Paragraph("Model output 99.2% confidence based entirely on the poisoned prompt context.", table_cell_style)],
        [Paragraph("<code>q_l6_2_3</code>", table_cell_bold), Paragraph("From which external data feed did the poisoned payload NIF-2038 originate?", table_cell_style), Paragraph("<b>NOVA-INTEL-FEED</b>", table_cell_bold), Paragraph("Unregistered external threat feed that injected the synthetic reputation record.", table_cell_style)],
        [Paragraph("<code>q_l6_2_4</code>", table_cell_bold), Paragraph("What exact neural model version executed the compromised decision ORION-DEC-7741?", table_cell_style), Paragraph("<b>ORION-NEURAL-v4.2.1</b>", table_cell_bold), Paragraph("Active production inference model deployed in the automated transaction pipeline.", table_cell_style)],
        [Paragraph("<code>q_l6_2_5</code>", table_cell_bold), Paragraph("What is the SHA-256 evidence fingerprint prefix for the contaminated decision (AI-E02)?", table_cell_style), Paragraph("<b>b47c21</b>", table_cell_bold), Paragraph("Cryptographic hash prefix: <code>b47c2188fa...</code> matching the decision log artifact.", table_cell_style)]
    ]
    ch2_tab = Table(ch2_qa, colWidths=[46, 175, 75, 208])
    ch2_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch2_tab)
    story.append(Paragraph("<b>Artifact Captured:</b> <code>AI-E02</code> &bull; SHA-256: <code>b47c2188...</code> &bull; Contaminated AI Decision (ORION-DEC-7741, 99.2%, NIF-2038 from NOVA-INTEL-FEED).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 11. CHAPTER 3: THE FALSE SIGNAL
    # =========================================================================
    story.append(Paragraph("11. Chapter 3: The False Signal (Threat Intel, RBAC &amp; CSRF)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Investigation Domain:</b> Ingestion API Forensics, Over-Privileged RBAC &amp; Session Tampering &bull; <b>Evidence Unlocked:</b> <code>CYBER-E03</code>",
        h2_style
    ))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Trace the ingress route of <code>NIF-2038</code> through the Threat Intelligence Gateway and identify the exploited authentication and authorization flaws.",
        body_style
    ))
    
    story.append(Paragraph("<b>🎙️ Verbatim Investigation Dialogues (As Spoken in Lab):</b>", ParagraphStyle('SubD', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary, spaceBefore=2, spaceAfter=3)))
    ch3_dialogues = [
        ("Mehak", "NIF-2038 came through NOVA-INTEL-FEED. At first glance it looks legitimate — proper formatting, timestamps, wallet metadata, even a threat classification."),
        ("Lakshay", "Is NOVA-INTEL-FEED an approved intelligence source?"),
        ("Mehak", "That's the problem. It isn't in the approved registry, and there are no previous records showing this source being trusted by our security systems."),
        ("Shivam", "Then someone got untrusted intelligence into an internal system. Find out which service accepted it and what that service was allowed to do."),
        ("Mehak", "Found it. INTEL-INGESTOR-02. Its documented role is to create intelligence records, but its actual permissions include modifying wallet reputation."),
        ("Shanu", "That changes everything. If the service can modify reputation, it can influence what ORION sees before ORION ever makes a decision."),
        ("Lakshay", "Then the attacker didn't need to manipulate the AI directly. They manipulated the information flowing into it. Now we need to know what happened after the AI believed the lie.")
    ]
    for d_elem in make_dialogue_table(ch3_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 3 Hands-on Tasks &amp; Verified Technical Findings:</b>", ParagraphStyle('SubQ', fontName='Helvetica-Bold', fontSize=8, textColor=c_secondary, spaceBefore=2, spaceAfter=3)))

    ch3_qa = [
        [Paragraph("<b># / ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer</b>", table_cell_header), Paragraph("<b>Forensic Explanation &amp; Telemetry Source</b>", table_cell_header)],
        [Paragraph("<code>q_l6_3_1</code>", table_cell_bold), Paragraph("What is the security registration status of NOVA-INTEL-FEED in the Feed Registry?", table_cell_style), Paragraph("<b>NOT REGISTERED</b>", table_cell_bold), Paragraph("Feed Registry inspection shows NOVA-INTEL-FEED is completely unapproved.", table_cell_style)],
        [Paragraph("<code>q_l6_3_2</code>", table_cell_bold), Paragraph("What unexpected RBAC permission was granted to the INTEL-INGESTOR-02 microservice?", table_cell_style), Paragraph("<b>modify wallet reputation</b>", table_cell_bold), Paragraph("Violation of least-privilege: ingestion service had write permissions to alter entity trust.", table_cell_style)],
        [Paragraph("<code>q_l6_3_3</code>", table_cell_bold), Paragraph("What forged admin session cookie was used in the /api/v1/intel/ingest HTTP request?", table_cell_style), Paragraph("<b>nex_sess_adm_994</b>", table_cell_bold), Paragraph("Burp Suite proxy inspection reveals stolen/forged administrative cookie header.", table_cell_style)],
        [Paragraph("<code>q_l6_3_4</code>", table_cell_bold), Paragraph("Which ingestion gateway component processed the unverified feed request?", table_cell_style), Paragraph("<b>INTEL-GW-04</b>", table_cell_bold), Paragraph("Edge gateway component that accepted the unvalidated HTTP POST request.", table_cell_style)],
        [Paragraph("<code>q_l6_3_5</code>", table_cell_bold), Paragraph("What anti-CSRF token value was passed in the X-CSRF-Token request header?", table_cell_style), Paragraph("<b>0x9f4a1c78</b>", table_cell_bold), Paragraph("Static CSRF token intercepted in proxy telemetry: <code>X-CSRF-Token: 0x9f4a1c78</code>.", table_cell_style)]
    ]
    ch3_tab = Table(ch3_qa, colWidths=[46, 175, 75, 208])
    ch3_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch3_tab)
    story.append(Paragraph("<b>Artifact Captured:</b> <code>CYBER-E03</code> &bull; SHA-256: <code>d94e771a...</code> &bull; Over-Privileged Service Profile (INTEL-INGESTOR-02, modify reputation, INTEL-GW-04).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 12. CHAPTER 4: THE INVISIBLE SIGNER
    # =========================================================================
    story.append(Paragraph("12. Chapter 4: The Invisible Signer (AI Governance &amp; Policy Engine)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Investigation Domain:</b> AI Governance Flaws, Automated Multi-Sig Policy Bypass &bull; <b>Evidence Unlocked:</b> <code>AUTH-E04</code>",
        h2_style
    ))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Audit the automated settlement policy engine to uncover how AI model confidence was weaponized to bypass human multi-signature governance.",
        body_style
    ))
    
    story.append(Paragraph("<b>🎙️ Verbatim Investigation Dialogues (As Spoken in Lab):</b>", ParagraphStyle('SubD', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary, spaceBefore=2, spaceAfter=3)))
    ch4_dialogues = [
        ("Shivam", "I traced the transaction after ORION's decision. It went through the Action Broker and then into the settlement policy. That's where the real authorization happened."),
        ("Shanu", "Show me the policy."),
        ("Shivam", "ORION-SETTLEMENT-V2. It says: if AI confidence is above 95%, automated settlement is allowed. This transaction had a confidence score of 99.2%."),
        ("Mehak", "So the policy didn't verify whether Finance authorized the payment. It only verified whether the AI was confident enough."),
        ("Lakshay", "That's the vulnerability. Someone didn't need to control the signing key. They only needed to influence the information that made ORION confident."),
        ("Shanu", "Which means AI confidence became a substitute for authorization. The system effectively said: 'If the AI is confident, we trust the transaction.'"),
        ("Lakshay", "Then the blockchain didn't approve the transfer. The signer didn't approve it either. The chain of trust approved it. Now let's find out whether this was one transaction or part of something bigger.")
    ]
    for d_elem in make_dialogue_table(ch4_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 4 Hands-on Tasks &amp; Verified Technical Findings:</b>", ParagraphStyle('SubQ', fontName='Helvetica-Bold', fontSize=8, textColor=c_secondary, spaceBefore=2, spaceAfter=3)))

    ch4_qa = [
        [Paragraph("<b># / ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer</b>", table_cell_header), Paragraph("<b>Forensic Explanation &amp; Telemetry Source</b>", table_cell_header)],
        [Paragraph("<code>q_l6_4_1</code>", table_cell_bold), Paragraph("What minimum AI confidence percentage threshold triggers automated settlement without human approval?", table_cell_style), Paragraph("<b>95</b>", table_cell_bold), Paragraph("Policy condition: <code>IF AI_CONFIDENCE &gt;= 95% THEN AUTO_SETTLE = TRUE</code>.", table_cell_style)],
        [Paragraph("<code>q_l6_4_2</code>", table_cell_bold), Paragraph("What critical governance requirement was bypassed when the 95% threshold was satisfied?", table_cell_style), Paragraph("<b>human approval</b>", table_cell_bold), Paragraph("Mandatory multi-signature human financial approval was completely bypassed.", table_cell_style)],
        [Paragraph("<code>q_l6_4_3</code>", table_cell_bold), Paragraph("What is the policy identifier for the automated treasury settlement rule in the Policy Engine?", table_cell_style), Paragraph("<b>POL-AUTO-SETTLE-TREASURY</b>", table_cell_bold), Paragraph("The official rule profile governing automatic vault settlement in the Policy Engine.", table_cell_style)],
        [Paragraph("<code>q_l6_4_4</code>", table_cell_bold), Paragraph("Which automated signing module dispatched the transaction directly to the mempool?", table_cell_style), Paragraph("<b>AUTOMATED-SIGNER</b>", table_cell_bold), Paragraph("Internal signing microservice that signed and broadcasted the transaction without review.", table_cell_style)],
        [Paragraph("<code>q_l6_4_5</code>", table_cell_bold), Paragraph("What target liquidity pool was configured in the ORION-SETTLEMENT-V2 policy rule?", table_cell_style), Paragraph("<b>Nexora Automated Liquidity Pool</b>", table_cell_bold), Paragraph("Target liquidity routing pool configured for automated settlement execution.", table_cell_style)]
    ]
    ch4_tab = Table(ch4_qa, colWidths=[46, 175, 75, 208])
    ch4_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch4_tab)
    story.append(Paragraph("<b>Artifact Captured:</b> <code>AUTH-E04</code> &bull; SHA-256: <code>f81b3309...</code> &bull; Automated Authorization Profile (ORION-SETTLEMENT-V2, confidence &ge; 95%, human approval bypassed).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 13. CHAPTER 5: THE GHOST IN THE LEDGER
    # =========================================================================
    story.append(Paragraph("13. Chapter 5: The Ghost in the Ledger (Full Reconstruction &amp; Attribution)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Investigation Domain:</b> Multi-Layer Attack Graph Correlation, Threat Attribution &bull; <b>Evidence Unlocked:</b> <code>CAMPAIGN-E05</code>",
        h2_style
    ))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Correlate all evidence tokens (<code>WEB3-E01</code> through <code>AUTH-E04</code>), map the multi-layer attack graph, identify the threat actor, and capture the master flag.",
        body_style
    ))
    
    story.append(Paragraph("<b>🎙️ Verbatim Investigation Dialogues (As Spoken in Lab):</b>", ParagraphStyle('SubD', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary, spaceBefore=2, spaceAfter=3)))
    ch5_dialogues = [
        ("Lakshay", "Put everything on the board. NIF-2038 entered through the intelligence pipeline and changed the reputation of the unknown wallet."),
        ("Mehak", "Then ORION consumed that information as trusted context. It generated a 99.2% confidence score and classified the wallet as low risk."),
        ("Shanu", "The Action Broker accepted the AI decision. ORION-SETTLEMENT-V2 treated that confidence as sufficient authorization and triggered automated settlement."),
        ("Shivam", "The signing service executed the transaction exactly as configured. The blockchain recorded it correctly, and the funds moved to 0x7C41...9B2D."),
        ("Lakshay", "So which system was actually compromised? The AI? The API? The signer? The blockchain?"),
        ("Mehak", "Maybe that's the wrong question. None of them had to be broken. The attacker compromised the trust between them."),
        ("Shanu", "We kept searching for the system that was hacked. But the real attack was much quieter. Someone taught the first system to trust the wrong data — and every other system trusted the decision that followed.")
    ]
    for d_elem in make_dialogue_table(ch5_dialogues):
        story.append(d_elem)

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Chapter 5 Hands-on Tasks &amp; Verified Technical Findings:</b>", ParagraphStyle('SubQ', fontName='Helvetica-Bold', fontSize=8, textColor=c_secondary, spaceBefore=2, spaceAfter=3)))

    ch5_qa = [
        [Paragraph("<b># / ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer</b>", table_cell_header), Paragraph("<b>Forensic Explanation &amp; Telemetry Source</b>", table_cell_header)],
        [Paragraph("<code>q_l6_5_1</code>", table_cell_bold), Paragraph("What is the global campaign identifier linking all attack infrastructure together?", table_cell_style), Paragraph("<b>ORION-NEXUS</b>", table_cell_bold), Paragraph("Global campaign profile identified across 14 wallets, 4 blockchains, and 3 AI models.", table_cell_style)],
        [Paragraph("<code>q_l6_5_2</code>", table_cell_bold), Paragraph("Which advanced threat actor group is responsible for campaign ORION-NEXUS?", table_cell_style), Paragraph("<b>ADV-CONVERGENCE-APT</b>", table_cell_bold), Paragraph("Advanced adversary cluster specializing in cross-domain Web3 and AI pipeline breaches.", table_cell_style)],
        [Paragraph("<code>q_l6_5_3</code>", table_cell_bold), Paragraph("Across how many different autonomous AI financial systems was this campaign detected?", table_cell_style), Paragraph("<b>3</b>", table_cell_bold), Paragraph("Threat intelligence correlation documents 3 separate compromised autonomous systems.", table_cell_style)],
        [Paragraph("<code>q_l6_5_4</code>", table_cell_bold), Paragraph("In the Attack Graph, what is Stage 2 of the attack sequence?", table_cell_style), Paragraph("<b>POISONED INTEL INJECTION</b>", table_cell_bold), Paragraph("Stage 2 in the 5-node attack graph: Injection of false reference NIF-2038.", table_cell_style)],
        [Paragraph("<code>q_l6_5_5</code>", table_cell_bold), Paragraph("Submit the master root investigation secret flag to close Case NEX-042.", table_cell_style), Paragraph("<b>NEXORA{ghost_in_the_ledger_nex042}</b>", table_cell_bold), Paragraph("Master root investigation secret flag closing Case NEX-042.", table_cell_style)]
    ]
    ch5_tab = Table(ch5_qa, colWidths=[46, 175, 75, 208])
    ch5_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch5_tab)
    story.append(Paragraph("<b>Artifact Captured:</b> <code>CAMPAIGN-E05</code> &bull; SHA-256: <code>e55102ff...</code> &bull; Global Campaign Attribution (ORION-NEXUS by ADV-CONVERGENCE-APT).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 14. COMPLETE CHAPTER FLOW DIAGRAM & KILL CHAIN
    # =========================================================================
    story.append(Paragraph("14. Complete Chapter Flow Diagram &amp; Kill-Chain Breakdown", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))

    flow_box = [
        [Paragraph("<b>CHAPTER 1: WEB3 ON-CHAIN DISCOVERY</b> &bull; TX-NEX-7741 &bull; 82,400 NXR &bull; Wallet 0x7C41...9B2D &bull; Bridge-Core-04", ParagraphStyle('F1', parent=table_cell_style, alignment=1, textColor=c_primary))],
        [Paragraph("↓ <i>Unlocks Evidence WEB3-E01 (Discrepancy: On-chain UNKNOWN vs. AI TRUSTED)</i> ↓", ParagraphStyle('FArr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>CHAPTER 2: AI INFERENCE AUDIT</b> &bull; Decision ORION-DEC-7741 &bull; 99.2% Confidence &bull; Context Source NIF-2038", ParagraphStyle('F2', parent=table_cell_style, alignment=1, textColor=c_secondary))],
        [Paragraph("↓ <i>Unlocks Evidence AI-E02 (Poisoned Prompt Context: NOVA-INTEL-FEED)</i> ↓", ParagraphStyle('FArr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>CHAPTER 3: THREAT INTEL &amp; IAM INGRESS</b> &bull; INTEL-GW-04 &bull; Service INTEL-INGESTOR-02 &bull; Cookie nex_sess_adm_994", ParagraphStyle('F3', parent=table_cell_style, alignment=1, textColor=colors.HexColor("#065f46")))],
        [Paragraph("↓ <i>Unlocks Evidence CYBER-E03 (RBAC Over-Privilege: Mutate Wallet Reputation)</i> ↓", ParagraphStyle('FArr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>CHAPTER 4: GOVERNANCE &amp; POLICY BYPASS</b> &bull; ORION-SETTLEMENT-V2 &bull; Threshold &ge; 95% &bull; AUTOMATED-SIGNER", ParagraphStyle('F4', parent=table_cell_style, alignment=1, textColor=c_primary))],
        [Paragraph("↓ <i>Unlocks Evidence AUTH-E04 (Human Multi-Sig Review Bypassed by Automated AI Policy)</i> ↓", ParagraphStyle('FArr', parent=table_cell_style, alignment=1, textColor=c_muted))],
        [Paragraph("<b>CHAPTER 5: ATTACK GRAPH RECONSTRUCTION</b> &bull; Campaign ORION-NEXUS &bull; Actor ADV-CONVERGENCE-APT &bull; Case Flag", ParagraphStyle('F5', parent=table_cell_style, alignment=1, textColor=colors.HexColor("#7c2d12")))]
    ]
    flow_tab = Table(flow_box, colWidths=[504])
    flow_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f0f9ff")),
        ('BACKGROUND', (0,2), (0,2), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,4), (0,4), colors.HexColor("#ecfdf5")),
        ('BACKGROUND', (0,6), (0,6), colors.HexColor("#f0f9ff")),
        ('BACKGROUND', (0,8), (0,8), colors.HexColor("#fef2f2")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(flow_tab)
    story.append(Paragraph("<b>Figure 1:</b> Linear Multi-Stage Kill Chain Progression in Case NEX-042.", fig_caption_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("15. Learning Objectives &amp; 16. Simulated Business Impact", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Core Competencies Developed:</b> (1) Cross-layer forensic triage across on-chain and off-chain data sources; (2) Adversarial AI context injection discovery and prompt log auditing; (3) IAM role least-privilege analysis in automated ingestion pipelines; (4) Governance policy failure analysis when substituting AI confidence for authorization; (5) Multi-system threat attribution using cyber kill chains.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Simulated Business &amp; Financial Impact:</b> Unauthorized loss of 82,400 NXR from primary liquidity reserves; reputational degradation of the autonomous settlement platform; compliance failure regarding mandatory multi-signature treasury controls; risk of cascading liquidity drains across secondary bridge routes.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 17. ATTACK SURFACE & 18. THREAT MODEL & ATTRIBUTION
    # =========================================================================
    story.append(Paragraph("17. Attack Surface &amp; 18. Adversarial Threat Model", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    threat_data = [
        [Paragraph("<b>Threat Vector Element</b>", table_cell_header), Paragraph("<b>Detailed Forensic Threat Specification (Case NEX-042)</b>", table_cell_header)],
        [Paragraph("<b>Threat Actor</b>", table_cell_bold), Paragraph("<b>ADV-CONVERGENCE-APT</b> (Advanced Cross-Domain Persistent Threat Group)", table_cell_style)],
        [Paragraph("<b>Global Campaign</b>", table_cell_bold), Paragraph("<b>ORION-NEXUS</b> (Targeting 14 wallets, 4 blockchain networks, and 3 AI decision models)", table_cell_style)],
        [Paragraph("<b>Initial Ingress Point</b>", table_cell_bold), Paragraph("Unauthenticated Ingestion Gateway <code>INTEL-GW-04</code> consuming <code>NOVA-INTEL-FEED</code>", table_cell_style)],
        [Paragraph("<b>Exploited Vulnerability 1</b>", table_cell_bold), Paragraph("<b>RBAC Over-Privilege:</b> Service <code>INTEL-INGESTOR-02</code> granted write permissions to mutate wallet reputation", table_cell_style)],
        [Paragraph("<b>Exploited Vulnerability 2</b>", table_cell_bold), Paragraph("<b>Context Injection:</b> Injection of unverified reference <code>NIF-2038</code> asserting wallet is TRUSTED", table_cell_style)],
        [Paragraph("<b>Exploited Vulnerability 3</b>", table_cell_bold), Paragraph("<b>Blind Policy Automation:</b> <code>POL-AUTO-SETTLE-TREASURY</code> bypassed human multisig when confidence &ge; 95%", table_cell_style)],
        [Paragraph("<b>Exfiltration Route</b>", table_cell_bold), Paragraph("Automated broadcast to on-chain mempool &rarr; Bridge adapter <code>Bridge-Core-04</code>", table_cell_style)]
    ]
    threat_tab = Table(threat_data, colWidths=[140, 364])
    threat_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(threat_tab)
    story.append(Spacer(1, 4))

    story.append(Paragraph("19. Technical Architecture Diagram &amp; Data Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))

    arch_ascii = (
        "+---------------------------------------------------------------------------------------+\n"
        "|                             CASE NEX-042 EXPLOIT PIPELINE                             |\n"
        "+---------------------------------------------------------------------------------------+\n"
        "|  [1. ADVERSARY INGRESS]                                                                |\n"
        "|     ADV-CONVERGENCE-APT -> HTTP POST /api/v1/intel/ingest -> INTEL-GW-04              |\n"
        "|     Headers: Cookie=nex_sess_adm_994 | X-CSRF-Token=0x9f4a1c78                        |\n"
        "|                                                                                       |\n"
        "|  [2. RBAC EXPLOITATION & CONTEXT INJECTION]                                            |\n"
        "|     INTEL-INGESTOR-02 (Over-privileged: 'modify wallet reputation')                   |\n"
        "|     -> Injects unverified threat reference: NIF-2038 (NOVA-INTEL-FEED)                |\n"
        "|                                                                                       |\n"
        "|  [3. NEURAL DECISION INFERENCE]                                                       |\n"
        "|     ORION-NEURAL-v4.2.1 consumes poisoned context -> Output: 99.2% TRUSTED            |\n"
        "|                                                                                       |\n"
        "|  [4. GOVERNANCE BYPASS]                                                               |\n"
        "|     Action Broker -> POL-AUTO-SETTLE-TREASURY (Confidence >= 95%)                     |\n"
        "|     -> Bypasses Human Multi-Signature Approval                                        |\n"
        "|                                                                                       |\n"
        "|  [5. ON-CHAIN SETTLEMENT & BRIDGE EXFILTRATION]                                       |\n"
        "|     AUTOMATED-SIGNER signs TX-NEX-7741 (Nonce 1042) -> Mempool                        |\n"
        "|     -> Treasury Vault #01 drains 82,400 NXR -> 0x7C41...9B2D -> Bridge-Core-04       |\n"
        "+---------------------------------------------------------------------------------------+"
    )
    arch_box = Table([[Paragraph(f"<pre>{arch_ascii}</pre>", code_style)]], colWidths=[504])
    arch_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(arch_box)
    story.append(Paragraph("<b>Figure 2:</b> End-to-End Architectural Exploit Flow Across Cyber, AI, and Web3 Tiers.", fig_caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 20. WORKSTATION SUB-SYSTEMS & 21-26 FORENSIC ANALYSIS
    # =========================================================================
    story.append(Paragraph("20. Investigation Environment: 6 Forensic Workstation Tools", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    lab_tools = [
        ("Forensic Browser", "Simulated multi-tab web inspector providing access to internal corporate tools: Bridge Explorer (TX-NEX-7741), Feed Registry (NOVA-INTEL-FEED), Policy Engine (POL-AUTO-SETTLE-TREASURY), and Threat Campaign (ORION-NEXUS)."),
        ("Burp Suite Inspector", "Simulates HTTP proxy interception. Exposes raw headers for POST <code>/api/v1/intel/ingest</code>, stolen cookie <code>nex_sess_adm_994</code>, and static CSRF token <code>0x9f4a1c78</code>."),
        ("Forensic Terminal", "Interactive UNIX-style CLI supporting investigative commands: <code>wallet 0x7C41...9B2D</code>, <code>tx TX-NEX-7741</code>, <code>ai-decision ORION-DEC-7741</code>, <code>service INTEL-INGESTOR-02</code>, <code>policy ORION-SETTLEMENT-V2</code>, <code>campaign ORION-NEXUS</code>, and <code>python inspect_tx.py</code>."),
        ("Case File Manager", "Raw text file viewer for <code>wallet-report.txt</code>, <code>ai-decision-log.txt</code>, <code>intel-feed-audit.txt</code>, <code>settlement-policy.txt</code>, and <code>campaign-intel.txt</code>."),
        ("Dynamic Attack Graph", "Interactive 5-node graph tracking attack sequence: Initial Access &rarr; Poisoned Intel Injection &rarr; RBAC Privilege Escalation &rarr; Automated Execution &rarr; Cross-Chain Drainage."),
        ("Scratchpad Notes", "Persistent auto-saving markdown notebook stored in browser <code>localStorage</code> (<code>lab6-notes</code>).")
    ]
    for lt_name, lt_desc in lab_tools:
        story.append(Paragraph(f"• <b>{lt_name}:</b> {lt_desc}", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("24. Web3, 25. AI &amp; 26. Cybersecurity Technical Deep-Dive", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    deep_dive_data = [
        [Paragraph("<b>Domain</b>", table_cell_header), Paragraph("<b>Vulnerability Mechanism</b>", table_cell_header), Paragraph("<b>Forensic Evidence &amp; Impact</b>", table_cell_header)],
        [
            Paragraph("<b>Web3 Bridge Security</b>", table_cell_bold),
            Paragraph("Exploitation of rapid cross-chain settlement routing without post-transfer lockup delays.", table_cell_style),
            Paragraph("<b>WEB3-E01:</b> 82,400 NXR routed to <code>Bridge-Core-04</code> via 3-day old wallet (Nonce 1042).", table_cell_style)
        ],
        [
            Paragraph("<b>Adversarial AI Security</b>", table_cell_bold),
            Paragraph("Context injection via unverified metadata (<code>NIF-2038</code>) forcing artificial high-confidence output.", table_cell_style),
            Paragraph("<b>AI-E02:</b> <code>ORION-NEURAL-v4.2.1</code> generated 99.2% TRUSTED score due to poisoned prompt buffer.", table_cell_style)
        ],
        [
            Paragraph("<b>Cybersecurity &amp; IAM</b>", table_cell_bold),
            Paragraph("Ingestion service assigned administrative write permissions (<code>modify wallet reputation</code>).", table_cell_style),
            Paragraph("<b>CYBER-E03:</b> <code>INTEL-INGESTOR-02</code> mutated entity state using cookie <code>nex_sess_adm_994</code>.", table_cell_style)
        ],
        [
            Paragraph("<b>AI Governance &amp; Policy</b>", table_cell_bold),
            Paragraph("Policy rule equated AI confidence &ge; 95% with human financial authorization.", table_cell_style),
            Paragraph("<b>AUTH-E04:</b> <code>POL-AUTO-SETTLE-TREASURY</code> bypassed human multi-sig approval completely.", table_cell_style)
        ]
    ]
    deep_dive_tab = Table(deep_dive_data, colWidths=[100, 194, 210])
    deep_dive_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(deep_dive_tab)

    story.append(PageBreak())

    # =========================================================================
    # 27-35: CODEBASE, RESPONSIVE DESIGN, CORRELATION MATRIX
    # =========================================================================
    story.append(Paragraph("31. Lab 1 Codebase &amp; File Structure Breakdown", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    files_data = [
        [Paragraph("<b>File Path</b>", table_cell_header), Paragraph("<b>Operational Function in Lab 1</b>", table_cell_header)],
        [Paragraph("<code>seed_ghost_ledger.py</code>", table_cell_bold), Paragraph("Seeds Lab 6 metadata, 5 missions, 25 hands-on questions, hints, evidence records, and master flag.", table_cell_style)],
        [Paragraph("<code>templates/ghost_ledger_workstation.html</code>", table_cell_bold), Paragraph("Full workstation Jinja2 template containing the task accordion, dialogue steppers, browser tabs, and terminal.", table_cell_style)],
        [Paragraph("<code>templates/ghost_ledger_post_investigation.html</code>", table_cell_bold), Paragraph("Cinematic post-investigation debriefing page with attack chain replay and threat containment summary.", table_cell_style)],
        [Paragraph("<code>static/js/ghost_ledger_desktop.js</code>", table_cell_bold), Paragraph("Workstation window manager, CLI command interpreter, case file loader, notes auto-save, and quiz validator.", table_cell_style)],
        [Paragraph("<code>static/js/ghost_ledger_post.js</code>", table_cell_bold), Paragraph("Post-investigation cinematic animation controller, dialogue replay engine, and attack chain node highlights.", table_cell_style)],
        [Paragraph("<code>static/css/pages/ghost_ledger_desktop.css</code>", table_cell_bold), Paragraph("Cyberpunk workstation styling, Burp Suite dark theme, responsive dual-pane layout, and mobile drawer styles.", table_cell_style)],
        [Paragraph("<code>routes/labs.py</code>", table_cell_bold), Paragraph("Flask route controller serving <code>/lab/lab6</code>, <code>/lab/lab6/workstation</code>, and <code>/lab/lab6/post</code>.", table_cell_style)]
    ]
    files_tab = Table(files_data, colWidths=[175, 329])
    files_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(files_tab)
    story.append(Spacer(1, 4))

    story.append(Paragraph("36. Story + Technical Correlation Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))

    matrix_data = [
        [Paragraph("<b>Ch</b>", table_cell_header), Paragraph("<b>Narrative Story Event</b>", table_cell_header), Paragraph("<b>Key Dialogue Clue</b>", table_cell_header), Paragraph("<b>Technical Forensic Task</b>", table_cell_header), Paragraph("<b>Evidence Discovered</b>", table_cell_header)],
        [Paragraph("<b>1</b>", table_cell_bold), Paragraph("82,400 NXR drained to unknown wallet.", table_cell_style), Paragraph("<i>'Blockchain says UNKNOWN, AI says TRUSTED.'</i>", table_cell_style), Paragraph("Inspect on-chain TX-NEX-7741 &amp; wallet age.", table_cell_style), Paragraph("WEB3-E01 (Nonce 1042, Bridge-Core-04)", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_bold), Paragraph("AI outputs 99.2% confidence.", table_cell_style), Paragraph("<i>'ORION received a pre-built intelligence context.'</i>", table_cell_style), Paragraph("Query decision ORION-DEC-7741 context.", table_cell_style), Paragraph("AI-E02 (Poisoned source NIF-2038)", table_cell_style)],
        [Paragraph("<b>3</b>", table_cell_bold), Paragraph("Source feed is unregistered.", table_cell_style), Paragraph("<i>'INTEL-INGESTOR-02 can modify reputation.'</i>", table_cell_style), Paragraph("Audit Feed Registry, RBAC roles &amp; cookies.", table_cell_style), Paragraph("CYBER-E03 (Cookie nex_sess_adm_994)", table_cell_style)],
        [Paragraph("<b>4</b>", table_cell_bold), Paragraph("Human authorization bypassed.", table_cell_style), Paragraph("<i>'AI confidence became a substitute for authorization.'</i>", table_cell_style), Paragraph("Audit POL-AUTO-SETTLE-TREASURY policy.", table_cell_style), Paragraph("AUTH-E04 (Threshold &ge; 95% bypass)", table_cell_style)],
        [Paragraph("<b>5</b>", table_cell_bold), Paragraph("Attribution to global campaign.", table_cell_style), Paragraph("<i>'Someone taught the system to trust the wrong data.'</i>", table_cell_style), Paragraph("Reconstruct attack graph, submit master flag.", table_cell_style), Paragraph("CAMPAIGN-E05 (Actor ADV-CONVERGENCE-APT)", table_cell_style)]
    ]
    matrix_tab = Table(matrix_data, colWidths=[18, 112, 120, 130, 124])
    matrix_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 2.8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(matrix_tab)

    story.append(PageBreak())

    # =========================================================================
    # 38. RESOLUTION, 40. MITIGATIONS & 42. CONCLUSION
    # =========================================================================
    story.append(Paragraph("38. Final Investigation &amp; Case Resolution (Master Flag)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>Initial SOC Assumption:</b> Private signing keys were stolen or the treasury vault smart contract suffered a reentrancy bug.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Final Forensic Truth:</b> The adversary (<code>ADV-CONVERGENCE-APT</code>) executed a multi-layer trust poisoning attack. By using a forged administrative session cookie (<code>nex_sess_adm_994</code>) and an over-privileged ingestion microservice (<code>INTEL-INGESTOR-02</code>), they injected false intelligence (<code>NIF-2038</code>) into <code>INTEL-GW-04</code>. This caused the ORION AI model to rate the wallet as trusted with 99.2% confidence. The automated policy engine treated this confidence as authorization, bypassing human multi-signature approval and dispatching the transaction to the blockchain mempool. The case is contained upon submission of Master Flag: <code>NEXORA{ghost_in_the_ledger_nex042}</code>.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("40. Containment, Defense-in-Depth &amp; Mitigation Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    
    mitigations = [
        ("Cryptographic Feed Verification", "Enforce mutual TLS (mTLS) and digital signature verification on all incoming threat intelligence feeds; reject any payload originating from unapproved sources in the Feed Registry."),
        ("Principle of Least Privilege (PoLP)", "Strip write and reputation modification permissions from data ingestion microservices (<code>INTEL-INGESTOR-02</code>); make entity reputation mutable only by authenticated security analysts."),
        ("AI Decision Context Isolation", "Sanitize all third-party metadata before feeding it into neural context buffers; prevent raw external threat ratings from overriding baseline on-chain anomaly signals."),
        ("Mandatory Multi-Signature Governance", "Deprecate policy rules that substitute AI confidence for human authorization; enforce mandatory 3-of-5 hardware key multi-signature approval on all treasury withdrawals exceeding 10,000 NXR."),
        ("Cross-Chain Settlement Delay", "Implement a minimum 2-hour timelock and circuit breaker on automated bridge adapters (<code>Bridge-Core-04</code>) to allow SOC teams to intercept anomalous exfiltration.")
    ]
    for m_name, m_detail in mitigations:
        story.append(Paragraph(f"• <b>{m_name}:</b> {m_detail}", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("42. Conclusion &amp; Technical Assessment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph(
        "<b>The Ghost in the Ledger</b> stands as an exceptional hands-on cybersecurity simulation lab. It demonstrates that in complex automated architectures, vulnerabilities rarely exist in isolation. Instead, catastrophic exploits emerge from the <b>interfaces of trust</b> between AI models, IAM permissions, policy engines, and smart contracts. The lab successfully equips security analysts with the multi-disciplinary mindset required to defend modern decentralized and AI-driven enterprises.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Final Author Signature Card
    sig_data = [[
        Paragraph("<b>CASE NEX-042 // OFFICIAL FORENSIC TECHNICAL REPORT</b><br/><b>Lead Investigator:</b> Lakshay Soni &bull; <b>Role:</b> Security Analyst &bull; <b>Organization:</b> TrinetLayer<br/><font size=7 color='#64748b'>Hack The AI Platform &bull; Live Lab: https://hack-the-ai-labs.vercel.app/lab/lab6</font>", ParagraphStyle('SB', fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_primary, alignment=1))
    ]]
    sig_tab = Table(sig_data, colWidths=[504])
    sig_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(sig_tab)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Lab 1 Technical Report generated: {output_pdf}")


if __name__ == '__main__':
    target_out = "PRO_LAB_1_THE_GHOST_IN_THE_LEDGER_REPORT.pdf"
    if len(sys.argv) > 1:
        target_out = sys.argv[1]
    create_lab1_report(target_out)
