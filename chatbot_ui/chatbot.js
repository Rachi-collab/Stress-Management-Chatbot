const API_URL = (window.location.protocol === 'file:' || window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost')
    ? 'http://localhost:8000/chat'
    : '/chat';
const sessionId = "user_" + Math.floor(Math.random() * 100000);

// ---------- Theme System ----------
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    
    if (theme === 'dark') {
        // SVG paths for Moon
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
        icon.setAttribute('class', 'feather-moon');
    } else {
        // SVG paths for Sun
        icon.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        `;
        icon.setAttribute('class', 'feather-sun');
    }
}

// Run theme initialization
initTheme();

// ---------- Chat Utilities ----------
function appendMessage(role, text) {
    const box = document.getElementById('chatBox');
    const msg = document.createElement('div');
    msg.classList.add('chat-message', role === 'User' ? 'user' : 'bot');

    const content = document.createElement('div');
    content.classList.add('message-content');
    content.textContent = text;

    const time = document.createElement('span');
    time.classList.add('message-time');
    const now = new Date();
    time.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    msg.appendChild(content);
    msg.appendChild(time);
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

function appendBotPlaceholder() {
    const box = document.getElementById('chatBox');
    const msg = document.createElement('div');
    msg.classList.add('chat-message', 'bot');

    const content = document.createElement('div');
    content.classList.add('message-content');
    
    // Typing indicator elements
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('typing-indicator');
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.classList.add('typing-dot');
        typingIndicator.appendChild(dot);
    }
    content.appendChild(typingIndicator);

    const time = document.createElement('span');
    time.classList.add('message-time');
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    msg.appendChild(content);
    msg.appendChild(time);
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;

    return content; // Return the content div to fill in the text later
}

// ---------- Send & Stream Messages ----------
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    // Send User Message
    appendMessage('User', message);
    input.value = '';

    // Create Bot Placeholder (with typing indicator)
    const botContentElement = appendBotPlaceholder();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: message })
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            botContentElement.textContent = errData.reply || `Error: Server returned status ${response.status}`;
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let botReply = "";
        let isFirstChunk = true;

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            
            // Process lines in the SSE stream
            const lines = chunk.split("\n\n");
            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const dataStr = line.slice(6).trim();
                    if (dataStr === "[DONE]") {
                        break;
                    }
                    try {
                        const data = JSON.parse(dataStr);
                        const content = data.choices[0].delta.content || "";
                        if (content) {
                            if (isFirstChunk) {
                                // Clear typing indicator
                                botContentElement.textContent = "";
                                isFirstChunk = false;
                            }
                            botReply += content;
                            botContentElement.textContent = botReply;
                            
                            // Auto-scroll chat box to bottom
                            const box = document.getElementById('chatBox');
                            box.scrollTop = box.scrollHeight;
                        }
                    } catch (e) {
                        // ignore JSON parser errors for partial chunks
                    }
                }
            }
        }
        
        // Handle fallback if no content was yielded at all
        if (isFirstChunk) {
            botContentElement.textContent = "Error: Received empty response from server.";
        }

    } catch (error) {
        botContentElement.textContent = "Error: Unable to reach the server. Please check if the backend is running.";
    }
}
