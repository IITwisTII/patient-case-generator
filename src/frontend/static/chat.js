window.onload = function() {
    const chatBox = document.getElementById('chatBox');
    
    // Check if there is a generated case stored
    const generatedCase = localStorage.getItem('generatedCase');
    console.log(generatedCase)
    
    if (generatedCase) {
        // Display the generated case as a bot message
        const botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('message', 'bot-message');
        botMessageDiv.innerHTML = `<span class="message-text">${generatedCase}</span>`;
        chatBox.appendChild(botMessageDiv);
        
        // Scroll chat to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear the case from localStorage after displaying
        localStorage.removeItem('generatedCase');
    }
}

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

        // Send message to the backend
        fetch('/chat/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: messageText }) // Send the user input as JSON
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            const botMessageDiv = document.createElement('div');
            botMessageDiv.classList.add('message', 'bot-message');
            botMessageDiv.innerHTML = `<span class="message-text">${data.response}</span>`;
            chatBox.appendChild(botMessageDiv);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
