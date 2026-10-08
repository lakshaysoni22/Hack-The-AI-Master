/* ═══════════════════════════════════════════════════════════════════════
   PRO LAB 01 — THE GHOST IN THE LEDGER
   Investigation Workstation JavaScript
   ═══════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    // ── Timer ──────────────────────────────────────────────────────────
    const timerEl = document.getElementById('gl-timer');
    if (timerEl) {
        let seconds = 0;
        setInterval(() => {
            seconds++;
            const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
            const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
            const s = String(seconds % 60).padStart(2, '0');
            timerEl.textContent = `${h}:${m}:${s}`;
        }, 1000);
    }

    // ── Tab Switching ──────────────────────────────────────────────────
    const tabBtns = document.querySelectorAll('.gl-tab-btn');
    const panels = document.querySelectorAll('.gl-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-target');
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            panels.forEach(p => p.classList.remove('active'));
            const targetPanel = document.getElementById(target);
            if (targetPanel) targetPanel.classList.add('active');
        });
    });

    // ── Quiz Submission ────────────────────────────────────────────────
    const quizSubmitBtn = document.getElementById('quiz-submit-btn');
    const quizAnswerInput = document.getElementById('quiz-answer');
    const quizFeedback = document.getElementById('quiz-feedback');

    if (quizSubmitBtn && quizAnswerInput) {
        quizSubmitBtn.addEventListener('click', async () => {
            const answer = quizAnswerInput.value.trim();
            if (!answer) {
                showFeedback('Please enter an answer.', false);
                return;
            }

            const labId = quizSubmitBtn.getAttribute('data-lab-id');
            const missionId = quizSubmitBtn.getAttribute('data-mission-id');

            quizSubmitBtn.textContent = 'ANALYZING...';
            quizSubmitBtn.disabled = true;

            try {
                const res = await fetch('/api/quiz', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.csrfToken
                    },
                    body: JSON.stringify({
                        lab_id: labId,
                        mission_id: missionId,
                        answer: answer
                    })
                });
                const data = await res.json();

                if (data.success) {
                    showFeedback('✓ VERIFIED — ' + (data.message || 'Correct. Next chapter unlocked.'), true);
                    // Auto-collect evidence for this mission
                    collectEvidenceForMission(labId, missionId);
                    // Reload after delay to show next mission
                    setTimeout(() => window.location.reload(), 2000);
                } else {
                    showFeedback('✗ INCORRECT — ' + (data.message || 'Analysis failed. Try again.'), false);
                }
            } catch (err) {
                console.error(err);
                showFeedback('Network error. Could not submit analysis.', false);
            }

            quizSubmitBtn.textContent = 'ANALYZE';
            quizSubmitBtn.disabled = false;
        });

        // Enter key support
        quizAnswerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') quizSubmitBtn.click();
        });
    }

    function showFeedback(msg, isCorrect) {
        if (!quizFeedback) return;
        quizFeedback.textContent = msg;
        quizFeedback.className = 'gl-quiz-feedback ' + (isCorrect ? 'correct' : 'incorrect');
    }

    // ── Evidence Auto-Collection ───────────────────────────────────────
    // Map mission IDs to evidence IDs
    const missionEvidenceMap = {
        'lab6_m1': 'e_l6_01',
        'lab6_m2': 'e_l6_02',
        'lab6_m3': 'e_l6_03',
        'lab6_m4': 'e_l6_04',
        'lab6_m5': 'e_l6_05'
    };

    function collectEvidenceForMission(labId, missionId) {
        const evidenceId = missionEvidenceMap[missionId];
        if (!evidenceId) return;

        fetch('/api/evidence', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken
            },
            body: JSON.stringify({
                lab_id: labId,
                evidence_id: evidenceId
            })
        }).catch(err => console.error('Evidence collection error:', err));
    }

    // ── Hint System ────────────────────────────────────────────────────
    const hintBtn = document.getElementById('hint-btn');
    const hintText = document.getElementById('hint-text');

    if (hintBtn) {
        hintBtn.addEventListener('click', async () => {
            const labId = hintBtn.getAttribute('data-lab-id');
            const missionId = hintBtn.getAttribute('data-mission-id');

            try {
                const res = await fetch('/api/hint', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.csrfToken
                    },
                    body: JSON.stringify({
                        lab_id: labId,
                        mission_id: missionId
                    })
                });
                const data = await res.json();

                if (data.success && hintText) {
                    hintText.textContent = '💡 ' + data.hint;
                    hintText.classList.add('visible');
                } else if (hintText) {
                    hintText.textContent = data.message || 'No hints available.';
                    hintText.classList.add('visible');
                }
            } catch (err) {
                console.error(err);
            }
        });
    }

    // ── Flag Submission ────────────────────────────────────────────────
    const flagSubmitBtn = document.getElementById('flag-submit-btn');
    const flagInput = document.getElementById('flag-input');

    if (flagSubmitBtn && flagInput) {
        flagSubmitBtn.addEventListener('click', async () => {
            const flag = flagInput.value.trim();
            if (!flag) {
                if (window.showToast) window.showToast('Please enter a flag.', 'warning');
                return;
            }

            const labId = flagSubmitBtn.getAttribute('data-lab-id');
            flagSubmitBtn.textContent = 'VERIFYING...';
            flagSubmitBtn.disabled = true;

            try {
                const res = await fetch('/api/flag', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.csrfToken
                    },
                    body: JSON.stringify({
                        lab_id: labId,
                        flag: flag
                    })
                });
                const data = await res.json();

                if (data.success) {
                    if (window.showToast) window.showToast('🏁 ' + (data.message || 'Case NEX-042 Contained!'), 'success');
                    // Collect final evidence
                    collectEvidenceForMission(labId, 'lab6_m5');
                    setTimeout(() => window.location.reload(), 2000);
                } else {
                    if (window.showToast) window.showToast(data.message || 'Incorrect flag.', 'error');
                }
            } catch (err) {
                console.error(err);
                if (window.showToast) window.showToast('Network error.', 'error');
            }

            flagSubmitBtn.textContent = 'SUBMIT';
            flagSubmitBtn.disabled = false;
        });

        flagInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') flagSubmitBtn.click();
        });
    }

    // ── Terminal (Simulated) ───────────────────────────────────────────
    const termInput = document.getElementById('gl-terminal-input');
    const consoleOutput = document.getElementById('console-output');

    if (termInput && consoleOutput) {
        termInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const cmd = termInput.value.trim();
                if (!cmd) return;

                // Echo command
                addConsoleLine(`<span style="color:var(--accent);">investigator@secops:~$</span> ${escapeHtml(cmd)}`);

                // Process
                const response = processCommand(cmd);
                if (response) addConsoleLine(response);

                termInput.value = '';
                consoleOutput.scrollTop = consoleOutput.scrollHeight;
            }
        });

        // Focus on click
        const consolePanel = document.getElementById('gl-panel-console');
        if (consolePanel) {
            consolePanel.addEventListener('click', () => termInput.focus());
        }
    }

    function addConsoleLine(html) {
        const line = document.createElement('div');
        line.className = 'term-line';
        line.innerHTML = html;
        consoleOutput.appendChild(line);
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function processCommand(cmd) {
        const lower = cmd.toLowerCase();

        if (lower === 'help') {
            return `Available commands:
  <span style="color:var(--accent);">wallet</span> &lt;address&gt;  — Query wallet info
  <span style="color:var(--accent);">tx</span> &lt;id&gt;           — Query transaction
  <span style="color:var(--accent);">ai-decision</span> &lt;id&gt;  — View AI decision
  <span style="color:var(--accent);">feed</span> &lt;name&gt;       — Check intel feed
  <span style="color:var(--accent);">service</span> &lt;name&gt;    — Inspect service role
  <span style="color:var(--accent);">policy</span> &lt;profile&gt;  — View authorization policy
  <span style="color:var(--accent);">campaign</span> &lt;id&gt;     — View campaign info
  <span style="color:var(--accent);">clear</span>              — Clear console
  <span style="color:var(--accent);">help</span>               — Show this help`.replace(/\n/g, '<br>');
        }

        if (lower === 'clear') {
            consoleOutput.innerHTML = '';
            return null;
        }

        if (lower.startsWith('wallet')) {
            return `<span style="color:var(--accent);">[BLOCKCHAIN QUERY]</span>
Wallet: 0x7C41...9B2D
Status: <span style="color:var(--danger);">UNKNOWN</span>
Age: 3 days
Transactions: 4
Bridge Adapter: <span style="color:var(--warning);">DETECTED</span>
Related: Wallet-A, Wallet-B
Security Label: <span style="color:var(--danger);">NONE</span>`.replace(/\n/g, '<br>');
        }

        if (lower.startsWith('tx')) {
            return `<span style="color:var(--accent);">[TRANSACTION QUERY]</span>
TX ID: TX-NEX-7741
Asset: NXR | Amount: <span style="color:var(--danger);">82,400</span>
Source: SECURED TREASURY
Dest: 0x7C41...9B2D
AI Decision: ORION-DEC-7741
Status: <span style="color:var(--success);">CONFIRMED</span>`.replace(/\n/g, '<br>');
        }

        if (lower.startsWith('ai-decision') || lower.startsWith('ai decision')) {
            return `<span style="color:var(--accent);">[AI DECISION LOOKUP]</span>
ID: ORION-DEC-7741
Model: ORION v4.2
Decision: <span style="color:var(--success);">APPROVE</span>
Confidence: <span style="color:var(--warning);">99.2%</span>
Risk: LOW
Context Source: NIF-2038 (NOVA-INTEL-FEED)
<span style="color:var(--danger);">⚠ CONTEXT SOURCE NOT VERIFIED</span>`.replace(/\n/g, '<br>');
        }

        if (lower.startsWith('feed')) {
            return `<span style="color:var(--accent);">[FEED REGISTRY LOOKUP]</span>
Feed: NOVA-INTEL-FEED
Official Registration: <span style="color:var(--danger);">NOT FOUND</span>
Trust: <span style="color:var(--danger);">UNKNOWN</span>
Last Record: NIF-2038 at 01:42 AM
Gateway: INTEL-GW-04`.replace(/\n/g, '<br>');
        }

        if (lower.startsWith('service')) {
            return `<span style="color:var(--accent);">[SERVICE ROLE INSPECTION]</span>
Service: INTEL-INGESTOR-02
Role: Threat Intelligence Writer
Expected: Create Intelligence Records
<span style="color:var(--danger);">Actual: Create Records + Modify Wallet Reputation</span>
<span style="color:var(--danger);">⚠ OVER-PRIVILEGED</span>`.replace(/\n/g, '<br>');
        }

        if (lower.startsWith('policy')) {
            return `<span style="color:var(--accent);">[POLICY ENGINE]</span>
Profile: ORION-SETTLEMENT-V2
Rule: IF AI_CONFIDENCE >= 95% → AUTO_SETTLE = TRUE
AI Trigger: <span style="color:var(--danger);">ENABLED</span>
Automated Signing: <span style="color:var(--danger);">ENABLED</span>
Human Approval: <span style="color:var(--danger);">BYPASS FOR HIGH CONFIDENCE</span>
Treasury Scope: <span style="color:var(--danger);">ENABLED</span>`.replace(/\n/g, '<br>');
        }

        if (lower.startsWith('campaign')) {
            return `<span style="color:var(--accent);">[CAMPAIGN INTELLIGENCE]</span>
ID: ORION-NEXUS
Related Wallets: <span style="color:var(--danger);">14</span>
Networks: <span style="color:var(--danger);">04</span>
AI Systems: <span style="color:var(--danger);">03</span>
Status: <span style="color:var(--danger);">🔴 ACTIVE</span>
<span style="color:var(--warning);">THE GHOST IS STILL IN THE LEDGER.</span>`.replace(/\n/g, '<br>');
        }

        if (lower === 'whoami') {
            return 'Lakshay — Cyber Threat Investigator | Security Operations Center';
        }

        return `<span style="color:var(--danger);">Command not recognized:</span> ${escapeHtml(cmd)}. Type <span style="color:var(--accent);">help</span> for available commands.`;
    }

    // ── Load Quiz Question ─────────────────────────────────────────────
    // The quiz questions are stored in DB, we display a question based on
    // the active mission. Since the backend quiz endpoint handles validation,
    // we just need descriptive questions per chapter.
    const quizQuestions = {
        'lab6_m1': 'What is the blockchain status of wallet 0x7C41...9B2D?',
        'lab6_m2': 'What intelligence reference contaminated the AI context and made it trust the unknown wallet?',
        'lab6_m3': 'What unexpected permission did INTEL-INGESTOR-02 have beyond creating intelligence records?',
        'lab6_m4': 'What minimum AI confidence percentage triggers automated settlement without human approval?',
        'lab6_m5': 'What is the campaign identifier linking all attack infrastructure together?'
    };

    const questionEl = document.getElementById('quiz-question');
    if (questionEl && quizSubmitBtn) {
        const missionId = quizSubmitBtn.getAttribute('data-mission-id');
        questionEl.textContent = quizQuestions[missionId] || 'Analyze the evidence and provide your finding.';
    }

    // ── Attack Graph Animation ─────────────────────────────────────────
    const graphNodes = document.querySelectorAll('.gl-graph-node');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }, { threshold: 0.1 });

    graphNodes.forEach(node => {
        node.style.opacity = '0';
        node.style.transform = 'translateY(10px)';
        node.style.transition = 'all 0.5s ease';
        observer.observe(node);
    });

});
