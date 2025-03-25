from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired

class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('user', 'User'), 
        ('support', 'Support Staff'),
        ('admin', 'Administrator')
    ])
    active = BooleanField('Active')
