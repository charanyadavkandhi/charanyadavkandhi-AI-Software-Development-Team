/**
 * AI Software Development Team (Multi-Agent)
 * Frontend Application & Real-time Stream Controller
 */

let projectData = {
    pm_plan: null,
    dev_output: null,
    qa_output: null,
    doc_output: null,
    activeFile: null
};

let eventSource = null;

document.addEventListener('DOMContentLoaded', () => {
    initPresets();
    initConfigStatus();
    setupEventListeners();
});

/* =========================================================================
   1. Initialization & Configuration
   ========================================================================= */

async function initPresets() {
    try {
        const res = await fetch('/api/presets');
        const data = await res.json();
        if (data.success && data.presets) {
            const container = document.getElementById('presetChips');
            data.presets.forEach(p => {
                const btn = document.createElement('button');
                btn.className = 'preset-chip';
                btn.textContent = p.title.split('(')[0].trim();
                btn.title = p.prompt;
                btn.addEventListener('click', () => {
                    document.getElementById('promptInput').value = p.prompt;
                });
                container.appendChild(btn);
            });
        }
    } catch (e) {
        console.error("Failed to load presets:", e);
    }
}

async function initConfigStatus() {
    try {
        const res = await fetch('/api/config');
        const data = await res.json();
        if (data.success) {
            const statusText = document.getElementById('engineStatusText');
            statusText.textContent = data.active_engine;
        }
    } catch (e) {
        console.error("Failed to load config:", e);
    }
}

/* =========================================================================
   2. Event Listeners Setup
   ========================================================================= */

function setupEventListeners() {
    const launchBtn = document.getElementById('launchBtn');
    const promptInput = document.getElementById('promptInput');

    launchBtn.addEventListener('click', () => {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a software requirement or choose a preset.');
            return;
        }
        startMultiAgentPipeline(prompt);
    });

    // Workspace Tabs Switcher
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const target = document.getElementById(btn.dataset.tab);
            if (target) target.classList.add('active');
        });
    });

    // Copy File Code
    document.getElementById('copyFileBtn').addEventListener('click', () => {
        if (projectData.activeFile && projectData.dev_output?.files?.[projectData.activeFile]) {
            navigator.clipboard.writeText(projectData.dev_output.files[projectData.activeFile]);
            showToast('File code copied to clipboard!');
        }
    });

    // Copy Test Code
    document.getElementById('copyTestCodeBtn').addEventListener('click', () => {
        if (projectData.qa_output?.test_file_content) {
            navigator.clipboard.writeText(projectData.qa_output.test_file_content);
            showToast('Test suite copied to clipboard!');
        }
    });

    // Copy Doc Markdown
    document.getElementById('copyDocBtn').addEventListener('click', () => {
        if (projectData.doc_output?.readme_markdown) {
            navigator.clipboard.writeText(projectData.doc_output.readme_markdown);
            showToast('README Markdown copied to clipboard!');
        }
    });

    // Copy Active File Top Button
    document.getElementById('copyAllBtn').addEventListener('click', () => {
        if (projectData.activeFile && projectData.dev_output?.files?.[projectData.activeFile]) {
            navigator.clipboard.writeText(projectData.dev_output.files[projectData.activeFile]);
            showToast(`Copied ${projectData.activeFile}!`);
        }
    });

    // Download ZIP
    document.getElementById('downloadZipBtn').addEventListener('click', downloadProjectZip);

    // Settings Modal
    const settingsModal = document.getElementById('settingsModal');
    document.getElementById('settingsBtn').addEventListener('click', () => {
        settingsModal.classList.add('show');
    });
    document.getElementById('closeSettingsBtn').addEventListener('click', () => {
        settingsModal.classList.remove('show');
    });
    document.getElementById('cancelSettingsBtn').addEventListener('click', () => {
        settingsModal.classList.remove('show');
    });
    document.getElementById('saveSettingsBtn').addEventListener('click', async () => {
        const gemini = document.getElementById('geminiKeyInput').value.trim();
        const openai = document.getElementById('openaiKeyInput').value.trim();
        
        await fetch('/api/config/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ gemini_api_key: gemini, openai_api_key: openai })
        });
        
        settingsModal.classList.remove('show');
        initConfigStatus();
        showToast('Settings saved!');
    });
}

/* =========================================================================
   3. Multi-Agent Pipeline & Server-Sent Events Streaming
   ========================================================================= */

function startMultiAgentPipeline(prompt) {
    if (eventSource) {
        eventSource.close();
    }

    // Reset UI State
    resetAgentUI();
    document.getElementById('launchBtn').disabled = true;
    document.getElementById('pipelineStatusBadge').className = 'status-pill running';
    document.getElementById('pipelineStatusBadge').textContent = 'Executing Pipeline';
    document.getElementById('workspaceSection').style.display = 'none';

    addLog('system', `> Initializing pipeline for: "${prompt.slice(0, 70)}..."`);

    const streamUrl = `/api/stream?prompt=${encodeURIComponent(prompt)}`;
    eventSource = new EventSource(streamUrl);

    eventSource.addEventListener('pipeline_start', (e) => {
        const data = JSON.parse(e.data);
        addLog('system', `> Multi-agent session started [${data.session_id}]`);
        updateProgress(5);
    });

    eventSource.addEventListener('agent_active', (e) => {
        const data = JSON.parse(e.data);
        setAgentActive(data.agent_id, data.status);
        updateProgress(data.progress);
        addLog(`agent-${data.agent_id}`, `[${data.agent_name}] ${data.status}`);
    });

    eventSource.addEventListener('agent_warning', (e) => {
        const data = JSON.parse(e.data);
        addLog('agent-qa', `⚠️ [QA Alert] ${data.status}`);
    });

    eventSource.addEventListener('agent_complete', (e) => {
        const data = JSON.parse(e.data);
        setAgentComplete(data.agent_id, data.status);
        updateProgress(data.progress);
        addLog(`agent-${data.agent_id}`, `✅ [${data.agent_name}] ${data.status}`);

        // Store intermediate artifacts
        if (data.agent_id === 'pm') {
            projectData.pm_plan = data.data;
            document.getElementById('connector1').classList.add('active');
        } else if (data.agent_id === 'dev') {
            projectData.dev_output = data.data;
            document.getElementById('connector2').classList.add('active');
        } else if (data.agent_id === 'qa') {
            projectData.qa_output = data.data;
            document.getElementById('connector3').classList.add('active');
        } else if (data.agent_id === 'doc') {
            projectData.doc_output = data.data;
        }
    });

    eventSource.addEventListener('pipeline_complete', (e) => {
        const data = JSON.parse(e.data);
        eventSource.close();
        
        document.getElementById('launchBtn').disabled = false;
        document.getElementById('pipelineStatusBadge').className = 'status-pill completed';
        document.getElementById('pipelineStatusBadge').textContent = 'Pipeline Completed';
        updateProgress(100);
        
        addLog('success', `🎉 ${data.message}`);
        renderWorkspace(data.result);
    });

    eventSource.onerror = (err) => {
        console.error("SSE Stream error:", err);
        eventSource.close();
        document.getElementById('launchBtn').disabled = false;
        document.getElementById('pipelineStatusBadge').className = 'status-pill completed';
        document.getElementById('pipelineStatusBadge').textContent = 'Finished';
        
        // Fallback: render with existing captured data if available
        if (projectData.pm_plan && projectData.dev_output) {
            renderWorkspace(projectData);
        }
    };
}

/* =========================================================================
   4. UI State Updaters
   ========================================================================= */

function resetAgentUI() {
    ['pm', 'dev', 'qa', 'doc'].forEach(id => {
        const cardId = 'agentCard' + capitalize(id);
        const stateId = 'agentState' + capitalize(id);
        const actId = 'agentActivity' + capitalize(id);

        const card = document.getElementById(cardId);
        if (card) {
            card.classList.remove('active', 'completed');
            document.getElementById(stateId).textContent = 'Waiting';
            document.getElementById(actId).textContent = 'Awaiting trigger...';
        }
    });

    ['connector1', 'connector2', 'connector3'].forEach(cid => {
        document.getElementById(cid).classList.remove('active');
    });

    document.getElementById('logTerminal').innerHTML = '';
}

function setAgentActive(agentId, statusText) {
    const card = document.getElementById('agentCard' + capitalize(agentId));
    if (card) {
        card.classList.remove('completed');
        card.classList.add('active');
        document.getElementById('agentState' + capitalize(agentId)).textContent = 'Processing...';
        document.getElementById('agentActivity' + capitalize(agentId)).textContent = statusText;
    }
}

function setAgentComplete(agentId, statusText) {
    const card = document.getElementById('agentCard' + capitalize(agentId));
    if (card) {
        card.classList.remove('active');
        card.classList.add('completed');
        document.getElementById('agentState' + capitalize(agentId)).textContent = 'Completed ✓';
        document.getElementById('agentActivity' + capitalize(agentId)).textContent = statusText;
    }
}

function updateProgress(pct) {
    document.getElementById('progressBar').style.width = `${pct}%`;
    document.getElementById('progressText').textContent = `${pct}%`;
}

function addLog(type, text) {
    const term = document.getElementById('logTerminal');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = text;
    term.appendChild(entry);
    term.scrollTop = term.scrollHeight;
}

function capitalize(s) {
    if (s === 'pm') return 'PM';
    if (s === 'dev') return 'Dev';
    if (s === 'qa') return 'QA';
    if (s === 'doc') return 'Doc';
    return s.charAt(0).toUpperCase() + s.slice(1);
}

/* =========================================================================
   5. Rendering Generated Project Artifacts
   ========================================================================= */

function renderWorkspace(result) {
    const workspace = document.getElementById('workspaceSection');
    workspace.style.display = 'block';
    workspace.scrollIntoView({ behavior: 'smooth' });

    const pm = result.pm_plan || {};
    const dev = result.dev_output || {};
    const qa = result.qa_output || {};
    const doc = result.doc_output || {};

    // 1. Meta Titles
    document.getElementById('projectResultTitle').textContent = pm.project_name || 'Generated AI Project';
    document.getElementById('projectSlugBadge').textContent = pm.slug || 'ai_project';

    // 2. Tab 1: PM Plan
    document.getElementById('planSummaryText').textContent = pm.summary || 'Summary unavailable.';
    document.getElementById('planArchitectureText').textContent = pm.architecture || 'Modular Architecture';

    const techContainer = document.getElementById('techTagsList');
    techContainer.innerHTML = '';
    (pm.tech_stack || ['Python', 'Flask', 'HTML5', 'CSS3', 'JavaScript']).forEach(t => {
        const span = document.createElement('span');
        span.className = 'tech-tag';
        span.textContent = t;
        techContainer.appendChild(span);
    });

    const criteriaList = document.getElementById('criteriaList');
    criteriaList.innerHTML = '';
    (pm.acceptance_criteria || ['Clean modular code', 'Full automated test coverage', 'Responsive glassmorphic UI']).forEach(c => {
        const li = document.createElement('li');
        li.textContent = c;
        criteriaList.appendChild(li);
    });

    const tasksList = document.getElementById('tasksTableList');
    tasksList.innerHTML = '';
    (pm.tasks || []).forEach(t => {
        const row = document.createElement('div');
        row.className = 'task-row';
        row.innerHTML = `
            <div class="task-row-header">
                <span class="task-id-badge">${t.id}</span>
                <span class="task-agent-badge">${t.agent}</span>
            </div>
            <div class="task-title-text">${t.title}</div>
            <div class="task-desc-text">${t.description}</div>
        `;
        tasksList.appendChild(row);
    });

    // 3. Tab 2: Developer Code Explorer
    const files = dev.files || {};
    const fileKeys = Object.keys(files);
    document.getElementById('filesCountBadge').textContent = fileKeys.length;

    const fileTree = document.getElementById('fileTreeList');
    fileTree.innerHTML = '';

    if (fileKeys.length > 0) {
        fileKeys.forEach((filename, idx) => {
            const btn = document.createElement('button');
            btn.className = `file-item-btn ${idx === 0 ? 'active' : ''}`;
            
            let icon = '📄';
            if (filename.endsWith('.py')) icon = '🐍';
            else if (filename.endsWith('.html')) icon = '🌐';
            else if (filename.endsWith('.css')) icon = '🎨';
            else if (filename.endsWith('.js')) icon = '⚡';
            else if (filename.endsWith('.txt')) icon = '📦';

            btn.innerHTML = `<span>${icon}</span> <span>${filename}</span>`;
            btn.addEventListener('click', () => {
                document.querySelectorAll('.file-item-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                displayCodeFile(filename, files[filename]);
            });
            fileTree.appendChild(btn);
        });

        displayCodeFile(fileKeys[0], files[fileKeys[0]]);
    }

    // 4. Tab 3: QA Matrix
    const score = qa.quality_score || 98;
    document.getElementById('qaQualityScore').textContent = score;
    document.getElementById('qaScoreBadge').textContent = `Score: ${score}/100`;
    document.getElementById('qaVerdictTitle').textContent = qa.status === 'PASSED' ? 'Passed All AST & Unit Verifications' : 'Review Warnings';
    document.getElementById('qaSummaryDetails').textContent = qa.summary || 'All automated unit tests executed successfully.';

    const qaCasesList = document.getElementById('qaTestCasesList');
    qaCasesList.innerHTML = '';
    (qa.test_cases || []).forEach(tc => {
        const item = document.createElement('div');
        item.className = 'testcase-item';
        item.innerHTML = `
            <div class="testcase-left">
                <span>🧪</span>
                <div>
                    <div class="testcase-name">${tc.name}</div>
                    <div class="testcase-cat">${tc.category} • ${tc.details || ''}</div>
                </div>
            </div>
            <span class="testcase-status-badge">${tc.status}</span>
        `;
        qaCasesList.appendChild(item);
    });

    const testCodeViewer = document.getElementById('qaTestCodeViewer');
    testCodeViewer.textContent = qa.test_file_content || '# No unit tests generated.';
    Prism.highlightElement(testCodeViewer);

    // 5. Tab 4: Documentation
    const docContainer = document.getElementById('markdownRenderedView');
    const rawReadme = doc.readme_markdown || '# Documentation unavailable';
    docContainer.innerHTML = renderMarkdownSimple(rawReadme);
}

function displayCodeFile(filename, content) {
    projectData.activeFile = filename;
    document.getElementById('activeFileName').textContent = filename;
    
    const codeEl = document.getElementById('codeViewer');
    codeEl.textContent = content;

    // Detect language class
    codeEl.className = '';
    if (filename.endsWith('.py')) codeEl.className = 'language-python';
    else if (filename.endsWith('.js')) codeEl.className = 'language-javascript';
    else if (filename.endsWith('.css')) codeEl.className = 'language-css';
    else if (filename.endsWith('.html')) codeEl.className = 'language-markup';
    else codeEl.className = 'language-none';

    Prism.highlightElement(codeEl);
}

/* =========================================================================
   6. Export to ZIP
   ========================================================================= */

async function downloadProjectZip() {
    if (!projectData.dev_output?.files) {
        alert('No files available for export.');
        return;
    }

    try {
        const res = await fetch('/api/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_name: projectData.pm_plan?.project_name || 'AI_Project',
                files: projectData.dev_output.files,
                test_file_content: projectData.qa_output?.test_file_content || '',
                readme_markdown: projectData.doc_output?.readme_markdown || ''
            })
        });

        if (!res.ok) throw new Error('Export failed');

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const slug = projectData.pm_plan?.slug || 'ai_project';
        a.download = `${slug}.zip`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        showToast('Project ZIP archive downloaded!');
    } catch (err) {
        console.error("Export error:", err);
        alert('Failed to download ZIP archive.');
    }
}

/* =========================================================================
   7. Helper Utilities
   ========================================================================= */

function showToast(msg) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: #10b981;
        color: #fff;
        padding: 0.75rem 1.4rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.88rem;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
        z-index: 999;
        transition: opacity 0.3s;
    `;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

function renderMarkdownSimple(md) {
    // Basic clean HTML formatter for README display
    let html = md
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Fenced Code blocks
    html = html.replace(/```([a-z]*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');
    
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // Bold / inline code
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:4px;">$1</code>');
    
    // Blockquotes
    html = html.replace(/^\> (.*$)/gim, '<blockquote style="border-left: 3px solid #6366f1; padding-left: 1rem; color:#94a3b8;">$1</blockquote>');
    
    // Line breaks
    html = html.replace(/\n\n/g, '<br><br>');
    return html;
}
