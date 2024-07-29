from flask import Flask
from views import views
from config import Configuration

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    config = Configuration()
    app_config = config.load_config()
    app.config['SQLALCHEMY_DATABASE_URI'] = app_config['DATABASE_URI']
    app.config['SECRET_KEY'] = app_config['SECRET_KEY']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to avoid overhead
    
    # Register blueprints
    app.register_blueprint(views, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
