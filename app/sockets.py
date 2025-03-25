from flask_socketio import emit, join_room
from flask_login import current_user
from app import socketio, db
from app.models import Ticket, Message
from datetime import datetime

def handle_ticket_update(ticket, update_type):
    # Emit to all interested parties
    data = {
        'ticket_id': ticket.id,
        'number': ticket.number,
        'status': ticket.status,
        'update_type': update_type,
        'timestamp': datetime.utcnow().isoformat(),
        'user': current_user.username
    }
    emit('ticket_activity', data, room=f'ticket_{ticket.id}')
    if current_user.role != 'admin':
        emit('admin_notification', data, room='admin_dashboard')

@socketio.on('join_ticket_room')
def handle_join_ticket_room(ticket_id):
    if current_user.is_authenticated:
        ticket = Ticket.query.get(ticket_id)
        if ticket and (current_user == ticket.author or current_user.role in ['admin', 'support']):
            join_room(f'ticket_{ticket_id}')
            emit('system_message', {'message': f'Joined ticket room {ticket_id}'})

@socketio.on('status_change')
def handle_status_change(data):
    if current_user.role not in ['admin', 'support']:
        return emit('error', {'message': 'Unauthorized'})
    
    ticket = Ticket.query.get(data['ticket_id'])
    if ticket:
        ticket.status = data['new_status']
        db.session.commit()
        handle_ticket_update(ticket, 'status_change')

@socketio.on('new_reply')
def handle_new_reply(data):
    ticket = Ticket.query.get(data['ticket_id'])
    if ticket and current_user.is_authenticated:
        if not (current_user == ticket.author or current_user.role in ['admin', 'support']):
            return emit('error', {'message': 'Unauthorized'})
        
        message = Message(
            content=data['content'],
            ticket_id=ticket.id,
            user_id=current_user.id
        )
        db.session.add(message)
        db.session.commit()
        
        emit('new_reply', {
            'content': data['content'],
            'author': current_user.username,
            'timestamp': datetime.utcnow().isoformat()
        }, room=f'ticket_{ticket.id}')
