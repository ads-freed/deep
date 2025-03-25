document.addEventListener('DOMContentLoaded', () => {
    // Notification handling
    const notificationBell = document.getElementById('notification-bell');
    const notificationCount = document.getElementById('notification-count');
    
    if (notificationBell) {
        notificationBell.addEventListener('click', () => {
            fetch('/notifications/mark-read')
                .then(() => notificationCount.textContent = '0');
        });
    }

    // Real-time updates
    const socket = io();
    socket.on('ticket_update', (data) => {
        if (data.ticket_id) {
            window.location.reload();
        }
    });
});
