document.addEventListener('DOMContentLoaded', () => {
    // Terminal logic (Simulated)
    const termInput = document.getElementById('terminal-input');
    if (termInput) {
        termInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const val = this.value.trim();
                const output = document.getElementById('terminal-output');
                
                // Echo command
                const cmdLine = document.createElement('div');
                cmdLine.className = 'term-line';
                cmdLine.innerHTML = `<span class="term-prompt">student@hacktheai:~$</span> ${val}`;
                
                // Insert before the input line
                this.parentElement.before(cmdLine);
                
                // Process command
                if (val !== '') {
                    const resLine = document.createElement('div');
                    resLine.className = 'term-line';
                    
                    if (val === 'help') {
                        resLine.innerText = "Available commands: help, ls, clear, whoami, ping";
                    } else if (val === 'clear') {
                        const lines = output.querySelectorAll('.term-line');
                        lines.forEach(l => {
                            if (l !== this.parentElement) l.remove();
                        });
                        this.value = '';
                        return;
                    } else if (val === 'whoami') {
                        resLine.innerText = "student";
                    } else if (val.startsWith('ping')) {
                        resLine.innerText = "PING target.techcorp.local (10.0.0.5) 56(84) bytes of data.\n64 bytes from 10.0.0.5: icmp_seq=1 ttl=64 time=0.034 ms";
                        resLine.style.whiteSpace = 'pre-line';
                    } else if (val === 'ls') {
                        resLine.innerText = "tools  exploits  notes.txt";
                    } else {
                        resLine.innerText = `bash: ${val}: command not found`;
                    }
                    this.parentElement.before(resLine);
                }
                
                this.value = '';
                output.scrollTop = output.scrollHeight;
            }
        });
        
        // Keep focus when clicking on terminal panel
        const termPanel = document.getElementById('panel-terminal');
        if (termPanel) {
            termPanel.addEventListener('click', () => {
                termInput.focus();
            });
        }
    }

    // Flag Submission
    const flagBtn = document.getElementById('submit-flag-btn');
    const flagInput = document.getElementById('flag-input');
    
    if (flagBtn && flagInput) {
        flagBtn.addEventListener('click', async () => {
            const labId = flagBtn.getAttribute('data-lab-id');
            const flag = flagInput.value.trim();
            
            if (!flag) {
                window.showToast('Please enter a flag.', 'warning');
                return;
            }
            
            const originalText = flagBtn.innerText;
            flagBtn.innerText = 'Submitting...';
            flagBtn.disabled = true;
            
            const result = await window.apiCall('/api/flag', { lab_id: labId, flag: flag }, window.csrfToken);
            
            if (result.success) {
                window.showToast(result.message || 'Flag Captured!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                window.showToast(result.message || 'Incorrect flag.', 'error');
            }
            
            flagBtn.innerText = originalText;
            flagBtn.disabled = false;
        });
    }

    // Quiz Options
    const quizOptions = document.querySelectorAll('.quiz-option');
    quizOptions.forEach(btn => {
        btn.addEventListener('click', async () => {
            const answer = btn.getAttribute('data-answer');
            const labId = btn.getAttribute('data-lab-id');
            const missionId = btn.getAttribute('data-mission-id');
            
            const result = await window.apiCall('/api/quiz', { lab_id: labId, mission_id: missionId, answer: answer }, window.csrfToken);
            
            if (result.success) {
                window.showToast(result.message || 'Correct answer!', 'success');
                btn.classList.remove('btn-secondary');
                btn.classList.add('btn-primary');
                
                // Disable all options
                quizOptions.forEach(b => b.disabled = true);
            } else {
                window.showToast(result.message || 'Incorrect answer.', 'error');
                btn.style.borderColor = 'var(--danger)';
            }
        });
    });
});
