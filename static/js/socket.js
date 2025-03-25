document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to WebSocket');
    });

    socket.on('new_private_message', (data) => {
        showNotification(`New message from ${data.sender_name}`, data.content);
    });

    socket.on('ticket_updated', (data) => {
        showNotification('Ticket Updated', `Ticket ${data.ticket_number} has been updated`);
    });

    function showNotification(title, message) {
        if (Notification.permission === 'granted') {
            new Notification(title, { body: message });
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    new Notification(title, { body: message });
                }
            });
        }
    }
});
