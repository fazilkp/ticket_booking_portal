from flask import Blueprint, request, jsonify, session
from models import Event, Ticket, User
from forms import LoginForm, RegistrationForm, TicketBookingForm
from payment import Payment
from email_service import EmailService
import logging
from bcrypt import hashpw, gensalt, checkpw

# Create a Blueprint for the views
views = Blueprint('views', __name__)

@views.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data
        if User.login(email, password):
            session['user'] = email
            return jsonify({'status': 'success', 'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'status': 'error', 'message': 'Invalid form data'}), 400

@views.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data
        if User.register(email, password):
            return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201
        else:
            return jsonify({'status': 'error', 'message': 'Email already exists'}), 409
    else:
        return jsonify({'status': 'error', 'message': 'Invalid form data'}), 400

@views.route('/events', methods=['GET'])
def get_events():
    query = request.args.to_dict()
    events = Event.get_events(query)
    return jsonify([{'id': event.id, 'name': event.name, 'date': event.date.isoformat(), 'location': event.location} for event in events]), 200

@views.route('/book_ticket', methods=['POST'])
def book_ticket():
    form = TicketBookingForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        event_id = form.event_id.data
        seat_number = form.seat_number.data
        price = form.price.data
        if Ticket.book_ticket(user_id, event_id, seat_number, price):
            return jsonify({'status': 'success', 'message': 'Ticket booked successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to book ticket'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid form data'}), 400

@views.route('/process_payment', methods=['POST'])
def process_payment():
    user_id = request.json.get('user_id')
    amount = request.json.get('amount')
    token = request.json.get('token')
    payment = Payment(user_id, amount)
    if payment.process_payment(token):
        return jsonify({'status': 'success', 'message': 'Payment processed successfully'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Payment failed'}), 500

@views.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.json.get('recipient')
    subject = request.json.get('subject')
    body = request.json.get('body')
    email_service = EmailService()
    if email_service.send_email(recipient, subject, body):
        return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to send email'}), 500
