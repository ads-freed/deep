from datetime import datetime
from app import db
from app.models import Ticket
import os
import bleach
from bs4 import BeautifulSoup

allowed_tags = bleach.ALLOWED_TAGS + [
    'h1', 'h2', 'h3', 'p', 'span', 'div', 'br', 'pre', 'code',
    'ul', 'ol', 'li', 'strong', 'em', 'u', 'img'
]

allowed_attributes = {
    'img': ['src', 'alt', 'title'],
    'a': ['href', 'title']
}

def sanitize_html(content):
    # Clean HTML content
    cleaned = bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)
    
    # Sanitize image sources
    soup = BeautifulSoup(cleaned, 'html.parser')
    for img in soup.find_all('img'):
        if not img['src'].startswith(('http://', 'https://')):
            img.decompose()
    
    return str(soup)

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
