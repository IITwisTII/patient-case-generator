const sendMessage = () => {
    const userInput = document.getElementById('userInput');
    const messageText = userInput.value;

    if (messageText.trim() !== "") {
        // Display user message
        const chatBox = document.getElementById('chatBox');
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user-message');
        userMessageDiv.innerHTML = `<span class="message-text">${messageText}</span>`;
        chatBox.appendChild(userMessageDiv);

        // Clear input field
        userInput.value = '';

        // Simulate bot response (for demonstration)
        setTimeout(() => {
            const botMessageDiv = document.createElement('div');
            botMessageDiv.classList.add('message', 'bot-message');
            botMessageDiv.innerHTML = `<span class="message-text">This is a simulated response.</span>`;
            chatBox.appendChild(botMessageDiv);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }, 1000);
    }
}

// Send message on button click
document.getElementById('sendButton').addEventListener('click', sendMessage);

// Send message on Enter key press
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
