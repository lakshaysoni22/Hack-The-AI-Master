// ============================================================
// TechCorp Lab controller
// ============================================================
let labTimerHandle = null;
let currentLabState = null;
let toastTimer = null;

function toggleTask(id) { const el = document.getElementById(id); if (el) el.classList.toggle('open'); }
function showHint(id) { const el = document.getElementById(id); if (el) el.classList.add('shown'); }
function fmtTime(total) {
  total = Math.max(0, Number(total) || 0);
  const h = Math.floor(total / 3600), m = Math.floor((total % 3600) / 60), s = total % 60;
  return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
}
function updateClock() {
  const now = new Date(); let h = now.getHours(); const m = String(now.getMinutes()).padStart(2,'0');
  const ampm = h >= 12 ? 'PM' : 'AM'; h = h % 12; if (!h) h = 12;
  const taskbarEl = document.getElementById('taskbar-clock'); if (taskbarEl) taskbarEl.textContent = `${h}:${m} ${ampm}`;
  const topbarEl = document.getElementById('topbar-clock');
  if (topbarEl) topbarEl.textContent = `${now.toLocaleDateString(undefined,{weekday:'short'})} ${now.toLocaleDateString(undefined,{month:'short'})} ${now.getDate()}, ${String(now.getHours()).padStart(2,'0')}:${m}`;
}
setInterval(updateClock, 15000);

async function startLab() {
  const btn = document.getElementById('start-lab-btn');
  if (btn) { btn.disabled = true; btn.textContent = 'Starting…'; }
  try {
    const res = await fetch('/api/start-lab', {method:'POST'}); const data = await res.json();
    document.getElementById('desktop-pane')?.classList.add('joined');
    startTimerLoop(); refreshState();
    if (btn) { btn.textContent = '● Lab Running'; btn.classList.remove('primary'); }
    notify('Lab started — live timer is now running.');
  } catch (e) { if (btn) { btn.disabled = false; btn.textContent = '▶ Start Lab'; } notify('Could not start the lab.'); }
}

// Backward-compatible join action: Join Lab now starts the actual timed lab.
function joinLab() { startLab(); }
function startTimerLoop() { if (labTimerHandle) return; labTimerHandle = setInterval(refreshState, 1000); }
function stopTimerLoop() { if (labTimerHandle) { clearInterval(labTimerHandle); labTimerHandle = null; } }

function openNextIncompleteTask(data) {
  const checks = [
    ['task-1', data.lab_status !== 'not_started'],
    ['task-2', data.logged_in],
    ['task-3', Number(data.mission || 1) >= 3],
    ['task-4', Number(data.mission || 1) >= 4],
    ['task-5', data.flag_captured],
    ['task-6', data.knowledge_check_passed],
    ['task-7', data.knowledge_check_passed]
  ];
  const next = checks.find(([_, done]) => !done);
  if (next) {
    const el = document.getElementById(next[0]);
    if (el && !el.classList.contains('open')) el.classList.add('open');
  }
}

function updateProgress(data) {
  const mission = Number(data.mission || 1);

  // Each UI task maps to a durable server-side state transition.
  const checks = {
    'task-check-1': data.lab_status !== 'not_started',
    'task-check-2': data.logged_in || mission >= 2,
    'task-check-3': mission >= 3,
    'task-check-4-a': mission >= 4,
    'task-check-4': data.flag_captured,
    'task-check-6': data.knowledge_check_passed,
    'task-check-final': data.knowledge_check_passed
  };

  Object.entries(checks).forEach(([id, done]) => {
    const el = document.getElementById(id);
    if (el) {
      el.classList.toggle('done', !!done);
      el.textContent = done ? '✓' : '';
      el.setAttribute('aria-label', done ? 'Completed' : 'Not completed');
    }
  });

  // Count the five actual missions, not the briefing/final UI wrappers.
  const completedMissions = [
    mission >= 2, // Mission 1: authentication
    mission >= 3, // Mission 2: portal mapping
    mission >= 4, // Mission 3: evidence
    data.flag_captured, // Mission 4: broken door
    data.knowledge_check_passed // Mission 5: explanation
  ].filter(Boolean).length;

  const countEl = document.getElementById('progress-count');
  if (countEl) countEl.textContent = `${completedMissions} / 5`;

  const bar = document.getElementById('progress-bar');
  if (bar) bar.style.width = `${completedMissions * 20}%`;

  const timer = document.getElementById('lab-timer');
  if (timer) timer.textContent = fmtTime(data.elapsed_seconds);

  const status = document.getElementById('lab-status');
  if (status) {
    status.textContent = data.lab_status === 'completed'
      ? '● COMPLETED'
      : data.lab_status === 'running'
        ? '● LIVE / RUNNING'
        : '● NOT STARTED';
    status.className = `timer-status ${data.lab_status}`;
  }

  const btn = document.getElementById('start-lab-btn');
  if (btn && data.lab_status === 'completed') {
    btn.disabled = false;
    btn.textContent = '✓ Lab Completed';
  } else if (btn && data.lab_status === 'running') {
    btn.disabled = true;
    btn.textContent = '● Lab Running';
  }

  if (data.lab_status === 'completed') {
    stopTimerLoop();
    const ct = document.getElementById('completion-time');
    if (ct) ct.textContent = fmtTime(data.elapsed_seconds);
    const banner = document.getElementById('completion-banner');
    if (banner) banner.style.display = 'block';
  }

  // Keep the learner oriented after a refresh/navigation.
  openNextIncompleteTask(data);
}

function toggleAppsMenu(e){e.stopPropagation();document.getElementById('apps-dropdown')?.classList.toggle('open');}
function closeAppsMenu(){document.getElementById('apps-dropdown')?.classList.remove('open');}
document.addEventListener('click',closeAppsMenu);
function notify(message){const el=document.getElementById('toast');if(!el)return;el.textContent=message;el.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('show'),3200);}

const browserWin=document.getElementById('browser-window');
const browserFrame=document.getElementById('browser-frame');
const browserAddress=document.getElementById('browser-address');
const browserTaskbarBtn=document.getElementById('taskbar-browser');
const terminalWin=document.getElementById('terminal-window');
const terminalTaskbarBtn=document.getElementById('taskbar-terminal');
function requireLab(){ if(currentLabState?.lab_status !== 'running' && currentLabState?.lab_status !== 'completed'){notify('Start the lab first.');return false;} return true; }
function navigateBrowser(path){if(browserFrame)browserFrame.src=path;}
function openBrowser(path){if(!requireLab())return;browserWin.classList.add('open');browserTaskbarBtn.classList.add('visible','active');bringToFront(browserWin);if(path)navigateBrowser(path);else if(!browserFrame.src||browserFrame.src==='about:blank')navigateBrowser('/login');}
function closeBrowser(){browserWin.classList.remove('open');browserTaskbarBtn.classList.remove('visible','active');}
function minimizeBrowser(){browserWin.classList.remove('open');browserTaskbarBtn.classList.remove('active');}
function reloadBrowser(){try{browserFrame.contentWindow.location.reload();}catch(e){}}
function browserBack(){try{browserFrame.contentWindow.history.back();}catch(e){}}
function browserForward(){try{browserFrame.contentWindow.history.forward();}catch(e){}}
function bringToFront(win){document.querySelectorAll('.browser-window,.terminal-window,.hidden-folder-window').forEach(w=>w.style.zIndex=20);win.style.zIndex=30;}
browserFrame?.addEventListener('load',()=>{try{browserAddress.textContent='127.0.0.1:5000'+browserFrame.contentWindow.location.pathname;}catch(e){browserAddress.textContent='127.0.0.1:5000';}refreshState();});
function openTerminal(){if(!requireLab())return;terminalWin.classList.add('open');terminalTaskbarBtn.classList.add('visible','active');bringToFront(terminalWin);setTimeout(()=>document.getElementById('terminal-input')?.focus(),50);}
function closeTerminal(){terminalWin.classList.remove('open');terminalTaskbarBtn.classList.remove('visible','active');}
function minimizeTerminal(){terminalWin.classList.remove('open');terminalTaskbarBtn.classList.remove('active');}
function openFolder(id){const el=document.getElementById(id);if(el){el.classList.add('open');bringToFront(el);}}
function closeWindow(id){document.getElementById(id)?.classList.remove('open');}
function minimizeWindow(id){document.getElementById(id)?.classList.remove('open');}

const fileContents={
 'notes.txt':'Employee portal investigation\nCheck access permissions.\nRemember: authentication and authorization are separate.',
 'access-review.txt':'ACCESS REVIEW\n\nEmployee: Alex Turner\nExpected: Dashboard + Profile\nRestricted: Team Management + Admin Panel\n\nInvestigate how the server makes the authorization decision.',
 'employee-notes.txt':'Sarah asked Alex to verify whether restricted resources are protected by a trusted server-side role.'
};
function openFile(name){const preview=document.getElementById('file-preview');if(preview)preview.textContent=fileContents[name]||'File is empty.';}
function openNotes(){if(!requireLab())return;const w=document.getElementById('notes-window');w.classList.add('open');bringToFront(w);const saved=localStorage.getItem('techcorp-lab-notes');if(saved!==null)document.getElementById('notes-editor').value=saved;}
function saveNotes(){localStorage.setItem('techcorp-lab-notes',document.getElementById('notes-editor').value);document.getElementById('notes-saved').textContent='Saved';setTimeout(()=>document.getElementById('notes-saved').textContent='',1200);}

const commandHelp='help — show commands\nwhoami — show current analyst\npwd — show current directory\nls — list files\ncat <file> — read a lab file\nclear — clear terminal\ncurl <path> — simulated HTTP status for the lab';
function terminalPrint(text){const out=document.getElementById('terminal-output');out.innerHTML+=`\n${text}\n<span class="terminal-prompt">alex@techcorp-analyst:~$</span> <input id="terminal-input" autocomplete="off" spellcheck="false" onkeydown="handleTerminalKey(event)">`;const input=document.getElementById('terminal-input');input.focus();out.scrollTop=out.scrollHeight;}
function handleTerminalKey(e){if(e.key!=='Enter')return;const input=e.target;const cmd=input.value.trim();input.remove();const safe=cmd.toLowerCase();if(safe==='clear'){document.getElementById('terminal-output').innerHTML='Terminal cleared.\n<span class="terminal-prompt">alex@techcorp-analyst:~$</span> <input id="terminal-input" autocomplete="off" spellcheck="false" onkeydown="handleTerminalKey(event)">';document.getElementById('terminal-input').focus();return;}let result='Command not found. Type help for available commands.';if(safe==='help')result=commandHelp;else if(safe==='whoami')result='alex';else if(safe==='pwd')result='/home/alex';else if(safe==='ls')result='Desktop  Documents  notes.txt  access-review.txt  employee-notes.txt';else if(safe.startsWith('cat ')){const name=cmd.slice(4).trim();result=fileContents[name]||'cat: file not found';}else if(safe==='curl /dashboard')result='HTTP/1.1 200 OK';else if(safe==='curl /admin')result='HTTP/1.1 403 FORBIDDEN (until the lab authorization flaw is demonstrated)';terminalPrint(result);}

async function refreshState(){try{const res=await fetch('/api/state');const data=await res.json();currentLabState=data;const el=document.getElementById('session-indicator');if(el)el.textContent=data.logged_in?`Logged in as ${data.username} (${data.role})`:'Not logged in';if(data.lab_status==='running'||data.lab_status==='completed')document.getElementById('desktop-pane')?.classList.add('joined');updateProgress(data);if(data.lab_status==='running')startTimerLoop();else if(data.lab_status==='completed')stopTimerLoop();}catch(e){}}

let flagCheckInProgress = false;

async function submitFlag() {
  const input = document.getElementById('flag-input');
  const feedback = document.getElementById('flag-feedback');
  const button = document.querySelector('#flag-input + .check-btn');
  if (!input || !feedback || flagCheckInProgress) return;

  const flag = input.value.trim();
  if (!flag) {
    feedback.className = 'answer-feedback show incorrect';
    feedback.textContent = '❌ Enter a flag first.';
    input.focus();
    return;
  }

  flagCheckInProgress = true;
  if (button) {
    button.disabled = true;
    button.textContent = 'Checking…';
  }

  try {
    const res = await fetch('/api/submit-flag', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({flag})
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    feedback.className = `answer-feedback show ${data.correct ? 'correct' : 'incorrect'}`;
    feedback.textContent = data.correct
      ? '✅ Correct! You confirmed the broken access control vulnerability.'
      : `❌ ${data.message || 'Incorrect flag.'}`;

    // Always refresh state so the ticks/progress stay synchronized.
    await refreshState();
  } catch (e) {
    feedback.className = 'answer-feedback show incorrect';
    feedback.textContent = '⚠️ Could not validate the flag. Check that the lab server is running.';
  } finally {
    flagCheckInProgress = false;
    if (button) {
      button.disabled = false;
      button.textContent = 'Check';
    }
  }
}
let knowledgeCheckInProgress = false;

async function submitKnowledgeCheck() {
  const feedback = document.getElementById('kc-feedback');
  const button = document.querySelector('#task-7 .check-btn');
  if (!feedback || knowledgeCheckInProgress) return;

  knowledgeCheckInProgress = true;
  if (button) {
    button.disabled = true;
    button.textContent = 'Checking…';
  }

  try {
    const res = await fetch('/api/knowledge-check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        auth_answer: document.getElementById('kc-auth').value,
        authz_answer: document.getElementById('kc-authz').value,
        summary: document.getElementById('kc-summary').value
      })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    feedback.classList.remove('correct', 'incorrect');
    feedback.classList.add('show', data.passed ? 'correct' : 'incorrect');

    if (data.passed) {
      feedback.textContent = '✅ Correct! Lab completed.';
    } else {
      let msg = '❌ Not quite there yet. ';
      if (!data.auth_ok) msg += 'Reconsider authentication (identity). ';
      if (!data.authz_ok) msg += 'Reconsider authorization (permissions/access). ';
      if (!data.summary_ok) msg += 'Add more detail to the summary. ';
      if (!data.flag_captured) msg += 'Capture the flag before the final check.';
      feedback.textContent = msg.trim();
    }

    // Synchronize every checkmark after every attempt.
    await refreshState();
  } catch (e) {
    feedback.className = 'answer-feedback show incorrect';
    feedback.textContent = '⚠️ Could not validate the answer. Check that the lab server is running.';
  } finally {
    knowledgeCheckInProgress = false;
    if (button) {
      button.disabled = false;
      button.textContent = 'Submit Answer';
    }
  }
}

async function resetLab(){if(!confirm('Reset the lab to its original state? This clears your progress, timer and login.'))return;await fetch('/lab/reset',{method:'POST'});stopTimerLoop();closeBrowser();closeTerminal();document.querySelectorAll('.task-check.done').forEach(el=>{el.classList.remove('done');el.textContent='';});document.getElementById('completion-banner').style.display='none';document.querySelectorAll('.answer-feedback').forEach(el=>el.classList.remove('show','correct','incorrect'));const btn=document.getElementById('start-lab-btn');btn.disabled=false;btn.textContent='▶ Start Lab';btn.classList.add('primary');currentLabState=null;refreshState();}

document.addEventListener('DOMContentLoaded',()=>{updateClock();refreshState();document.getElementById('task-1')?.classList.add('open');});
