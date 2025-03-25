from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db, limiter
from .models import User, Ticket, Message
from .forms import LoginForm, RegistrationForm, TicketForm, MessageForm
from functools import wraps
import os

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')
tickets = Blueprint('tickets', __name__, url_prefix='/tickets')
messages = Blueprint('messages', __name__, url_prefix='/messages')

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    # Implement login logic

@auth.route('/logout')
@login_required
def logout():
    # Implement logout logic

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Implement registration logic

@tickets.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            content=form.content.data,
            priority=form.priority.data,
            author=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        generate_ticket_number(ticket)
        
        if form.attachment.data:
            file = form.attachment.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{ticket.id}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name))
                ticket.attachment = unique_name
                db.session.commit()
        
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))
    return render_template('tickets/create.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_ticket_number(ticket):
    now = datetime.now()
    month_year = now.strftime("%m-%y")
    last_ticket = Ticket.query.filter(Ticket.number.like(f"%{month_year}-%")).order_by(Ticket.id.desc()).first()
    sequence = 1 if not last_ticket else int(last_ticket.number.split('-')[-1]) + 1
    ticket.number = f"TICKET-{month_year}-{sequence:04d}"
    db.session.commit()

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
