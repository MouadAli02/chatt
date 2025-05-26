let currentConversationId = null;
let messageIdToFeedback = null; // Track which message is receiving feedback

// Load conversations when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadConversations();
    loadFeedbacks(); // Ensure feedbacks are loaded
});

// Function to load conversations
async function loadConversations() {
    try {
        const response = await fetch('/conversations');
        const conversations = await response.json();
        displayConversations(conversations);
    } catch (error) {
        console.error('Error loading conversations:', error);
    }
}

// Function to display conversations in the sidebar
function displayConversations(conversations) {
    const conversationsList = document.getElementById('conversations-list');
    conversationsList.innerHTML = '';

    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = `conversation-item ${conv.id === currentConversationId ? 'active' : ''}`;
        item.innerHTML = `
            <i class="fas fa-comments"></i>
            <span class="conversation-title">${conv.title}</span>
            <button class="delete-conversation" onclick="deleteConversation('${conv.id}')">
                <i class="fas fa-trash"></i>
            </button>
        `;
        item.onclick = (e) => {
            if (!e.target.closest('.delete-conversation')) {
                loadConversation(conv.id);
            }
        };
        conversationsList.appendChild(item);
    });
}

// Function to start a new chat
async function startNewChat() {
    try {
        const response = await fetch('/conversations', {
            method: 'POST'
        });
        const data = await response.json();
        currentConversationId = data.id;
        clearChatMessages();
        loadConversations();
    } catch (error) {
        console.error('Error creating new conversation:', error);
    }
}

// Function to load a specific conversation
async function loadConversation(conversationId) {
    try {
        const response = await fetch(`/conversations/${conversationId}`);
        const conversation = await response.json();
        currentConversationId = conversationId;
        
        // Update chat messages
        displayConversationMessages(conversation.messages);
        
        // Update active state in sidebar
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.toggle('active', item.dataset.id === conversationId);
        });
    } catch (error) {
        console.error('Error loading conversation:', error);
    }
}

// Function to format message content with markdown-like syntax
function formatMessageContent(content) {
    if (!content) return '';
    
    // Convert line breaks to HTML
    content = content.replace(/\n/g, '<br>');
    
    // Format code blocks
    content = content.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Format inline code
    content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Format bold text
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Format italic text
    content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Format lists
    content = content.replace(/^\s*[-*]\s+(.+)$/gm, '<li>$1</li>');
    content = content.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    return content;
}

// Function to display conversation messages
function displayConversationMessages(messages) {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    
    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.role}`;
        messageDiv.dataset.messageId = message.id;  // Store message ID as a data attribute
        messageDiv.dataset.conversationId = currentConversationId;
        
        const formattedContent = formatMessageContent(message.content);
        const date = new Date(message.timestamp);
        
        // Only show feedback options for assistant messages
        const feedbackButtons = message.role === 'assistant' ? `
            <div class="message-feedback">
                <button class="feedback-btn like ${message.feedback && message.feedback.type === 'like' ? 'active' : ''}" 
                        onclick="submitMessageFeedback('${currentConversationId}', '${message.id}', 'like')">
                    <i class="fas fa-thumbs-up"></i>
                </button>
                <button class="feedback-btn dislike ${message.feedback && message.feedback.type === 'dislike' ? 'active' : ''}" 
                        onclick="submitMessageFeedback('${currentConversationId}', '${message.id}', 'dislike')">
                    <i class="fas fa-thumbs-down"></i>
                </button>
            </div>
        ` : '';
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-role">${message.role === 'assistant' ? 'ChatEbus' : 'You'}</span>
                <span class="message-time">${date.toLocaleTimeString()}</span>
            </div>
            <div class="message-content">${formattedContent}</div>
            ${feedbackButtons}
        `;
        chatMessages.appendChild(messageDiv);
    });
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to delete a conversation
async function deleteConversation(conversationId) {
    if (!confirm('Are you sure you want to delete this conversation?')) {
        return;
    }
    
    try {
        await fetch(`/conversations/${conversationId}`, {
            method: 'DELETE'
        });
        if (currentConversationId === conversationId) {
            currentConversationId = null;
            clearChatMessages();
        }
        loadConversations();
    } catch (error) {
        console.error('Error deleting conversation:', error);
    }
}

// Function to clear chat messages
function clearChatMessages() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <p>Welcome! Ask me questions about your documents.</p>
        </div>
    `;
}

// Function to format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Submit feedback for a specific message
async function submitMessageFeedback(conversationId, messageId, feedbackType) {
    if (!conversationId || !messageId) {
        alert('Error: Message information is missing');
        return;
    }

    try {
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                conversation_id: conversationId, 
                message_id: messageId,
                feedback_type: feedbackType 
            })
        });

        if (response.ok) {
            // Update the UI to show the feedback
            const messageElement = document.querySelector(`.message[data-message-id="${messageId}"]`);
            if (messageElement) {
                const likeBtn = messageElement.querySelector('.feedback-btn.like');
                const dislikeBtn = messageElement.querySelector('.feedback-btn.dislike');
                
                if (likeBtn) likeBtn.classList.toggle('active', feedbackType === 'like');
                if (dislikeBtn) dislikeBtn.classList.toggle('active', feedbackType === 'dislike');
            }
            
            // Update the feedback list
            loadFeedbacks();
        } else {
            console.error('Error submitting feedback:', response.statusText);
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
    }
}

// Updated function to load feedbacks
async function loadFeedbacks() {
    try {
        const response = await fetch('/feedback');
        if (!response.ok) throw new Error('Failed to fetch feedbacks');
        const feedbacks = await response.json();

        const feedbackList = document.getElementById('feedback-list');
        feedbackList.innerHTML = '';

        feedbacks.forEach(feedback => {
            const feedbackItem = document.createElement('div');
            feedbackItem.className = `feedback-item ${feedback.type}`;
            
            const icon = document.createElement('i');
            icon.className = feedback.type === 'like' ? 'fas fa-thumbs-up' : 'fas fa-thumbs-down';
            
            const date = new Date(feedback.timestamp);
            const formattedDate = date.toLocaleString();
            
            const textSpan = document.createElement('span');
            
            // Truncate message content if too long
            const messagePreview = feedback.message_content && feedback.message_content.length > 30 
                ? feedback.message_content.substring(0, 30) + '...' 
                : feedback.message_content || 'Message';
                
            textSpan.textContent = `${feedback.type === 'like' ? 'Liked' : 'Disliked'} "${messagePreview}" (${formattedDate})`;
            
            feedbackItem.appendChild(icon);
            feedbackItem.appendChild(textSpan);
            feedbackList.appendChild(feedbackItem);
        });
        
        // Scroll to the bottom of the feedback list
        if (feedbacks.length > 0) {
            feedbackList.scrollTop = feedbackList.scrollHeight;
        }
    } catch (error) {
        console.error('Error loading feedbacks:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const questionInput = document.getElementById('question-input');
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');

    // Auto-resize textarea
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send message on Enter (without Shift)
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });

    // Update status
    function updateStatus(status, color) {
        statusIndicator.style.backgroundColor = color;
        statusText.textContent = status;
    }
    
    // Load conversations and feedbacks
    loadConversations();
    loadFeedbacks();
});

// Modified sendQuestion function to improve user experience
async function sendQuestion() {
    const questionInput = document.getElementById('question-input');
    const question = questionInput.value.trim();
    
    if (!question) return;
    
    // Clear input and reset height
    questionInput.value = '';
    questionInput.style.height = 'auto';
    
    // Add user message to chat
    addMessage('user', question);
    
    // Add thinking indicator
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'thinking-indicator';
    thinkingDiv.innerHTML = 'Thinking...';
    document.getElementById('chat-messages').appendChild(thinkingDiv);
    
    // Update status indicator
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    statusIndicator.style.backgroundColor = '#ffcc00';
    statusText.textContent = 'Thinking...';
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                conversation_id: currentConversationId
            })
        });
        
        // Remove thinking indicator
        thinkingDiv.remove();
        
        // Reset status
        statusIndicator.style.backgroundColor = '#00cc00';
        statusText.textContent = 'Ready';
        
        const data = await response.json();
        
        // Update current conversation ID if new
        if (data.conversation_id) {
            currentConversationId = data.conversation_id;
            loadConversations();
        }
        
        // Add bot response to chat with message ID for feedback
        addMessage('assistant', data.response, data.message_id);
        
    } catch (error) {
        // Remove thinking indicator
        thinkingDiv.remove();
        
        // Update status to error
        statusIndicator.style.backgroundColor = '#ff0000';
        statusText.textContent = 'Error';
        
        console.error('Error:', error);
        addMessage('error', 'An error occurred while processing your request.');
    }
}

// Function to add a message to the chat
function addMessage(role, content, messageId = null) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    // Store message ID as a data attribute if provided
    if (messageId) {
        messageDiv.dataset.messageId = messageId;
        messageDiv.dataset.conversationId = currentConversationId;
    }
    
    const formattedContent = formatMessageContent(content);
    const timestamp = new Date().toISOString();
    
    // Only show feedback options for assistant messages
    const feedbackButtons = role === 'assistant' && messageId ? `
        <div class="message-feedback">
            <button class="feedback-btn like" onclick="submitMessageFeedback('${currentConversationId}', '${messageId}', 'like')">
                <i class="fas fa-thumbs-up"></i>
            </button>
            <button class="feedback-btn dislike" onclick="submitMessageFeedback('${currentConversationId}', '${messageId}', 'dislike')">
                <i class="fas fa-thumbs-down"></i>
            </button>
        </div>
    ` : '';
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-role">${role === 'assistant' ? 'ChatEbus' : 'You'}</span>
            <span class="message-time">${new Date().toLocaleTimeString()}</span>
        </div>
        <div class="message-content">${formattedContent}</div>
        ${feedbackButtons}
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}