from datetime import datetime
from app import db
from app.models import Ticket
import os

def generate_ticket_number(ticket):
    now = datetime.now()
    month_year = now.strftime("%m-%y")
    last_ticket = Ticket.query.filter(Ticket.number.like(f"%{month_year}-%")).order_by(Ticket.id.desc()).first()
    sequence = 1 if not last_ticket else int(last_ticket.number.split('-')[-1]) + 1
    ticket.number = f"TICKET-{month_year}-{sequence:04d}"
    db.session.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_attachment(file, ticket_id):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_name = f"{ticket_id}_{datetime.now().timestamp()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(file_path)
        return unique_name
    return None
