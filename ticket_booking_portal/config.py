## config.py
import os

class Configuration:
    """
    Configuration class to handle application settings.
    """
    def __init__(self):
        self.database_uri: str = os.getenv('DATABASE_URI', 'postgresql://user:password@localhost/dbname')
        self.secret_key: str = os.getenv('SECRET_KEY', 'your_secret_key_here')

    def load_config(self) -> dict:
        """
        Load the configuration settings into a dictionary.
        
        Returns:
            dict: A dictionary containing configuration settings.
        """
        return {
            'DATABASE_URI': self.database_uri,
            'SECRET_KEY': self.secret_key
        }
