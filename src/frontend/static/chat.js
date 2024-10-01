let chatHistory = [];

window.onload = function() {
    const chatBox = document.getElementById('chatBox');
    console.log("[window.onload] Window loaded, chatBox found:", chatBox); // Debugging
    displayGeneratedCase(chatBox, chatHistory);
};

const displayGeneratedCase = (chatBox, chatHistory) => {
    const generatedCase = localStorage.getItem('generatedCase');
    console.log("[displayGeneratedCase] Generated case from localStorage:", generatedCase); // Debugging
    
    if (generatedCase) {
        appendMessage(chatBox, 'bot', generatedCase, chatHistory);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll chat to the bottom
        console.log("[displayGeneratedCase] Generated case appended to chatBox."); // Debugging
        localStorage.removeItem('generatedCase'); // Clear the case from localStorage
    }
};

const appendMessage = (chatBox, sender, message, chatHistory) => {
    console.log(`[appendMessage] Appending message from ${sender}: ${message}`); // Debugging

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.innerHTML = `<span class="message-text">${message}</span>`;
    chatBox.appendChild(messageDiv);

    console.log("[appendMessage] Message appended to chatBox:", messageDiv); // Debugging

    // Store the message in the temporary chat history
    chatHistory.push(`${sender.charAt(0).toUpperCase() + sender.slice(1)}: ${message}`);
    console.log("[appendMessage] Updated chatHistory:", chatHistory); // Debugging
};

const sendMessage = () => {
    const userInput = document.getElementById('userInput');
    const messageText = userInput.value.trim();

    console.log("[sendMessage] User message input:", messageText); // Debugging

    if (messageText !== "") {
        const chatBox = document.getElementById('chatBox');
        appendMessage(chatBox, 'user', messageText, chatHistory); // Display user message
        console.log("[sendMessage] User message sent and appended."); // Debugging

        userInput.value = ''; // Clear input field
        console.log("[sendMessage] User input field cleared."); // Debugging

        fetchResponse(messageText, chatBox, chatHistory);
    } else {
        console.log("[sendMessage] User message is empty, nothing to send."); // Debugging
    }
};

const fetchResponse = (messageText, chatBox, chatHistory) => {
    console.log("[fetchResponse] Fetching response for message:", messageText); // Debugging

    fetch('/chat/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: messageText })
    })
    .then(response => response.json())
    .then(data => {
        console.log("[fetchResponse] Response received from backend:", data); // Debugging
        handleResponse(data, chatBox, chatHistory);
    })
    .catch(error => {
        console.error('[fetchResponse] Error fetching response from backend:', error);
        alert('Something went wrong, please try again later.');
    });
};

const handleResponse = (data, chatBox, chatHistory) => {
    if (data.error) {
        alert(`[handleResponse] Error: ${data.error}`);
        return;
    }

    console.log("[handleResponse] Handling response data:", data); // Debugging

    appendMessage(chatBox, 'bot', data.response, chatHistory); // Display bot response
    console.log("[handleResponse] Bot response appended to chatBox:", data.response); // Debugging

    // Display chat history if needed
    if (data.history) {
        console.log("[handleResponse] Updating chatBox with history:", data.history); // Debugging
        chatBox.innerHTML = ''; // Clear chatBox
        data.history.forEach(line => {
            const sender = line.startsWith('User:') ? 'user' : 'bot';
            appendMessage(chatBox, sender, line, chatHistory);
        });
    }

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom after updating chat history
    console.log("[handleResponse] ChatBox scrolled to bottom."); // Debugging
};

// Event listeners
document.getElementById('sendButton').addEventListener('click', () => {
    console.log("[sendButton] Send button clicked."); // Debugging
    sendMessage();
});

document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission on Enter
        console.log("[userInput] Enter key pressed."); // Debugging
        sendMessage();
    }
});
