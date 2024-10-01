let chatHistory = [];
window.onload = function() {
    const chatBox = document.getElementById('chatBox');
    displayGeneratedCase(chatBox, chatHistory);
};

const displayGeneratedCase = (chatBox, chatHistory) => {
    const generatedCase = localStorage.getItem('generatedCase');
    
    if (generatedCase) {
        appendMessage(chatBox, 'bot', generatedCase, chatHistory);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll chat to the bottom
        localStorage.removeItem('generatedCase'); // Clear the case from localStorage
    }
};

const appendMessage = (chatBox, sender, message, chatHistory) => {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.innerHTML = `<span class="message-text">${message}</span>`;
    chatBox.appendChild(messageDiv);

    // Store the message in the temporary chat history
    chatHistory.push(`${sender.charAt(0).toUpperCase() + sender.slice(1)}: ${message}`);
};

const sendMessage = () => {
    const userInput = document.getElementById('userInput');
    const messageText = userInput.value.trim();

    if (messageText !== "") {
        const chatBox = document.getElementById('chatBox');
        appendMessage(chatBox, 'user', messageText, chatHistory); // Display user message

        userInput.value = ''; // Clear input field
        
        fetchResponse(messageText, chatBox, chatHistory);
    }
};

const fetchResponse = (messageText, chatBox, chatHistory) => {
    fetch('/chat/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: messageText })
    })
    .then(response => response.json())
    .then(data => handleResponse(data, chatBox, chatHistory))
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong, please try again later.');
    });
};

const handleResponse = (data, chatBox, chatHistory) => {
    if (data.error) {
        alert(`Error: ${data.error}`);
        return;
    }

    appendMessage(chatBox, 'bot', data.response, chatHistory); // Display bot response

    // Display chat history if needed
    if (data.history) {
        chatBox.innerHTML = ''; // Clear chatBox
        data.history.forEach(line => {
            const sender = line.startsWith('User:') ? 'user' : 'bot';
            appendMessage(chatBox, sender, line, chatHistory);
        });
    }

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom after updating chat history
};

// Event listeners
document.getElementById('sendButton').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission on Enter
        sendMessage();
    }
});
