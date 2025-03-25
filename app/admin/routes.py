from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Ticket
from .forms import UserEditForm

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def require_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('main.dashboard'))

@admin.route('/users')
def user_management():
    users = User.query.all()
    return render_template('dashboard/admin.html', users=users)

@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated', 'success')
        return redirect(url_for('admin.user_management'))
    return render_template('admin/edit_user.html', form=form)

@admin.route('/tickets')
def ticket_management():
    tickets = Ticket.query.all()
    return render_template('dashboard/admin.html', tickets=tickets)
