## payment.py
import stripe
from models import User
from database import Database
import logging
from stripe.error import CardError, RateLimitError, InvalidRequestError
from config import Configuration

class Payment:
    """
    Payment class to handle payment processing.
    """
    def __init__(self, user_id: int, amount: float, method: str = 'stripe'):
        """
        Initialize the Payment instance.

        Args:
            user_id (int): The ID of the user making the payment.
            amount (float): The amount to be charged.
            method (str): The payment method to be used. Default is 'stripe'.
        """
        config = Configuration()
        self.user_id = user_id
        self.amount = amount
        self.method = method
        self.stripe_api_key = config.stripe_api_key  # API key moved to configuration

    def process_payment(self, token: str) -> bool:
        """
        Process the payment using the specified method.

        Args:
            token (str): The payment token obtained from the user.

        Returns:
            bool: True if the payment is processed successfully, False otherwise.
        """
        if self.method == 'stripe':
            return self._process_stripe_payment(token)
        else:
            logging.error(f"Payment method {self.method} is not supported.")
            return False

    def _process_stripe_payment(self, token: str) -> bool:
        """
        Process the payment using Stripe.

        Args:
            token (str): The payment token obtained from the user.

        Returns:
            bool: True if the payment is processed successfully, False otherwise.
        """
        stripe.api_key = self.stripe_api_key
        session = Database().get_session()
        user = session.query(User).filter_by(id=self.user_id).first()
        session.close()

        if not user:
            logging.error("User not found.")
            return False

        try:
            charge = stripe.Charge.create(
                amount=int(self.amount * 100),  # Stripe requires amount in cents
                currency='usd',
                description='Event ticket purchase',
                source=token  # Use the provided token
            )
            if charge['paid']:
                return True
            else:
                logging.error("Stripe charge was not successful.")
                return False
        except CardError as e:
            logging.error(f"Card error: {e.user_message}")
            return False
        except RateLimitError:
            logging.error("Rate limit exceeded for Stripe API requests.")
            return False
        except InvalidRequestError as e:
            logging.error(f"Invalid request: {e.user_message}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return False
