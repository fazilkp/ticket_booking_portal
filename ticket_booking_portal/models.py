## models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import logging
from database import Database  # Use Database class for session management

Base = declarative_base()
logging.basicConfig(level=logging.ERROR)

class Event(Base):
    """
    Event class to represent event details in the database.
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    location = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="event")

    @staticmethod
    def get_events(query: dict) -> list:
        """
        Fetch events based on a query dictionary.

        Args:
            query (dict): A dictionary containing query parameters.

        Returns:
            list: A list of Event instances that match the query.
        """
        session = Database().get_session()
        query_result = session.query(Event).filter_by(**query).all()
        session.close()
        return query_result

class Ticket(Base):
    """
    Ticket class to represent ticket details in the database.
    """
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    seat_number = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    event = relationship("Event", back_populates="tickets")
    user_id = Column(Integer, ForeignKey('users.id'))

    @staticmethod
    def book_ticket(user_id: int, event_id: int, seat_number: str, price: float) -> bool:
        """
        Book a ticket for a user.

        Args:
            user_id (int): The ID of the user booking the ticket.
            event_id (int): The ID of the event for which the ticket is booked.
            seat_number (str): The seat number of the ticket.
            price (float): The price of the ticket.

        Returns:
            bool: True if booking is successful, False otherwise.
        """
        session = Database().get_session()
        ticket = Ticket(user_id=user_id, event_id=event_id, seat_number=seat_number, price=price)
        session.add(ticket)
        try:
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logging.error(f"Error occurred: {e}")
            return False
        finally:
            session.close()

class User(Base):
    """
    User class to represent user details in the database.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    tickets = relationship("Ticket")

    @staticmethod
    def login(email: str, password: str) -> bool:
        """
        Authenticate a user based on email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        session = Database().get_session()
        user = session.query(User).filter_by(email=email, password=password).first()
        session.close()
        return user is not None

    @staticmethod
    def register(email: str, password: str) -> bool:
        """
        Register a new user with an email and password.

        Args:
            email (str): The email to register.
            password (str): The password for the new account.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        session = Database().get_session()
        if session.query(User).filter_by(email=email).first() is not None:
            session.close()
            return False  # User already exists
        new_user = User(email=email, password=password)
        session.add(new_user)
        try:
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logging.error(f"Error occurred: {e}")
            return False
        finally:
            session.close()
