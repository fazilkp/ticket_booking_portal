import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Configuration
import logging

class EmailService:
    """
    EmailService class to handle sending emails.
    """
    def __init__(self):
        """
        Initialize the EmailService with configuration settings.
        """
        config = Configuration()
        self.smtp_server = config.email_smtp_server
        self.smtp_port = config.email_smtp_port
        self.smtp_user = config.email_smtp_user
        self.smtp_password = config.email_smtp_password

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Send an email to a specified recipient.

        Args:
            recipient (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body of the email.

        Returns:
            bool: True if the email is sent successfully, False otherwise.
        """
        message = MIMEMultipart()
        message['From'] = self.smtp_user
        message['To'] = recipient
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, recipient, message.as_string())
            return True
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return False
