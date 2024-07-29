## database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Configuration

class Database:
    """
    Database class to handle database connections and sessions.
    """
    def __init__(self):
        """
        Initialize the Database class with configuration settings.
        """
        config = Configuration()
        self.engine = create_engine(config.database_uri)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def get_session(self):
        """
        Provides a thread-local session for database operations.

        Returns:
            Session: A SQLAlchemy session object.
        """
        return self.Session()

    def close_session(self):
        """
        Closes the current session.
        """
        self.Session.remove()
