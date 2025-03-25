const socket = io();

// Ticket room management
function joinTicketRoom(ticketId) {
    socket.emit('join_ticket_room', ticketId);
}

socket.on('ticket_activity', (data) => {
    if (data.update_type === 'status_change') {
        updateTicketStatus(data.ticket_id, data.status);
        showNotification(`Ticket ${data.number} status changed to ${data.status}`);
    }
});

socket.on('new_reply', (data) => {
    const messagesDiv = document.getElementById('messages-container');
    const newMessage = createMessageElement(data);
    messagesDiv.appendChild(newMessage);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Collaborative editing (basic example)
const contentEditor = document.getElementById('content-editor');
if (contentEditor) {
    contentEditor.addEventListener('input', (e) => {
        socket.emit('content_update', {
            ticket_id: ticketId,
            content: e.target.value
        });
    });

    socket.on('content_update', (data) => {
        if (data.user !== currentUser) {
            contentEditor.value = data.content;
        }
    });
}
