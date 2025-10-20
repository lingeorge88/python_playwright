/**
 * Amazon Product Search - Client-Side JavaScript
 * Author: George Lin
 * City of Los Angeles GSD Evaluation Program
 */

// DOM Element References
const searchForm = document.getElementById('searchForm');
const searchBtn = document.getElementById('searchBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultCard = document.getElementById('resultCard');
const resultTitle = document.getElementById('resultTitle');
const resultContent = document.getElementById('resultContent');
const logsContainer = document.getElementById('logsContainer');
const logsContent = document.getElementById('logsContent');
const clearLogsBtn = document.getElementById('clearLogs');
const rateLimitWarning = document.getElementById('rateLimitWarning');
const rateLimitTime = document.getElementById('rateLimitTime');

// Rate limit configuration (must match backend)
const RATE_LIMIT_SECONDS = 15;

/**
 * Handle form submission
 */
searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const searchTerm = document.getElementById('searchTerm').value.trim();
    const headless = document.getElementById('headlessMode').checked;

    if (!searchTerm) {
        showError('Please enter a search term');
        return;
    }

    // Reset UI
    resetUI();

    // Show loading state
    loadingSpinner.style.display = 'block';
    searchBtn.disabled = true;
    searchBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Searching...';

    // Show logs container
    logsContainer.style.display = 'block';
    addLog('Sending request to server...');

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                search_term: searchTerm,
                headless: headless
            })
        });

        const data = await response.json();

        // Display logs from backend
        if (data.logs && data.logs.length > 0) {
            data.logs.forEach(log => addLog(log));
        }

        // Display result
        if (data.success) {
            showSuccess(data.product_name, data.price);
        } else {
            showError(data.error);
        }

        // Show rate limit warning with countdown
        showRateLimitWarning();

    } catch (error) {
        addLog(`Error: ${error.message}`);
        showError(`Failed to connect to server: ${error.message}`);
    } finally {
        // Reset button state
        loadingSpinner.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.innerHTML = '<i class="bi bi-play-circle"></i> Start Search';
    }
});

/**
 * Clear logs button handler
 */
clearLogsBtn.addEventListener('click', () => {
    logsContent.innerHTML = '';
});

/**
 * Reset UI to initial state
 */
function resetUI() {
    resultCard.style.display = 'none';
    resultCard.className = 'result-card';
    logsContent.innerHTML = '';
}

/**
 * Add a log entry to the logs container
 * @param {string} message - Log message to display
 */
function addLog(message) {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = message;
    logsContent.appendChild(logEntry);

    // Auto-scroll to bottom
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

/**
 * Display success result
 * @param {string} productName - Product name
 * @param {string} price - Product price
 */
function showSuccess(productName, price) {
    resultCard.className = 'result-card success';
    resultTitle.innerHTML = '<i class="bi bi-check-circle-fill"></i> Success!';
    resultContent.innerHTML = `
        <div class="product-info">
            <div class="mb-2">
                <strong>Product:</strong>
                <div class="product-name mt-1">${escapeHtml(productName)}</div>
            </div>
            <div>
                <strong>Price:</strong>
                <div class="product-price mt-1">${escapeHtml(price)}</div>
            </div>
        </div>
    `;
    resultCard.style.display = 'block';
}

/**
 * Display error message
 * @param {string} errorMessage - Error message to display
 */
function showError(errorMessage) {
    resultCard.className = 'result-card error';
    resultTitle.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i> Error';
    resultContent.innerHTML = `
        <p class="mb-0"><strong>Error:</strong> ${escapeHtml(errorMessage)}</p>
    `;
    resultCard.style.display = 'block';
}

/**
 * Show rate limit warning with countdown timer
 */
function showRateLimitWarning() {
    rateLimitWarning.style.display = 'block';
    let timeLeft = RATE_LIMIT_SECONDS;
    rateLimitTime.textContent = timeLeft;

    const countdown = setInterval(() => {
        timeLeft--;
        rateLimitTime.textContent = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(countdown);
            rateLimitWarning.style.display = 'none';
        }
    }, 1000);
}

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} - Escaped HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
