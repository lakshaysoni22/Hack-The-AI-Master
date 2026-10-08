// proctoring.js - Advanced Anti-Cheat and Proctoring Mechanisms

document.addEventListener('DOMContentLoaded', () => {
    console.log("Proctoring & Anti-Cheat initialized.");
    
    // 1. Disable Copy, Paste, Cut, and Context Menu — except inside the
    // actual answer/flag submission fields. Learners are expected to find
    // a flag or a value (a cookie, a request header, etc.) elsewhere and
    // paste it in to submit it; blocking that everywhere breaks the core
    // task instead of preventing cheating.
    const isSubmissionField = (target) =>
        !!(target && target.closest && target.closest('input, textarea'));

    document.addEventListener('copy', (e) => {
        if (isSubmissionField(e.target)) return;
        e.preventDefault();
        showProctoringAlert("Copying is disabled during this session.");
    });
    
    document.addEventListener('paste', (e) => {
        if (isSubmissionField(e.target)) return;
        e.preventDefault();
        showProctoringAlert("Pasting is disabled during this session.");
    });
    
    document.addEventListener('cut', (e) => {
        if (isSubmissionField(e.target)) return;
        e.preventDefault();
        showProctoringAlert("Cutting is disabled during this session.");
    });
    
    document.addEventListener('contextmenu', (e) => {
        if (isSubmissionField(e.target)) return;
        e.preventDefault();
        showProctoringAlert("Right-click is disabled during this session.");
    });

    // 2. Tab Visibility & Focus Detection (Blackout/Badreading)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            logSuspiciousActivity("USER_SWITCHED_TABS");
            showProctoringAlert("Warning: Tab switching is strictly monitored. Please remain on this page.");
        }
    });

    window.addEventListener('blur', () => {
        logSuspiciousActivity("WINDOW_LOST_FOCUS");
    });

    // 3. Web Proctoring: Camera Activation
    const videoElement = document.getElementById('proctoring-video');
    if (videoElement) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then((stream) => {
                videoElement.srcObject = stream;
                console.log("Camera access granted.");
                logSuspiciousActivity("CAMERA_ACTIVATED");
            })
            .catch((error) => {
                console.error("Camera access denied or unavailable: ", error);
                showProctoringAlert("Camera access is required for this session. Please grant permission.");
                logSuspiciousActivity("CAMERA_DENIED");
            });
    }

    // CSS injection for user-select: none to prevent text selection
    const style = document.createElement('style');
    style.innerHTML = `
        .no-select {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
    `;
    document.head.appendChild(style);
    document.body.classList.add('no-select');
});

function showProctoringAlert(message) {
    // Attempt to use the platform's toast system if it exists
    if (typeof showToast === 'function') {
        showToast(message, 'error');
    } else {
        alert("Proctoring Alert: " + message);
    }
}

function logSuspiciousActivity(action) {
    console.log("Suspicious activity logged: ", action);
    // Send to backend
    fetch('/api/proctoring_alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': (typeof LAB_CONFIG !== 'undefined') ? LAB_CONFIG.csrfToken : ''
        },
        body: JSON.stringify({ action: action, timestamp: new Date().toISOString() })
    }).catch(err => console.error("Failed to log activity:", err));
}
