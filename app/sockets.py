from app import socketio
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        join_room(str(current_user.id))
        emit('notification', {'type': 'connection', 'message': 'Connected'})

@socketio.on('private_message')
def handle_private_message(data):
    recipient_id = data['recipient_id']
    message = {
        'sender_id': current_user.id,
        'sender_name': current_user.username,
        'content': data['content'],
        'timestamp': datetime.utcnow().isoformat()
    }
    emit('new_private_message', message, room=recipient_id)
    emit('message_confirmation', {'status': 'delivered'})

@socketio.on('ticket_update')
def handle_ticket_update(data):
    ticket_id = data['ticket_id']
    emit('ticket_updated', data, room=f'ticket_{ticket_id}')
