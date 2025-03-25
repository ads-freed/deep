from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    content = TextAreaField('Content', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'), 
        ('medium', 'Medium'), 
        ('high', 'High')
    ])
    attachment = FileField('Attachment')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])
    attachment = FileField('Attachment')
