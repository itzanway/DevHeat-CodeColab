// WebSocket setup
const roomName = document.getElementById('room-name').textContent.trim();  // hidden element in room.html
const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const socket = new WebSocket(`${wsProtocol}//${window.location.host}/ws/code/${roomName}/`);

// DOM Elements
const codeEditor = document.getElementById('code-editor');
const runButton = document.getElementById('run-code');
const outputDiv = document.getElementById('output');
const languageSelect = document.getElementById('language');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');
const sendMessageButton = document.getElementById('send-message');
const aiButton = document.getElementById('ai-complete');  // AI Autocomplete Button

// Time formatting
function formatTimestamp(date) {
    return date.toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });
}

// Chat message display
function addChatMessage(username, message, timestamp) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message';
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="username">${username}</span>
            <span class="timestamp">${timestamp}</span>
        </div>
        <div class="message-content">${message}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Debounced code update
let typingTimer;
const doneTypingInterval = 100;

function sendCodeUpdate() {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'code_update',
            code: codeEditor.value
        }));
    }
}

codeEditor.addEventListener('input', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(sendCodeUpdate, doneTypingInterval);
});

// Run Code
runButton.addEventListener('click', function () {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'execute_code',
            code: codeEditor.value,
            language: languageSelect.value
        }));
    }
});

// Chat Message Send
function sendChatMessage() {
    const message = chatInput.value.trim();
    if (message && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: 'chat_message',
            message: message
        }));
        chatInput.value = '';
    }
}

chatInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendChatMessage();
});
if (sendMessageButton) sendMessageButton.addEventListener('click', sendChatMessage);

// Tab in editor
codeEditor.addEventListener('keydown', function (e) {
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 4;
    }
});

// Cursor Tracking
const userCursors = new Map();
const cursorContainer = document.createElement('div');
cursorContainer.id = 'cursor-container';
cursorContainer.style.position = 'absolute';
cursorContainer.style.inset = '0';
cursorContainer.style.pointerEvents = 'none';
document.getElementById('code-editor-container').appendChild(cursorContainer);

function getCaretCoordinates(textarea, position) {
    const mirror = document.createElement('div');
    const style = window.getComputedStyle(textarea);
    ['fontFamily', 'fontSize', 'fontWeight', 'letterSpacing', 'lineHeight', 'padding', 'border', 'boxSizing', 'whiteSpace', 'wordWrap', 'tabSize']
        .forEach(prop => mirror.style[prop] = style[prop]);
    mirror.style.position = 'absolute';
    mirror.style.visibility = 'hidden';
    mirror.style.overflow = 'hidden';
    mirror.style.width = `${textarea.clientWidth}px`;
    const textBeforeCursor = textarea.value.substring(0, position);
    const textLine = textBeforeCursor.split('\n');
    const currentLineNumber = textLine.length - 1;
    const currentLineText = textLine[currentLineNumber];
    mirror.textContent = textBeforeCursor;
    document.body.appendChild(mirror);
    const caretHeight = parseInt(style.lineHeight);
    const top = currentLineNumber * caretHeight;
    const measureSpan = document.createElement('span');
    measureSpan.textContent = currentLineText;
    mirror.appendChild(measureSpan);
    const spanRect = measureSpan.getBoundingClientRect();
    const left = spanRect.width;
    document.body.removeChild(mirror);
    return {
        top: top + parseInt(style.paddingTop),
        left: left + parseInt(style.paddingLeft)
    };
}

function updateRemoteCursor(username, position) {
    let cursor = userCursors.get(username);
    if (!cursor) {
        cursor = document.createElement('div');
        cursor.className = 'remote-cursor';
        cursor.innerHTML = `
            <div class="cursor-line" style="background: ${stringToColor(username)}"></div>
            <div class="cursor-flag" style="background: ${stringToColor(username)}">
                ${username}
            </div>
        `;
        cursor.style.position = 'absolute';
        cursor.style.pointerEvents = 'none';
        cursorContainer.appendChild(cursor);
        userCursors.set(username, cursor);
    }
    cursor.style.transition = 'transform 0.1s ease-out';
    cursor.style.transform = `translate(${position.coords.left}px, ${position.coords.top}px)`;
}

const style = document.createElement('style');
style.textContent = `
.remote-cursor {
    position: absolute;
    pointer-events: none;
    z-index: 1000;
    opacity: 0.8;
}
.cursor-flag {
    position: absolute;
    top: 0;
    left: 2px;
    padding: 1px 4px;
    border-radius: 2px;
    font-size: 10px;
    color: white;
    white-space: nowrap;
    opacity: 0.8;
    transform: translateY(-50%);
}
.cursor-line {
    position: absolute;
    width: 2px;
    height: 24px;
    background: inherit;
}
.remote-cursor:hover .cursor-flag {
    opacity: 1;
}
`;
document.head.appendChild(style);

function stringToColor(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return `hsl(${hash % 360}, 70%, 50%)`;
}

function sendCursorUpdate() {
    if (socket.readyState === WebSocket.OPEN) {
        const position = codeEditor.selectionStart;
        const coords = getCaretCoordinates(codeEditor, position);
        socket.send(JSON.stringify({
            type: 'cursor_update',
            position: {
                index: position,
                coords: coords
            }
        }));
    }
}

codeEditor.addEventListener('click', sendCursorUpdate);
codeEditor.addEventListener('keyup', sendCursorUpdate);
codeEditor.addEventListener('mousemove', sendCursorUpdate);

// WebSocket handler
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log('Received WebSocket message:', data);

    switch (data.type) {
        case 'code_update':
            if (codeEditor.value !== data.code) {
                const cursorPosition = codeEditor.selectionStart;
                codeEditor.value = data.code;
                codeEditor.setSelectionRange(cursorPosition, cursorPosition);
            }
            break;
        case 'execution_result':
            outputDiv.innerHTML = data.output.replace(/\n/g, '<br>');
            outputDiv.style.color = 'white';
            break;
        case 'execution_error':
            outputDiv.textContent = 'Error: ' + data.error;
            outputDiv.style.color = 'red';
            break;
        case 'chat_message':
            addChatMessage(data.username, data.message, data.timestamp || formatTimestamp(new Date()));
            break;
        case 'cursor_update':
            updateRemoteCursor(data.username, data.position);
            break;
    }
};

socket.onclose = function () {
    console.error('WebSocket connection closed unexpectedly');
    outputDiv.textContent = 'Connection lost. Please refresh the page.';
    outputDiv.style.color = 'red';
};

// ✅ AI-Powered Code Autocomplete
if (aiButton) {
    aiButton.addEventListener('click', async () => {
        const code = codeEditor.value;
        const response = await fetch('/ai-autocomplete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ code: code })
        });

        if (response.ok) {
            const data = await response.json();
            const suggestion = data.suggestion || '';

            const start = codeEditor.selectionStart;
            const end = codeEditor.selectionEnd;

            // Insert suggestion at current cursor position
            codeEditor.value = codeEditor.value.slice(0, start) + suggestion + codeEditor.value.slice(end);

            // Move cursor to end of inserted suggestion
            codeEditor.selectionStart = codeEditor.selectionEnd = start + suggestion.length;
            codeEditor.focus();
        } else {
            alert('AI Suggestion failed.');
        }
    });
}

