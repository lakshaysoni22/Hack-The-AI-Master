/**
 * Lab Engine Client - Redesigned UI
 */

(function () {
    'use strict';

    let sessionId = null;
    let targetUrl = null;
    let labData = null;
    let timerInterval = null;
    let elapsedSeconds = 0;
    let hintsRevealed = {}; 
    let answeredQuestions = {}; 

    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    document.addEventListener('DOMContentLoaded', () => {
        initPanelResize();
        startLabSession();
    });

    // The task/flag panel is now a permanently-visible sidebar rather than
    // a hidden drawer, so "Tasks & Flag" just scrolls it into focus and
    // draws attention to the flag box instead of toggling visibility.
    window.toggleTaskPanel = function () {
        const panel = $('#panel-left');
        const flagBox = $('#lab-flag-box');
        if (!panel) return;
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (flagBox) {
            flagBox.classList.add('flag-box-highlight');
            setTimeout(() => flagBox.classList.remove('flag-box-highlight'), 1500);
        }
    };

    function showCompletionModal(points) {
        const pointsEl = $('#completion-points');
        if (pointsEl) pointsEl.textContent = points;
        const modal = $('#completion-modal');
        if (modal) modal.classList.add('open');
        const btn = $('#btn-lab-completed');
        if (btn) btn.disabled = false;
    }

    async function startLabSession() {
        $('#loading-status').textContent = 'Creating lab session...';
        try {
            const res = await apiPost('/api/lab-engine/start', { lab_id: LAB_CONFIG.labId });
            if (!res.success) {
                showError(res.message || 'Failed to start lab session.');
                return;
            }
            sessionId = res.session_id;
            targetUrl = res.target_url;

            $('#loading-status').textContent = 'Loading lab progress...';
            await loadProgress();

            startTimer();
            loadTargetEnvironment();

            $('#lab-loading').style.display = 'none';
            $('#lab-content').style.display = 'block';

            $('#live-status-badge').innerHTML = '<span class="dot active"></span> ACTIVE';
            $('#machine-ip-text').textContent = targetUrl ? targetUrl.replace(/^https?:\/\//, '') : 'None';

        } catch (err) {
            console.error(err);
            showError('Network error. Please try again.');
        }
    }

    window.stopSession = async function() {
        if (!sessionId) return;
        if (!confirm('Restart this lab? Your session will be reset.')) return;
        try {
            await apiPost('/api/lab-engine/stop', { session_id: sessionId });
        } catch (e) { }
        window.location.reload();
    };

    async function loadProgress() {
        const res = await apiPost('/api/lab-engine/progress', { session_id: sessionId });
        if (!res.success) return;
        labData = res;

        $('#investigation-fraction').textContent = `${res.missions_completed}/${res.missions_total}`;
        const pct = res.missions_total ? (res.missions_completed / res.missions_total) * 100 : 0;
        $('#investigation-fill').style.width = `${pct}%`;

        if (res.missions_completed === res.missions_total && res.missions_total > 0) {
            $('#btn-lab-completed').disabled = false;
        }

        buildAccordions(res.missions);
        updateFlagBox(res.status);
    }

    // The flag box isn't tied to any single mission (the platform stores
    // flags per-lab, not per-mission), so it's shown/hidden based on the
    // session's overall status rather than any one mission's state.
    function updateFlagBox(status) {
        const box = $('#lab-flag-box');
        if (!box) return;
        if (status === 'COMPLETED') {
            box.style.display = 'block';
            const input = $('#lab-flag-input');
            const btn = $('#btn-lab-flag');
            if (input) { input.disabled = true; input.value = '✓ Captured'; }
            if (btn) { btn.disabled = true; btn.textContent = 'Captured'; }
        } else {
            box.style.display = 'block';
        }
    }

    window.submitLabFlag = async function () {
        const input = $('#lab-flag-input');
        const feedback = $('#lab-flag-feedback');
        const btn = $('#btn-lab-flag');
        if (!input || !feedback) return;
        const val = input.value.trim();
        if (!val) return;

        btn.disabled = true;
        btn.textContent = 'Checking…';
        try {
            const res = await apiPost('/api/lab-engine/submit-flag', {
                session_id: sessionId, flag: val
            });
            feedback.style.display = 'block';
            if (res.correct) {
                feedback.className = 'q-feedback correct';
                feedback.textContent = 'Flag accepted!';
                input.disabled = true;
                btn.textContent = 'Captured';
                await loadProgress();
                showCompletionModal(res.xp || 0);
            } else {
                feedback.className = 'q-feedback incorrect';
                feedback.textContent = res.message || 'Incorrect flag.';
                btn.disabled = false;
                btn.textContent = 'Submit Flag';
            }
        } catch (e) {
            feedback.style.display = 'block';
            feedback.className = 'q-feedback incorrect';
            feedback.textContent = e && e.isSessionExpired
                ? 'Your session timed out. Please refresh the page (your progress is saved) and submit the flag again.'
                : 'Could not reach the server. Check your connection and try again.';
            btn.disabled = false;
            btn.textContent = 'Submit Flag';
        }
    };

    function buildAccordions(missions) {
        const container = $('#mission-accordions');
        container.innerHTML = '';

        missions.forEach((mission, index) => {
            const isCompleted = mission.status === 'COMPLETED';
            const isAvailable = mission.status === 'AVAILABLE' || mission.status === 'IN_PROGRESS';
            
            const acc = document.createElement('div');
            acc.className = `task-accordion ${isAvailable ? 'active' : ''} ${isCompleted ? 'completed' : ''}`;
            
            let icon = isCompleted ? '✓' : '▶';
            
            acc.innerHTML = `
                <div class="task-header" onclick="toggleTask(this)">
                    <div class="task-title-area">
                        <span class="task-num">TASK ${index + 1}</span>
                        <span class="task-name">${mission.title}</span>
                    </div>
                    <div class="task-status-icon ${isCompleted ? 'checked' : ''}">${icon}</div>
                </div>
                <div class="task-body" style="display: ${isAvailable ? 'block' : 'none'}">
                    ${mission.storyline_text ? `<p class="task-story">${mission.storyline_text}</p>` : ''}
                    ${mission.objective ? `<div class="task-obj"><strong>Objective:</strong> ${mission.objective}</div>` : ''}
                    
                    ${mission.instructions && mission.instructions.length > 0 ? 
                        `<ul class="task-inst">${mission.instructions.map(i => `<li>${i}</li>`).join('')}</ul>` 
                        : ''}
                    
                    ${buildQuestionsHtml(mission)}
                    ${buildFlagHtml(mission, isCompleted)}
                </div>
            `;
            container.appendChild(acc);
        });
    }

    window.toggleTask = function(headerElem) {
        const body = headerElem.nextElementSibling;
        const isHidden = body.style.display === 'none';
        
        $$('.task-body').forEach(b => b.style.display = 'none');
        $$('.task-accordion').forEach(a => a.classList.remove('active'));
        
        if (isHidden) {
            body.style.display = 'block';
            headerElem.parentElement.classList.add('active');
        }
    };

    function buildQuestionsHtml(mission) {
        if (!mission.questions || mission.questions.length === 0) return '';
        let html = '<div class="task-questions">';
        mission.questions.forEach(q => {
            const isAns = answeredQuestions[q.question_id];
            html += `
                <div class="t-question" id="q-${q.question_id}">
                    <p>${q.question_text}</p>
                    <div class="t-q-input">
                        <input type="text" id="ans-${q.question_id}" placeholder="Answer..." ${isAns ? 'disabled' : ''}>
                        <button class="btn ${isAns ? 'btn-success' : 'btn-gray'}" ${isAns ? 'disabled' : ''} onclick="submitAnswer('${q.question_id}', '${mission.mission_id}')">
                            ${isAns ? '✓' : 'Submit'}
                        </button>
                    </div>
                    <div class="q-feedback" id="fb-${q.question_id}" style="display:none"></div>
                </div>
            `;
        });
        html += '</div>';
        return html;
    }

    function buildFlagHtml(mission, isCompleted) {
        if (!mission.flag_id) return '';
        if (isCompleted) {
            return `<div class="task-flag-area"><div class="alert alert-success">Mission Completed! ✓</div></div>`;
        }
        return `
            <div class="task-flag-area">
                <input type="text" id="flag-${mission.mission_id}" class="flag-input" placeholder="FLAG{...}">
                <button class="btn btn-primary" id="btn-flag-${mission.mission_id}" onclick="submitFlag('${mission.mission_id}')">Submit Flag</button>
                <div id="fb-flag-${mission.mission_id}" style="display:none;" class="q-feedback"></div>
            </div>
        `;
    }

    window.submitAnswer = async function(qId, mId) {
        const val = $(`#ans-${qId}`).value.trim();
        if(!val) return;
        try {
            const res = await apiPost('/api/lab-engine/submit-answer', {
                session_id: sessionId, mission_id: mId, question_id: qId, answer: val
            });
            const fb = $(`#fb-${qId}`);
            fb.style.display = 'block';
            if(res.correct) {
                fb.className = 'q-feedback correct';
                fb.textContent = 'Correct!';
                answeredQuestions[qId] = true;
                await loadProgress();
            } else {
                fb.className = 'q-feedback incorrect';
                fb.textContent = 'Incorrect.';
            }
        } catch(e) {
            fb.style.display = 'block';
            fb.className = 'q-feedback incorrect';
            fb.textContent = e && e.isSessionExpired
                ? 'Your session timed out. Please refresh the page and try again.'
                : 'Could not reach the server. Try again.';
        }
    };

    window.submitFlag = async function(mId) {
        const val = $(`#flag-${mId}`).value.trim();
        if(!val) return;
        try {
            const res = await apiPost('/api/lab-engine/submit-flag', {
                session_id: sessionId, mission_id: mId, flag: val
            });
            const fb = $(`#fb-flag-${mId}`);
            fb.style.display = 'block';
            if(res.correct) {
                fb.className = 'q-feedback correct';
                fb.textContent = 'Flag Accepted!';
                await loadProgress();
                showCompletionModal(res.xp || 0);
            } else {
                fb.className = 'q-feedback incorrect';
                fb.textContent = 'Incorrect Flag.';
            }
        } catch(e) {
            fb.style.display = 'block';
            fb.className = 'q-feedback incorrect';
            fb.textContent = e && e.isSessionExpired
                ? 'Your session timed out. Please refresh the page and try again.'
                : 'Could not reach the server. Try again.';
        }
    };

    function startTimer() {
        if(timerInterval) clearInterval(timerInterval);
        const startTime = labData ? new Date(labData.start_time).getTime() : Date.now();
        timerInterval = setInterval(() => {
            const now = Date.now();
            elapsedSeconds = Math.floor((now - startTime) / 1000);
            
            const h = String(Math.floor(elapsedSeconds / 3600)).padStart(2, '0');
            const m = String(Math.floor((elapsedSeconds % 3600) / 60)).padStart(2, '0');
            const s = String(elapsedSeconds % 60).padStart(2, '0');
            
            $('#timer-display').textContent = `${h}:${m}:${s}`;
        }, 1000);
    }

    function loadTargetEnvironment() {
        if (!targetUrl) {
            $('#target-loading').style.display = 'none';
            $('#target-unavailable').style.display = 'flex';
            return;
        }

        const iframe = $('#target-iframe');
        iframe.src = targetUrl;
        
        $('#virtual-browser').style.display = 'flex';
        $('#target-url-display').textContent = targetUrl;
        $('#target-loading').style.display = 'none';
    }

    function initPanelResize() {
        const divider = $('#panel-divider');
        const leftPanel = $('#panel-left');
        let isResizing = false;

        divider.addEventListener('mousedown', (e) => {
            isResizing = true;
            document.body.style.cursor = 'col-resize';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const newWidth = (e.clientX / window.innerWidth) * 100;
            if (newWidth > 20 && newWidth < 80) {
                leftPanel.style.flex = `0 0 ${newWidth}%`;
            }
        });

        document.addEventListener('mouseup', () => {
            if (isResizing) {
                isResizing = false;
                document.body.style.cursor = 'default';
            }
        });
    }

    async function apiPost(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': LAB_CONFIG.csrfToken
            },
            body: JSON.stringify(data)
        });

        // A failed CSRF check (e.g. a stale token on a page left open a
        // while) or a server error comes back as an HTML page, not JSON.
        // Parsing that as JSON throws a confusing, unrelated-looking error,
        // so detect it explicitly and say what's actually going on instead
        // of letting the caller's catch block blame the wrong thing (like
        // making a correct flag look "invalid").
        const contentType = response.headers.get('content-type') || '';
        if (!contentType.includes('application/json')) {
            const err = new Error('SESSION_EXPIRED');
            err.isSessionExpired = true;
            err.status = response.status;
            throw err;
        }

        return await response.json();
    }

    function showError(msg) {
        const el = $('#lab-loading');
        el.innerHTML = `<div class="alert alert-danger">${msg}</div>`;
    }

})();
