## forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    """
    Form for handling user login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class RegistrationForm(FlaskForm):
    """
    Form for handling new user registration.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class TicketBookingForm(FlaskForm):
    """
    Form for booking tickets.
    """
    user_id = IntegerField('User ID', validators=[DataRequired()])
    event_id = IntegerField('Event ID', validators=[DataRequired()])
    seat_number = StringField('Seat Number', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
