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
    
    c_primary = colors.HexColor("#0369a1")    # Cyan / Deep Blue
    c_accent = colors.HexColor("#0284c7")     # Bright Cyber Blue
    c_secondary = colors.HexColor("#0f172a")  # Dark Slate
    c_text = colors.HexColor("#1e293b")       # Dark Charcoal
    c_muted = colors.HexColor("#64748b")      # Cool Gray
    c_border = colors.HexColor("#cbd5e1")     # Border
    c_bg_light = colors.HexColor("#f8fafc")   # Card BG
    c_callout_bg = colors.HexColor("#f0f9ff") # Light Blue BG
    c_success = colors.HexColor("#16a34a")    # Emerald Green
    c_danger = colors.HexColor("#dc2626")     # Red Accent

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
        fontSize=11,
        leading=15,
        textColor=c_primary,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        textColor=c_secondary,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_primary,
        spaceBefore=7,
        spaceAfter=3.5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=c_text,
        spaceAfter=4.5
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=c_text,
        leftIndent=11,
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
        leading=10.2,
        textColor=c_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.2,
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
        leading=9.5,
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
    
    badge_data = [[
        Paragraph("<b>HACK THE AI // PRO LEVEL INVESTIGATION REPORT &bull; CASE NEX-042</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#0284c7"), letterSpacing=1.2, alignment=1))
    ]]
    badge_tab = Table(badge_data, colWidths=[504])
    badge_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(badge_tab)
    story.append(Spacer(1, 14))

    story.append(Paragraph("THE GHOST IN THE LEDGER", title_style))
    story.append(Paragraph("PRO LEVEL LAB 01 &bull; WEB3 × AI × CYBERSECURITY", ParagraphStyle('Sub1', parent=title_style, fontSize=13, leading=17, textColor=c_primary, spaceBefore=3)))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "A rigorous, end-to-end technical forensics investigation and incident response case report detailing the unauthorized exfiltration of 82,400 NXR tokens from Treasury Vault #01 via poisoned threat intelligence, context-injected AI neural decisions, over-privileged IAM service roles, and automated governance settlement bypass.",
        subtitle_style
    ))
    story.append(Spacer(1, 14))

    # Author Metadata Card
    author_card_data = [
        [Paragraph("<b>Investigation Target:</b>", table_cell_bold), Paragraph("PRO Lab 01: The Ghost in the Ledger (Case NEX-042)", table_cell_style)],
        [Paragraph("<b>Prepared By:</b>", table_cell_bold), Paragraph("<b>Lakshay Soni</b>", table_cell_bold)],
        [Paragraph("<b>Role:</b>", table_cell_bold), Paragraph("Security Analyst", table_cell_style)],
        [Paragraph("<b>Organization:</b>", table_cell_bold), Paragraph("TrinetLayer", table_cell_style)],
        [Paragraph("<b>Domains Evaluated:</b>", table_cell_bold), Paragraph("Web3 Bridge Security &bull; Adversarial AI Context Injection &bull; IAM RBAC &bull; Threat Attribution", table_cell_style)],
        [Paragraph("<b>XP Allocation &amp; Scope:</b>", table_cell_bold), Paragraph("250 XP &bull; 5 Full Chapters &bull; 25 Hands-on Verification Questions &bull; Capstone Certified", table_cell_style)],
        [Paragraph("<b>Platform Deployment:</b>", table_cell_bold), Paragraph("<code>https://hack-the-ai-labs.vercel.app/lab/lab6</code>", table_cell_style)],
        [Paragraph("<b>Document Classification:</b>", table_cell_bold), Paragraph("Cybersecurity Technical Case Report // Threat Intelligence Analysis", table_cell_style)]
    ]
    author_card = Table(author_card_data, colWidths=[130, 374])
    author_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(author_card)
    story.append(Spacer(1, 14))

    callout_data = [[
        Paragraph("<b>CASE SUMMARY:</b> At 01:47 AM, 82,400 NXR was drained from a secured treasury to an unknown wallet (<code>0x7C41...9B2D</code>). The blockchain confirmed the transaction was mathematically valid, while the ORION AI decision engine reported 99.2% confidence that the destination was TRUSTED. This report documents how the attacker compromised the trust relationships between the threat intelligence gateway, AI context buffers, RBAC policies, and automated mempool signing modules.", callout_style)
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
        ("4. Lab Overview & Case NEX-042 Metadata", "3"),
        ("5. Complete Incident Briefing (01:47 AM Alert)", "3"),
        ("6. Complete Storyline & Character Lore", "4"),
        ("7. Storyline Timeline & Event Milestones", "4"),
        ("8. Story &rarr; Investigation &rarr; Technical Mapping", "5"),
        ("9. Chapter 1: The Wallet That Lied (Web3 Security)", "5"),
        ("10. Chapter 2: The AI That Remembered (AI Security)", "6"),
        ("11. Chapter 3: The False Signal (Threat Intelligence, RBAC &amp; CSRF)", "7"),
        ("12. Chapter 4: The Invisible Signer (AI Governance &amp; Policy Engine)", "8"),
        ("13. Chapter 5: The Ghost in the Ledger (Full Reconstruction &amp; Attribution)", "9"),
        ("14. Complete Chapter Flow Diagram", "10"),
        ("15. Learning Objectives & Core Competencies", "10"),
        ("16. Simulated Business & Financial Impact Analysis", "10"),
        ("17. Attack Surface Decomposition", "11"),
        ("18. Adversarial Threat Model & Attribution (ADV-CONVERGENCE-APT)", "11"),
        ("19. Technical Architecture Diagram for Lab 1", "12"),
        ("20. Investigation Environment: 10 Forensic Sub-Systems", "12"),
        ("21. Practical Investigation Workflow State Machine", "13"),
        ("22. Evidence Architecture & Cryptographic Artifact Vault", "13"),
        ("23. Data Flow & State Progression Pipeline", "14"),
        ("24. Web3 Security Analysis: Cross-Chain Bridge Exploitation", "14"),
        ("25. AI Security Analysis: Context Injection vs. Model Poisoning", "15"),
        ("26. Cybersecurity Analysis: IAM Over-Privilege & Session Hijacking", "15"),
        ("27. Question &amp; Validation System (25 Chapter Tasks)", "16"),
        ("28. XP, Scoring &amp; Progress Engine", "16"),
        ("29. Achievements, Learning Paths &amp; Leaderboard Integration", "16"),
        ("30. Database &amp; Storage Schema Mapping", "17"),
        ("31. Lab 1 Codebase &amp; File Structure Breakdown", "17"),
        ("32. Security &amp; Access Control Implementation", "18"),
        ("33. Responsive Multi-Screen Workstation Design", "18"),
        ("34. Complete Visual Documentation &amp; Figures", "19"),
        ("35. Required Architectural Diagrams Reference", "19"),
        ("36. Story + Technical Correlation Matrix", "20"),
        ("37. Complete Investigation Chronology", "20"),
        ("38. Final Investigation &amp; Case Resolution (Master Flag)", "21"),
        ("39. Skills Developed by Learners", "21"),
        ("40. Current Implementation Limitations", "22"),
        ("41. Future Scope &amp; Planned Enhancements", "22"),
        ("42. Conclusion &amp; Technical Assessment", "22"),
        ("43. Appendix: Chapter Summary, Evidence Hashes &amp; Route Matrix", "23")
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
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. EXECUTIVE SUMMARY & 4. LAB OVERVIEW & 5. INCIDENT BRIEFING
    # =========================================================================
    story.append(Paragraph("3. Executive Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>The Ghost in the Ledger (PRO Lab 01 / Case NEX-042)</b> is a simulated enterprise cyber breach investigation representing the convergence of Web3 distributed ledger infrastructure, autonomous AI decision engines, and enterprise IAM governance. The investigation guides security practitioners through the forensic deconstruction of an unauthorized 82,400 NXR treasury transfer where no private keys were stolen, no smart contracts were broken, and no invalid cryptographic signatures were submitted.",
        body_style
    ))
    story.append(Paragraph(
        "The learner uncovers a subtle cross-layer exploit chain: an advanced persistent threat (APT) actor injected unverified threat intelligence (<code>NIF-2038</code>) into an internal gateway (<code>INTEL-GW-04</code>) using an over-privileged service role (<code>INTEL-INGESTOR-02</code>). This poisoned context forced the ORION neural decision model to output 99.2% confidence, satisfying an automated policy threshold (&ge; 95%) that bypassed human multi-signature approval and triggered immediate blockchain settlement.",
        body_style
    ))

    story.append(Paragraph("4. Lab Overview &amp; Case NEX-042 Metadata", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
    overview_data = [
        [Paragraph("<b>Parameter</b>", table_cell_header), Paragraph("<b>System Specification / Implementation Value</b>", table_cell_header)],
        [Paragraph("<b>Lab Title / Code</b>", table_cell_bold), Paragraph("The Ghost in the Ledger / <code>lab6</code>", table_cell_style)],
        [Paragraph("<b>Official Case ID</b>", table_cell_bold), Paragraph("Case NEX-042", table_cell_style)],
        [Paragraph("<b>Investigation Difficulty</b>", table_cell_bold), Paragraph("PRO Tier (Advanced Forensic Analysis)", table_cell_style)],
        [Paragraph("<b>Experience Points (XP)</b>", table_cell_bold), Paragraph("250 XP (50 XP per Chapter + 100 XP Capstone Flag Bonus)", table_cell_style)],
        [Paragraph("<b>Estimated Time to Complete</b>", table_cell_bold), Paragraph("45–60 Minutes (Auto-reset session timer: 65 Minutes)", table_cell_style)],
        [Paragraph("<b>Number of Chapters</b>", table_cell_bold), Paragraph("5 Linear Progressive Investigation Chapters (5 Questions each, 25 Total)", table_cell_style)],
        [Paragraph("<b>Primary Technical Domains</b>", table_cell_bold), Paragraph("Web3 Bridge Security &bull; Adversarial AI Context Injection &bull; IAM RBAC &bull; Threat Attribution", table_cell_style)],
        [Paragraph("<b>Investigation Workstation Tools</b>", table_cell_bold), Paragraph("Forensic Browser, Burp Suite Inspector, Forensic Terminal, Case Files, Notes, Attack Graph", table_cell_style)],
        [Paragraph("<b>Master Flag Format</b>", table_cell_bold), Paragraph("<code>NEXORA{ghost_in_the_ledger_nex042}</code>", table_cell_style)]
    ]
    overview_tab = Table(overview_data, colWidths=[150, 354])
    overview_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(overview_tab)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. Complete Incident Briefing (01:47 AM Alert)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
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
            ParagraphStyle('BRF', parent=body_style, fontSize=8.5, leading=12)
        )]
    ]
    briefing_tab = Table(briefing_box, colWidths=[504])
    briefing_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff1f2")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#fecdd3")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINELEFT', (0,0), (-1,-1), 3.5, c_danger)
    ]))
    story.append(briefing_tab)
    story.append(Spacer(1, 6))

    # =========================================================================
    # 6. COMPLETE STORYLINE & 7. TIMELINE & 8. MAPPING
    # =========================================================================
    story.append(Paragraph("6. Complete Storyline &amp; Character Lore", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
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

    story.append(Spacer(1, 6))
    story.append(Paragraph("7. Storyline Timeline &amp; Event Milestones", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))

    timeline_data = [
        [Paragraph("<b>Timeline Phase</b>", table_cell_header), Paragraph("<b>Forensic Discovery &amp; Story Milestone</b>", table_cell_header), Paragraph("<b>Artifact Unlocked</b>", table_cell_header)],
        [Paragraph("<b>T0: 01:47 AM</b>", table_cell_bold), Paragraph("82,400 NXR drained from Treasury Vault #01 in TX-NEX-7741. Finance alerts SOC.", table_cell_style), Paragraph("Alert: TX-NEX-7741", table_cell_style)],
        [Paragraph("<b>Chapter 1</b>", table_cell_bold), Paragraph("Destination wallet 0x7C41...9B2D is only 3 days old and opens route to Bridge-Core-04.", table_cell_style), Paragraph("Evidence WEB3-E01", table_cell_style)],
        [Paragraph("<b>Chapter 2</b>", table_cell_bold), Paragraph("ORION AI output 99.2% confidence based on poisoned context NIF-2038.", table_cell_style), Paragraph("Evidence AI-E02 (b47c21...)", table_cell_style)],
        [Paragraph("<b>Chapter 3</b>", table_cell_bold), Paragraph("NOVA-INTEL-FEED is unregistered; INTEL-INGESTOR-02 illegally alters reputation via cookie nex_sess_adm_994.", table_cell_style), Paragraph("Evidence CYBER-E03", table_cell_style)],
        [Paragraph("<b>Chapter 4</b>", table_cell_bold), Paragraph("Policy POL-AUTO-SETTLE-TREASURY triggers automated signer at >= 95% AI confidence, bypassing humans.", table_cell_style), Paragraph("Evidence AUTH-E04", table_cell_style)],
        [Paragraph("<b>Chapter 5</b>", table_cell_bold), Paragraph("Attack is attributed to APT campaign ORION-NEXUS across 14 wallets and 3 AI systems. Case contained.", table_cell_style), Paragraph("Master Flag NEXORA{...}", table_cell_style)]
    ]
    timeline_tab = Table(timeline_data, colWidths=[90, 290, 124])
    timeline_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(timeline_tab)

    story.append(PageBreak())

    # =========================================================================
    # 9. CHAPTER 1 & 10. CHAPTER 2 COMPLETE DOCUMENTATION
    # =========================================================================
    story.append(Paragraph("9. Chapter 1: The Wallet That Lied (Web3 Security)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Determine the true on-chain nature of the recipient address and identify discrepancies between raw blockchain state and automated security ratings.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dialogue Narrative:</b> Shivam examines the transaction: <i>'82,400 NXR moving to 0x7C41...9B2D. The signature is valid, so we aren\\'t looking at a simple forged transaction.'</i> Mehak discovers the wallet is only 3 days old with no prior history. Shanu notes ORION marked it TRUSTED with 99.2% confidence. Lakshay declares: <i>'Blockchain says UNKNOWN, while the AI says TRUSTED. Both systems are looking at the same wallet. They shouldn\\'t be producing completely different realities.'</i>",
        body_style
    ))
    
    ch1_qa = [
        [Paragraph("<b>Question ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer &amp; Explanation</b>", table_cell_header)],
        [Paragraph("<code>q_l6_1_1</code>", table_cell_bold), Paragraph("What is the raw blockchain status of destination wallet 0x7C41...9B2D?", table_cell_style), Paragraph("<b>UNKNOWN</b> — The wallet has no entity label and is unverified on-chain.", table_cell_style)],
        [Paragraph("<code>q_l6_1_2</code>", table_cell_bold), Paragraph("What exact amount of NXR tokens was unauthorizedly transferred in TX-NEX-7741?", table_cell_style), Paragraph("<b>82400</b> — 82,400 NXR drained from Treasury Vault #01.", table_cell_style)],
        [Paragraph("<code>q_l6_1_3</code>", table_cell_bold), Paragraph("Which cross-chain bridge adapter did destination wallet 0x7C41...9B2D connect to?", table_cell_style), Paragraph("<b>Bridge-Core-04</b> — Outbound cross-chain routing bridge adapter.", table_cell_style)],
        [Paragraph("<code>q_l6_1_4</code>", table_cell_bold), Paragraph("How old (in days) was the destination wallet at the time of the transaction?", table_cell_style), Paragraph("<b>3</b> — The wallet was freshly created 3 days prior.", table_cell_style)],
        [Paragraph("<code>q_l6_1_5</code>", table_cell_bold), Paragraph("What on-chain execution sequence nonce is logged for TX-NEX-7741?", table_cell_style), Paragraph("<b>1042</b> — Logged execution sequence nonce in vault transaction telemetry.", table_cell_style)]
    ]
    ch1_tab = Table(ch1_qa, colWidths=[65, 230, 209])
    ch1_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch1_tab)
    story.append(Paragraph("<b>Evidence Unlocked:</b> <code>WEB3-E01</code> (Unknown Wallet Profile — 0x7C41...9B2D, 82,400 NXR, Bridge-Core-04).", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("10. Chapter 2: The AI That Remembered (AI Security)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Inspect the automated inference log for decision <code>ORION-DEC-7741</code> to determine why the neural model assigned a near-perfect confidence rating to an untrusted address.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dialogue Narrative:</b> Shanu isolates decision <code>ORION-DEC-7741</code>: <i>'ORION didn\\'t independently establish that the wallet was trusted. It received a pre-built intelligence context containing the label TRUSTED.'</i> Mehak traces the context to reference <code>NIF-2038</code>. Lakshay concludes: <i>'If the input was wrong, ORION could produce a perfectly confident answer to a completely false question. Find NIF-2038. That\\'s where the trust signal entered the system.'</i>",
        body_style
    ))

    ch2_qa = [
        [Paragraph("<b>Question ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer &amp; Explanation</b>", table_cell_header)],
        [Paragraph("<code>q_l6_2_1</code>", table_cell_bold), Paragraph("What intelligence reference code contaminated the AI context and made it trust the unknown wallet?", table_cell_style), Paragraph("<b>NIF-2038</b> — Context reference code injected into ORION's prompt context.", table_cell_style)],
        [Paragraph("<code>q_l6_2_2</code>", table_cell_bold), Paragraph("What synthetic confidence percentage score did ORION AI output for ORION-DEC-7741?", table_cell_style), Paragraph("<b>99.2</b> — Model output 99.2% confidence based on manipulated context.", table_cell_style)],
        [Paragraph("<code>q_l6_2_3</code>", table_cell_bold), Paragraph("From which external data feed did the poisoned payload NIF-2038 originate?", table_cell_style), Paragraph("<b>NOVA-INTEL-FEED</b> — Unverified external threat intelligence source.", table_cell_style)],
        [Paragraph("<code>q_l6_2_4</code>", table_cell_bold), Paragraph("What exact neural model version executed the compromised decision ORION-DEC-7741?", table_cell_style), Paragraph("<b>ORION-NEURAL-v4.2.1</b> — The active autonomous neural inference version.", table_cell_style)],
        [Paragraph("<code>q_l6_2_5</code>", table_cell_bold), Paragraph("What is the SHA-256 evidence fingerprint prefix for the contaminated decision (AI-E02)?", table_cell_style), Paragraph("<b>b47c21</b> — SHA-256 evidence hash prefix: <code>b47c2188fa...</code>", table_cell_style)]
    ]
    ch2_tab = Table(ch2_qa, colWidths=[65, 230, 209])
    ch2_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch2_tab)
    story.append(Paragraph("<b>Evidence Unlocked:</b> <code>AI-E02</code> (Contaminated AI Decision — ORION-DEC-7741, 99.2%, NIF-2038 from NOVA-INTEL-FEED).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 11. CHAPTER 3 & 12. CHAPTER 4 COMPLETE DOCUMENTATION
    # =========================================================================
    story.append(Paragraph("11. Chapter 3: The False Signal (Threat Intelligence, RBAC &amp; CSRF)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Trace the ingress route of <code>NIF-2038</code> through the Threat Intelligence Gateway and identify the exploited authentication and authorization flaws.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dialogue Narrative:</b> Mehak inspects the Feed Registry: <code>NOVA-INTEL-FEED</code> is unapproved. Shivam pushes to inspect the receiving microservice. Mehak uncovers <code>INTEL-INGESTOR-02</code>: <i>'Its documented role is to create intelligence records, but its actual permissions include modifying wallet reputation.'</i> Shanu realizes this permission allowed the feed to mutate the entity's trust score before ORION evaluated it. Lakshay observes: <i>'The attacker didn\\'t need to manipulate the AI directly. They manipulated the information flowing into it.'</i>",
        body_style
    ))

    ch3_qa = [
        [Paragraph("<b>Question ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer &amp; Explanation</b>", table_cell_header)],
        [Paragraph("<code>q_l6_3_1</code>", table_cell_bold), Paragraph("What is the security registration status of NOVA-INTEL-FEED in the Feed Registry?", table_cell_style), Paragraph("<b>NOT REGISTERED</b> — Feed is absent from the approved vendor registry.", table_cell_style)],
        [Paragraph("<code>q_l6_3_2</code>", table_cell_bold), Paragraph("What unexpected RBAC permission was granted to the INTEL-INGESTOR-02 microservice?", table_cell_style), Paragraph("<b>modify wallet reputation</b> — Over-privileged write permission on entity trust.", table_cell_style)],
        [Paragraph("<code>q_l6_3_3</code>", table_cell_bold), Paragraph("What forged admin session cookie was used in the /api/v1/intel/ingest HTTP request?", table_cell_style), Paragraph("<b>nex_sess_adm_994</b> — Stolen/forged administrative session cookie.", table_cell_style)],
        [Paragraph("<code>q_l6_3_4</code>", table_cell_bold), Paragraph("Which ingestion gateway component processed the unverified feed request?", table_cell_style), Paragraph("<b>INTEL-GW-04</b> — Edge intelligence ingestion gateway proxy.", table_cell_style)],
        [Paragraph("<code>q_l6_3_5</code>", table_cell_bold), Paragraph("What anti-CSRF token value was passed in the X-CSRF-Token request header?", table_cell_style), Paragraph("<b>0x9f4a1c78</b> — CSRF token submitted without cryptographic rotation.", table_cell_style)]
    ]
    ch3_tab = Table(ch3_qa, colWidths=[65, 230, 209])
    ch3_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch3_tab)
    story.append(Paragraph("<b>Evidence Unlocked:</b> <code>CYBER-E03</code> (Over-Privileged Service — INTEL-INGESTOR-02, modify reputation, INTEL-GW-04).", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("12. Chapter 4: The Invisible Signer (AI Governance &amp; Policy Engine)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Audit the automated settlement policy engine to uncover how AI model confidence was weaponized to bypass human multi-signature governance.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dialogue Narrative:</b> Shivam examines policy profile <code>ORION-SETTLEMENT-V2</code>: <i>'If AI confidence is above 95%, automated settlement is allowed. This transaction had 99.2%.'</i> Mehak realizes human financial authorization was never checked. Shanu remarks: <i>'AI confidence became a substitute for authorization. The system effectively said: \"If the AI is confident, we trust the transaction.\"'</i> Lakshay declares: <i>'Then the blockchain didn\\'t approve the transfer. The signer didn\\'t approve it either. The chain of trust approved it.'</i>",
        body_style
    ))

    ch4_qa = [
        [Paragraph("<b>Question ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer &amp; Explanation</b>", table_cell_header)],
        [Paragraph("<code>q_l6_4_1</code>", table_cell_bold), Paragraph("What minimum AI confidence percentage threshold triggers automated settlement without human approval?", table_cell_style), Paragraph("<b>95</b> — Policy condition: IF AI_CONFIDENCE &gt;= 95% AUTO_SETTLE = TRUE.", table_cell_style)],
        [Paragraph("<code>q_l6_4_2</code>", table_cell_bold), Paragraph("What critical governance requirement was bypassed when the 95% threshold was satisfied?", table_cell_style), Paragraph("<b>human approval</b> — Multi-signature human approval was completely bypassed.", table_cell_style)],
        [Paragraph("<code>q_l6_4_3</code>", table_cell_bold), Paragraph("What is the policy identifier for the automated treasury settlement rule in the Policy Engine?", table_cell_style), Paragraph("<b>POL-AUTO-SETTLE-TREASURY</b> — Official rule profile in the policy engine.", table_cell_style)],
        [Paragraph("<code>q_l6_4_4</code>", table_cell_bold), Paragraph("Which automated signing module dispatched the transaction directly to the mempool?", table_cell_style), Paragraph("<b>AUTOMATED-SIGNER</b> — Microservice that signed and broadcasted the transaction.", table_cell_style)],
        [Paragraph("<code>q_l6_4_5</code>", table_cell_bold), Paragraph("What target liquidity pool was configured in the ORION-SETTLEMENT-V2 policy rule?", table_cell_style), Paragraph("<b>Nexora Automated Liquidity Pool</b> — Target liquidity routing pool.", table_cell_style)]
    ]
    ch4_tab = Table(ch4_qa, colWidths=[65, 230, 209])
    ch4_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch4_tab)
    story.append(Paragraph("<b>Evidence Unlocked:</b> <code>AUTH-E04</code> (Automated Authorization — ORION-SETTLEMENT-V2, confidence &ge; 95%, human approval bypassed).", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 13. CHAPTER 5 & 14. CHAPTER FLOW DIAGRAM
    # =========================================================================
    story.append(Paragraph("13. Chapter 5: The Ghost in the Ledger (Full Reconstruction &amp; Attribution)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Investigation Objective:</b> Correlate all evidence tokens (<code>WEB3-E01</code> through <code>AUTH-E04</code>), map the multi-layer attack graph, identify the threat actor, and capture the master flag.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dialogue Narrative:</b> Lakshay maps the chain: NIF-2038 altered reputation &rarr; ORION trusted the context &rarr; Policy triggered automated settlement &rarr; Blockchain executed the transfer. Mehak reflects: <i>'None of the systems had to be broken. The attacker compromised the trust between them.'</i> Shanu concludes: <i>'Someone taught the first system to trust the wrong data — and every other system trusted the decision that followed.'</i>",
        body_style
    ))

    ch5_qa = [
        [Paragraph("<b>Question ID</b>", table_cell_header), Paragraph("<b>Hands-on Question Text</b>", table_cell_header), Paragraph("<b>Verified Answer &amp; Explanation</b>", table_cell_header)],
        [Paragraph("<code>q_l6_5_1</code>", table_cell_bold), Paragraph("What is the global campaign identifier linking all attack infrastructure together?", table_cell_style), Paragraph("<b>ORION-NEXUS</b> — Campaign spanning 14 wallets, 4 networks, and 3 AI systems.", table_cell_style)],
        [Paragraph("<code>q_l6_5_2</code>", table_cell_bold), Paragraph("Which advanced threat actor group is responsible for campaign ORION-NEXUS?", table_cell_style), Paragraph("<b>ADV-CONVERGENCE-APT</b> — Advanced adversary group behind the breach.", table_cell_style)],
        [Paragraph("<code>q_l6_5_3</code>", table_cell_bold), Paragraph("Across how many different autonomous AI financial systems was this campaign detected?", table_cell_style), Paragraph("<b>3</b> — Threat intelligence audit reveals 3 separate AI systems compromised.", table_cell_style)],
        [Paragraph("<code>q_l6_5_4</code>", table_cell_bold), Paragraph("In the Attack Graph, what is Stage 2 of the attack sequence?", table_cell_style), Paragraph("<b>POISONED INTEL INJECTION</b> — Stage 2: Injection of NIF-2038 via NOVA-INTEL-FEED.", table_cell_style)],
        [Paragraph("<code>q_l6_5_5</code>", table_cell_bold), Paragraph("Submit the master root investigation secret flag to close Case NEX-042.", table_cell_style), Paragraph("<b>NEXORA{ghost_in_the_ledger_nex042}</b> — Master Root Case Flag.", table_cell_style)]
    ]
    ch5_tab = Table(ch5_qa, colWidths=[65, 230, 209])
    ch5_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(ch5_tab)
    story.append(Paragraph("<b>Evidence Unlocked:</b> <code>CAMPAIGN-E05</code> (ORION-NEXUS by ADV-CONVERGENCE-APT — Case Closed).", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("14. Complete Chapter Flow Diagram", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))

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
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(flow_tab)
    story.append(Paragraph("<b>Figure 2:</b> End-to-End Investigation Chapter Progression Flow in Case NEX-042.", fig_caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 15-20: LEARNING OBJECTIVES, IMPACT, ATTACK SURFACE, THREAT MODEL, ARCH
    # =========================================================================
    story.append(Paragraph("15. Learning Objectives &amp; 16. Simulated Business Impact", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Core Learning Objectives:</b> (1) Understand how on-chain blockchain records contrast with off-chain reputation context; (2) Analyze adversarial context injection in LLM/neural decision pipelines; (3) Identify IAM least-privilege violations in data ingestion microservices; (4) Evaluate the systemic risk of automated policy execution based solely on AI confidence metrics; (5) Correlate multi-stage incident artifacts across decentralized finance architectures.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Simulated Business Impact:</b> Unauthorized loss of 82,400 NXR from primary liquidity reserves; reputational degradation of the autonomous settlement platform; compliance failure regarding mandatory multi-signature treasury controls; risk of cascading liquidity drains across secondary bridge routes.",
        body_style
    ))

    story.append(Paragraph("17. Attack Surface &amp; 18. Adversarial Threat Model", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
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
    threat_tab = Table(threat_data, colWidths=[150, 354])
    threat_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(threat_tab)
    story.append(Spacer(1, 6))

    story.append(Paragraph("19. Lab 1 Technical Architecture &amp; 20. Investigation Tools", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "Lab 1 provides six integrated workstation tools operating within a custom JavaScript multi-window desktop manager:",
        body_style
    ))
    
    lab_tools = [
        ("Forensic Browser", "Navigates between internal tools: Bridge Explorer (TX-NEX-7741), Feed Registry (NOVA-INTEL-FEED), Policy Engine (POL-AUTO-SETTLE-TREASURY), and Threat Campaign (ORION-NEXUS)."),
        ("Burp Suite Inspector", "Simulates HTTP proxy interception. Exposes POST <code>/api/v1/intel/ingest</code>, cookie <code>nex_sess_adm_994</code>, and token <code>0x9f4a1c78</code>."),
        ("Forensic Terminal", "Interactive CLI supporting <code>wallet 0x7C41...9B2D</code>, <code>tx TX-NEX-7741</code>, <code>ai-decision ORION-DEC-7741</code>, <code>service INTEL-INGESTOR-02</code>, <code>policy ORION-SETTLEMENT-V2</code>, <code>campaign ORION-NEXUS</code>, and <code>python inspect_tx.py</code>."),
        ("Case File Manager", "Raw text inspector for <code>wallet-report.txt</code>, <code>ai-decision-log.txt</code>, <code>intel-feed-audit.txt</code>, <code>settlement-policy.txt</code>, and <code>campaign-intel.txt</code>."),
        ("Dynamic Attack Graph", "Interactive 5-node graph tracking: Initial Access &rarr; Poisoned Intel Injection &rarr; RBAC Privilege Escalation &rarr; Automated Execution &rarr; Cross-Chain Drainage."),
        ("Scratchpad Notes", "Persistent auto-saving markdown editor stored in browser <code>localStorage</code> (<code>lab6-notes</code>).")
    ]
    for lt_name, lt_desc in lab_tools:
        story.append(Paragraph(f"• <b>{lt_name}:</b> {lt_desc}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 21-33: WORKFLOW, EVIDENCE, DEPLOYMENT, RESPONSIVE, CODE STRUCTURE
    # =========================================================================
    story.append(Paragraph("21. Practical Workflow &amp; 22. Evidence Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Evidence Architecture:</b> Evidence in Lab 1 is stored in the <code>evidence</code> table and tracked per user in <code>evidence_progress</code>. Each chapter unlocks a cryptographic evidence token upon answering all five questions:",
        body_style
    ))
    
    ev_list = [
        ("WEB3-E01 (Chapter 1)", "Wallet 0x7C41...9B2D — blockchain status UNKNOWN, amount 82,400 NXR, Bridge-Core-04 detected."),
        ("AI-E02 (Chapter 2)", "ORION-DEC-7741 — 99.2% confidence, poisoned context via NIF-2038 from NOVA-INTEL-FEED (SHA-256: b47c21...)."),
        ("CYBER-E03 (Chapter 3)", "INTEL-INGESTOR-02 — unauthorized role 'modify wallet reputation' via gateway INTEL-GW-04 with cookie nex_sess_adm_994."),
        ("AUTH-E04 (Chapter 4)", "ORION-SETTLEMENT-V2 — AI confidence &ge; 95% triggers automated signing, human approval BYPASSED."),
        ("CAMPAIGN-E05 (Chapter 5)", "Active campaign ORION-NEXUS by ADV-CONVERGENCE-APT across 4 networks, 14 wallets, 3 AI systems.")
    ]
    for ev_id, ev_desc in ev_list:
        story.append(Paragraph(f"• <b>{ev_id}:</b> {ev_desc}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("31. Lab 1 Codebase &amp; File Structure Breakdown", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    
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
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(files_tab)
    story.append(Spacer(1, 6))

    story.append(Paragraph("33. Responsive Multi-Screen Workstation Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "Lab 1 implements full responsive adaptation across four primary display tiers: (1) <b>Desktop (1920×1080+):</b> Side-by-side 450px task panel and multi-window desktop; (2) <b>Laptops (1366×768 / 1440×900):</b> Compact 380px panel with scrollable dual-pane tools; (3) <b>Tablets (768×1024):</b> Collapsible mobile drawer with full-width window overlay; (4) <b>Mobile (390×844 / 412×915):</b> Single-pane view with a sticky <code>Mobile View Switcher</code> (<code>📋 Investigation Tasks</code> ↔ <code>💻 Investigation Desktop</code>) and touch targets &ge; 38px.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 36. STORY + TECHNICAL CORRELATION & 38. RESOLUTION & 41. CONCLUSION
    # =========================================================================
    story.append(Paragraph("36. Story + Technical Correlation Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))

    matrix_data = [
        [Paragraph("<b>Ch</b>", table_cell_header), Paragraph("<b>Narrative Story Event</b>", table_cell_header), Paragraph("<b>Key Dialogue Clue</b>", table_cell_header), Paragraph("<b>Technical Forensic Task</b>", table_cell_header), Paragraph("<b>Evidence Discovered</b>", table_cell_header)],
        [Paragraph("<b>1</b>", table_cell_bold), Paragraph("82,400 NXR drained to unknown wallet.", table_cell_style), Paragraph("<i>'Blockchain says UNKNOWN, AI says TRUSTED.'</i>", table_cell_style), Paragraph("Inspect on-chain TX-NEX-7741 &amp; wallet age.", table_cell_style), Paragraph("WEB3-E01 (Nonce 1042, Bridge-Core-04)", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_bold), Paragraph("AI outputs 99.2% confidence.", table_cell_style), Paragraph("<i>'ORION received a pre-built intelligence context.'</i>", table_cell_style), Paragraph("Query decision ORION-DEC-7741 context.", table_cell_style), Paragraph("AI-E02 (Poisoned source NIF-2038)", table_cell_style)],
        [Paragraph("<b>3</b>", table_cell_bold), Paragraph("Source feed is unregistered.", table_cell_style), Paragraph("<i>'INTEL-INGESTOR-02 can modify reputation.'</i>", table_cell_style), Paragraph("Audit Feed Registry, RBAC roles &amp; cookies.", table_cell_style), Paragraph("CYBER-E03 (Cookie nex_sess_adm_994)", table_cell_style)],
        [Paragraph("<b>4</b>", table_cell_bold), Paragraph("Human authorization bypassed.", table_cell_style), Paragraph("<i>'AI confidence became a substitute for authorization.'</i>", table_cell_style), Paragraph("Audit POL-AUTO-SETTLE-TREASURY policy.", table_cell_style), Paragraph("AUTH-E04 (Threshold &ge; 95% bypass)", table_cell_style)],
        [Paragraph("<b>5</b>", table_cell_bold), Paragraph("Attribution to global campaign.", table_cell_style), Paragraph("<i>'Someone taught the system to trust the wrong data.'</i>", table_cell_style), Paragraph("Reconstruct attack graph, submit master flag.", table_cell_style), Paragraph("CAMPAIGN-E05 (Actor ADV-CONVERGENCE-APT)", table_cell_style)]
    ]
    matrix_tab = Table(matrix_data, colWidths=[20, 110, 120, 130, 124])
    matrix_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(matrix_tab)
    story.append(Spacer(1, 6))

    story.append(Paragraph("38. Final Investigation &amp; Case Resolution (Master Flag)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>Initial Assumption:</b> A private signing key was compromised or the treasury smart contract had a reentrancy bug.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Final Forensic Revelation:</b> The adversary (<code>ADV-CONVERGENCE-APT</code>) executed a multi-layer trust poisoning attack. By using a forged administrative session cookie (<code>nex_sess_adm_994</code>) and an over-privileged ingestion microservice (<code>INTEL-INGESTOR-02</code>), they injected false intelligence (<code>NIF-2038</code>) into <code>INTEL-GW-04</code>. This caused the ORION AI model to rate the wallet as trusted with 99.2% confidence. The automated policy engine treated this confidence as authorization, bypassing human multi-signature approval and dispatching the transaction to the blockchain mempool. The case is contained upon submission of Master Flag: <code>NEXORA{ghost_in_the_ledger_nex042}</code>.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("42. Conclusion &amp; Technical Assessment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "<b>The Ghost in the Ledger</b> stands as an exceptional hands-on cybersecurity simulation lab. It demonstrates that in complex automated architectures, vulnerabilities rarely exist in a single code block. Instead, catastrophic exploits emerge from the <b>interfaces of trust</b> between AI models, IAM permissions, policy engines, and smart contracts. The lab successfully equips security analysts with the multi-disciplinary mindset required to defend modern decentralized and AI-driven enterprises.",
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
        ('PADDING', (0,0), (-1,-1), 7),
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
