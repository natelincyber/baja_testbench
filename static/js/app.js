// Main application logic
document.addEventListener('DOMContentLoaded', () => {
    // Initialize health monitoring
    healthMonitor.init();

    // Output type switching
    document.querySelectorAll('.output-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-type');
            
            // Update button states
            document.querySelectorAll('.output-type-btn').forEach(b => {
                b.classList.remove('active');
            });
            btn.classList.add('active');

            // Update panel visibility
            document.querySelectorAll('.output-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            document.getElementById(`output-${type}`).classList.add('active');
        });
    });
});

// Test execution functions
function runTest(testId) {
    const progressEl = document.getElementById(`test-${testId}-progress`);
    const progressFill = progressEl.querySelector('.progress-fill');
    
    // Show progress
    progressEl.style.display = 'block';
    progressFill.style.width = '0%';

    // Simulate test progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            addLog(`[${new Date().toLocaleTimeString()}] [INFO] Test ${testId} completed.`);
        }
        progressFill.style.width = `${progress}%`;
    }, 500);

    addLog(`[${new Date().toLocaleTimeString()}] [INFO] Starting test: ${testId}`);
    
    // TODO: Replace with actual API call
    // fetch(`/api/v1/tests/${testId}/run`, { method: 'POST' })
    //     .then(response => response.json())
    //     .then(data => {
    //         clearInterval(interval);
    //         progressFill.style.width = '100%';
    //         addLog(`[${new Date().toLocaleTimeString()}] [INFO] Test ${testId} completed.`);
    //     });
}

function viewTestDetails(testId) {
    addLog(`[${new Date().toLocaleTimeString()}] [INFO] Viewing details for test: ${testId}`);
    // TODO: Implement test details view
}

// Log management
function addLog(message, level = 'info') {
    const logViewer = document.getElementById('log-viewer');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    const time = new Date().toLocaleTimeString();
    logEntry.innerHTML = `
        <span class="log-time">[${time}]</span>
        <span class="log-level ${level}">[${level.toUpperCase()}]</span>
        <span class="log-message">${message}</span>
    `;
    
    logViewer.appendChild(logEntry);
    logViewer.scrollTop = logViewer.scrollHeight;
}

function clearLogs() {
    const logViewer = document.getElementById('log-viewer');
    logViewer.innerHTML = '';
    addLog('Logs cleared.');
}

function exportLogs() {
    const logs = Array.from(document.querySelectorAll('.log-entry')).map(entry => {
        return entry.textContent;
    }).join('\n');
    
    const blob = new Blob([logs], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-logs-${new Date().toISOString()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    
    addLog('Logs exported.');
}

function refreshMetrics() {
    addLog('Refreshing metrics...');
    // TODO: Implement metrics refresh
}

function generateReport() {
    addLog('Generating test report...');
    // TODO: Implement report generation
}

